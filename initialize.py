import cv2
from utils import ArducamUtils
import subprocess


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


cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
arducam_utils = ArducamUtils(0)
cap.set(cv2.CAP_PROP_CONVERT_RGB, arducam_utils.convert2rgb)
print(cv2.CAP_PROP_EXPOSURE)
show_info(arducam_utils)

#subprocess.run(['v4l2-ctl','-d','0','-c','exposure=500'])

a = input('taper quit pour sortir')

cap.release()
