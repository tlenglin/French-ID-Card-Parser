import imutils
import os
import time
import re


#def revert_file():

def choose_line(lines):
    i = 1
    res = 0
    j = 1
    #print len(lines)
    while i < len(lines) - 1:
        if (len(lines[str(i)]) + len(lines[str(i + 1)])) > res:
            res = len(lines[str(i)]) + len(lines[str(i + 1)])
            j = i
        i = i + 1
        #print i
    lines["1"] = lines[str(j)]
    lines["2"] = lines[str(j + 1)]
    return lines
        

def delete_spaces(line):
    line = line.replace(" ", "")
    line = line.replace("\n", "")
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
    file.write(mrz[0])
    file.write("\n")
    file.write(mrz[1])
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
    i = line1.find("IDF", 0, 10)
    j = line1.find("DFR", 0, 10)
    k = line1.find("FRA", 0, 10)
    if (i != -1 or j != -1 or k != -1):
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
    i = line1.rfind("<", 15)
    if i != -1:
        index = i
    else :
        index = -1
    return index

def check_begining_line2(line2):
    i = 0
    while (re.findall('[A-Z]{2}|$', line2[i:i+2])[0] == '' and i < (len(line2) - 1)):
        i = i + 1
    if i == len(line2) - 1:
        index = -1
    else:
        index = i
    return index

def check_end_line2(line2):
    if re.findall('(\d+(M|F)\d+$)|$', line2)[0] == '':
        index = -1
    else:
        index = re.finditer('(\d+(M|F)\d+$)|$', line2)
        print index
    return index

def score1(line1):
    print("starting score1")
    #print line1
    s = check_char(0, "I", line1, 1, -1)
    s = s + check_char(1, "D", line1, 2, -2)
    s = s + check_char(2, "F", line1, 3, -3)
    s = s + check_char(3, "R", line1, 4, -4)
    s = s + check_char(4, "A", line1, 5, -5)
    i = 5
    while (i < 36):
        if (i < 30):
            s = s + check_letters(i, line1, 1, -1)
        else:
            s = s + check_digits(i, line1, 1, -1)
        i = i + 1
    return s * 100 / 45

def score2(line2):
    print("starting score2")
    i = 0
    s = 0
    while (i < 36):
        if (i < 13 or (i > 26 and i < 34) or i == 35):
            s = s + check_digits(i, line2, 1, -1)
        elif (i > 12 and i < 27):
            s = s + check_letters(i, line2, 1, -1)
        else:
            if check_char(34, "M", line2, 5, -5) == -5 and check_char(34, "F", line2, 5, -5) == -5:
                s = s - 5
            else:
                s = s + 5
        i = i + 1
    return s * 100 / 40
    

def align_line1(aligned_MRZ, line1):
    i1_beg = check_begining_line1(line1)
    i1_end = check_end_line1(line1)
    if (i1_beg != -1):
        i = 0
        while (i1_beg < len(line1) and i < len(aligned_MRZ)):
            if score1(aligned_MRZ[:i] + line1[i1_beg] + aligned_MRZ[i + 1:]) >= score1(aligned_MRZ):
                aligned_MRZ = aligned_MRZ[:i] + line1[i1_beg] + aligned_MRZ[i + 1:]
            else:
                break
            i = i + 1
            i1_beg = i1_beg + 1
    if (i1_end != -1):
        i = len(aligned_MRZ) - 1 # -1  sur ? et i1_end aussi -1 ?
        i1_end = i1_end + 6 #si on sort de la chaine ?
        if i1_end >= len(line1):
            i = 36 - (i1_end - len(line1))
            i1_end = len(line1) - 1
            
        # print "i = ", i
        # print "i1_end = ", i1_end
        # print "line1[end] = ", line1[i1_end]
        # print "test"
        while (i1_end >= 0 and i >= 0):
            # print("ON EST DANS LA BOUCLE")
            # print i
            # print i1_end
            # print aligned_MRZ[:i]
            # print len(line1)
            # print line1[i1_end]
            # print len(aligned_MRZ)
            # print aligned_MRZ[i]
            if ((i == len(aligned_MRZ) - 1) and (score1(aligned_MRZ[:i] + line1[i1_end]) >= score1(aligned_MRZ))): #atenttion premiere somme avec i = len
                aligned_MRZ = aligned_MRZ[:i] + line1[i1_end]
                #print "on est dans le premier if"
            elif score1(aligned_MRZ[:i] + line1[i1_end] + aligned_MRZ[i + 1:]) >= score1(aligned_MRZ):
                aligned_MRZ = aligned_MRZ[:i] + line1[i1_end] + aligned_MRZ[i + 1:]
                #print "on est dans le if"
            else:
                #print "on est dans le break"
                break
            i = i - 1
            i1_end = i1_end - 1
        #print "sortie de while"
    return aligned_MRZ

def align_line2(aligned_MRZ, line2):
    i2_beg = check_begining_line2(line2)
    i2_end = check_end_line2(line2)
    if (i2_beg != -1):
        i = 0
        if i2_beg < 13:
            i2_beg = 0
            i = 13 - i2_beg
        else:
            i2_beg = i2_beg - 13
        while (i2_beg < len(line2) and i < len(aligned_MRZ)):
            if score2(aligned_MRZ[:i] + line2[i2_beg] + aligned_MRZ[i + 1:]) >= score2(aligned_MRZ):
                aligned_MRZ = aligned_MRZ[:i] + line2[i2_beg] + aligned_MRZ[i + 1:]
            else:
                break
            i = i + 1
            i2_beg = i2_beg + 1
    if (i2_end != -1):
        i = len(aligned_MRZ)
        i2_end = i2_end + 1
        if i1_end >= len(line1):
            i = 36 - (i1_end - len(line1))
            i1_end = len(line1) - 1
        while (i2_end >= 0 and i >= 0):
            if ((i == len(aligned_MRZ) - 1) and (score2(aligned_MRZ[:i] + line2[i2_end]) >= score2(aligned_MRZ))): #atenttion premiere somme avec i = len
                aligned_MRZ = aligned_MRZ[:i] + line2[i2_end]
            if score2(aligned_MRZ[:i] + line2[i2_end] + aligned_MRZ[i + 1:]) >= score2(aligned_MRZ): #atenttion premiere somme avec i = len
                aligned_MRZ = aligned_MRZ[:i] + line2[i2_end] + aligned_MRZ[i + 1:]
            else:
                break
            i = i - 1
            i2_end = i2_end - 1
    return aligned_MRZ


def align_lines(aligned_MRZ, line1, line2):
    aligned_MRZ[0] = align_line1(aligned_MRZ[0], line1)
    aligned_MRZ[1] = align_line2(aligned_MRZ[0], line2)
    return aligned_MRZ

def check_char(index, X, line, pos, neg):
    if line[index] == "x":
        return 0
    elif line[index] == X:
        return pos
    else:
        return neg

def check_letters(index, line, pos, neg):
    if line[index] == "x":
        return 0
    elif re.findall('[A-Z]|<|$', line[index]) != '':
        return pos
    else:
        return neg

def check_digits(index, line, pos, neg):
    if line[index] == "x":
        return 0
    elif re.findall('[0-9]|$', line[index]) != '':
        return pos
    else:
        return neg

def score(line1, line2):
    return (score1(line1) + score2(line2)) / 2

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

    print "test sortie de if"
    print lines
    cleaned_MRZ = line_fixer(lines["1"], lines["2"])
    return cleaned_MRZ


print "starting OCR_to_text"
cleaned_MRZ = ocr()
print "sortie de ocr()"
print cleaned_MRZ
aligned_MRZ = ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]
aligned_MRZ = align_lines(aligned_MRZ, cleaned_MRZ[0], cleaned_MRZ[1])
s0 = score(aligned_MRZ[0], aligned_MRZ[1])
print "s0 = ", s0

if s0 < 90:
    print "s0 < 80"
    from MRZ_crop import MRZ_crop
    MRZ_crop(90)
    new_MRZ = ocr()
    print "passage du 2eme ocr()"
    aligned_MRZ = align_lines(aligned_MRZ, new_MRZ[0], new_MRZ[1])
    MRZ_crop(160)
    new_MRZ = ocr()
    print "passage du 3eme ocr"
    aligned_MRZ = align_lines(aligned_MRZ, new_MRZ[0], new_MRZ[1])
    s1 = score(aligned_MRZ[0], aligned_MRZ[1])
    print "s1 = ", s1
    if s1 < 90:
        print "s1 < 80"
        MRZ_crop(60)
        new_MRZ = ocr()
        aligned_MRZ = align_lines(aligned_MRZ, new_MRZ[0], new_MRZ[1])
        MRZ_crop(190)
        new_MRZ = ocr()
        aligned_MRZ = align_lines(aligned_MRZ, new_MRZ[0], new_MRZ[1])
        s2 = score(aligned_MRZ[0], aligned_MRZ[1])
        print "s2 = ", s2
        if s2 < 90:
            if s2 > 50:
                print "uncertain result, 50 < s2 < 80"
            else:
                print "probably no result s2 < 50"

print ("creation of step4.txt")
fill_file(aligned_MRZ, "step4.txt")