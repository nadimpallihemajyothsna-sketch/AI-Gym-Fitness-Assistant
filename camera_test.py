import cv2

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        print("Camera not working")
        break

    cv2.imshow("Webcam Test", frame)

    # Press ESC to close
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()