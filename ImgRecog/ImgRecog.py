#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt

storeXYWH = []
cornerWA = [0, 0]
cornerWD = [0, 0]
cornerSD = [0, 0]
cornerSA = [0, 0]
cornerSET = False
maxWH = 0
img = cv2.imread('test - Copy.png',cv2.IMREAD_GRAYSCALE)

detimg = np.copy(img)
A = B = C = D = 0

blur = cv2.GaussianBlur(img, (15,15), 0)
(ret3, threshold) = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY
								  + cv2.THRESH_OTSU)
contours = imutils.grab_contours(cv2.findContours(threshold,
								 cv2.RETR_TREE,
								 cv2.CHAIN_APPROX_SIMPLE))
(height, width) = threshold.shape

for cnt in contours:
	approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True),
							  True)
	if len(approx) > 4:
		#cv2.drawContours(img, [approx], 0, 0, 5)
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius)
		img = cv2.circle(img,center,radius,255,3)
		xywh = cv2.boundingRect(approx)
		storeXYWH.append(xywh)
detimg2 = np.copy(img)
tolXYWH = 0

for i in range(len(storeXYWH)):
	if storeXYWH[i][0] > width * 0.4 and storeXYWH[i][0] < width * 0.6:
		storeXYWH[i] = 0
tolXYWH = height
storeXYWH = [i for i in storeXYWH if i]
chg = False
while len(storeXYWH) > 4:
	for i in range(len(storeXYWH)):
		
		if tolXYWH < (storeXYWH[i][2]+storeXYWH[i][3])*.5:
			storeXYWH[i] = 0
			chg = True
	if chg:
		storeXYWH = [j for j in storeXYWH if j]
		chg = False
	else:
		tolXYWH -= 1
for i in storeXYWH:
	if i[0] < width / 2 and i[1] < height / 2:
		cornerWA = i
	elif i[0] > width / 2 and i[1] < height / 2:
		cornerWD = i
	elif i[0] > width / 2 and i[1] > height / 2:
		cornerSD = i
	else:
		cornerSA = i
src_pts = np.array([[cornerWA[0] + cornerWA[2], cornerWA[1]
				   + cornerWA[3]], cornerWD[:2], cornerSD[:2],
				   cornerSA[:2]], dtype=np.float32)
dst_pts = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
				   [0, height - 1]], dtype='float32')
img = cv2.warpPerspective(detimg, cv2.getPerspectiveTransform(src_pts,
						  dst_pts), (width, height))
blur = cv2.GaussianBlur(img, (15, 15), 0)
(ret3, threshold) = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY
								  + cv2.THRESH_OTSU)
contours = imutils.grab_contours(cv2.findContours(threshold.copy(),
								 cv2.RETR_TREE,
								 cv2.CHAIN_APPROX_SIMPLE))
font = cv2.FONT_HERSHEY_TRIPLEX
(height, width) = threshold.shape
for cnt in contours:
	approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True),
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
	elif len(approx) == 4:
		(x, y, w, h) = cv2.boundingRect(approx)
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
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius)
		img = cv2.circle(img,center,radius,255,3)
titles = ['Input','Output: A({})B({})C({})D({})'.format(A,
		  B, C, D)]
		
images = [detimg2, img]
for i in range(2):
	(plt.subplot(1, 2, i + 1), plt.imshow(images[i], 'gray'),plt.subplots_adjust(left=0, bottom=0.1, right=1, top=0.9, wspace=0, hspace=0))
	plt.title(titles[i])
	(plt.xticks([]), plt.yticks([]))
plt.show()
