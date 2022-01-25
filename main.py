# This is a sample Python script.

from os import listdir
from os.path import isfile, join
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import copy


SHOW_FULLSIZE = False
DELAY = 2000                # in milliseconds
INPUT_PATH = 'data/hardy/'
OUTPUT_PATH = 'output/'
OUTPUT_THRESHOLD = 88       # Threshold for final output
CROPPING_THRESHOLD_UPPER = 255      # Threshold used to select the crop outline
CROPPING_THRESHOLD_LOWER = 250



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    onlyfiles = [f for f in listdir(INPUT_PATH) if isfile(join(INPUT_PATH, f))]
    print(onlyfiles)


for f in onlyfiles:
    # print("Processing file "+f)

    # Read image as BGR array
    img = cv2.imread(filename=INPUT_PATH + f)
    #img = cv2.bitwise_not(imgreal)
    # Convert to greyscale
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Calculate threshold for OCR output
    ret, thresh = cv2.threshold(grey, OUTPUT_THRESHOLD, 255, cv2.THRESH_OTSU)
    # Find the contours of the largest object
    _, cropthresh = cv2.threshold(thresh, CROPPING_THRESHOLD_LOWER, CROPPING_THRESHOLD_UPPER, cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(cropthresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maxc = []
    maxa = 0
    for c in contours:
        a = cv2.contourArea(c)
        if a > maxa:
            maxc = c
            maxa = a
            # print('new maximum: ' + str(maxa))
    cont = maxc

    # Find the bounding box of that contour
    x, y, w, h = cv2.boundingRect(cont)

    boundbox = copy.deepcopy(img)
    cv2.rectangle(boundbox, (x, y), (x + w, y + h), (0, 255, 0), 20)

    crop = img[y:y + h, x:x + w]
    thumb = cv2.resize(crop,None,fx=0.1,fy=0.1)

    cropocr = thresh[y:y + h, x:x + w]

    noext = Path(OUTPUT_PATH+f).with_suffix('')
    cropfile = noext.with_suffix('.jpg')
#    print('Writing cropped colour image to '+noext.__str__() + '-cropped.jpg')
    _ = cv2.imwrite(img=crop, filename=''+noext.__str__() + '-cropped.jpg')
 #   print('Writing cropped thresholded image for OCR processing to '+noext.__str__())
    _ = cv2.imwrite(img=boundbox, filename=noext.__str__() + '-thresholded.jpg')
 #   print('Writing cropped thresholded image for OCR processing to '+noext.__str__())
    _ = cv2.imwrite(img=thumb, filename=noext.__str__() + '-thumb.jpg')


print("Done.")