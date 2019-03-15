# import the necessary packages
import numpy as np
import sys
import argparse
import cv2
 
def main(argv):
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help = "path to the image")
	args = vars(ap.parse_args())
	 
	# load the image
	image = cv2.imread(args["image"])

	# define the list of boundaries
	boundaries = [
	([160, 220, 220],[175, 255, 255])
	]

	# loop over the boundaries
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
	 
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output1 = cv2.bitwise_and(image, image, mask = mask)
	 
		# show the images
		#result = cv2.imshow("images", np.hstack([image, output]))
		#cv2.imwrite('result.png', np.hstack([output]))
#		cv2.waitKey(0)

	boundaries = [
	([250, 250, 250],[255, 255, 255])
	]

	# loop over the boundaries
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
	 
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output2 = cv2.bitwise_and(image, image, mask = mask)

	result = cv2.bitwise_or(output1, output2)
	cv2.imwrite('result.png', np.hstack([result]))

	im_gray = cv2.imread('result.png', cv2.IMREAD_GRAYSCALE)
	(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	cv2.imwrite('bw_image.png', im_bw)

	sin_img = cv2.imread('/Users/varsha.abhinandan/Downloads/bw.png')
	my_img = cv2.imread('bw_image.png')
	not_img = cv2.bitwise_not(sin_img)
	vvv = cv2.bitwise_and(my_img,not_img)
	cv2.imwrite('impact.png', vvv)


if __name__ == "__main__":
	main(sys.argv)