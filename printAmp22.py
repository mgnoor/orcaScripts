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
	spline = romspline.readSpline(fileNames[i - 2], group='amp_l2_m2')

	#select dt and use that to make arrays of the corresponding times
	dt = .5
	times = np.arange(spline.X[0],spline.X[-1],dt)

	#print spin 1s
	plt.clf()
	plt.plot(times, spline(times))
	plt.xlabel("Time (s)")
	plt.ylabel("Amplitude")

	#export spin 1s
	name = sys.argv[i]
	name = name.replace(".h5", "")
	plt.savefig(name + "_amp22")


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