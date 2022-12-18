# DJI Tello User Control and QR scanning camera
#  WASD - Lateral movement
#  QE - Yaw movement
#  Up/Down Arrows - Elevation

from djitellopy import Tello
from pyzbar.pyzbar import decode
import numpy as np
import cv2

# Tello startup sequence
print("Connecting to Tello...")
telloBot = Tello()
telloBot.connect()
# telloBot.get_video_capture()
telloBot.for_back_velocity = 0
telloBot.left_right_velocity = 0
telloBot.up_down_velocity = 0
telloBot.yaw_velocity = 0
telloBot.speed = 0
print("Tello Connected.")
print("Battery life: " + str(telloBot.get_battery()) + "%")
telloBot.streamoff()  # Camera turn off and turn on
telloBot.streamon()

# # Tello Package version incompatible features
# print(telloBot.query_sdk_version())
# telloBot.set_video_bitrate(5)
# telloBot.set_video_fps('high')
# telloBot.set_video_resolution('high')


# Draw Rectangle around detected QR code
def drawqrbounds(qrimage, srcimage):
    pts = np.array([qrimage.polygon], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(srcimage, [pts], True, (255, 0, 200), 2)
    pts2 = qrimage.rect
    cv2.putText(srcimage, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 200), 2)


# User input to control drone
LINEAR_SPEED = 15
ANGULAR_SPEED = 50
def userinput(drone: Tello):
    leftright, forwardback, updown, yaw = 0, 0, 0, 0
    key = cv2.waitKey(1) & 0xFF                         # This is actually doing AND bit operations

    # Forward/Backward
    if key == ord('w'):
        forwardback = LINEAR_SPEED
    elif key == ord('s'):
        forwardback = -LINEAR_SPEED

    # Left/Right (Lateral)
    if key == ord('a'):
        leftright = -LINEAR_SPEED
    elif key == ord('d'):
        leftright = LINEAR_SPEED

    # Left/Right (Yaw)
    if key == ord('q'):
        yaw = -ANGULAR_SPEED
    elif key == ord('e'):
        yaw = ANGULAR_SPEED

    # Up/Down
    if key == ord('r'):
        updown = LINEAR_SPEED
    elif key == ord('f'):
        updown = -LINEAR_SPEED

    # Liftoff/Landing
    if key == ord('t'):
        drone.takeoff()
    elif key == ord('g'):
        drone.land()

    drone.send_rc_control(leftright, forwardback, updown, yaw)


# Tello Main Loop
cv2.waitKey(300)
used_code = []
while True:
    img = telloBot.get_frame_read().frame

    for qr in decode(img):
        myData = qr.data.decode('UTF-8')  # convets to str
        if qr.data.decode('UTF-8') not in used_code:
            # print(qr.data)
            # print(myData)
            drawqrbounds(qr, img)
            used_code.append(myData)
            cv2.waitKey(1)
        elif qr.data.decode('UTF-8') in used_code:
            # print("Already seen, try a different qr.")
            drawqrbounds(qr, img)
            cv2.waitKey(1)
        else:
            pass
        if len(used_code) == 7:
            print(used_code)
        else:
            pass

    cv2.imshow("Bot Camera", img)

    userinput(telloBot)

    # Exit Program conditions
    if cv2.waitKey(1) & 0xFF == 27:
        cv2.destroyAllWindows()
        telloBot.streamoff()
        telloBot.end()
        print("Ending Program")
        break
