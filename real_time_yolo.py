import cv2
import numpy as np
import time

def object_detection(feed):    
    
    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0
    
    # Load Yolo
    # path_loader = "C:\Users\PLasterbrain\Desktop\py-vrep\yolov3_tiny_last.weights"
    # cfg_loader = "C:\Users\PLasterbrain\Desktop\py-vrep\yolov3_tiny.cfg"    
    net = cv2.dnn.readNet( "yolov3_tiny_last.weights", "yolov3_tiny.cfg")
    classes = ['Rover']
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    
    # Loading image
    cap = cv2.VideoCapture(feed)
    # cap = feed

    while True:
        _, frame = cap.read()
        frame_id += 1
        height, width, channels = frame.shape
    
        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    
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
                    # Object Coordinates
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
    
                    # Bounding Box Coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
    
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)
    
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                #label = str(classes[i])  
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, label + " " + str(round(confidence*100, 2)), (x, y + 30), font, 3, (6,0,225), 2)
                if confidence>0.7:
                    state = 1
                else:
                    state = 0
                cv2.putText(frame, "State: " + str(state), (10, 30), font, 2, (71,99,225), 2)
    
    
        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 80), font, 2, (255,69,0), 2)
        
        cv2.imshow("Image", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    
    cap.release()
    
    cv2.destroyAllWindows()
    print("video destroyed")
    
    return None

object_detection("Bideo.avi")