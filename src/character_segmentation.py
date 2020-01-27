import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def segment_characters(img):

    ret, thresh = cv.threshold(img, 127, 255,cv.THRESH_BINARY + cv.THRESH_OTSU)
    im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    imgs=[]
    pos=[]
    for i in range(len(contours)):
        hi=hierarchy[0][i].tolist()
        if i==0:
            continue
        if (cv.contourArea(contours[i]) > 1000 and hi[3]==0): 
            drawing = 255 * np.ones(img.shape, np.uint8)
            cv.fillPoly(drawing, pts =[contours[i]], color=(15,15,15))
            for j in range(len(contours)):
                hi2=hierarchy[0][j].tolist()
                if hi2[3]==i and cv.contourArea(contours[j]) > 1000:
                    cv.fillPoly(drawing, pts =[contours[j]], color=(255,255,255))
            (x,y,w,h) = cv.boundingRect(contours[i])
            crop_img = drawing[y:y+h, x:x+w]
            new_img=np.stack((crop_img,)*3, axis=-1)
            imgs.append((new_img,(x,y,w,h)))

    imgs=sorted(imgs,key=lambda entry: entry[1][0])

    char_list=[]
    for item in imgs:
        char_list.append(item[0])

    return char_list
    

