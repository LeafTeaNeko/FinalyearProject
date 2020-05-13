import cv2
import numpy as np
font = cv2.FONT_HERSHEY_PLAIN

def frame_buffer(feed):
    detection_output = object_detection(feed)
    print("Data parsed to DNN")
    # time.sleep(0.0100)
    return detection_output

def object_detection(frames):
    # Load Yolo
    net = cv2.dnn.readNet( "yolov3_tiny_last.weights", "yolov3_tiny.cfg")
    classes = ["Rover"]
    
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    
    # Loading frames
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
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,69,225), 2)
            cv2.putText(img, label, (x, y + 30),  font, 2, (225,225,225), 2)
            cv2.putText(img, label + " " + str(round(printer_confidence*100, 2)), (x, y + 30), font, 2, (6,0,225), 2)
            # if confidence>0.5:
            #     state = 1
            # else:
            #     state = 0
            # cv2.putText(img, "State: " + str(state), (10, 30), font, 2, (71,99,225), 2)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1000) & 0XFF

    cv2.destroyAllWindows()
    return img
