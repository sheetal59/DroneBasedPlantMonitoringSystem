import cv2
import numpy as np
from deep_sort import DeepSort
from yolov4 import Detector

# Initialize YOLOv4
yolo = Detector(gpu=True, config_path="cfg/yolov4.cfg", weights_path="yolov4.weights", labels_path="data/coco.names")

# Initialize DeepSORT
deep_sort = DeepSort()

# Video stream or image directory
video = cv2.VideoCapture("drone_footage.mp4")

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Object Detection
    detections = yolo.detect(frame)
    bbox_xywh = []
    confs = []
    for detection in detections:
        x, y, w, h = detection['box']
        bbox_xywh.append([x, y, w, h])
        confs.append(detection['confidence'])

    bbox_xywh = np.array(bbox_xywh)
    confs = np.array(confs)

    # Object Tracking
    outputs = deep_sort.update(bbox_xywh, confs, frame)

    # Draw results
    for output in outputs:
        x, y, w, h, obj_id = output
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f"ID {obj_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
