# OSSOS_LSST
Research with the LSST group using stack on the OSSOS survey

The goal of this project is to analyze the data found during the Outer Solar System Origins Survey (OSSOS) using the LSST stack to understand how well the programs compare to the methods used by OSSOS for faint object detection. The LSST stack was run on the same cfht images used for OSSOS, and the results were compared to that of the matt and jmp programs. A 1.5 pixel tolerance was set to match the catalogs against one another: LSST to jmp, LSST to matt, and LSST to jmp and matt matched.

Once the sources were extracted from the images, the matt catalog was
plotted against its LSST catalog matches, and a linear regression was
performed to convert matt readings to LSST standard flux readings. The same
was done for the other matches found. A cut was introduced to avoid taking the saturated readings into account. On average, for the JMP catalog the cut was 33000, and 2.5e6 for matt. The linear regression code for JMP is below, it parallels those for the matt and matches. 

M-1609158_ccd01.png
Example of linear regression on the matt-lsst matches, with the 2.5e6 flux cut. The cut could have been established around 3e6, but as is seen here the majority of the points are in the lower half of the linear fit, so it was not necessary.


With the slopes and intercepts from the linear regression, I then transferred the jmp and matt findings to LSST flux readings. Example of the transfer code shown below.


After all the matches were transferred to LSST standard flux, then I made histograms of the different matches by image and ccd number.

It may be seen here that there are point sources that do not seem to be part of background noise that only LSST's programs have caught, ones that may be viable Trans-Neptunian Objects (TNOs). There are some issues with the background subtracting that are to be addressed in later runs on the image.

Plots of the SNR ratios were made for the LSST catalog, since the error in flux reading was known. Using curvefit, the fit was found to be ~flux^(1/2). Knowing that the matt and JMP catalogs are on the same images, it may be possible that the SNR for matt and JMP has the same corellation. Under that assumption, I plotted the SNR of LSST, matt and JMP, using the matt and jmp detections that are within a 1.5 pixel tolerance of each other. The histogram may be viewed in the issues section. 

