#!/usr/bin/python
# -*- coding: utf-8 -*-
from ImgRecodModule import recog
import cv2
from matplotlib import pyplot as plt
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description="Image parser for underwater robot")
ap.add_argument("img", help = "path to the image file")
ap.add_argument('-n','--no-detection', dest='detection', action='store_false')
ap.set_defaults(detection=True)
args = vars(ap.parse_args())
detimg = cv2.imread(args["img"],cv2.IMREAD_GRAYSCALE)
img,A,B,C,D = recog(detimg,args["detection"])




titles = ['Input','Output: A({})B({})C({})D({})'.format(A,
		  B, C, D)]
		
images = [detimg, img]

for i in range(2):
	(plt.subplot(1, 2, i + 1), plt.imshow(images[i], 'gray'),plt.subplots_adjust(left=0, bottom=0.1, right=1, top=0.9, wspace=0, hspace=0))
	plt.title(titles[i])
	(plt.xticks([]), plt.yticks([]))
plt.show()
