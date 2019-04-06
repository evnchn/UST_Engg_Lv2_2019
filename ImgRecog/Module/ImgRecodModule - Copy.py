#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt

def recog(img,boolean):
	storeXYWH = []
	storeCIRCLE = []
	circleH = circleW = 1
	maxWH = cornerWA = cornerWD = cornerSD = cornerSA = A = B = C = D = 0
	detimg = np.copy(img)
	if boolean:
		(ret3, threshold) = cv2.threshold(cv2.GaussianBlur(img, (15,15), 0), 127, 255, cv2.THRESH_BINARY
										+ cv2.THRESH_OTSU)
		contours = imutils.grab_contours(cv2.findContours(threshold,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE))
		(height, width) = threshold.shape
		tolXYWH = height
		for cnt in contours:
			approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True),
									True)
			if len(approx) > 4:
				(x,y),radius = cv2.minEnclosingCircle(cnt)
				center = (int(x),int(y))
				radius = int(radius)
				img = cv2.circle(img,center,radius,255,3)
				storeXYWH.append(cv2.boundingRect(approx))
		
		for i in range(len(storeXYWH)):
			if storeXYWH[i][0] > width * 0.4 and storeXYWH[i][0] < width * 0.6:
				storeXYWH[i] = 0
		storeXYWH = [i for i in storeXYWH if i]
		chg = False
		while len(storeXYWH) > 4:
			for i in range(len(storeXYWH)):
				
				if tolXYWH < (storeXYWH[i][2]+storeXYWH[i][3])*.5:
					circleW+=storeXYWH[i][2]
					circleH+=storeXYWH[i][3]
					storeXYWH[i] = 0
					chg = True
			if chg:
				storeXYWH = [j for j in storeXYWH if j]
				chg = False
			else:
				tolXYWH -= 1
		for i in storeXYWH:
			if not cornerWA and i[0] < width / 4 and i[1] < height / 4:
				cornerWA = i
			elif not cornerWD and i[0] > width / 4 and i[1] < height / 4:
				cornerWD = i
			elif not cornerSD and i[0] > width / 4 and i[1] > height / 4:
				cornerSD = i
			elif not cornerSA and i[0] < width / 4 and i[1] > height / 4:
				cornerSA = i
			else:
				return
		
		properw = int(width*circleH/circleW)
		img = cv2.warpPerspective(detimg, cv2.getPerspectiveTransform(np.array([[cornerWA[0] + cornerWA[2], cornerWA[1]
						+ cornerWA[3]], cornerWD[:2], cornerSD[:2],
						cornerSA[:2]], dtype=np.float32),
								np.array([[0, 0], [properw - 1, 0], [properw - 1, height - 1],
						[0, height - 1]], dtype=np.float32)), (properw, height))
	(ret3, threshold) = cv2.threshold(cv2.GaussianBlur(img, (15, 15), 0), 0, 255, cv2.THRESH_BINARY
									  + cv2.THRESH_OTSU)
	contours = imutils.grab_contours(cv2.findContours(threshold.copy(),
									 cv2.RETR_TREE,
									 cv2.CHAIN_APPROX_SIMPLE))
	font = cv2.FONT_HERSHEY_TRIPLEX
	(height, width) = threshold.shape
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True),
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
			if width - 10 > w and height - 10 > h:
				if ar >= 0.3 and ar <= 1.7:
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