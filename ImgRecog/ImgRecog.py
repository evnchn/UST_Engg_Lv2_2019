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
minWH = 1000000
maxWH = 0
img = cv2.imread('test.png', 0)
A = B = C = D = 0

blur = cv2.GaussianBlur(img, (15, 15), 0)
(ret3, threshold) = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY
                                  + cv2.THRESH_OTSU)
contours = imutils.grab_contours(cv2.findContours(threshold.copy(),
                                 cv2.RETR_TREE,
                                 cv2.CHAIN_APPROX_SIMPLE))
font = cv2.FONT_HERSHEY_COMPLEX
(height, width) = threshold.shape
detimg = np.copy(img)
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True),
                              True)
    cv2.drawContours(img, [approx], 0, 0, 5)
    if len(approx) > 4:
        xywh = cv2.boundingRect(approx)
        storeXYWH.append(xywh)

for i in storeXYWH:
    wh = sum(i[2:])
    minWH = min(minWH, wh)
    maxWH = max(maxWH, wh)
tolXYWH = (maxWH - minWH) / 6
for i in range(len(storeXYWH)):
    if minWH == storeXYWH[i][2] + storeXYWH[i][3] / 2:
        storeXYWH[i] = 0
    elif maxWH - tolXYWH < (storeXYWH[i][2] + storeXYWH[i][3]) / 2:

        storeXYWH[i] = 0
storeXYWH = [i for i in storeXYWH if i]
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
    approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True),
                              True)
    cv2.drawContours(img, [approx], 0, 0, 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if len(approx) == 3:
        cv2.putText(
            img,
            'A',
            (x, y),
            font,
            3,
            0,
            )
        A += 1
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        if width - 10 > w and height - 10 > h:
            if ar >= 0.75 and ar <= 1.25:
                cv2.putText(
                    img,
                    'B',
                    (x, y),
                    font,
                    3,
                    0,
                    )
                B += 1
            else:
                cv2.putText(
                    img,
                    'C',
                    (x, y),
                    font,
                    3,
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
            3,
            0,
            )
titles = ['Input', 'Warped', 'Output: A({})B({})C({})D({})'.format(A,
          B, C, D)]
images = [detimg, img, threshold]
for i in range(3):
    (plt.subplot(1, 3, i + 1), plt.imshow(images[i], 'gray'))
    plt.title(titles[i])
    (plt.xticks([]), plt.yticks([]))
plt.show()
