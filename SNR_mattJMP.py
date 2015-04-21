import lsst.daf.persistence as dafPersistence
import lsst.afw.display.ds9 as ds9
import lsst.afw.geom as afwGeom
import numpy as np
import os, sys 
import matplotlib.pyplot as plt

np.seterr(divide='ignore', invalid='ignore')


expnum = int(sys.argv[1])
ccdnum = int(sys.argv[2])

jmpfile = '%s/ccd%.2d/%s%.2d.obj.jmp' %(expnum, ccdnum, expnum, ccdnum)
mattfile = '%s/ccd%.2d/%s%.2d.obj.matt' %(expnum, ccdnum, expnum, ccdnum)


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




lsstflux = []
lsstfluxerr = []
for s in src:
    x = s.getX()
    y = s.getY()
    flux = s.getPsfFlux()
    fluxerr = s.getPsfFluxErr()
    fluxflag = s.getPsfFluxFlag()
    if not fluxflag:
        lsstflux.append(flux)
        lsstfluxerr.append(fluxerr)

bbox = im.getBBox()

#lsstfluxerr1 = map(float,lsstfluxerr)
#print type(lsstfluxerr1)

lsstfluxerr1 = np.array(lsstfluxerr)
lsstflux1 = np.array(lsstflux)

tolerance = 1.5

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




jmpflux = aboth['jmpflux']
mattflux = aboth['mattflux']


#jmpflux = np.genfromtxt(jmpfile, usecols=(2))
#mattflux = np.genfromtxt(mattfile, usecols=(2))
SNR_jmp = np.sqrt(jmpflux)
SNR_matt = np.sqrt(mattflux)
SNR_lsst = np.sqrt(lsstflux1)


plt.hist([SNR_jmp,SNR_matt,SNR_lsst],bins=1000, histtype = 'barstacked',color=['blue','red','green'],label=['SNR for JMP','SNR for matt','SNR for lsst'],alpha = 0.5)

#plt.hist(SNR_lsst,bins=50,histtype='bar')
plt.legend()
plt.xlim(0,250)
plt.title('SNR Histogram for %s, ccd %02d' %(expnum,ccdnum))
plt.savefig('./histogramsSNR/%s_%s_histograms2.jpg' %(expnum,ccdnum))
#plt.show()

