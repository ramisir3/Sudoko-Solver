import cv2
import numpy as np
from DigitDetect import *
import os
import time

def takeImageExtractGrid(model):
    os.system("libcamera-jpeg -o test2.jpg -t 1500")
    imagePath = ("./test2.jpg")
    imageHeight = 900
    imageWidth = 900

    img = cv2.imread(imagePath)
    img = cv2.resize(img, (imageWidth, imageHeight))
    # cv2.imshow('Steps', img)
    # cv2.waitKey(0)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThresh = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)

    # cv2.imshow('Steps', imgThresh)
    # cv2.waitKey(0)

    imgContours = img.copy()
    imgContour2 = img.copy()
    contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

    # cv2.imshow('Steps', imgContours)
    # cv2.waitKey(0)

    biggest = np.array([])
    maxArea = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    # print(biggest)

    if biggest.size != 0:
        biggest = biggest.reshape((4, 2))
        orderedPoints = np.zeros((4, 1, 2), dtype=np.int32)
        add = biggest.sum(1)
        orderedPoints[0] = biggest[np.argmin(add)]
        orderedPoints[3] = biggest[np.argmax(add)]
        diff = np.diff(biggest, axis=1)
        orderedPoints[1] = biggest[np.argmin(diff)]
        orderedPoints[2] = biggest[np.argmax(diff)]
        biggest = orderedPoints
        cv2.drawContours(imgContour2, biggest, -1, (0, 0, 255), 20)
    #     print(biggest)
    #     cv2.imshow('Steps', imgContour2)
    #     cv2.waitKey(0)

        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [imageWidth, 0], [0, imageHeight], [imageWidth, imageHeight]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv2.warpPerspective(imgGray, matrix, (imageWidth, imageHeight))
    #     cv2.imshow('Steps', imgWarp)
    #     cv2.waitKey(0)

        BW = cv2.adaptiveThreshold(imgWarp, 255, 1, 1, 19, 11)
    #     cv2.imwrite("./thres.jpg", BW)
    #     cv2.imshow('Steps', BW)
    #     cv2.waitKey(0)

        rows = np.vsplit(BW, 9)
        boxes = []
        for r in rows:
            cols = np.hsplit(r, 9)
            for box in cols:
                shape = box.shape
                height = shape[0]
                width = shape[1]
    #             print(box.shape)
                cropped = box[10:(height-5), 10:(width-10)]
                resized = cv2.resize(cropped, (28, 28))
                # cv2.imshow('Steps', cropped)
                # cv2.waitKey(0)
                boxes.append(resized)
        numbers = getPredection(boxes, model)
        numbers = ''.join(str(v) for v in numbers)
        print(numbers)
        return numbers
    #     print(numbers)

