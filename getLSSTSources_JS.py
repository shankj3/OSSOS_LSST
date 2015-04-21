# make sure you 
#  .. use the system wide LSST stack by using
# source /astro/apps6/opt/lsstStacks/lsst/loadLSST.csh
#  and then in the OSSOS_DATA directory, use the new afw / obs_cfht by
# cd lsstGitRepos
# setup -r obs_cfht
# setup -r afw

import lsst.daf.persistence as dafPersistence
import lsst.afw.display.ds9 as ds9
import lsst.afw.geom as afwGeom
import numpy as np
import os, sys

expnum = int(sys.argv[1])
ccdnum = int(sys.argv[2])

butler = dafPersistence.Butler('test_out_acb2')
cam = butler.mapper.camera

calexp = butler.get('calexp', dataId={'visit':expnum, 'filter':'r', 'ccd':ccdnum})
src = butler.get('src', dataId={'visit':expnum, 'filter':'r', 'ccd':ccdnum})


im = calexp.getMaskedImage().getImage()
imsize = im.getDimensions()

xoff = cam['ccd%02d'%(ccdnum)]['0,0'].getRawHorizontalOverscanBBox().getDimensions().getX()
if ccdnum < 18:
    yoff = cam['ccd%02d'%(ccdnum)]['0,0'].getRawVerticalOverscanBBox().getDimensions().getY()
else:
    yoff = 0

# Retrieve the LSST catalogs
lsst = {}
lsst['x'] = []
lsst['y'] = []
lsst['flux'] = []
for s in src:
    x = s.getX()
    y = s.getY()
    flux = s.getPsfFlux()
    fluxflag = s.getPsfFluxFlag()
    if not fluxflag:
        lsst['x'].append(x)
        lsst['y'].append(y)
        lsst['flux'].append(flux)
for k in lsst:
    lsst[k] = np.array(lsst[k], 'float')
    
bbox = im.getBBox()


# Read the .jmp and .matt catalogs (and modify x/y to match LSST x/y)
jmpfile = '%s/ccd%.2d/%s%.2d.obj.jmp' %(expnum, ccdnum, expnum, ccdnum)
mattfile = '%s/ccd%.2d/%s%.2d.obj.matt' %(expnum, ccdnum, expnum, ccdnum)

try:
    file = open(jmpfile, 'r')
    jmp = {}
    jmp['x'] = []
    jmp['y'] = []
    jmp['flux'] = []
    for line in file:
        if line.startswith('#'):
            continue
        x = float(line.split()[0])
        y = float(line.split()[1])
        if ccdnum < 18:
            x = imsize.getX() - x + xoff
            y = imsize.getY() - y + yoff
        else:
            x = x - xoff
            y = y - yoff
        pt = afwGeom.PointI(int(x), int(y))
        if bbox.contains(pt):
            jmp['x'].append(x)
            jmp['y'].append(y)
            jmp['flux'].append(float(line.split()[2]))
    jmp['x'] = np.array(jmp['x'], float)
    jmp['y'] = np.array(jmp['y'], float)
    jmp['flux'] = np.array(jmp['flux'], float)
except IOError:
    print 'No JMP file %s' %(jmpfile)
    jmp = {}
    jmp['x'] = []
    jmp['y'] = []
    jmp['flux'] = []

try:
    file = open(mattfile, 'r')
    matt = {}
    matt['x'] = []
    matt['y'] = []
    matt['flux'] = []
    for line in file:
        if line.startswith('#'):
            continue
        x = float(line.split()[0])
        y = float(line.split()[1])
        if ccdnum < 18:
            x = imsize.getX() - x + xoff
            y = imsize.getY() - y + yoff
        else:
            x = x - xoff
            y = y - yoff
        pt = afwGeom.PointI(int(x), int(y))
        if bbox.contains(pt):
            matt['x'].append(x)
            matt['y'].append(y)
            matt['flux'].append(float(line.split()[2]))
    matt['x'] = np.array(matt['x'], float)
    matt['y'] = np.array(matt['y'], float)
    matt['flux'] = np.array(matt['flux'], float)
except IOError:
    print 'No MATT file %s' %(mattfile)
    matt = {}
    matt['x'] = []
    matt['y'] = []
    matt['flux'] = []


mboth = {}
mboth['x'] = []
mboth['y'] = []
mboth['flux'] = []
mboth['mattx'] = []
mboth['matty'] = []
mboth['mattflux'] = []
mboth['lsstx'] = []
mboth['lssty'] = []
mboth['lsstflux'] = []


jboth = {}
jboth['x'] = []
jboth['y'] = []
jboth['flux'] = []
jboth['jmpx'] = []
jboth['jmpy'] = []
jboth['jmpflux'] = []
jboth['lsstx'] = []
jboth['lssty'] = []
jboth['lsstflux'] = []

aboth = {}
aboth['x'] = []
aboth['y'] = []
aboth['flux'] = []
aboth['jmpx'] = []
aboth['jmpy'] = []
aboth['jmpflux'] = []
aboth['mattx'] = []
aboth['matty'] = []
aboth['mattflux'] = []

tolerance = 1.5
for x, y, flux in zip(lsst['x'],lsst['y'],lsst['flux']):
    jdiffx = jmp['x'] - x
    jdiffy = jmp['y'] - y
    jmatch = np.where((abs(jdiffx) < tolerance ) & (abs(jdiffy) < tolerance))[0]
    if len(jmatch) == 1:
        jboth['x'].append(x)
        jboth['y'].append(y)
        jboth['flux'].append(flux)
        jboth['lsstx'].append(x)
        jboth['lssty'].append(y)
        jboth['lsstflux'].append(flux)
        jboth['jmpx'].append(jmp['x'][jmatch][0])
        jboth['jmpy'].append(jmp['y'][jmatch][0])
        jboth['jmpflux'].append(jmp['flux'][jmatch][0])
        lsstjmp = zip(jboth['lsstflux'],jboth['jmpflux'],jboth['x'],jboth['y'])
        np.savetxt('J-%s_ccd%.2d.jboth' %(expnum, ccdnum), lsstjmp,header='lsstflux jmpflux x y')
        

for x, y, flux in zip(lsst['x'],lsst['y'],lsst['flux']):
    mdiffx = matt['x'] - x
    mdiffy = matt['y'] - y
    mmatch = np.where((abs(mdiffx) < tolerance ) & (abs(mdiffy) < tolerance))[0]
    if len(mmatch) == 1: 
        mboth['x'].append(x)
        mboth['y'].append(y)
        mboth['flux'].append(flux)
        mboth['lsstx'].append(x)
        mboth['lssty'].append(y)
        mboth['lsstflux'].append(flux)     
	mboth['mattx'].append(matt['x'][mmatch][0])
	mboth['matty'].append(matt['y'][mmatch][0])
	mboth['mattflux'].append(matt['flux'][mmatch][0])
	lsstmatt = zip(mboth['lsstflux'],mboth['mattflux'],mboth['x'],mboth['y'])
	np.savetxt('M-%s_ccd%.2d.mboth' %(expnum, ccdnum),lsstmatt,header='lsstflux mattflux x y')
	


for x, y, flux in zip(jmp['x'],jmp['y'],jmp['flux']):
    adiffx = matt['x'] - x
    adiffy = matt['y'] - y
    amatch = np.where((abs(adiffx) < tolerance ) & (abs(adiffy) < tolerance))[0]
    if len(amatch) == 1: 
        aboth['x'].append(x)
        aboth['y'].append(y)
        aboth['jmpx'].append(x)
        aboth['jmpy'].append(y)
        aboth['jmpflux'].append(flux)
	aboth['mattx'].append(matt['x'][amatch][0])
	aboth['matty'].append(matt['y'][amatch][0])
	aboth['mattflux'].append(matt['flux'][amatch][0])
	ajmpmatt = zip(aboth['mattflux'], aboth['jmpflux'], aboth['x'],aboth['y'])
	np.savetxt('A-%s_ccd%.2d.aboth' %(expnum, ccdnum),ajmpmatt,header='mattflux jmpflux x y ')
	

	
'''	
jmpflux = 0
mattflux = 0

ds9.mtv(im)
with ds9.Buffering(): 
    for s in src: 
        x = s.getX()
        y = s.getY()
        ds9.dot('o', x, y, size=11, ctype='red')
        
with ds9.Buffering():
    for x, y, flux in zip(jmp['x'], jmp['y'], jmp['flux']):
        if flux > jmpflux:
            ds9.dot('o', x, y, size=8, ctype='green')
           
    for x, y, flux in zip(matt['x'], matt['y'], matt['flux']):
        if flux > mattflux:
            ds9.dot('o', x, y, size=5, ctype='blue')

mattmatchx, mattmatchy = np.loadtxt('1616316_ccd20.mboth', usecols=(2,3),unpack=True)
jmpmatchx, jmpmatchy = np.loadtxt('1616316_ccd20.jboth', usecols=(2,3), unpack=True)

with ds9.Buffering():
    for mx, my in zip(mattmatchx,mattmatchy):
        ds9.dot('x', mx, my, size=9, ctype='blue')
        
with ds9.Buffering(): 
    for jx, jy in zip(jmpmatchx,jmpmatchy):
        ds9.dot('x', jx, jy, size=18, ctype='yellow')
'''
## NOW matt, jmp and LSST are in the same x/y system.
# Go match them! (you need to match each source to one another)
# Then after that, you can figure out the scaling to match LSST flux against Matt or JMP flux
# and add the LSST sources onto the other histograms.

