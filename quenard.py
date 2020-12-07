# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 18:52:54 2020

@author: julien
"""
import cv2
from utils import ArducamUtils
import subprocess
import time

def show_info(arducam_utils):
    _, firmware_version = arducam_utils.read_dev(ArducamUtils.FIRMWARE_VERSION_REG)
    _, sensor_id = arducam_utils.read_dev(ArducamUtils.FIRMWARE_SENSOR_ID_REG)
    _, serial_number = arducam_utils.read_dev(ArducamUtils.SERIAL_NUMBER_REG)
    print("Firmware Version: {}".format(firmware_version))
    print("Sensor ID: 0x{:04X}".format(sensor_id))
    print("Serial Number: 0x{:08X}".format(serial_number))


def resize(frame, dst_width):
    width = frame.shape[1]
    height = frame.shape[0]
    scale = dst_width * 1.0 / width
    return cv2.resize(frame, (int(scale * width), int(scale * height)))



cmd1 = 'v4l2-ctl -d 0 -c exposure=400'
cmd2 = 'v4l2-ctl -d 0 -C exposure'
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
arducam_utils = ArducamUtils(0)
cap.set(cv2.CAP_PROP_CONVERT_RGB, arducam_utils.convert2rgb)
show_info(arducam_utils)



# Aquisition des dimentions de l'image en provenance du capteur
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)




list_frame=[]


# needed to purge the frame with default exposure
for i in range(6):
    subprocess.call(cmd1, shell=True)
    ret, frame = cap.read()

# loop to process the image at  manual exposure
for i in range(10): # Nombre d'images
    ret, frame = cap.read()
    list_frame.append(frame)
    
for index,frame in enumerate(list_frame):
    frame = frame.reshape(int(h), int(w))
    frame = arducam_utils.convert(frame)
#    frame = resize(frame, 1280.0)

# creation de l'image et de son appellation
    cv2.imwrite('test'+str(index)+'.jpg',frame)

# soulage
cap.release()


