# Rename Olympus files with their EXIF date
"""
Script to rename image files with their EXIF date
It renames file with the extensions JPG and ORF (Unprocessed RAW photo taken with an Olympus digital camera)
The date is not extracted from the ORF file (see https://exiftool.org/TagNames/Olympus.html)
"""

import os
import re
import fnmatch
from itertools import islice
from exif import Image # https://pypi.org/project/exif/ It cannot process .ORF files

MAX = 5 # Limit of number of files to list in the output

def show_menu():
    print()
    print("Enter 1 to see the list of files.")
    print("Enter 2 to remove orphan ORF files.")
    print("Enter 3 to rename files with their EXIF date.")
    print("Enter 0 to exit the application.")    
    option = input("\nEnter your option: ")
    return option


def list_files(path) -> list:
    if os.path.exists(path):
        candidates = sorted(os.listdir(path))
        # Change to the target directory in the same way as the UNIX cd command.
        os.chdir(path) 
    return candidates


def isImage(file) -> bool : # the filename is an Image object
    with open(file, 'rb') as image_file:
        try:
            my_image = Image(image_file)
            my_image.has_exif
            return True
        except:
            return False


def pairImages(files):
    images =[]
    enum = enumerate(files)
    for e in enum:
        filename = e[1].split('.') # split() returns a list
        # Is Image and the filename doesn't contain more than one dot?
        if isImage(e[1]) and len(filename) < 3:
            for file in files:
                if re.match(rf"{filename[0]}.[Oo][Rr][Ff]$", file):
                    el = list(e) # turn the tuple to list so it can append elements
                    el.append(file) # add the raw image
                    images.append(el) # add the compressed image
    return images

path = input("Enter the location of the folder containing the Olympus files, for instance /home/user/pics: ")

files = list_files(path)

paired = pairImages(files)

print(paired)


"""

def show_files(files, path):
    fslashes = len([key for key, val in enumerate(path) if val in set(["/"])]) 
    print("\nThere are {} files in [...]/{}. These are the first {}:\n".format(len(files),path.split("/")[fslashes],MAX))
    count = 0
    while count < MAX:
        for i in islice(files, 0, MAX):
            count += 1
            print(i)
    print('[...]')


def rename_files(jpgs, orfs):
    count = 0
    for jpg in jpgs:
        filename = jpg.split('.',maxsplit=1)[0]
        tagged = Image(jpg)
        new_name = tagged.datetime_original.replace(":", "").replace(" ","_")
        if new_name != '0000-00-00 00:00:00.0000':
            new_jpg_name = new_name + '.jpg'
            if jpg != new_jpg_name and new_jpg_name != '0000-00-00 00:00:00.0000':
                os.rename(jpg,new_jpg_name)
                count += 1
                print(jpg ,' > ', new_jpg_name)
            orf = filename + '.' +'orf' 
            if orf in orfs:
                new_orf_name = new_name + '.orf'
                if orf != new_orf_name:
                    os.rename(orf,new_orf_name)
                    count += 1
                    print(orf ,' > ', new_orf_name)
    return count 

# MAIN

# Ask where the folder with the files is.
path = input("Enter the location of the folder containing the Olympus files, for instance /home/user/pics: ")

option = show_menu()

while option != '0':
    files = list_files(path) # refresh the list so that the options are independent to each other
    if option == '1':
        show_files(files,path)
    elif option == '2':
        print("\nThere are {} files.\n".format(len(files)))
        if remove_unpaired(find_mismatch(classify_by_extension(files))):
            print("\nAll the ORF files without equivalent JPEG were deleted.")
        else:
            print("\nAll the raw ORF files have compressed JPEG versions. No raw file to remove.")
    elif option == '3':
        print("\nThere are {} files.\n".format(len(files)))
        res = rename_files(classify_by_extension(files)[0], classify_by_extension(files)[1])
        if res > 0:
            print("\nRenamed {} files with their EXIF dates.".format(res))
        else:
            print("\nNo file renamed.")
    else:
        print("\nWrong option.")
    option = show_menu()        

print("\nBye.\n")
"""