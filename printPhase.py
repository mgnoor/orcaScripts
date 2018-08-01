import lalsimulation as sim
from pycbc import pnutils, waveform
import h5py as h5
from pycbc.waveform import get_td_waveform
import numpy as np
import scipy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys

#sys[0] is the path to this file
#sys[1] is the path to the directory in which the shell script was called
#sys[2...] is filenames, assumed ot be given starting from the directory in which the script was called

files = []
fileNames = []
#set base path to directory in which shell script was called
fileBasePath = sys.argv[1] + "/"

#import files from base path and provided filename
for i in range(2, len(sys.argv)):
	fileNames.append(fileBasePath + sys.argv[i])
	files.append(h5.File(fileNames[i - 2], 'r'))

#assume default parameters, arbitrary; may later add functionality to choose them
inclination = 0
distance = 444.0
sampleRate = 4096.0
massTotal = 70.0
fref = 25.0
flow = 25.0
dt = 1 / sampleRate

#the file attributes mass1 and mass2 are relative, not absolute; we scale them to the chosen total mass
mass1List = []
mass2List = []
for file in files:
    m1 = file.attrs['mass1']
    m2 = file.attrs['mass2']
    mass1List.append(m1 * massTotal / (m1 + m2))
    mass2List.append(m2 * massTotal / (m1 + m2))
#this should be an array with len == num files and arr[i] == total mass for all i
massTotalArray = np.array(mass1List) + np.array(mass2List)


fLowList = []
for i, file in enumerate(files):
    #gets value for lower frequency assuming one solar mass, then adjusts that number based on the total mass we chose
    fLowList.append(file.attrs['f_lower_at_1MSUN'] / (mass1List[i] + mass2List[i]))

spin1List = []
spin2List = []
for i,file in enumerate(fileNames):
    referenceFrequency = fref
    #gets and stores the spins for both bodies in the binary from the file, the reference frequency, and the chosen total mass
    s1x, s1y, s1z, s2x, s2y, s2z = sim.SimInspiralNRWaveformGetSpinsFromHDF5File(referenceFrequency, massTotalArray[i], file)
    spin1List.append([s1x, s1y, s1z])
    spin2List.append([s2x, s2y, s2z])

hpList = []
hcList = []
for i, name in enumerate(fileNames):
    referenceFrequency = fref
    #generates a waveform from all the data we pulled from the file, as well as some of the arbitrary values we chose at the beginning
    #performed for each file and stores the values in {hp/hc}List
    #hp is plus polarization and hc is cross polarization; it seems in most cases without external interference hc should be hp shifted to the right a bit?
    #hc is shifted hp: "This holds for systems where the orbital plane of the binary doesn't precess"
    hp, hc = get_td_waveform(approximant = 'NR_hdf5',
                             numrel_data = name,
                             mass1 = mass1List[i],
                             mass2 = mass2List[i],
                             spin1x = spin1List[i][0],
                             spin1y = spin1List[i][1],
                             spin1z = spin1List[i][2],
                             spin2x = spin2List[i][0],
                             spin2y = spin2List[i][1],
                             spin2z = spin2List[i][2],
                             delta_t = dt,
                             f_lower = flow,
                             fref = fref,
                             inclination = inclination,
                             coa_phase = 0.0,
                             distance = distance)
    hpList.append(hp)
    hcList.append(hc)

ampList = []
phaseList = []
for i, name in enumerate(fileNames):
    hp = hpList[i]
    hc = hcList[i]
    #calculates amplitude and phase from hp and hc, presumably of strain as that seems to be output of get_td_waveform in most cases
    ampList.append(waveform.utils.amplitude_from_polarizations(hp, hc))
    phaseList.append(waveform.utils.phase_from_polarizations(hp, hc))

ampInterpList = []
phaseInterpList = []
for i, name in enumerate(fileNames):
    amp = ampList[i]
    phase = phaseList[i]
    #performs a cubic interpolation on the amp and phase; this should be a function
    ampInterpList.append(scipy.interpolate.interp1d(amp.sample_times, amp, kind='cubic'))
    phaseInterpList.append(scipy.interpolate.interp1d(phase.sample_times, phase, kind='cubic'))

ampInterpolatedList = []
phaseInterpolatedList = []
startTimesList = []
endTimesList = []
for i in range(len(ampList)):
	startTimesList.append(ampList[i].sample_times[0])
	endTimesList.append(ampList[i].sample_times[-1])
#selects times within the ranges of all data points starting at the latest start point and spaced by dt
times = np.arange(max(startTimesList), min(endTimesList), dt)
for i, name in enumerate(fileNames):
    amp = ampInterpList[i]
    phase = phaseInterpList[i]
    #finds values at specific times from the interpolation function previously chosen
    ampInterpolatedList.append(amp(times))
    phaseInterpolatedList.append(phase(times))
for i in range(len(phaseInterpolatedList)):
	plt.clf()
	plt.plot(times, phaseInterpolatedList[i], label = sys.argv[i + 2])
	plt.legend(loc='best')
	plt.xlabel("Time (s)")
	plt.ylabel("Phase")
	plt.yscale('linear')
	name = sys.argv[i + 2]
	name = name.replace(".h5", "")
	plt.savefig(name + "_strain_phase_vs_time.pdf")