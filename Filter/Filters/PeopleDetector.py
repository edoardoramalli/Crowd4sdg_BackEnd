from Filter.Filters.Filter import Filter
import cv2
import numpy as np
import os
from django.conf import settings


class PeopleDetector(Filter):

    def __init__(self):
        Filter.__init__(self)
        self.name = "yolo"
        self.net = cv2.dnn.readNet(model=os.path.join(settings.BASE_DIR, "Files/FilterModels/yolov3.weights"),
                                   config=os.path.join(settings.BASE_DIR, "Files/FilterModels/yolov3.cfg"))
        self.classes = []
        with open(os.path.join(settings.BASE_DIR, "Files/FilterModels/coco.names")) as f:
            self.classes = [line.strip() for line in f.readlines()]
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.min_people = 1

        self.detailed_output = False

    def classify(self, pil_image):
        # Loading image
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        people = 0
        if img is not None:
            img = cv2.resize(img, None, fx=0.4, fy=0.4)
            height, width, channels = img.shape

            # Detecting objects
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            people_confidences = []     # to be sorted
            
            # TODO confidence of the second (min people) highest (at least two (min people) people)

            for i in range(len(boxes)):
                if i in indexes:
                    label = str(self.classes[class_ids[i]])
                    if label == 'person':
                        people += 1
                        people_confidences.append(confidences[i])
                        if people >= self.min_people and not self.detailed_output:
                            return True, np.prod(people_confidences), people

        return people >= self.min_people, 1, people