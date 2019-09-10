import cv2 as cv2
import numpy as np
import queue as queue
from picamera import PiCamera
import imutils
import time
import sys


class ImageProcessor():
    def __init__(self):
        global referenceImg, cntRef1, cntRef2, cntRef3
        self.jobs = queue.Queue()

        referenceImg = cv2.imread("./training_images/1.jpg")
        referenceImg = cv2.cvtColor(referenceImg, cv2.COLOR_BGR2GRAY)
        retT, thT = cv2.threshold(referenceImg, 0, 255, cv2.THRESH_BINARY)
        imgT, contoursT, hT = cv2.findContours(
            thT, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contoursT:
            approxT = cv2.approxPolyDP(
                cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if (len(approxT) == 7):
                cntRef1 = cnt
                break

        referenceImg2 = cv2.imread("./training_images/2.jpg")
        referenceImg2 = cv2.cvtColor(referenceImg2, cv2.COLOR_BGR2GRAY)
        retT, thT = cv2.threshold(referenceImg2, 0, 255, cv2.THRESH_BINARY)
        imgT, contoursT, hT = cv2.findContours(
            thT, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contoursT:
            approxT = cv2.approxPolyDP(
                cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if (len(approxT) == 7):
                cntRef2 = cnt
                break

        referenceImg3 = cv2.imread("./training_images/3.jpg")
        referenceImg3 = cv2.cvtColor(referenceImg3, cv2.COLOR_BGR2GRAY)
        retT, thT = cv2.threshold(referenceImg3, 0, 255, cv2.THRESH_BINARY)
        imgT, contoursT, hT = cv2.findContours(
            thT, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contoursT:
            approxT = cv2.approxPolyDP(
                cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if (len(approxT) == 7):
                cntRef3 = cnt
                break

    # Continue to take photos and save photos when requested from PC
    def captureTest(self):
        global camera
        camera = PiCamera(resolution=(340, 240))
        camera.rotation = 270
        currentPath = str(sys.path[0])
        name = str(time.time())
        try:
            camera.capture(
                currentPath+"/capture/{}.jpg".format(name))
            print("Captured Image")
            return name
        except Exception as e:
            print("Exception in Capture: "+str(e))
        finally:
            if (camera != None):
                camera.close()

    def capture(self, listenerFromPC):
        global camera
        camera = PiCamera(resolution=(340, 240))
        camera.rotation = 270
        currentPath = str(sys.path[0])
        try:
            while True:
                # To signal taking a photo from receiving sensor readings
                sensorReadings = listenerFromPC.recv()
                camera.capture(
                    currentPath+"/capture/{}.jpg".format(sensorReadings))
                listenerFromPC.send("Captured Image")
                self.jobs.put(sensorReadings)
        except Exception as e:
            print("Exception in Capture: "+str(e))
        finally:
            if (camera != None):
                camera.close()

    global mse

    def mse(imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

    def processTest(self, name):
        global referenceImg, currentPath
        print('Waiting for any captured images to process...')
        currentPath = str(sys.path[0])
        name = str(time.time()) + "_processed"
        try:
            while True:
                resultMsg = ""
                imageTest = None
                # If there are images captured not yet processed
                imageTest = cv2.imread(currentPath+"/capture/{}.jpg".format(name))
                if (imageTest is not None):
                    cv2.imwrite(
                        currentPath+"/capture/{}.jpg".format(name), imageTest)
                    result, sensorID = checkImageTest(imageTest)
                    print('|'+result+'|'+sensorID)
                else:
                    time.sleep(0.5)

        except Exception as e:
            print('Exception: ' + str(e))
            camera.close()

    def processImage(self, listenerToRpi):
        global referenceImg, currentPath
        print('Waiting for any captured images to process...')
        currentPath = str(sys.path[0])
        try:
            while True:
                resultMsg = ""
                imageTest = None
                # If there are images captured not yet processed
                if (self.jobs.empty() == False):
                    print('Processing of captured images...')
                    sensorReadings = self.jobs.get()
                    imageTest = cv2.imread(
                        currentPath+"/capture/{}.jpg".format(sensorReadings))
                    if (imageTest is not None):
                        cv2.imwrite(
                            currentPath+"/capture/{}.jpg".format(sensorReadings), imageTest)
                        result, sensorID = checkImage(
                            imageTest, sensorReadings)
                        listenerToRpi.send(
                            sensorReadings + '|'+result+'|'+sensorID)

                # Poll every 0.5 seconds
                else:
                    time.sleep(0.5)

        except Exception as e:
            print('Exception: ' + str(e))
            camera.close()

    global checkImage

    def checkImageTest(imageTest, imgName):
        global cntRef1, cntRef2, cntRef3, currentPath
        # Do not have to swap the original X and Y axis since changed config; original imgX = shape[1]
        imgX = imageTest.shape[1]
        imgY = imageTest.shape[0]
        #imageTest = imutils.resize(imageTest, height = 300)
        gray = cv2.cvtColor(imageTest, cv2.COLOR_BGR2GRAY)
        blurred = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(blurred, 30, 200)
        img, contours, h = cv2.findContours(
            edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        imgPos = '-1'
        thresholdMatch = 5
        tempContours = []
        tempMSE = []
        matchShapeArr = np.zeros(3)
        ##
        finalContour = imageTest.copy()
        ##
        for cnt in contours:
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            area = cv2.contourArea(cnt)
            matchShapeArr[0] = cv2.matchShapes(cntRef1, cnt, 1, 0.0)
            matchShapeArr[1] = cv2.matchShapes(cntRef2, cnt, 1, 0.0)
            matchShapeArr[2] = cv2.matchShapes(cntRef3, cnt, 1, 0.0)
            matchShapeVal = np.amin(matchShapeArr)

            if (6 <= len(approx) <= 8 and matchShapeVal <= thresholdMatch):
                ##
                print(area)
                cv2.drawContours(finalContour, [approx], -1, (0, 255, 0), 2)
                cv2.imwrite('finalContour.jpg', finalContour)
                ##
                x, y, w, h = cv2.boundingRect(approx)
                tempImg = imageTest[y:y+h, x:x+w]
                if tempImg.size > 0:
                    tempImg = cv2.resize(tempImg, (200, 200))
                tempImg = tempImg[:, :, 0]
                if (w > 0 and h > 0):
                    if (280 < area and area < 15000):
                        resized = cv2.resize(
                            tempImg, (referenceImg.shape[0], referenceImg.shape[1]))
                        tempMSE.append(mse(referenceImg, resized))
                        tempContours.append(cnt)

        if (len(tempMSE) > 0):
            if np.amin(tempMSE) < 13000:
                print('MSE:' + str(np.amin(tempMSE)))
                matchShapeArr[0] = cv2.matchShapes(cntRef1, cnt, 1, 0.0)
                matchShapeArr[1] = cv2.matchShapes(cntRef2, cnt, 1, 0.0)
                matchShapeArr[2] = cv2.matchShapes(cntRef3, cnt, 1, 0.0)
                matchShapeVal = np.amin(matchShapeArr)
                print('matchShape Value: ' + str(matchShapeVal))
                cnt = tempContours[np.argmin(tempMSE)]
                cntArea = cv2.contourArea(cnt)
                imgArea = imgX*imgY
                arrowRatio = cntArea/imgArea
                print('Arrow ratio:' + str(arrowRatio))

                M = cv2.moments(cnt)
                cx = int(M["m10"]/M["m00"])

                ###################################
                # Definitely center
                if 0.05 < arrowRatio < 0.20:
                    imgPos = '1'

                # Possibly left/center/right
                else:
                    # Center
                    if imgX/3 < cx < 2*(imgX/3):
                        imgPos = '1'

                    # Left
                    elif cx < imgX/3:
                        imgPos = '0'

                    # Right
                    else:
                        imgPos = '2'

                ###################################

                cv2.drawContours(imageTest, [cnt], -1, (255, 0, 0), 1)
                cv2.imwrite(
                    currentPath+"/capture/{}.jpg".format(imgName), imageTest)
                return 'True', imgPos
            else:
                return 'False', imgPos
        else:
            return 'False', imgPos

    def checkImage(imageTest, imgName):
        global cntRef1, cntRef2, cntRef3, currentPath
        # Do not have to swap the original X and Y axis since changed config; original imgX = shape[1]
        imgX = imageTest.shape[1]
        imgY = imageTest.shape[0]
        #imageTest = imutils.resize(imageTest, height = 300)
        gray = cv2.cvtColor(imageTest, cv2.COLOR_BGR2GRAY)
        blurred = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(blurred, 30, 200)
        img, contours, h = cv2.findContours(
            edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        imgPos = '-1'
        thresholdMatch = 5
        tempContours = []
        tempMSE = []
        matchShapeArr = np.zeros(3)
        ##
        finalContour = imageTest.copy()
        ##
        for cnt in contours:
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            area = cv2.contourArea(cnt)
            matchShapeArr[0] = cv2.matchShapes(cntRef1, cnt, 1, 0.0)
            matchShapeArr[1] = cv2.matchShapes(cntRef2, cnt, 1, 0.0)
            matchShapeArr[2] = cv2.matchShapes(cntRef3, cnt, 1, 0.0)
            matchShapeVal = np.amin(matchShapeArr)

            if (6 <= len(approx) <= 8 and matchShapeVal <= thresholdMatch):
                ##
                print(area)
                cv2.drawContours(finalContour, [approx], -1, (0, 255, 0), 2)
                cv2.imwrite('finalContour.jpg', finalContour)
                ##
                x, y, w, h = cv2.boundingRect(approx)
                tempImg = imageTest[y:y+h, x:x+w]
                if tempImg.size > 0:
                    tempImg = cv2.resize(tempImg, (200, 200))
                tempImg = tempImg[:, :, 0]
                if (w > 0 and h > 0):
                    if (280 < area and area < 15000):
                        resized = cv2.resize(
                            tempImg, (referenceImg.shape[0], referenceImg.shape[1]))
                        tempMSE.append(mse(referenceImg, resized))
                        tempContours.append(cnt)

        if (len(tempMSE) > 0):
            if np.amin(tempMSE) < 13000:
                print('MSE:' + str(np.amin(tempMSE)))
                matchShapeArr[0] = cv2.matchShapes(cntRef1, cnt, 1, 0.0)
                matchShapeArr[1] = cv2.matchShapes(cntRef2, cnt, 1, 0.0)
                matchShapeArr[2] = cv2.matchShapes(cntRef3, cnt, 1, 0.0)
                matchShapeVal = np.amin(matchShapeArr)
                print('matchShape Value: ' + str(matchShapeVal))
                cnt = tempContours[np.argmin(tempMSE)]
                cntArea = cv2.contourArea(cnt)
                imgArea = imgX*imgY
                arrowRatio = cntArea/imgArea
                print('Arrow ratio:' + str(arrowRatio))

                M = cv2.moments(cnt)
                cx = int(M["m10"]/M["m00"])

                ###################################
                # Definitely center
                if 0.05 < arrowRatio < 0.20:
                    imgPos = '1'

                # Possibly left/center/right
                else:
                    # Center
                    if imgX/3 < cx < 2*(imgX/3):
                        imgPos = '1'

                    # Left
                    elif cx < imgX/3:
                        imgPos = '0'

                    # Right
                    else:
                        imgPos = '2'

                ###################################

                cv2.drawContours(imageTest, [cnt], -1, (255, 0, 0), 1)
                cv2.imwrite(
                    currentPath+"/capture/{}.jpg".format(imgName), imageTest)
                return 'True', imgPos
            else:
                return 'False', imgPos
        else:
            return 'False', imgPos
