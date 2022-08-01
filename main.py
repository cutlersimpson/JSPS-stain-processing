import os
import cv2
import sys
from pprint import pprint
import image_similarity_measures
from image_similarity_measures.quality_metrics import rmse, ssim, sre

stain = cv2.imread('./images/stain_snapshot.png')
gray_stain = cv2.cvtColor(stain, cv2.COLOR_BGR2GRAY)
histogram = cv2.calcHist([stain], [0], None, [256], [0, 256])

files_dict = {}
ssim_measures = {}
rmse_measures = {}
sre_measures = {}

scale_percent = 100
width = int(stain.shape[1] * scale_percent / 100)
height = int(stain.shape[0] * scale_percent / 100)
dim = (width, height)

threshold = 100

for file_name in [f for f in os.listdir('./images') if f.endswith('.tif')]:
    img = os.path.abspath('./images') + "/" + file_name
    image = cv2.imread(img)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("Processing: " + img)

    rmse_measures[img]= rmse(stain, image)
    sre_measures[img]= sre(stain, image)
    ssim_measures[img]= ssim(stain, image)

    histogram1 = cv2.calcHist([image], [0], None, [256], [0, 256])
    i = 0
    c1 = 0
    while i<len(histogram) and i<len(histogram1):
        c1+=(histogram[i]-histogram1[i])**2
        i+= 1
    c1 = c1**(1 / 2)
    value = c1.item(0)
    files_dict.update({img: value})

def calc_closest_val(dict, checkMax):
    result = {}
    if (checkMax):
    	closest = max(dict.values())
    else:
    	closest = min(dict.values())

    for key, value in dict.items():
    	print("The difference between ", key ," and the original image is: ", value)
    	if (value == closest):
    	    result[key] = closest

    print("The closest value: ", closest)
    print("######################################################################")
    return result


ssim = calc_closest_val(ssim_measures, True)
rmse = calc_closest_val(rmse_measures, False)
sre = calc_closest_val(sre_measures, True)
hist = calc_closest_val(files_dict, False)

print("The most similar according to SSIM: " , ssim)
print("The most similar according to RMSE: " , rmse)
print("The most similar according to SRE: " , sre)
print("The most similar according to hist: " , hist)
