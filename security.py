import cv2
import time
import subprocess

capture = False
oldtime = 11
compareImage = None
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)
out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"),
                      20,
                      size)


def isDeviceConnected():
    p = subprocess.Popen("bluetoothctl connect 00:57:C1:59:9F:A8 | grep 'Connection successful'", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p.wait()
    if output:
        p = subprocess.Popen("bluetoothctl disconnect 00:57:C1:59:9F:A8 | grep 'Successful disconnected'", stdout=subprocess.PIPE, shell=True)
        p.wait()
        print("True")
        return True
    else:
        print("False")
        return False


while True:
    check, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayFrame = cv2.GaussianBlur(grayFrame, (25, 25), 0)

    if compareImage is None:
        compareImage = grayFrame
        continue

    delta = cv2.absdiff(compareImage, grayFrame)
    threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    (contours, _) = cv2.findContours(threshold,
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 10000 and time.time() - \
                oldtime > 10 and isDeviceConnected is False:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

            compareImage = grayFrame
            oldtime = time.time()
            capture = True
        elif time.time() - oldtime > 10:
            capture = False

    if capture is True:
        out.write(frame)

    cv2.imshow("Color Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
