# Rename Olympus files with their EXIF date and remove raw images without compressed equivalent
"""
The script removes raw images without their compressed versions and it renames files with the timestamp of their creation date. The date is not extracted from the ORF files but this script renames them by taking it from the compressed one.
"""

import os
import re
from itertools import islice
from time import perf_counter
from exif import Image # https://pypi.org/project/exif/ It cannot process .ORF files

MAX = 5 # Limit of number of files to list in the output

def show_menu():
    print()
    print("Enter 1 to see the list of files.")
    print("Enter 2 to remove orphan ORF files and rename files with their EXIF date.")
    print("Enter 0 to exit the application.")    
    option = input("\nEnter your option: ")
    return option


def list_files(path) -> list:
    files = sorted(os.listdir(path))
    # Change to the target directory in the same way as the UNIX cd command.
    os.chdir(path) 
    return files


def show_files(files, path):
    fslashes = len([key for key, val in enumerate(path) if val in set(["/"])]) 
    print("\nThere are {} files in [...]/{}. These are the first {}:".format(len(files),path.split("/")[fslashes],MAX))
    count = 0
    while count < MAX:
        for i in islice(enumerate(files), 0, MAX):
            count += 1
            print(i[0]+1,': ',i[1], sep="")
    print('[...]')


def isImage(file) -> bool : # the file is an Image object
    with open(file, 'rb') as image_file:
        try:
            my_image = Image(image_file)
            return my_image.has_exif
        except:
            return False


def extensionORF(pattern,string) -> bool: # the file has an orf extension
    return re.match(rf"{pattern}.[Oo][Rr][Ff]$",string)


def classifyFiles(files) -> tuple:
    compressed, raw = [], []
    for file in files:
        filename = file.split('.') # split() returns a list
        # Is Image object as per the module exif
        if isImage(file):
            compressed.append(file)
        elif extensionORF(filename[0],file):
            raw.append(file) # add the compressed image
    return compressed, raw


def listCommonName(jpgs,orfs) -> list:
    paired = []
    for jpg in jpgs:
        r = re.compile(jpg.split('.')[0])
        if len(list(filter(r.match, orfs))) == 1:
            paired.append(jpg.split('.')[0])
    return paired


def rename_orf(filename,new_name, raw):
    r = re.compile(filename+"\.[Oo][Rr][Ff]")
    newlist = list(filter(r.match, raw))
    new_orf_name = new_name + '.orf'
    for elem in newlist:
        os.rename(elem,new_orf_name)


def rename(files, paired, compressed, raw) -> tuple:
    removed, renamed = 0, 0
    for file in files:
        if file.split('.')[0] not in paired and file not in compressed:
            try:
                os.remove(file)
                removed += 1
            except:
                print("Couldn't delete file {}".format(file))
        elif file.split('.')[0] in paired and file in compressed:
            tagged = Image(file)
            new_name = tagged.datetime_original.replace(":", "").replace(" ","_")
            new_jpg_name = new_name + '.jpg'
            os.rename(file,new_jpg_name)
            renamed += 1
            if rename_orf(file.split('.')[0],new_name, raw):
                renamed += 1
    return removed, renamed

# MAIN

# Ask where the folder with the files is.
path = input("Enter the path of the folder containing the Olympus files, for instance /home/user/downloads: ")
while not os.path.exists(path):
    path = input("Enter the path of the folder containing the Olympus files, for instance /home/user/downloads: ")

option = show_menu()

while option != '0':
    files = list_files(path) # refresh the list so that the options are independent to each other
    if option == '1':
        show_files(files,path)
    elif option == '2':
        start = perf_counter()
        jpgs = classifyFiles(files)[0]
        orfs = classifyFiles(files)[1]
        paired = listCommonName(jpgs,orfs)
        changes = rename(files, paired, jpgs, orfs)
        end = perf_counter()
        if changes[0] > 0 and changes[1] > 0:
            print("\n{} ORF files without equivalent JPG were deleted.".format(changes[0]))
            print("Renamed {} files with their EXIF dates in {} seconds.".format(changes[1], round(end-start,1)))
        elif changes[0] > 0 and changes[1] == 0:
            print("\n{} ORF files without equivalent JPG were deleted in {} seconds.".format(changes[0],round(end-start,1)))
        elif changes[0] == 0 and changes[1] > 0:
            print("\nAll the raw ORF files have compressed JPG versions. No raw file to remove.") 
            print("Renamed {} files with their EXIF dates in {} seconds.".format(changes[1], round(end-start,1)))
        else:
            print("\nNo file removed or renamed.")
    else:
        print("\nWrong option.")
    option = show_menu()        

print("\nBye.\n")