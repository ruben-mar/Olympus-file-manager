README

# Olympus-file-manager

This application renames batches of ORF files with the date and time of the creation of the picture. The date in the file names allow the storage of batches of images recorded in RAW mode in the same folder, easy to sort and select.

[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg)](/LICENSE.md)

# 1\. Overview

## 1.1. RAW files and their JPEG equivalent

Olympus cameras save their loss less compressed RAW pictures in a ORF file format, based in TIFF. The size of ORF files is approx. 17.3 MB. The size of their equivalent lossy compressed JPEG ones is rarely larger than 10 MB (even for counts of pixels larger than 3200 x 2400 and compression rates of 1/2.7).

## 1.2. Exploring your photos and managing JPEG and ORF files

The imported JPEG image files from Olympus digital cameras are easier to browse than the heavier ORF ones because computers load the comparatively lighter JPEG files faster.

Image viewers allow the removal of consecutive JPEG files as you examine the content of the folder containing the imported images. The deletion of JPEG files leaves their ORF equivalent in the folder. These orphan ORF files can be deleted.

## 1.3. File names of Olympus cameras

Olympus cameras name the image files with as **Pmdd0000.jpg** ("P" for sRGB color space) where 'm' is month and 'dd' day, e.g. P1260078.JPG and P1260078.ORF.

Read more at [Olympus file name syntax](https://en.wikipedia.org/wiki/ORF_format#File_name_syntax).

This script manages extensions .jpg in lower and upper case like .JPG and even files with missing extensions.

# 2\. Get started

This application removes orphaned ORF files whose JPEG equivalent ones where removed while browing the folder in a GUI application and renames the remaing JPEG and ORF files with the timestamp of the creation of the image.

## 2.1. Requirements

This application is written in Python so it runs successfully on the following operating systems:
    - *Linux*
    - *Windows*
    - *Mac OS*
as long as they have Python >=3.6 and the project [exif](https://pypi.org/project/exif/) installed.

> pip install exif

## 2.2. How to use

Import the files from your Olympus camera into your computer. The script removes files that are not EXIF tagged files or that that don't have JPG or ORF extensions. 

Run the script from the command line

> python3 process_images.py

## 2.3. Disclaimer

For better performance you should create a folder specifically for your import with only the imported files from your Olympus camera. The author of this script releases it as is, without any warranty of its correct operation. Back up your files before executing the script. 

# 3\. Develop

- **Found issues?** Then please **file an issue** [here](https://github.com/ruben-mar/Olympus-file-manager/issues).