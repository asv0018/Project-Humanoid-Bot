import threading as thread
import psutil
import sys
import cv2 as cv
from UserWrittenModules import MultiprocessingFunctions as multi

if __name__ == '__main__':
    stopper = psutil.Process()
    speech = thread.Thread(target=multi.SpeechToText)
    face_cascade = cv.CascadeClassifier(r"Assets/Haarcascades/haarcascade_frontalface_default.xml")
    cam = cv.VideoCapture(0)
    if not cam.isOpened():
        print("Camera Failed to Open!.")
        sys.exit(0)

    # initialisations of threads
    while 1:
        ret, img = cam.read()
        physicalDistancing = thread.Thread(target=multi.DetectPhysicalDistancing, args=(img.copy(),))
        if not physicalDistancing.is_alive():
            physicalDistancing.start()
        upper_body = face_cascade.detectMultiScale(
            img,
            scaleFactor=1.1,
            minNeighbors=10,
            # Niran!you may find some issues here, min size of the face detection may change with respect to the camera.
            minSize=(80, 80),
            flags=cv.CASCADE_SCALE_IMAGE
        )
        if len(upper_body):  # if upper body is detected! then mark the person

            for (x, y, w, h) in upper_body:
                cv.rectangle(img, (x, y), (x + w, y + h), (15, 85, 90), 5)
                if not speech.is_alive():
                    speech = thread.Thread(target=multi.SpeechToText)
                    speech.start()

        else:
            print("NO HUMAN IS DETECTED!")

        cv.imshow("Eye of Humanoid Bot - Wuhan Hunter Squad!", img)
        cv.waitKey(1)

    cam.release()
    cv.destroyAllWindows()
