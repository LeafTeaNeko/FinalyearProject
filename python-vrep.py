#py 3.7 and Spyder 4.1.2
import math
import time
import numpy as np
import sim as vrep
import cv2
from framebyframe import frame_buffer
from ATF import alphatrimmer
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
frame_id = 0
FONT = cv2.FONT_HERSHEY_PLAIN

returnCode,Lidar = vrep.simxGetObjectHandle( clientID, 'Lidar', vrep.simx_opmode_blocking)
#Errorcode,Sonar = vrep.simxGetObjectHandle( clientID, 'sonar', vrep.simx_opmode_blocking)

if clientID!= -1:
    starting_time = time.time()
    res, v1 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    returnCode, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
    #returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, Sonar, vrep.simx_opmode_streaming)
    returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, Lidar, vrep.simx_opmode_streaming)
    while vrep.simxGetConnectionId(clientID) != -1:
        returnCode, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
        #returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, Sonar, vrep.simx_opmode_buffer)
        returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, Lidar, vrep.simx_opmode_buffer)
        norm_distance = np.linalg.norm(detectedPoint_lidar)
        filtered_data = alphatrimmer( 7, 2, str(norm_distance))
        frame_id += 1
        if returnCode == vrep.simx_return_ok:
            img = np.array( image, dtype=np.uint8)
            img.resize( [resolution[1], resolution[0], 3])
            vision_sensor_output = cv2.rotate(img, cv2.ROTATE_180)    
            try:
                parsing_data = frame_buffer(vision_sensor_output)
                # Camera_based_distance = ((known_width*FOV)/parsing_data[3])/2
                Camera_based_distance = round((1/2*(math.tan(0.52)*parsing_data[4]))*10, 2)
                cv2.putText(parsing_data[0], "VS_Dist: " + str(Camera_based_distance), (10, 30), FONT, 2, (71,99,225), 2)
                cv2.putText(parsing_data[0], "LS_Dist: " + str(next(filtered_data)), (10, 60), FONT, 2, (71,99,225), 2) 
                elapsed_time = time.time() - starting_time
                fps = frame_id / elapsed_time
                cv2.putText(parsing_data[0], "FPS: " + str(round(fps, 2)), (10, 90), FONT, 2, (255,69,0), 2)
                cv2.putText(parsing_data[0], "State: "+str(parsing_data[5]), (10, 120), FONT, 2, (71, 99, 225), 2)

                cv2.imshow("Image", parsing_data[0])
                cv2.waitKey(100)
                print("Detection successful")
            
            except:
                cv2.imshow("Image", vision_sensor_output)                        

        elif returnCode == vrep.simx_return_novalue_flag:
            pass
        else:
            print (returnCode)
else:
    vrep.simxFinish(clientID)
cv2.destroyAllWindows()




###############################################################################################################
            # elapsed_time = time.time() - starting_time
            # fps = frame_id / elapsed_time
            # cv2.putText(vision_sensor_output, "FPS: " + str(round(fps, 2)), (10, 80), FONT, 2, (255,69,0), 2)
            # cv2.imshow("Image", parsing_data)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break