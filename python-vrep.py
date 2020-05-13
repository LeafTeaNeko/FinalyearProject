
#py 3.7 and Spyder 4.1.2

import sim as vrep
import cv2
import numpy as np
from framebyframe import frame_buffer
# from real_time_yolo import object_detection
import time


vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
frame_id = 0
font = cv2.FONT_HERSHEY_PLAIN

#Errorcode,Lidar = vrep.simxGetObjectHandle( clientID, 'Lidar', vrep.simx_opmode_blocking)
#Errorcode,Sonar = vrep.simxGetObjectHandle( clientID, 'sonar', vrep.simx_opmode_blocking)

if clientID!=-1:
    starting_time = time.time()
    res, v1 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    returnCode, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
    #returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Sonar,vrep.simx_opmode_streaming);
    #returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Lidar,vrep.simx_opmode_streaming);
    while (vrep.simxGetConnectionId(clientID) != -1):
        returnCode, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
        #returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Sonar,vrep.simx_opmode_buffer);
        #returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Lidar,vrep.simx_opmode_buffer);
        frame_id += 1

        if returnCode == vrep.simx_return_ok:
            img = np.array(image,dtype=np.uint8)
            img.resize([resolution[1],resolution[0],3])
            vision_sensor_output = cv2.rotate(img, cv2.ROTATE_180)
            
            
            # print(type(vision_sensor_output))
            # object_vision_sensor_output = object_detection(vision_sensor_output)
            
            try:
                parsing_data = frame_buffer(vision_sensor_output)
                # parsing_data = real_time_yolo(vision_sensor_output)
                # time.sleep(0.1)
                cv2.imshow("Image", vision_sensor_output)
                cv2.waitKey(100)
                print("Detection successful")
            
            except:
                cv2.imshow("Image", vision_sensor_output)
            
            
            # elapsed_time = time.time() - starting_time
            # fps = frame_id / elapsed_time
            # cv2.putText(vision_sensor_output, "FPS: " + str(round(fps, 2)), (10, 80), font, 2, (255,69,0), 2)
            # cv2.imshow("Image", parsing_data)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        
        elif returnCode == vrep.simx_return_novalue_flag:
            pass
        else:
          print (returnCode)
else:
  vrep.simxFinish(clientID)

cv2.destroyAllWindows()