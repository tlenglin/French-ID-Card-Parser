# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
from PIL import Image

def finishing_threshold(roi, th):
    img = cv2.threshold(roi, th, 255, cv2.THRESH_BINARY)[1]
    return img

def MRZ_crop(th):
    image = cv2.imread("./step1.jpg")
    image = imutils.resize(image, height=600)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)


    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")


    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=4)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, rectKernel)


    p = int(image.shape[1] * 0.05)
    thresh[:, 0:p] = 0
    thresh[:, image.shape[1] - p:] = 0

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)


    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        crWidth = w / float(gray.shape[1])
    
        
        if ar > 3 and crWidth > 0.15:
            
            pX = int((x + w) * 0.03)
            pY = int((y + h) * 0.03)
            (x, y) = (x - pX, y - pY)
            (w, h) = (w + (pX * 2), h + (pY * 2))
    
            roi = image[y:y + h, x:x + w].copy()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break


    roi = finishing_threshold(roi, 125)
    cv2.imwrite("step2.jpg", roi)

rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 30))

MRZ_crop(125)