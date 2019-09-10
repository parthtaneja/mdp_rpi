# import the necessary packages
import imutils
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt

from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep




def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	print (err)
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
 
def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	return m


camera =PiCamera()
camera.resolution = (640,480)

camera.start_preview()
sleep(5)
camera.capture('captured.jpg')
camera.stop_preview()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())


# load the query image, compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread("captured.jpg")
ratio = image.shape[0] / 300.0
orig = image.copy()
image = imutils.resize(image, height = 300)
 
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)

# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
_, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
screenCnt = None

# loop over our contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# if our approximated contour has four points, then
	# we can assume that we have found our screen
	if len(approx) == 7:
		screenCnt = approx
		break

#Get exact arrow contours
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
#cv2.imshow("ARROW", image)
#cv2.waitKey(0)

#Get bounding box contours
x,y,w,h = cv2.boundingRect(screenCnt)
cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)

cv2.imwrite('box.png',image)
#cv2.imshow("BOX", image)
#cv2.waitKey(0)

###Crop out the box
img = cv2.imread("box.png")
cropped =img[y:y+h,x:x+w]
#cv2.imshow("Cropped", cropped)
#cv2.waitKey(0)
cropped = cv2.resize(cropped, (200, 200)) 
cv2.imwrite('arrowbox.png',cropped)


# load the images -- the original, the original + contrast,
# and the original + photoshop
right = cv2.imread("right.png")
left = cv2.imread("left.png")
up = cv2.imread("up.png")
down = cv2.imread("down.png")
imagetaken = cv2.imread("arrowbox.png")


# convert the images to grayscale
right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
up = cv2.cvtColor(up, cv2.COLOR_BGR2GRAY)
down = cv2.cvtColor(down, cv2.COLOR_BGR2GRAY)
imagetaken = cv2.cvtColor(imagetaken, cv2.COLOR_BGR2GRAY)

 
# compare the images
R=compare_images(right, imagetaken, "Right vs. Original")
L=compare_images(left, imagetaken, "Left vs. Original")
U=compare_images(up, imagetaken, "Up vs. Original")
D=compare_images(down, imagetaken, "Down vs. Original")


#Store all into array [1 ,2,3,4]
myList= [float(R),float(L),float(U),float(D)]
minIndex = myList.index(min(myList))
if minIndex == 0:
        print ("Right")
        image = cv2.imread("captured.jpg")
        ratio = image.shape[0] / 300.0
        orig = image.copy()
        image = imutils.resize(image, height = 300)
         
        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
        screenCnt = None

        # loop over our contours
        for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
         
                # if our approximated contour has four points, then
                # we can assume that we have found our screen
                if len(approx) == 7:
                        screenCnt = approx
                        break

        #Get bounding box contours
        x,y,w,h = cv2.boundingRect(screenCnt)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
        cv2.putText(image,"RIGHT",(x,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("RIGHT", image)
        cv2.waitKey(0)
elif minIndex == 1:
        print ("Left")
        image = cv2.imread("captured.jpg")
        ratio = image.shape[0] / 300.0
        orig = image.copy()
        image = imutils.resize(image, height = 300)
         
        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
        screenCnt = None

        # loop over our contours
        for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
         
                # if our approximated contour has four points, then
                # we can assume that we have found our screen
                if len(approx) == 7:
                        screenCnt = approx
                        break

        #Get bounding box contours
        x,y,w,h = cv2.boundingRect(screenCnt)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
        cv2.putText(image,"LEFT",(x,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("LEFT", image)
        cv2.waitKey(0)
elif minIndex == 2:
        print ("Up")
        image = cv2.imread("captured.jpg")
        ratio = image.shape[0] / 300.0
        orig = image.copy()
        image = imutils.resize(image, height = 300)
         
        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
        screenCnt = None

        # loop over our contours
        for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
         
                # if our approximated contour has four points, then
                # we can assume that we have found our screen
                if len(approx) == 7:
                        screenCnt = approx
                        break

        #Get bounding box contours
        x,y,w,h = cv2.boundingRect(screenCnt)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
        cv2.putText(image,"UP",(x,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("UP", image)
        cv2.waitKey(0)
else:
        print("Down")
        image = cv2.imread("captured.jpg")
        ratio = image.shape[0] / 300.0
        orig = image.copy()
        image = imutils.resize(image, height = 300)
         
        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
        screenCnt = None

        # loop over our contours
        for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
         
                # if our approximated contour has four points, then
                # we can assume that we have found our screen
                if len(approx) == 7:
                        screenCnt = approx
                        break

        #Get bounding box contours
        x,y,w,h = cv2.boundingRect(screenCnt)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
        cv2.putText(image,"DOWN",(x,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("DOWN", image)
        cv2.waitKey(0)













