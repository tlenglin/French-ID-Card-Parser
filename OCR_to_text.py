import argparse
import imutils
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to images directory")
args = vars(ap.parse_args())

os.system('tesseract ./MRZ/step2.jpg step3')

def revert_file():
    

def check_MRZ(mrz):


def line_fixer(line):
    

def fill_file(mrz):


def empty_line(line):
    for i in range(len(lines)):
        if i != ' '
            return 0
    return 1

def reversed_line(line):
    for i in range(len(line)):
        if i == '>'
            return 0
    return 1

file = open("step3", "r")

cleaned_MRZ = ''

for line in file:
    if line is not None and empty_line(line) == 0:
        if reversed_line(line) == 0:
            revert_file()
            return 0
        else:
            fixed_line = line_fixer(line)
            cleaned_MRZ = cleaned_MRZ + fixed_line + '\n'

if check_MRZ(cleaned_MRZ) == 1:
    fill_file(cleaned_MRZ)
else:
    return 0