from math import sqrt, pi
from ctypes import *
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def angle_detection(img, pt1, pt2):
    shape_image = np.zeros_like(img)

    offset = 10    
    y1 = max([pt1[0] - offset, 0])
    y2 = min([pt2[0] + offset, 1280])
    x1 = max([pt1[1] - offset, 0])
    x2 = min([pt2[1] + offset, 728])
    
    shape_image[x1:x2, y1:y2] = img[x1:x2, y1:y2]
    cv2.imshow("Drawn Image", shape_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    shape_image = cv2.cvtColor(shape_image, cv2.COLOR_BGR2GRAY)
    
    shape_image = cv2.GaussianBlur(shape_image, (3,3), 1)
    _,thresh = cv2.threshold(shape_image,0,255,cv2.THRESH_OTSU)
    cv2.imshow("Drawn Image", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    thresh[x1:x2, y1:y2] = 255 - thresh[x1:x2, y1:y2]
    
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(thresh,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 2)
    cv2.imshow("Drawn Image", dilation)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    erosion1 = cv2.erode(dilation,kernel,iterations = 1)
    cv2.imshow("Drawn Image", erosion1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    contours, _ = cv2.findContours(erosion1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    img_contour = img.copy()
    contour_color = (180, 100, 50)
    cv2.drawContours(img_contour, contours, -1, contour_color, 2)
    img_contour_rgb = cv2.cvtColor(img_contour, cv2.COLOR_BGR2RGB)
    plt.imshow(img_contour_rgb)
    plt.title("Contours (Blue)")
    plt.axis("off")
    plt.show()

    if len(contours) > 0:
        min_area = 500
        idx = -1
        print(contours)
        for i,cnt in enumerate(contours):
            #print(i, cnt)
            print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > min_area: 
                a = cv2.approxPolyDP(cnt, epsilon=0.08*cv2.arcLength(cnt, closed=True), closed=True)
                min_area=cv2.contourArea(cnt)
                idx = i

        if idx == -1:
            print("No contour found((")
            return -1, -1, -1

        rect = cv2.minAreaRect(contours[idx])
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        print(box)
        
        edge1 = box[1] - box[0]
        edge2 = box[2] - box[1]
        print(edge1, edge2)
        cx = int(rect[0][0])
        cy = int(rect[0][1])

        print(edge1)
        print(edge2)
        print(np.dot(edge1, edge1))
        print(np.dot(edge2, edge2))
        if np.dot(edge1, edge1) > np.dot(edge2, edge2):
            print("edge1")
            shape_angle = np.arctan2(edge1[0], edge1[1])
        else:
            print("edge2")
            shape_angle = np.arctan2(edge2[0], edge2[1])
        print('!!')
        shape_angle = min(shape_angle, 2*pi-shape_angle)
        print(cx, cy, shape_angle)
        return cx, cy, shape_angle

    else: 
        return -1, -1, 0