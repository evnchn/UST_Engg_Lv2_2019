from Module.ImgRecodModule import recog
import cv2
import os
A=B=C=D=Ao=Bo=Co=Do=0
confident={}

def cls():
	os.system('cls' if os.name=='nt' else 'clear')
def show_webcam(mirror=False):
	cam = cv2.VideoCapture(0)
	while True:
		printit=False
		global A
		global B
		global C
		global D
		global Ao
		global Bo
		global Co
		global Do
		global confident
		ret_val, img = cam.read()
		if mirror: 
			img = cv2.flip(img, 1)
		if 1:
			try:
				(img2,A,B,C,D) = recog(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),True)
			except:
				A=B=C=D=0
			if Ao==A and Bo==B and Co==C and Do==D and Ao and Bo and Co and Do:
				try: 
					confident["{},{},{},{}".format(A,B,C,D)] += 10
					confident["{},{},{},{}".format(A,B,C,D)] *= 2
					confident = {k: v / 2 for k, v in confident.items()}
				except:
					confident["{},{},{},{}".format(A,B,C,D)] = 0
				printit = True
			else:
				try:
					confident["{},{},{},{}".format(Ao,Bo,Co,Do)] *= 0.5
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
					for k, v in s:
						print("A({})B({})C({})D({})---Score:({})".format(*(x.strip() for x in k.split(',')), v))
				except:
					confident["{},{},{},{}".format(A,B,C,D)] = 0
		
		cv2.imshow('my webcam', img)
		
		try:
				cv2.imshow('my webcam2', img2)
		except:
			pass
		if cv2.waitKey(1) == 27: 
			break  # esc to quit
	cv2.destroyAllWindows()

show_webcam()