#!/usr/bin/python
# -*- coding: utf-8 -*-
from Module2.extractRect import *
import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt


def recog(img,boolean):
	ih,iw = img.shape
	storeXYWH = []
	storeCIRCLE = []
	circleH = circleW = 1
	maxWH = cornerWA = cornerWD = cornerSD = cornerSA = A = B = C = D = 0
	detimg = np.copy(img)
	if boolean:
		(ret3, threshold) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY
										+ cv2.THRESH_OTSU)

		im_floodfill = threshold.copy()
 
		# Mask used to flood filling.
		# Notice the size needs to be 2 pixels than the image.
		h, w = threshold.shape[:2]
		mask = np.zeros((h+2, w+2), np.uint8)
		 
		# Floodfill from point (0, 0)
		cv2.floodFill(im_floodfill, mask, (0,0), 255);
		 
		# Invert floodfilled image
		im_floodfill_inv = cv2.bitwise_not(im_floodfill)
		 
		# Combine the two images to get the foreground.
		im_out = threshold | im_floodfill_inv







		a = im_out[::-1].T
		idx_in  = np.where(a==255) 
		idx_out = np.where(a==0) 
		aa = np.ones_like(a)
		aa[idx_in]  = 0


		rect_coord_ori = findRotMaxRect(aa, flag_opt=True, nbre_angle=1, \
																 flag_parallel=False,		 \
																 flag_out=None,		 \
																 flag_enlarge_img=False,	  \
																 limit_image_size=50		 )
		img = cv2.warpPerspective(detimg, cv2.getPerspectiveTransform(np.array(rect_coord_ori, dtype=np.float32),
								np.array([[0, 0], [iw, 0], [iw,ih],
						[0, ih]], dtype=np.float32)), (iw,ih))
	(ret3, threshold) = cv2.threshold(cv2.GaussianBlur(img, (15, 15), 0), 0, 255, cv2.THRESH_BINARY
									  + cv2.THRESH_OTSU)
	contours = imutils.grab_contours(cv2.findContours(threshold.copy(),
									 cv2.RETR_TREE,
									 cv2.CHAIN_APPROX_SIMPLE))
	font = cv2.FONT_HERSHEY_TRIPLEX
	(height, width) = threshold.shape
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.045 * cv2.arcLength(cnt, True),
								  True)
		cv2.drawContours(img, [approx], 0, 0, 3)
		x = approx.ravel()[0]
		y = approx.ravel()[1]
		if len(approx) == 3:
			cv2.putText(
				img,
				'A',
				(x, y),
				font,
				1,
				0,
				)
			A += 1
		elif len(approx) == 2:
			cv2.putText(
				img,
				'C',
				(x, y),
				font,
				1,
				0,
				)
			C += 1
		elif len(approx) == 4:
			(_, _, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
			if width/w > 2 or height/h > 2:
				if width - 10 > w and height - 10 > h:
					if ar >= 0.5 and ar <= 1.5:
						cv2.putText(
							img,
							'B',
							(x, y),
							font,
							1,
							0,
							)
						B += 1
					else:
						cv2.putText(
							img,
							'C',
							(x, y),
							font,
							1,
							0,
							)
						C += 1
		else:
			(_, _, w, h) = cv2.boundingRect(approx)
			if width/w < 7 or height/h < 7:
				D += 1

				cv2.putText(
					img,
					'D',
					(x, y),
					font,
					1,
					0,
					)
	cv2.putText(
		img,
		"A({})B({})C({})D({})".format(A,B,C,D),
		(20,50),
		font,
		1,
		0,
		)
	return img,A,B,C,D