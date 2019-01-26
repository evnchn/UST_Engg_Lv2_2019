
from Module.ImgRecodModule import recog
import cv2
import os
import numpy as np
import timeit
from matplotlib import pyplot as plt


def cls():
	os.system('cls' if os.name=='nt' else 'clear')
def show_webcam():
	firstrun = True
	cam = cv2.VideoCapture(0)
	A=B=C=D=Ao=Bo=Co=Do=0
	confident={}
	correction = True
	tarstrings = ""
	while True:
		printit=False
		ret_val, img = cam.read()
		img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		if firstrun: 
			img2 = np.copy(img)
			firstrun = False
		if 1:
			try:
				(img2y,A,B,C,D) = recog(img,correction)
			except:
				A=B=C=D=0
			if A and B and C and D and (A+B+C+D) < 16:
				try:
					img2 = np.copy(img2y)
				except:
					pass
				if Ao==A and Bo==B and Co==C and Do==D:
					try: 
						confident["{},{},{},{}".format(A,B,C,D)] += 10
						confident["{},{},{},{}".format(A,B,C,D)] *= 2
						confident = {k: v / 2 for k, v in confident.items()}
					except:
						confident["{},{},{},{}".format(A,B,C,D)] = 0
					printit = True
			else:
				try:
					confident["{},{},{},{}".format(Ao,Bo,Co,Do)] *= 1
				except:
					confident["{},{},{},{}".format(Ao,Bo,Co,Do)] = 0
			Ao=A
			Bo=B
			Co=C
			Do=D
			if printit:
				try:
					cls()
					print("!New result({}): A({})B({})C({})D({})".format(confident["{},{},{},{}".format(A,B,C,D)],A,B,C,D))
					print("Results and confident score")
					
					confident = {key:val for key, val in confident.items() if val}
					s = sorted(confident.items(), key=lambda x: x[1], reverse=True)
					first = True
					for k, v in s:
						print(strings)
				except:
					confident["{},{},{},{}".format(A,B,C,D)] = 0
		tarimg = cv2.resize(np.hstack((img,img2)), (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
		cv2.imshow('result', tarimg)
		key = cv2.waitKey(1)
		if key == 27: 
			break
	cv2.destroyAllWindows()

show_webcam()