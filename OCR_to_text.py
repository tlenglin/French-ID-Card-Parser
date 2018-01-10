import argparse
import imutils
import os
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to images directory")
args = vars(ap.parse_args())

os.system('/Users/tlenglin/.brew/Cellar/tesseract/3.05.01/bin/tesseract ./step2.jpg step3')
time.sleep(2)
#def revert_file():
    

#def check_first_line():
    

#def check_first_line():


# def check_MRZ(mrz):
#     line1, line2 = mrz.split("\n")
#     if check_first_line(line1) == 1 and check_second_line(line2) == 1:
#         return 1
#     else:
#         return 0

#fixers
letters = {'0': 'O', '1': 'I', '2': 'Z', '4': 'A', '5': 'S', '6': 'G', '8': 'B' }
numbers = {'B': '8', 'C': '0', 'D': '0', 'G': '6', 'I': '1', 'O': '0', 'Q': '0', 'S': '5', 'Z': '2'}

def line_fixer(line1, line2):
    line1 = line1.upper()
    line2 = line2.upper()
    for i in range(len(line1)):
        if i < 31 and letters.get(line1[i]) != None:
            line1[i] = letters[line1[i]]
        elif i > 30 and numbers.get(line1[i]) != None:
            line1[i] = numbers[line1[i]]

    for i in range(len(line2)):
        if ((i > 12 and i < 27)) and letters.get(line2[i]) != None:
            line2 = line2[:13] + line2[13:27].replace(line2[i], letters[line2[i]]) + line2[27:]
        elif (i < 13 or (i > 26 and i < 34)) and numbers.get(line2[i]) != None:
            line2 = line2[:13].replace(line2[i], numbers[line2[i]]) + line2[13:27] + line2[27:34].replace(line2[i], numbers[line2[i]]) + line2[34:]
    return line1 + line2

def fill_file(mrz, filename):
    file = open(filename, "w")
    file.write(mrz)
    file.close()

def empty_line(line): #si ligne pas complete, ou trop longue ? 
    for i in range(len(line)):
        if line[i] != " ":
            return 0
    return 1

def reversed_line(line):
    for i in range(len(line)):
        if line[i] == '>':
            return 0
    return 1

file = open("step3.txt", "r")

cleaned_MRZ = ''

i = 0
lines = {}
for line in file:
    if line is not None and empty_line(line) == 0:
        i = i + 1
        if reversed_line(line) == 0:
            #revert_file()
            print "error : file reverted"
            sys.exit
        lines[str(i)] = line
cleaned_MRZ = line_fixer(lines["1"], lines["2"])

fill_file(cleaned_MRZ, "step4.txt")

# if check_MRZ(cleaned_MRZ) == 1:
#     fill_file(cleaned_MRZ)
# else:
#     return 0