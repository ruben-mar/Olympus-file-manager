# Rename Olympus files with their EXIF date
"""
Script to rename image files with their EXIF date
It renames file with the extensions JPG and ORF (Unprocessed RAW photo taken with an Olympus digital camera)
The date is not extracted from the ORF file (see https://exiftool.org/TagNames/Olympus.html)
"""

import os
import re
import fnmatch
from exif import Image # https://pypi.org/project/exif/ It cannot process .ORF files


def show_menu():
    print()
    print("Enter 1 to see the list of files.")
    print("Enter 2 to triage files.")
    print("Enter 3 to remove orphan ORF files.")
    print("Enter 4 to rename files with their EXIF date.")
    print("Enter 0 to exit the application.")    
    option = input("\nEnter your option: ")
    return option


def classify_by_extension(path):
    # Return a list containing the names of the entries in the directory given by path.
    if os.path.exists(path):
        candidates = sorted(os.listdir(path))
        # Change to the target directory in the same way as the UNIX cd command.
        os.chdir(path) 
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
            print("{} to unpaired".format(candidate))
            unpaired.append(candidate)
    return unpaired


def remove_unpaired(orphan_orfs):
    for orphan in orphan_orfs:
        try:
            os.remove(orphan)
            print("Removed {}".format(orphan))
        except OSError as e:  ## if failed, report it back to the user ##
            print("Error: %s - %s." % (e.file, e.strerror))


def rename_files(jpgs, orfs):
    for file in jpgs:
        filename = file.split('.',maxsplit=1)[0]
        tagged = Image(file)
        new_name = tagged.datetime_original.replace(":", "").replace(" ","_")
        new_jpg_name = new_name + '.jpg'
        print(file ,' > ', new_jpg_name)
        os.rename(file,new_jpg_name)
        orf = filename + '.ORF'
        if orf in orfs: # Tests whether there are ORF files as well as JPEG ones.
            new_orf_name = new_name + '.orf'
            print(orf ,' > ', new_orf_name)
            os.rename(orf,new_orf_name)

# MAIN

# Ask where the folder with the files is.
path = input("Enter the location of the folder containing the Olympus files, for instance /home/user/pics: ")

unpaired = find_mismatch(classify_by_extension(path))
remove_unpaired(unpaired)

"""
option = show_menu()

while option != '0':
    if option == '1':
        show_files(content_dir)
    elif option == '2':
        compressed = list_jpgs(content_dir)
        raws = list_orfs(content_dir)
        orphaned = triage_files(content_dir, compressed, raws)
    elif option == '3':
        remove_unpaired(orphaned)
        print("\nAll the ORF files without equivalent JPEG were deleted.")
    elif option == '4':
        rename_files(compressed, raws)
    else:
        print("\nWrong option.")
        
    content_dir =  list_files(path)
    option = show_menu()        

print("\nBye.\n")
"""