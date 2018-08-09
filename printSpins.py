# Import necessary modules
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os
import h5py
from subprocess import call

# Uncomment next two lines if romSpline is not in your PYTHONPATH
# import sys
# sys.path.append(<path to your copy of romspline>)

#import romspline

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
try:
	import romspline
except:
	username = ""
	if os.path.isdir(dir_path + "/romspline"):
		pass #print("romspline or directory with this name already exists")
	elif os.path.exists(dir_path + "/romspline"):
		raise Exception("file named romspline exists; cannot import romspline until this file is deleted")
	else:
		print dir_path
		call(["git", "-C", dir_path, "clone", "https://" + username + "@bitbucket.org/chadgalley/romspline.git"])
		print "https://" + username + "@bitbucket.org/chadgalley/romspline.git"

sys.path.append(dir_path)
import romspline

#sys[0] is the path to this file
#sys[1] is the path to the directory in which the shell script was called
#sys[2...] is filenames, assumed to be given starting from the directory in which the script was called

files = []
fileNames = []
#set base path to directory in which shell script was called
fileBasePath = sys.argv[1] + "/"

#import files from base path and provided filename
for i in range(2, len(sys.argv)):
	fileNames.append(fileBasePath + sys.argv[i])

	#read in h5 files
	spline1x = romspline.readSpline(fileNames[i - 2], group='spin1x-vs-time')
	spline1y = romspline.readSpline(fileNames[i - 2], group='spin1y-vs-time')
	spline1z = romspline.readSpline(fileNames[i - 2], group='spin1z-vs-time')
	spline2x = romspline.readSpline(fileNames[i - 2], group='spin2x-vs-time')
	spline2y = romspline.readSpline(fileNames[i - 2], group='spin2y-vs-time')
	spline2z = romspline.readSpline(fileNames[i - 2], group='spin2z-vs-time')

	#select dt and use that to make arrays of the corresponding times
	dt = .5
	times1x = np.arange(spline1x.X[0],spline1x.X[-1],dt)
	times1y = np.arange(spline1y.X[0],spline1y.X[-1],dt)
	times1z = np.arange(spline1z.X[0],spline1z.X[-1],dt)
	times2x = np.arange(spline2x.X[0],spline2x.X[-1],dt)
	times2y = np.arange(spline2y.X[0],spline2y.X[-1],dt)
	times2z = np.arange(spline2z.X[0],spline2z.X[-1],dt)

	#print spin 1s
	plt.clf()
	plt.plot(times1x, spline1x(times1x), color = 'red', label = "Spin1x")
	plt.plot(times1y, spline1y(times1y), color = 'green', label = "Spin1y")
	plt.plot(times1z, spline1z(times1z), color = 'blue', label = "Spin1z")
	plt.legend(loc='best')
	plt.xlabel("Time (s)")
	plt.ylabel("Spin")

	#export spin 1s
	name1 = sys.argv[i]
	name1 = name1.replace(".h5", "")
	plt.savefig(name1 + "_spin1_vs_time.pdf")

	#print spin 2s
	plt.clf()
	plt.plot(times2x, spline2x(times2x), color = 'red', label = "Spin2x")
	plt.plot(times2y, spline2y(times2y), color = 'green', label = "Spin2y")
	plt.plot(times2z, spline2z(times2z), color = 'blue', label = "Spin2z")
	plt.legend(loc='best')
	plt.xlabel("Time (s)")
	plt.ylabel("Spin")

	#export spin 2s
	name2 = sys.argv[i]
	name2 = name2.replace(".h5", "")
	plt.savefig(name2 + "_spin2_vs_time.pdf")


'''x = np.linspace(-1, 1, 100001)

def f(x):
    return 100.*( (1.+x)*np.sin(5.*(x-0.2)**2) + np.exp(-(x-0.5)**2/2./0.01)*np.sin(100*x) )

plt.clf()
plt.plot(x, f(x), 'k-');
plt.xlabel('$x$');
plt.ylabel('Test function values');
name = 'test'
plt.savefig(name)

#spline = romspline.ReducedOrderSpline(x, f(x), verbose=True)'''