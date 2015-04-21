import numpy as np
import numpy.lib.recfunctions as rf
import os, sys


jmpfluxdat = np.loadtxt('jmp_lsst_fluxes.dat', usecols=(0,1,2,3), dtype=[('img', np.int), ('ccd', 'S10'), ('slope', 'float'), ('intercept', 'float')])

#print fluxdat
#print fluxdat['img']
jmpfiles = ['%s/ccd%s/%s%s.obj.jmp' %(el['img'], el['ccd'][-2:], el['img'], el['ccd'][-2:]) for el in jmpfluxdat]
#jmpfiles = ['%s/ccd%s/%s%s.obj.jmp' %(el['img'], el['ccd'][-2:], el['img'], el['ccd'][-2:]) for el in fluxdat]
#filenames = [str(row['img']) + '_' + str(row['ccd']) + '.both' for row in fluxdat]

#print filenames

#for i in 
     
for jmpfilename, fluxcalib in zip(jmpfiles, jmpfluxdat):
    slope = fluxcalib['slope']
    intercept = fluxcalib['intercept']
    jmp = np.loadtxt(jmpfilename, dtype=[('jmpx','float'),('jmpy','float'),('jmpflux','float')])
    #jmp = np.loadtxt(jmpfilename, dtype=[('jmpx','float'),('jmpy','float'),('jmpflux','float')])
    q = []
    for j in jmp: 
         q.append(slope * j['jmpflux'] + intercept)
    #np.savetxt(str(fluxcalib['img'])+str(fluxcalib['ccd'])+'newjmp1'+'.dat',q)
    np.savetxt('J'+'-'+str(fluxcalib['img'])+str(fluxcalib['ccd'])+'newjmp1'+'.dat',q)
	
	
	
