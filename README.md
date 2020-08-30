# Olympus-file-manager
This application renames batches of ORF files with the date and time of the creation of the picture. The date in the files names allow the storage of massive amounts of images recorded in RAW mode in the same folder, easy to sort and select

[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg)](/LICENSE.md)

# 1. Overview

## 1.a. RAW files and their JPEG equivalent

Olympus cameras save their loss less compressed RAW pictures in a ORF file format. The size of ORF files is approx. 17.3 MB. The size of their equivalent lossy compressed JPEG ones is rarely larger than 10 MB (even for counts of pixels larger than 3200 x 2400 and compression rates of 1/2.7).


## 1.b. Managing JPEG and ORF files

The imported JPEG image files from Olympus digital cameras are easier to browse than the heavier ORF ones because computers load JPEG files faster. 

Image viewers allow the removal of consecutive JPEG files as you examine the content of the folder containing the imported images. The deletion of JPEG files leaves their ORF equivalent in the folder.

## 1.c. File names of Olympus cameras

Olympus cameras name the image files with as Pmdd0000.jpg (for sRGB color space) where 'm' is month and 'dd' day, e.g. P1260078.JPG and P1260078.ORF.

Read more at [Olympus file name syntax](https://en.wikipedia.org/wiki/ORF_format#File_name_syntax)).

# 2. Get started

This application removes orphaned ORF files whose JPEG equivalent ones where removed while browing the folder in a GUI application and renames the remaing JPEG and ORF files with the timestamp of the creation of the image.

This application is written in Python so it runs successfully on the following operating systems:

- _Linux_
- _Windows_
- _Mac OS_

as long as they have Python installed.

# 3. Develop

This application requires Python >=3.6 and the project [exif 1.0.0](https://pypi.org/project/exif/).
- **Found issues?** Then please **file an issue** [here](https://github.com/ruben-mar/Olympus-file-manager/issues).


