import argparse
import cv2
import sys
import numpy as np
from utils.process_night_image import ProcessNightImage


def process_night_image(img, img_out=None):
    # aerial_pic = cv2.imread('/Users/skuppasa/workspace/hackathon/impactathon2019/data/night1.png')
    # input_img = cv2.imread(img)
    inc_contrast = ProcessNightImage(img).change_constrast()
    grey = ProcessNightImage(inc_contrast).convert_to_greyscale()
    bw = ProcessNightImage(grey).convert_to_black_or_white()
    # bw = ProcessNightImage(grey).convert_to_bw_given_thresh(175)
    # cv2.imwrite('bw.png', bw)

    # mapimg = cv2.imread('/Users/skuppasa/workspace/hackathon/impactathon2019/bw_image.png')
    #
    # # output = cv2.bitwise_and(bw, bw)
    # # output = cv2.bitwise_and(mapimg, mapimg)
    # output = cv2.bitwise_and(mapimg, bw)
    if img_out:
        cv2.imwrite(img_out, bw)
    return bw


def process_map_image(img, img_out=None):
    # input_img = cv2.imread(img)
    roads = ProcessNightImage(img).get_roads_in_map()
    roads_grey = ProcessNightImage(roads).convert_to_greyscale()
    roads_bw = ProcessNightImage(roads_grey).convert_to_black_or_white()
    if img_out:
        cv2.imwrite(img_out, roads_bw)
    return roads_bw


def process_images(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--map_image", help="path to the map image")
    ap.add_argument("--night_image", help="path to night image")
    ap.add_argument("--output", help="path to store output image")
    args = vars(ap.parse_args())
    print(args)
    night_img = cv2.imread(args["night_image"])
    map_img = cv2.imread(args["map_image"])

    output_night_img = "night_image_bw.png"
    output_map_img = "map_image_bw.png"

    night_img_bw = process_night_image(night_img, output_night_img)
    map_img_bw = process_map_image(map_img, output_map_img)

    # # convert white to red
    # # map_img_bw = cv2.cvtColor(map_img_bw, cv2.COLOR_RGBA2BGR) cv2.COLORBGR2
    # map_img_bw[np.where((map_img_bw == [255, 255, 255]).all(axis=2))] = [0, 0, 255]
    #
    # # convert black to transparent
    # map_img_transparent = cv2.cvtColor(map_img_bw, cv2.COLOR_BGR2RGBA)
    # map_img_transparent[np.all(map_img_transparent == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]

    # cv2.imwrite("transparent-red.png", map_img_transparent)

    not_night_img = cv2.bitwise_not(night_img_bw)
    result = cv2.bitwise_and(map_img_bw, not_night_img)
    cv2.imwrite(args['output'], result)


if __name__ == '__main__':
    # python test.py --map-image <path> --night-image <path>
    process_images(sys.argv)