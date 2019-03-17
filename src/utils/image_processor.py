import cv2
import numpy as np


class ImageProcessor:
    def __init__(self, input_image):
        self.input_image = input_image

    def convert_to_greyscale(self):
        grey = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
        return grey

    def change_constrast(self):
        clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8, 8))
        # convert from BGR to LAB color space
        lab = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)  # split on 3 different channels

        l2 = clahe.apply(l)  # apply CLAHE to the L-channel

        lab = cv2.merge((l2, a, b))  # merge channels
        # convert from LAB to BGR
        output_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return output_image

    def convert_to_bw_otsu(self):
        (thresh, im_bw) = cv2.threshold(self.input_image, 128, 255,
                                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # print("thresh is", thresh)
        return im_bw

    def convert_to_bw_given_thresh(self, thresh):
        im_bw = cv2.threshold(self.input_image, thresh, 255, cv2.THRESH_BINARY)[1]
        return im_bw

    def get_roads_in_map(self):
        yellow = [([160, 220, 220], [175, 255, 255])]
        white = [([250, 250, 250], [255, 255, 255])]
        output1 = output2 = None

        for (lower, upper) in yellow:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            # find yellow colors and apply mask
            mask = cv2.inRange(self.input_image, lower, upper)
            output1 = cv2.bitwise_and(self.input_image, self.input_image,
                                      mask=mask)

        for (lower, upper) in white:
            # create NumPy from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            # find white colors and apply mask
            mask = cv2.inRange(self.input_image, lower, upper)
            output2 = cv2.bitwise_and(self.input_image, self.input_image,
                                      mask=mask)

        result = cv2.bitwise_or(output1, output2)
        return result

    def blend_non_transparent(self, overlay_img):
        # self.input_image will be treated as background

        # Let's find a mask covering all the non-black (foreground) pixels
        # NB: We need to do this on grayscale version of the image
        gray_overlay = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2GRAY)
        overlay_mask = cv2.threshold(gray_overlay, 1, 255, cv2.THRESH_BINARY)[1]

        # And the inverse mask, that covers all the black (background) pixels
        background_mask = 255 - overlay_mask

        # Turn the masks into three channel, so we can use them as weights
        overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
        background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

        # Create a masked out face image, and masked out overlay
        # We convert the images to floating point in range 0.0 - 1.0
        face_part = (self.input_image * (1 / 255.0)) * (background_mask * (1 / 255.0))
        overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

        # And finally just add them together, and rescale it back to an 8bit integer image
        return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))
