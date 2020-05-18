import cv2
import numpy as np
import math
import threading as thread
import psutil
import sys
from UserWrittenModules import MultiprocessingFunctions as multi
from random import *
print("[INFO] |WANG REDA CAN ABLE TO MONITER SOCIAL DISTANCING.")
yelling = ["Hey, please maintain little distance between each other",
           "Guys, maintain some distance, be consious about it",
           "This is very bad!, i do not expect you to violate the social distancing",
           "If you violate the social distancing!, i will click your pictures and report it.",
           "Man!, understand the necessity of social distancing, you should maintain some distance",
           "You, You only. please, unserstand, the necessity of social distancing.",
           "You will not stop violating distancing rule until i report about your action to my master",
           "Do you even aware about what you are trying to commit, please, we robots know about your social distancing, but you dont",
           "Bad, Very bad, i should definetly report about your activity to my master!. i may have to do it, if you dont move away from each other",
           "We robots run on Linux, we are not just safe from corona, but from all!. its you who need to understand this"
           ]
yell = thread.Thread(target=multi.MakeAwareness, args=(str(yelling[randint(0, 9)]),))
labelsPath = "./Assets/YOLO/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

np.random.seed(42)

weightsPath = "./Assets/YOLO/yolov3.weights"
configPath = "./Assets/YOLO/yolov3.cfg"

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
name = net.getLayerNames()
out = net.getUnconnectedOutLayers()
outputlayernames = [name[i[0] - 1] for i in out]




# Social Distance Tracking on a video footage
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, img = cap.read()
    if ret == False:
        continue

    # Object Detection
    (H, W) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    output = net.forward(outputlayernames)
    boxes, confidences, class_ids = [], [], []
    height, width, shape = img.shape

    for m in output:
        for detection in m:
            scores = detection[5:]
            class_ids = np.argmax(scores)
            confidence = scores[class_ids]
            if confidence > 0.6 and class_ids == 0:
                #print(detection[0:4])
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))

    # Boxes around the objects
    ind = []
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.5)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            ind.append([x, y, w, h])

    # Alert for not maintaining social distance
    red_boxes = []
    for j in range(len(ind)):
        for k in range(len(ind)):
            if k == j:
                break
            else:
                x1, y1 = ind[j][:2]
                x2, y2 = ind[k][:2]
                dist = np.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                if dist <= 130:
                    red_boxes.append(ind[j])
                    red_boxes.append(ind[k])
    flagging = False
    for r in red_boxes:
        A, B, C, D = r
        if not flagging:
            if not yell.is_alive():
                yell = thread.Thread(target=multi.MakeAwareness, args=(str(yelling[randint(0, 9)]),))
                yell.start()
            flagging = True
        cv2.putText(img, "ALERT! Physical distancing is violated", (int(A), int(B) - 5), cv2.FONT_HERSHEY_PLAIN, 0.5, [0, 0, 255], 1)
        cv2.rectangle(img, (A, B), (A + C, B + D), [0, 0, 255], 2)
    cv2.imshow('Eye of Wang Reda | Team Wuhan Hunter Squad', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()


