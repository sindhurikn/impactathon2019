import argparse
import cv2
import sys
import numpy as np
from utils.process_night_image import ProcessNightImage


def process_night_image(img, img_out=None):
    # aerial_pic = cv2.imread('/Users/skuppasa/workspace/hackathon/impactathon2019/data/night1.png')
    # input_img = cv2.imread(img)
    # inc_contrast = ProcessNightImage(img).change_constrast()
    grey = ProcessNightImage(img).convert_to_greyscale()
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
    ap.add_argument("--background", help="background image to overlay final result on")
    args = vars(ap.parse_args())
    print(args)
    night_img = cv2.imread(args["night_image"])
    map_img = cv2.imread(args["map_image"])

    output_night_img = "night_image_bw.png"
    output_map_img = "map_image_bw.png"

    night_img_bw = process_night_image(night_img, output_night_img)
    map_img_bw = process_map_image(map_img, output_map_img)

    rows,cols = night_img_bw.shape
    M = np.float32([[1,0,0],[0,1,-5]])
    map_img_up = cv2.warpAffine(night_img_bw,M,(cols,rows))

    M = np.float32([[1,0,0],[0,1,5]])
    map_img_down = cv2.warpAffine(night_img_bw,M,(cols,rows))

    M = np.float32([[1,0,-5],[0,1,0]])
    map_img_left = cv2.warpAffine(night_img_bw,M,(cols,rows))

    M = np.float32([[1,0,5],[0,1,0]])
    map_img_right = cv2.warpAffine(night_img_bw,M,(cols,rows))

    result = cv2.bitwise_and(map_img_bw, cv2.bitwise_not(night_img_bw))
    result1 = cv2.bitwise_and(map_img_bw, cv2.bitwise_not(map_img_up))
    result2 = cv2.bitwise_and(map_img_bw, cv2.bitwise_not(map_img_down))
    result3 = cv2.bitwise_and(map_img_bw, cv2.bitwise_not(map_img_left))
    result4 = cv2.bitwise_and(map_img_bw, cv2.bitwise_not(map_img_right))

    result = cv2.bitwise_and(result, result1)
    result = cv2.bitwise_and(result, result2)
    result = cv2.bitwise_and(result, result3)
    result = cv2.bitwise_and(result, result4)

    # convert white to red
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    result[np.where((result == [255, 255, 255]).all(axis=2))] = [0, 0, 255]

    # convert black to transparent
    result_transparent = cv2.cvtColor(result, cv2.COLOR_BGR2RGBA)

    result_transparent[np.all(result_transparent == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
    result_transparent = cv2.cvtColor(result_transparent, cv2.COLOR_RGBA2RGB)

    background = cv2.imread(args['background'])

    final_image = ProcessNightImage(background).blend_non_transparent(result_transparent)

    cv2.imwrite(args['output'], final_image)



if __name__ == '__main__':
    # python src/test.py --map_image <path> --night_image <path> --output <path> --background <path>
    # Eg: python src/test.py --map_image data/map-no-label1.png --night_image data/night1.png --output data/output.png --background data/map1.png
    process_images(sys.argv)
