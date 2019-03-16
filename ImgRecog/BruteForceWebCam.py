

import cv2
import threading
index = 0
arr = []
while True:
	cap = cv2.VideoCapture(index)
	if cap is None or not cap.isOpened():
		break
	elif cap.read()[0]:
		arr.append(index)
	else:
		break
	cap.release()
	index += 1
def show_webcam(vcid):
	cam = cv2.VideoCapture(vcid)
	while True:
		cv2.imshow(str(vcid), cam.read()[1])
		if cv2.waitKey(1) == 27: 
			break
	cv2.destroyAllWindows()
print(arr)
for x in arr:
	show_webcam(x)
