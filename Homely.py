import cv2
import numpy as np
import time
import picamera
import RPi.GPIO as GPIO

def LEDSetup():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        ledList = (15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21)
        for val in ledList:
                GPIO.setup(val, GPIO.OUT)
                GPIO.output(val, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(val, GPIO.LOW)

def LEDCluster(ledList):
        for val in ledList:
                GPIO.output(val, GPIO.HIGH)
        time.sleep(1)
        for val in ledList:
                GPIO.output(val, GPIO.LOW)

def CheckUpDown(yList):	
	difference =yList[0] - yList[9]
	if difference > 0:
		return False
	else:
		return True

def getAngle(p1, p2):
	diffX = p1[0] - p2[0]
	diffY = p1[1] - p2[1]
	angle = np.arctan2(diffX, diffY)
	angle = angle * 180 / np.pi
	if diffX < 0:
		if diffY < 0:
			angle += 180
		else:
			angle -= 180
	return angle


def checkDirection(xList, yList):
        differenceX = abs(xList[0] - xList[4])
        differenceY = abs(yList[0] - yList[4])
        if differenceX > differenceY:
                if xList[0] > xList[4]:
                        LEDCluster(ledLeft)
                        return "LEFT"
                else:
                        LEDCluster(ledRight)
                        return "RIGHT"
        else:
                if yList[0] > yList[4]:
                        LEDCluster(ledDown)
                        return "DOWN"
                else:
                        LEDCluster(ledUp)
                        return "UP"

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')





cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
noFaceCnt = 0
#yList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
yList = [0, 0, 0, 0, 0]
#xList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
xList = [0, 0, 0, 0, 0]
ledRight = (16, 20, 21)
ledLeft = (1, 7, 12)
ledUp = (8, 25, 24)
ledDown = (23, 18, 15)
#coordList = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]


faceState = False
LEDSetup()

while True:
	ret, img = cap.read()
	#print(str(ret))

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	face = faceCascade.detectMultiScale(gray, 1.3, 5)
	faceState = False
	for (x, y, w, h) in face:
		faceState = True
		yList.insert(0, y)
		yList.pop()
		xList.insert(0, x)
		xList.pop()
		#coordList.insert(0,(x,y))
		#coordList.pop()
		cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
	#print(str(faceState))
	if faceState == False:
		noFaceCnt += 1
		if noFaceCnt == 3:
			#new = coordList[0]
			#old = coordList[9]
			print(checkDirection(xList, yList))
			#print(getDirection(degrees))
#			if CheckUpDown(yList):
#				print("UP")
#			elif ~CheckUpDown(yList):
#				print("DOWN")
#			elif CheckUpDown(xList):
#				print("RIGHT")
#			elif ~CheckUpDown(xList):
#				print("LEFT")
			#noFaceCnt = 0
	else:
		noFaceCnt = 0
	#print("faceState is: "+str(faceState)+ "nofacecnt is: "+str(noFaceCnt))
	cv2.imshow('img', img)
	k = cv2.waitKey(30) & 0xff
	if k == 27:

		break

cap.release()
cv2.destroyAllWindows()
