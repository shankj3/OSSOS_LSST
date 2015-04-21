import os,sys 
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
import sys

filename = sys.argv[1]
fluxcut = float(sys.argv[2])

lsstflux,jmpflux = np.loadtxt(filename, usecols=(0,1), unpack=True)
m = np.where(jmpflux<fluxcut)
n = np.where(jmpflux>fluxcut)


slope, intercept, r_value, p_value, slope_std_error = stats.linregress(jmpflux[m], lsstflux[m])
predict_y = intercept + slope*jmpflux[m]
print ('intercept,slope=')
print intercept,slope

tmpxflux = jmpflux[m]
tmpyflux = lsstflux[m]

array_length = len(tmpxflux) 

residual_y = tmpyflux - predict_y
stdev = np.std(residual_y)
new_indx = np.where(np.abs(residual_y) < 5*stdev)
slope, intercept, r_val, p_val, slope_stderr = stats.linregress(tmpxflux[new_indx], tmpyflux[new_indx])

print ('New Intercept, New Slope=')
print intercept, slope 
filebase, file_ext = filename.split('.')
outfile = filebase+'.dat'

visit, chipname = filebase.split("_")
jvisit, jexpnum = visit.split("-")

with open('jmp_lsst_fluxes.dat','a') as f:
	f.write( str(jexpnum)+' ')
	f.write( str(chipname)+' ') 
	f.write( str(slope)+' ')
	f.write( str(intercept)+' ')
	f.write( str(r_val)+' ')
	f.write( str(p_val)+' ')
	f.write( str(slope_stderr)+' ')
    	f.write( "\n" )


ax = subplot(211)
plt.scatter(tmpxflux[new_indx], tmpyflux[new_indx])
plt.plot(tmpxflux[new_indx], intercept+slope*tmpxflux[new_indx])


ax = subplot(212)
plt.scatter(jmpflux[n],lsstflux[n],label='After Saturation')
plt.scatter(jmpflux[m],lsstflux[m],color='k',label='Before Saturation')
plt.plot(jmpflux[m],predict_y,color='r')
plt.xlim(-5000,50000)
plt.legend(loc=2,shadow=True)
plt.xlabel('lsst flux')
plt.ylabel('jmp flux')

filebase, file_ext = filename.split('.')
savefig(filebase+'.png', bbox_inches='tight')

#plt.show()
