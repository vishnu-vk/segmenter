import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def segment_words(img):

    ret, thresh = cv.threshold(img, 127, 255,cv.THRESH_BINARY + cv.THRESH_OTSU)
    im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    res=[]

    for i in range(len(contours)):
        hi=hierarchy[0][i].tolist()
        if cv.contourArea(contours[i])>1000 and hi[3]==0:
            (x,y,w,h) = cv.boundingRect(contours[i])
            res.append((x-25,y,x+w+25,y+h))
    res=sorted(res, key=lambda entry:entry[0])


    words=[]
    startX=res[0][0]
    endX=res[0][2]
    startY=res[0][1]
    endY=res[0][3]

    for i in range(1,len(res)):
        if(res[i][0]<endX):
            endX=res[i][2]
            if(res[i][1]<startY):
                startY=res[i][1]
            if(res[i][3]>endY):
                endY=res[i][3]
        else:
            words.append((startX,startY,endX,endY))
            startX=res[i][0]
            endX=res[i][2]
            startY=res[i][1]
            endY=res[i][3]
    words.append((startX,startY,endX,endY))
    
    word_list=[]
    for word in words:
        crop_img = im[word[1]-10:word[3]+10, word[0]:word[2]]
        word_list.append(crop_img)
    return word_list
