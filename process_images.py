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
        return(candidates)


def show_files(files, path):
    fslashes = len([key for key, val in enumerate(path) if val in set(["/"])]) 
    print("\nThere are {} files in [...]/{}. These are the first {}:\n".format(len(files),path.split("/")[fslashes],MAX))
    count = 0
    while count < MAX:
        for i in islice(files, 0, MAX):
            count += 1
            print(i)
    print('[...]\n')


def classify_by_extension(candidates):
    jpgs, orfs = [], []
    for i in range(0,len(candidates)):
        file = candidates[i].split('.',maxsplit=1)
        if fnmatch.fnmatch(file[1], '[Jj][Pp][Gg]'):
            jpgs.append(candidates[i])
        elif fnmatch.fnmatch(file[1], '[Oo][Rr][Ff]'):
            orfs.append(candidates[i])
    return jpgs, orfs


def find_mismatch(classified):
    unpaired = []
    for candidate in classified[0]+classified[1]:
        filename = candidate.split('.')
        reconstructed = str(filename[0])+'.JPG'
        regexp = r'[Oo][Rr][Ff]'
        z = re.match(regexp,filename[1])
        if z and reconstructed.lower() not in classified[0]:
            unpaired.append(candidate)
    return unpaired


def remove_unpaired(orphan_orfs):
    if isinstance(orphan_orfs,list) and len(orphan_orfs) > 0:
        print("\nThere are {} ORF raw files without equivalent JPG compressed versions.\n".format(len(orphan_orfs)))
        for orphan in orphan_orfs:
            try:
                os.remove(orphan)
                print("Removed {}".format(orphan))        
            except OSError as e:  ## if failed, report it back to the user ##
                print("Error: %s - %s." % (e.file, e.strerror))


def rename_files(jpgs, orfs):
    count = 0
    for jpg in jpgs:
        filename = jpg.split('.',maxsplit=1)[0]
        tagged = Image(jpg)
        new_name = tagged.datetime_original.replace(":", "").replace(" ","_")
        new_jpg_name = new_name + '.jpg'
        if jpg != new_jpg_name:
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
    files = list_files(path) # refresh the list so that the options are independent of their previous one
    if option == '1':
        show_files(files,path)
    elif option == '2':
        if remove_unpaired(find_mismatch(classify_by_extension(files))):
            print("\nAll the ORF files without equivalent JPEG were deleted.")
        else:
            print("\nAll the raw ORF files have compressed JPEG versions. No raw file to remove.")
    elif option == '3':
        res = rename_files(classify_by_extension(files)[0], classify_by_extension(files)[1])
        if res > 0:
            print("Renamed {} files with their EXIF dates.".format(res))
        else:
            print("\nNo file renamed.")

    else:
        print("\nWrong option.")
        
    option = show_menu()        

print("\nBye.\n")   