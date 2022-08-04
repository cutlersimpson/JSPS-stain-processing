# Blog about package
# https://up42.com/blog/tech/image-similarity-measures

import os
import cv2
import sys
import image_similarity_measures
from pprint import pprint
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from image_similarity_measures.quality_metrics import (
    rmse,
    psnr,
    ssim,
    fsim,
    issm,
    sre,
    sam,
    uiq,
)


def get_stain():
    print("Select stain image")
    return askopenfilename()


def get_path():
    print("Select directory with slice images")
    return askdirectory()


def get_dimensions(stain):
    scale_percent = 100
    width = int(stain.shape[1] * scale_percent / 100)
    height = int(stain.shape[0] * scale_percent / 100)
    return (width, height)


def process_images(
    dim,
    path,
    stain,
    rmse_measures,
    psnr_measures,
    ssim_measures,
    fsim_measures,
    issm_measures,
    sre_measures,
    sam_measures,
    uiq_measures,
):
    for file_name in [f for f in os.listdir(path) if f.endswith(".tif")]:
        img = path + "/" + file_name
        image = cv2.imread(img)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        print("Processing: " + img)

        # rmse_measures[img] = rmse(stain, image)
        # psnr_measures[img] = psnr(stain, image)
        # ssim_measures[img] = ssim(stain, image)
        # fsim_measures[img] = fsim(stain, image)
        # issm_measures[img] = issm(stain, image)
        # sre_measures[img] = sre(stain, image)
        sam_measures[img] = sam(stain, image)
        # uiq_measures[img] = uiq(stain, image)


def get_closest_value(
    rmse_measures,
    psnr_measures,
    ssim_measures,
    fsim_measures,
    issm_measures,
    sre_measures,
    sam_measures,
    uiq_measures,
):
    # rmse = calc_closest_val(rmse_measures, False)
    # psnr = calc_closest_val(psnr_measures, True)
    # ssim = calc_closest_val(ssim_measures, True)
    # fsim = calc_closest_val(fsim_measures, True)
    # issm = calc_closest_val(issm_measures, True)
    # sre = calc_closest_val(sre_measures, True)
    # sam = calc_closest_val(sam_measures, True)
    # uiq = calc_closest_val(uiq_measures, True)

    # print_result(rmse)
    # print_result(psnr)
    # print_result(ssim)
    # print_result(fsim)
    # print_result(issm)
    # print_result(sre)
    print_in_order(sam_measures, True)
    # print_result(uiq)


def calc_closest_val(dict, checkMax):
    result = {}
    if checkMax:
        closest = max(dict.values())
    else:
        closest = min(dict.values())

    for key, value in dict.items():
        if value == closest:
            result[key] = closest

    return result


def print_result(result):
    path = list(result.keys())[0]
    file_name = os.path.split(path)[-1]

    print("The slice image most similar to the stain is:", file_name)


def print_in_order(results, reverse):
    top = {}
    scores = list(results.values())
    scores.sort(reverse=reverse)

    for score in scores:
        for img, value in results.items():
            if value == score:
                top.update({os.path.split(img)[-1]: value.item()})

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Values in order based on SAM rankings")
    pprint(top, sort_dicts=False)


def print_disclaimers():
    print(
        """
    ______________________________________________________________________________
    |This is intended to be used as a guide to determine which slice images      |
    |match to the stain image. It is not definiteive and the images should       |
    |still be manually verified.                                                 |
    |                                                                            |
    |To use the tool, select the stain image you are interested in when          |
    |the first pop up shows, then during the second pop up choose the directory  |
    |where the slice images are located. The results of the script will be the   |
    |files and their SAM scores in order of most similar to least.               |
    ______________________________________________________________________________
        """
    )


if __name__ == "__main__":
    print_disclaimers()

    Tk().withdraw()

    rmse_measures = {}
    psnr_measures = {}
    ssim_measures = {}
    fsim_measures = {}
    issm_measures = {}
    sre_measures = {}
    sam_measures = {}
    uiq_measures = {}

    stain = cv2.imread(get_stain())
    path = get_path()
    dim = get_dimensions(stain)

    process_images(
        dim,
        path,
        stain,
        rmse_measures,
        psnr_measures,
        ssim_measures,
        fsim_measures,
        issm_measures,
        sre_measures,
        sam_measures,
        uiq_measures,
    )

    get_closest_value(
        rmse_measures,
        psnr_measures,
        ssim_measures,
        fsim_measures,
        issm_measures,
        sre_measures,
        sam_measures,
        uiq_measures,
    )
