# TODO: - Increase resolution of the obtained QR code before and after warping
#       - Properly warp when oriented at different angles to the QR code

import cv2
import numpy as np

WIDTH_OUTPUT, HEIGHT_OUTPUT = 400, 400
ptsOutput = np.float32([[0, 0],
                        [WIDTH_OUTPUT, 0],
                        [0, HEIGHT_OUTPUT],
                        [WIDTH_OUTPUT, HEIGHT_OUTPUT]])  # Output size format for Image warping


def getContours(img):
    # Contour Collection
    contours, heirarchy = cv2.findContours(img,
                                           cv2.RETR_EXTERNAL,       # Retrieve the extreme outer contours
                                           cv2.CHAIN_APPROX_NONE)   # Request ALL contour values without compressing

    # Contour Processing
    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Draw Contours
        if area > 700:
            # Draw ALL such contours
            cv2.drawContours(frameContours, cnt, -1, (0, 255, 0), 3)  # (image, contour, contourIndex, color, thickness)
                                                                      # contourIndex = -1 means draw all contour points

            # Find Perimeter and Corners
            cntperim = cv2.arcLength(cnt, True)  # Calculate contour perimeter (True expecting closed shapes)
            approxcorners = cv2.approxPolyDP(cnt, 0.02 * cntperim, True)  # Approximate the best fit shape

            # Warp the contour to a square image using source and output corner points
            if len(approxcorners) == 4:
                # We only want to warp contours closest to a square (numCorners = 4)
                ptsSource = np.float32([[approxcorners[0][0][0], approxcorners[0][0][1]],
                                        [approxcorners[2][0][0], approxcorners[0][0][1]],
                                        [approxcorners[0][0][0], approxcorners[2][0][1]],
                                        [approxcorners[2][0][0], approxcorners[2][0][1]]])
                matrix = cv2.getPerspectiveTransform(ptsSource, ptsOutput)
                frameWarped = cv2.warpPerspective(frame, matrix, (WIDTH_OUTPUT, HEIGHT_OUTPUT))
                cv2.imshow("warp", frameWarped)

                # QR detect and read
                data, bbox, _ = qrdetector.detectAndDecode(frameWarped)
                if bbox is not None:
                    cv2.rectangle(frame,
                                  (int(bbox[0][0][0]), int(bbox[0][0][1])),
                                  (int(bbox[0][2][0]), int(bbox[0][2][1])),
                                  (255, 0, 0),
                                  2)
                    print(data)

            # Bounding boxes for analysis
            rect = cv2.minAreaRect(cnt)                                             # Rotatable Bounding box (Red)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frameContours, [box], 0, (0, 0, 255), 2)


# Main Video Capture Loop
ONBOARD_CAMERA = 0  # If there is no onboard camera, use this value for external cameras
EXTERNAL_CAMERA = 1

capture = cv2.VideoCapture(EXTERNAL_CAMERA)

qrdetector = cv2.QRCodeDetector()

while True:
    success, frame = capture.read()

    # Processing
    frameGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlur = cv2.GaussianBlur(frameGrey, (5, 5), 1)
    frameCanny = cv2.Canny(frameBlur, 75, 200, 1)
    frameContours = frame.copy()

    getContours(frameCanny)

    cv2.imshow("contour detection", frameContours)

    if cv2.waitKey(1) & 0xFF == 27:  # Esc
        break

cv2.destroyAllWindows()
