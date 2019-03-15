import cv2


class ProcessNightImage:
    def __init__(self, input_image):
        self.input_image = input_image

    def convert_to_greyscale(self):
        grey = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
        return grey

    def change_constrast(self, contrast_percent):
        clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8, 8))
        lab = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        l, a, b = cv2.split(lab)  # split on 3 different channels

        l2 = clahe.apply(l)  # apply CLAHE to the L-channel

        lab = cv2.merge((l2, a, b))  # merge channels
        output_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
        return output_image

    def change_brightness(self, brightness_percent):
        pass

    def convert_to_black_or_white(self):
        (thresh, im_bw) = cv2.threshold(self.input_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        print("thresh is %s", thresh)
        return im_bw

    def convert_to_bw_given_thresh(self, thresh):
        im_bw = cv2.threshold(self.input_image, thresh, 255, cv2.THRESH_BINARY)[1]
        return im_bw