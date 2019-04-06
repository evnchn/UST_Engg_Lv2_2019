
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import imutils
from Module2.extractRect import *
img = cv.imread('photo.jpg',0)
img = cv.medianBlur(img,5)

blur = cv.GaussianBlur(img,(5,5),0)
ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)


im_floodfill = th3.copy()
 
# Mask used to flood filling.
# Notice the size needs to be 2 pixels than the image.
h, w = th3.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
 
# Floodfill from point (0, 0)
cv2.floodFill(im_floodfill, mask, (0,0), 255);
 
# Invert floodfilled image
im_floodfill_inv = cv2.bitwise_not(im_floodfill)
 
# Combine the two images to get the foreground.
im_out = th3 | im_floodfill_inv







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
print(rect_coord_ori)
pts = np.array(rect_coord_ori)

pts = pts.reshape((-1,1,2))

print(pts)
cv2.fillPoly(th3, pts = np.int32([pts]), color=(128,128,128))

titles = ['Original Image', 'Global Thresholding (v = 127)',""]
images = [img, th3,im_out]

for i in range(3):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()


