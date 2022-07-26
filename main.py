import os
import cv2
import sys

stain = cv2.imread('./images/stain.jpg')
gray_image = cv2.cvtColor(stain, cv2.COLOR_BGR2GRAY)
histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

minimum = sys.float_info.max
min_file = ""

for file_name in [f for f in os.listdir('./images/') if f.endswith('.tif')]:
    img = os.path.abspath('./images') + "/" + file_name
    image = cv2.imread(img)
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])

    i = 0
    c1 = 0
    while i<len(histogram) and i<len(histogram1):
        c1+=(histogram[i]-histogram1[i])**2
        i+= 1
    c1 = c1**(1 / 2)
    value = c1.item(0)

    if value < minimum:
        minimum = value
        min_file = img

print(minimum)
print(min_file)

