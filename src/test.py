import argparse
import cv2
import sys
import numpy as np
from utils.image_processor import ImageProcessor


def process_night_image(img, img_out=None):
    # inc_contrast = ImageProcessor(img).change_constrast()
    grey = ImageProcessor(img).convert_to_greyscale()
    bw = ImageProcessor(grey).convert_to_bw_given_thresh(128)
    if img_out:
        cv2.imwrite(img_out, bw)
    return bw


def process_map_image(img, img_out=None):
    roads = ImageProcessor(img).get_roads_in_map()
    roads_grey = ImageProcessor(roads).convert_to_greyscale()
    roads_bw = ImageProcessor(roads_grey).convert_to_bw_given_thresh(128)
    if img_out:
        cv2.imwrite(img_out, roads_bw)
    return roads_bw


def process_images(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--map_image", help="path to the map image")
    ap.add_argument("--night_image", help="path to night image")
    ap.add_argument("--output", help="path to store output image")
    ap.add_argument("--background", help="background image to overlay final result on")
    args = vars(ap.parse_args())

    night_img = cv2.imread(args["night_image"])
    map_img = cv2.imread(args["map_image"])
    output_night_img = "night_image_bw.png"
    output_map_img = "map_image_bw.png"

    night_img_bw = process_night_image(night_img, output_night_img)
    map_img_bw = process_map_image(map_img, output_map_img)

    # try to account for skew in night_img_bw
    # - shift image by 5 pixels in each direction
    # - compute bitwise_and of each of these images with the original image
    rows, cols = night_img_bw.shape
    M_list = [
        np.float32([[1, 0, 0],  [0, 1, -5]]),  # shift up
        np.float32([[1, 0, 0],  [0, 1, 5]]),   # shift down
        np.float32([[1, 0, -5], [0, 1, 0]]),   # shift left
        np.float32([[1, 0, 5],  [0, 1, 0]])    # shift right
    ]
    shift_result_list = []
    for M in M_list:
        night_img_shift = cv2.warpAffine(night_img_bw, M, (cols, rows))
        shift_result_list.append(
            cv2.bitwise_and(map_img_bw, cv2.bitwise_not(night_img_shift))
        )

    # map_img_bw AND (NOT night_img_bw)
    # - take shift_result_list also into account to compute result
    result = cv2.bitwise_and(map_img_bw, cv2.bitwise_not(night_img_bw))
    for r in shift_result_list:
        result = cv2.bitwise_and(result, r)

    # convert white to blue
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    result[np.where((result == [255, 255, 255]).all(axis=2))] = [0, 0, 255]

    # convert black to transparent
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)
    result[np.all(result == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
    result = cv2.cvtColor(result, cv2.COLOR_RGBA2RGB)

    # overlay result on map image
    background = cv2.imread(args['background'])
    final_image = ImageProcessor(background).blend_non_transparent(result)
    cv2.imwrite(args['output'], final_image)


if __name__ == '__main__':
    # python src/test.py --map_image <path> --night_image <path> --output <path> --background <path>
    # Eg: python src/test.py --map_image data/map-no-label1.png --night_image data/night1.png --output data/output.png --background data/map1.png
    process_images(sys.argv)
