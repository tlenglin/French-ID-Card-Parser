import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="path to the ID card")
ap.add_argument("-s", "--step", help="step you want to execute : 1 for rotate, 2 for crop the mrz, 3 for the OCR, 4 for parse the mrz")
args = vars(ap.parse_args())

import_list = {}
import_list["1"] = "rotation_spacing"
import_list["2"] = "MRZ_crop"
import_list["3"] = "OCR_to_text"
import_list["4"] = "MRZ_parsing"

filename = args["file"]
image = cv2.imread(filename)
cv2.imwrite("step0.jpg", image)

if args["step"] != None:
    steps = args["step"]
    for i in range(len(steps)):
        module = import_list[steps[i]]
        command = __import__(module)
        command.run()
else:
    import rotation_spacing
    import MRZ_crop
    import OCR_to_text
    import MRZ_parsing
