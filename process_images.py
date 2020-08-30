# Rename Olympus files with their EXIF date
"""
Script to rename image files with their EXIF date
It renames file with the extensions JPG and ORF (Unprocessed RAW photo taken with an Olympus digital camera)
The date is not extracted from the ORF file (see https://exiftool.org/TagNames/Olympus.html)
"""

import os
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

    
def list_files(path):
    # Return a list containing the names of the entries in the directory given by path.
    if os.path.exists(path):
        candidates = sorted(os.listdir(path))
        # Change to the target directory in the same way as the UNIX cd command.
        os.chdir(path)
    return candidates


def list_jpgs(candidates):
    jpgs = []
    for i in range(0,len(candidates)):
        file = candidates[i].split('.',maxsplit=1)
        if fnmatch.fnmatch(file[1], 'JPG'):
           jpgs.append(candidates[i])
    return jpgs


def show_files(candidates):
    for elem in candidates:
        print(elem)


def list_orfs(candidates):
    orfs = []
    for i in range(0,len(candidates)):
        file = candidates[i].split('.',maxsplit=1)
        if fnmatch.fnmatch(file[1], 'ORF'):
           orfs.append(candidates[i])
    return orfs


def triage_files(candidates, jpgs, orfs):
    paired = []
    unpaired = []
    for candidate in candidates:
        file = candidate.split('.',maxsplit=1)
        extension = file[1]
        reconstructed = str(file[0])+'.JPG'
        if fnmatch.fnmatch(extension, 'ORF') and reconstructed in jpgs:
            print("{} to paired".format(candidate))
            paired.append(candidate)
        elif fnmatch.fnmatch(extension, 'ORF') and reconstructed not in jpgs:
            print("{} to unpaired".format(candidate))
            unpaired.append(candidate)
    print("Paired are {}".format(paired))
    print("Unpaired are {}".format(unpaired))
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
path = input("Enter the location of the folder containing the JPEG files, for instance /home/user/pics: ")

content_dir =  list_files(path)

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