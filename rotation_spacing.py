# -*- coding: utf-8 -*-
"""
Automatically detect rotation and line spacing of an image of text using
Radon transform
If image is rotated by the inverse of the output, the lines will be
horizontal (though they may be upside-down depending on the original image)
It doesn't work with black borders
"""

from __future__ import division, print_function
from skimage.transform import radon
from PIL import Image
from numpy import asarray, mean, array, blackman
import numpy
from numpy.fft import rfft
import matplotlib.pyplot as plt
from matplotlib.mlab import rms_flat
from imutils import paths
try:
    # More accurate peak finding from
    # https://gist.github.com/endolith/255291#file-parabolic-py
    from parabolic import parabolic

    def argmax(x):
        return parabolic(x, numpy.argmax(x))[0]
except ImportError:
    from numpy import argmax


filename = "step0.jpg"
img = Image.open(filename)

# Load file, converting to grayscale
I = asarray(Image.open(filename).convert('L'))
I = I - mean(I)  # Demean; make the brightness extend above and below zero

sinogram = radon(I)

# Find the RMS value of each row and find "busiest" rotation,
# where the transform is lined up perfectly with the alternating dark
# text and white lines
r = array([rms_flat(line) for line in sinogram.transpose()])
rotation = argmax(r)
print('Rotation: {:.2f} degrees'.format(90 - rotation))

img2 = img.rotate(90 - rotation, expand=True)
img2.convert('L').save("./step1.jpg") #save a grayscale version of the image ?
#save it in a "rotated_images" directory ?