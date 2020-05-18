import numpy as np
import cv2
FONT = cv2.FONT_HERSHEY_PLAIN
COLOR = (225, 225, 225)

def frame_buffer(feed):
    #passes data for processing in object detection, helps to have explicit calling function, delays can be adjusted
    detection_output = object_detection(feed)
    print("Data parsed to DNN")
    # time.sleep(0.0100)
    return detection_output

def object_detection(frames):
    # Load Yolo
    net = cv2.dnn.readNet("yolov3_tiny_last.weights", "yolov3_tiny.cfg")
    classes = ["Rover"]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    # img = cv2.imread(frames)
    # img = cv2.resize(img, None, fx=0.4, fy=0.4)
    img = frames
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

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
                printer_confidence = confidence
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    state = 0
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(img, (x, y), (x + w, y + h), COLOR, 2)
            cv2.putText(img, label, (x, y + 30), FONT, 2, COLOR, 2)
            cv2.putText(img, label + " "+str(round(printer_confidence*100, 2)), (x, y+30), FONT, 2, (6, 0, 225), 2)
            if printer_confidence*100 > 80:
                state = 1
                print("Detected #####")
            else:
                state = 0
                print("Failed to detect rovers in frame")
            # cv2.putText(img, "State: "+str(state), (10, 120), FONT, 2, (71, 99, 225), 2)
        cv2.imshow("Image", img)
    cv2.waitKey(100) & 0XFF
#########################

    cv2.destroyAllWindows()
    return img, x, y, w, h, state



    # while cv2.getWindowProperty('img', 0) >= 0:
    #     print("frame destroyed")
    #     # cv2.imshow("Image", img)