import imutils
import os
import time


#def revert_file():
    

#def check_first_line():
    

#def check_first_line():


# def check_MRZ(mrz):
#     line1, line2 = mrz.split("\n")
#     if check_first_line(line1) == 1 and check_second_line(line2) == 1:
#         return 1
#     else:
#         return 0

def choose_line(lines):
    i = 0
    res = 0
    j = 0
    while i < range(len(lines)) - 1:
        if (len(lines[str(i)]) + len(lines[str(i + 1)])) > res:
            res = len(lines[str(i)]) + len(lines[str(i + 1)])
            j = i
    lines["1"] = lines[str(j)]
    lines["2"] = lines[str(j + 1)]
    return lines
        

def delete_spaces(line):
    line = line.replace(" ", "")
    return line

#fixers
letters = {'0': 'O', '1': 'I', '2': 'Z', '4': 'A', '5': 'S', '6': 'G', '8': 'B' }
numbers = {'B': '8', 'C': '0', 'D': '0', 'G': '6', 'I': '1', 'O': '0', 'Q': '0', 'S': '5', 'Z': '2'}

def line_fixer(line1, line2):
    line1 = line1.upper()
    line2 = line2.upper()

    for i in range(len(line1)):
        if i < 30 and letters.get(line1[i]) != None:
            line1 = line1[:30].replace(line1[i], letters[line1[i]]) + line1[30:]
        elif i > 29 and numbers.get(line1[i]) != None:
            line1 = line1[:30] + line1[30:].replace(line1[i], numbers[line1[i]])
    for i in range(len(line2)):
        if ((i > 12 and i < 27)) and letters.get(line2[i]) != None:
            line2 = line2[:13] + line2[13:27].replace(line2[i], letters[line2[i]]) + line2[27:]
        elif (i < 13 or (i > 26 and i < 34)) and numbers.get(line2[i]) != None:
            line2 = line2[:13].replace(line2[i], numbers[line2[i]]) + line2[13:27] + line2[27:34].replace(line2[i], numbers[line2[i]]) + line2[34:]
    return [line1, line2]

def fill_file(mrz, filename):
    file = open(filename, "w")
    file.write(mrz)
    file.close()

def empty_line(line): #si ligne pas complete, ou trop longue ? 
    line = line.replace(" ", "")
    for i in range(len(line)):
        if line[i] != " ":
            return 0
    if len(line) < 15:
        return 0
    return 1

def reversed_line(line):
    for i in range(len(line)):
        if line[i] == '>':
            return 0
    return 1

def check_begining_line1(line1):
    if (i = line1.find("IDF", 0, 10)) != -1 or (j = line1.find("DFR", 0, 10)) != -1 or (k = line1.find("FRA", 0, 10)) != -1:
        if i != -1:
            index = i
        elif j != -1:
            index = j - 1
        else :
            index = j - 2
    else :
        index = -1
    return index

def check_end_line1(line1):
    if (i = line1.rfind("<", 15)) != -1:
        index = i
    else :
        index = -1
    return index

def align_line1(aligned_MRZ, line1):
    if ((i1_beg = check_begining_line1(line1)) != -1):
        i = 0
        while (i1_beg < len(line1) and i < len(aligned_MRZ)):
            if score1(aligned_MRZ[:i] + line1[i1_beg] + align_line1[i + 1:]) >= score1(aligned_MRZ):
                aligned_MRZ = aligned_MRZ[:i] + line1[i1_beg] + align_line1[i + 1:]
            else:
                break
            i = i + 1
            i1_beg = i1_beg + 1
    if ((i1_end = check_begining_line1(line1)) != -1):
        i = 0
        i1_end = i1_end + 6 #si on sort de la chaine ?
        while (i1_end >= 0 and i >= 0):
            if score1(aligned_MRZ[:i] + line1[i1_end] + align_line1[i + 1:]) >= score1(aligned_MRZ):
                aligned_MRZ = aligned_MRZ[:i] + line1[i1_end] + align_line1[i + 1:]
            else:
                break
            i = i - 1
            i1_end = i1_end - 1
    return aligned_MRZ


def align_line2(aligned_MRZ, line2):
    


def align_lines(aligned_MRZ, line1, line2):
    aligned_MRZ[0] = align_line1(aligned_MRZ[0], line1)
    aligned_MRZ[1] = align_line1(aligned_MRZ[0], line2)
    return aligned_MRZ

def score(line1, line2):



def ocr():
    os.system('/Users/tlenglin/.brew/Cellar/tesseract/3.05.01/bin/tesseract ./step2.jpg step3' )
    time.sleep(2)

    file = open("step3.txt", "r")

    i = 0
    lines = {}
    for line in file:
        if line is not None and empty_line(line) == 0:
            i = i + 1
            if reversed_line(line) == 0:
                #revert_file()
                print "error : file reverted"
                sys.exit
            line = delete_spaces(line)
            lines[str(i)] = line
    if (i > 2):
        print "more than 2 lines detected"
        lines = choose_line(lines)

    cleaned_MRZ = line_fixer(lines["1"], lines["2"])
    return cleaned_MRZ



cleaned_MRZ = ocr()
aligned_MRZ = ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]
aligned_MRZ = align_lines(aligned_MRZ, cleaned_MRZ[0], cleaned_MRZ[1])
s0 = score(aligned_MRZ[0], aligned_MRZ[1])

if s0 < 80:
    MRZ_crop.MRZ_crop(90)
    new_MRZ = ocr()
    aligned_MRZ = align_lines(aligned_MRZ, new_MRZ[0], new_MRZ[1])
    MRZ_crop.MRZ_crop(160)
    new_MRZ = ocr()
    aligned_MRZ = align_lines(aligned_MRZ, new_MRZ[0], new_MRZ[1])
    s1 = score(aligned_MRZ[0], aligned_MRZ[1])
    if s1 < 80:
        MRZ_crop.MRZ_crop(60)
        new_MRZ = ocr()
        aligned_MRZ = align_lines(aligned_MRZ, new_MRZ[0], new_MRZ[1])
        MRZ_crop.MRZ_crop(190)
        new_MRZ = ocr()
        aligned_MRZ = align_lines(aligned_MRZ, new_MRZ[0], new_MRZ[1])
        s2 = score(aligned_MRZ[0], aligned_MRZ[1])
        if s2 < 80:
            if s2 > 50:
                print "uncertain result"
            else:
                sys.exit()


fill_file(cleaned_MRZ, "step4.txt")