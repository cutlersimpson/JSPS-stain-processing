# Blog about package
# https://up42.com/blog/tech/image-similarity-measures

import os
import cv2
import sys
from pprint import pprint
import image_similarity_measures
from image_similarity_measures.quality_metrics import rmse, psnr, ssim, fsim, issm, sre, sam, uiq

stain = cv2.imread('./images/stain_snapshot.png')
gray_stain = cv2.cvtColor(stain, cv2.COLOR_BGR2GRAY)
histogram = cv2.calcHist([stain], [0], None, [256], [0, 256])

scale_percent = 100
width = int(stain.shape[1] * scale_percent / 100)
height = int(stain.shape[0] * scale_percent / 100)
dim = (width, height)

hist_measures = {}
rmse_measures = {}
psnr_measures = {}
ssim_measures = {}
fsim_measures = {}
issm_measures = {}
sre_measures = {}
sam_measures = {}
uiq_measures = {}

for file_name in [f for f in os.listdir('./images') if f.endswith('.tif')]:
    img = os.path.abspath('./images') + "/" + file_name
    image = cv2.imread(img)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("Processing: " + img)

    #rmse_measures[img]= rmse(stain, image)
    #psnr_measures[img] = psnr(stain,image)
    #ssim_measures[img]= ssim(stain, image)
    #fsim_measures[img]= fsim(stain, image)
    #issm_measures[img]= issm(stain, image)
    #sre_measures[img]= sre(stain, image)
    sam_measures[img]= sam(stain, image)
    #uiq_measures[img]= uiq(stain, image)

    histogram1 = cv2.calcHist([image], [0], None, [256], [0, 256])
    i = 0
    c1 = 0
    while i<len(histogram) and i<len(histogram1):
        c1+=(histogram[i]-histogram1[i])**2
        i+= 1
    c1 = c1**(1 / 2)
    value = c1.item(0)
    hist_measures.update({img: value})

def calc_closest_val(dict, checkMax):
    result = {}
    if (checkMax):
    	closest = max(dict.values())
    else:
    	closest = min(dict.values())

    for key, value in dict.items():
    	if (value == closest):
    	    result[key] = closest

    return result


#hist = calc_closest_val(hist_measures, False)
#rmse = calc_closest_val(rmse_measures, False)
#psnr = calc_closest_val(psnr_measures, True)
#ssim = calc_closest_val(ssim_measures, True)
#fsim = calc_closest_val(fsim_measures, True)
#issm = calc_closest_val(issm_measures, True) #TODO this might need to be flipped back
#sre = calc_closest_val(sre_measures, True)
sam = calc_closest_val(sam_measures, True)
#uiq = calc_closest_val(uiq_measures, True)

#print("The most similar according to hist: " , hist)
#print("The most similar according to RMSE: " , rmse)
#print("The most similar according to PSNR: " , psnr)
#print("The most similar according to SSIM: " , ssim)
#print("The most similar according to FSIM: " , fsim)
#print("The most similar according to ISSM: " , issm)
#print("The most similar according to SRE: " , sre)
print("The most similar according to SAM: " , sam)
#print("The most similar according to UIQ: " , uiq)
