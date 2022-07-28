import os
import cv2
import sys
from pprint import pprint

stain = cv2.imread('./images/stain.jpg')
gray_image = cv2.cvtColor(stain, cv2.COLOR_BGR2GRAY)
histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

minimum = sys.float_info.max
min_file = ""
files_dict = {}

threshold = 100

for file_name in [f for f in os.listdir('./images') if f.endswith('.tif')]:
    img = os.path.abspath('./images') + "/" + file_name
    image = cv2.imread(img)
    print("Processing: " + img)
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    count = 0
    total = 0

    for i, row in enumerate(gray_image1):
        for j, pixel in enumerate(gray_image1):
            pixel = gray_image1[i][j]
            total += 1
            if pixel <= threshold:
                count += 1


    percent = (count / float(total))
    print(percent)
    if percent > 0.30:
        continue

    histogram1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])
    i = 0
    c1 = 0
    while i<len(histogram) and i<len(histogram1):
        c1+=(histogram[i]-histogram1[i])**2
        i+= 1
    c1 = c1**(1 / 2)
    value = c1.item(0)

    files_dict.update({value: file_name})

values = list(files_dict.keys())
values.sort()
top_100 = values[:100]
top_100_dict = {}

for val in top_100:
    f = files_dict[val]
    top_100_dict.update({f: val})

print("Top 100 closest images:")
pprint(list(top_100_dict.keys()))


