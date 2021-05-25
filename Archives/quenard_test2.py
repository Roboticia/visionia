# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 18:52:54 2020

@author: julien
"""
import cv2

cap = cv2.VideoCapture(0)

list_frame=[]

# loop to process the image at  manual exposure
for i in range(100):
    ret, frame = cap.read()
    list_frame.append(frame)

for index,frame in enumerate(list_frame):
    cv2.imwrite('test'+str(index)+'.jpg',frame)

cap.release()

