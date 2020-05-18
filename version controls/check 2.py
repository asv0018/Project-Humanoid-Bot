import threading as thread
import psutil
import sys
import cv2
from UserWrittenModules import MultiprocessingFunctions as multi
import math
import numpy as np
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'Assets/Dialogflow credentials/humanoid-bot-qxmcwn-c1ebdc7db876.json' # it is there in this folder inside the currrent working directory
DIALOGFLOW_PROJECT_ID = 'humanoid-bot-qxmcwn'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'
labelsPath = "coco.names.txt"
LABELS = open(labelsPath).read().strip().split("\n")
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                           dtype="uint8")
weightsPath = r"yolov3.weights"
configPath = r"yolov3.cfg"
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


if __name__ == '__main__':
    stopper = psutil.Process()
    speech = thread.Thread(target=multi.SpeechToText)
    face_cascade = cv2.CascadeClassifier(r"Assets/Haarcascades/haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Camera Failed to Open!.")
        sys.exit(0)

    # initialisations of threads
    while 1:
        ret, image = cam.read()
        (H, W) = image.shape[:2]
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        boxes = []
        confidences = []
        classIDs = []
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > 0.1 and classID == 0:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
        ind = []
        for i in range(0, len(classIDs)):
            if (classIDs[i] == 0):
                ind.append(i)
        a = []
        b = []

        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                a.append(x)
                b.append(y)

        distance = []
        nsd = []
        for i in range(0, len(a) - 1):
            for k in range(1, len(a)):
                if (k == i):
                    break
                else:
                    x_dist = (a[k] - a[i])
                    y_dist = (b[k] - b[i])
                    d = math.sqrt(x_dist * x_dist + y_dist * y_dist)
                    distance.append(d)
                    if (d <= 100):
                        nsd.append(i)
                        nsd.append(k)
                    nsd = list(dict.fromkeys(nsd))
                    print(nsd)
        color = (0, 0, 255)
        for i in nsd:
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "Alert"
            # playsound('alert.wav')
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.imshow("Social Distancing Detector", image)
            cv2.waitKey(1)
            p = 99
        color = (0, 255, 0)

        if len(idxs) > 0:
            for i in idxs.flatten():
                if (i in nsd):
                    break
                else:
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                    text = 'OK'
                    cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imshow("Social Distancing Detector", image)
        cv2.waitKey(1)

    cam.release()
    cv.destroyAllWindows()
