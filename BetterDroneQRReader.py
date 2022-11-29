from djitellopy import Tello
from pyzbar.pyzbar import decode
import numpy as np
import cv2

# Tello startup sequence
telloBot = Tello()
telloBot.connect()
# telloBot.get_video_capture()
telloBot.for_back_velocity = 0
telloBot.left_right_velocity = 0
telloBot.up_down_velocity = 0
telloBot.yaw_velocity = 0
telloBot.speed = 0

# print(telloBot.query_sdk_version())

# telloBot.set_video_bitrate(5)
# telloBot.set_video_fps('high')
# telloBot.set_video_resolution('high')

telloBot.streamoff()  # Camera turn off and turn on
telloBot.streamon()

used_code = []

print("Battery life: " + str(telloBot.get_battery()) + "%")

cv2.waitKey(300)


# User input to control drone
# def userinput():
#     if 0xFF == ord('e'):
#         print("Taking off/Landing Protocol")
#         telloBot.takeoff() if telloBot.is_flying else telloBot.land()
#         cv2.waitKey(10)


# Tello Main Loop
while True:
    img = telloBot.get_frame_read().frame

    for qr in decode(img):
        myData = qr.data.decode('UTF-8')  # convets to str
        if qr.data.decode('UTF-8') not in used_code:
            # print(qr.data)
            # print(myData)
            pts = np.array([qr.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 200), 2)
            pts2 = qr.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 200), 2)
            used_code.append(myData)
            cv2.waitKey(1)
        elif qr.data.decode('UTF-8') in used_code:
            pts = np.array([qr.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 200), 2)
            pts2 = qr.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 200), 2)
            # print("Already seen, try a different qr.")
            cv2.waitKey(1)
        else:
            pass
        if len(used_code) == 7:
            print(used_code)
        else:
            pass

    cv2.imshow("Bot Camera", img)

#     userinput()

    if cv2.waitKey(1) & 0xFF == 27:
        telloBot.streamoff()
        telloBot.end()
        break
