#py 3.7 and Spyder 4.1.2
# import math
import time
import numpy as np
import sim as vrep
import cv2
from framebyframe import frame_buffer
from ATF import alphatrimmer
from support import info_frame, kalman_filter2, PtC
from CF import ComplementaryFilter
# from KF import kalman_filter2

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
frame_id = 0
FONT = cv2.FONT_HERSHEY_PLAIN
RPY = [0,0,0]                               

ERRORCODE, Lidar = vrep.simxGetObjectHandle(clientID, 'laser_sensor#2', vrep.simx_opmode_blocking)
#using absoulte position of the rover as a stand in for Magnetometer
ERRORCODE, Magref = vrep.simxGetObjectHandle(clientID,'rover#2',vrep.simx_opmode_blocking)
res, v1 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor0#2', vrep.simx_opmode_oneshot_wait)
ERRORCODE, Rover3 = vrep.simxGetObjectHandle(clientID, 'rover#3', vrep.simx_opmode_blocking)



if clientID != -1:
    starting_time = time.time()
    ERRORCODE, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
    ERRORCODE, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, Lidar, vrep.simx_opmode_streaming)
    ERRORCODE, eulerAngles=vrep.simxGetObjectOrientation( clientID, Magref, -1, vrep.simx_opmode_streaming)
    ERRORCODE, gyro_out = vrep.simxGetStringSignal(clientID, "myGyroData#2", vrep.simx_opmode_streaming)
    ERRORCODE, accel_out = vrep.simxGetStringSignal(clientID, "myaccData#2", vrep.simx_opmode_streaming)
    ERRORCODE, position = vrep.simxGetObjectPosition( clientID, Magref, -1, vrep.simx_opmode_streaming)
    ERRORCODE, position2 = vrep.simxGetObjectPosition( clientID, Rover3, -1, vrep.simx_opmode_streaming)




    while vrep.simxGetConnectionId(clientID) != -1:
        ERRORCODE, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
        ERRORCODE, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, Lidar, vrep.simx_opmode_buffer)
        # ERRORCODE, gyro_data = vrep.simxGetFloatSignal(clientID, gyroRef, vrep.simx_opmode_buffer)
        ERRORCODE, eulerAngles=vrep.simxGetObjectOrientation( clientID, Magref, -1, vrep.simx_opmode_buffer)        
        ERRORCODE, gyro_out = vrep.simxGetStringSignal( clientID, "myGyroData#2", vrep.simx_opmode_buffer)
        ERRORCODE, accel_out = vrep.simxGetStringSignal( clientID, "myaccData#2", vrep.simx_opmode_buffer)
        ERRORCODE, position = vrep.simxGetObjectPosition( clientID, Magref, -1, vrep.simx_opmode_buffer)
        ERRORCODE, position2 = vrep.simxGetObjectPosition( clientID, Rover3, -1, vrep.simx_opmode_buffer)

        norm_distance = np.linalg.norm(detectedPoint_lidar)
        filtered_data = alphatrimmer(7, 2, str(norm_distance))
        frame_id += 1

        if ERRORCODE == vrep.simx_return_ok:
            img = np.array(image, dtype=np.uint8)
            img.resize([resolution[1], resolution[0], 3])
            vision_sensor_output = cv2.rotate(img, cv2.ROTATE_180)
            try:
                parsing_data = frame_buffer(vision_sensor_output)
                elapsed_time = time.time() - starting_time
                fps = frame_id / elapsed_time
                floatValues1 = vrep.simxUnpackFloats( gyro_out)
                floatValues2 = vrep.simxUnpackFloats( accel_out)
                CF_out = ComplementaryFilter(floatValues2, floatValues1, eulerAngles, RPY)

                # KF_Out = kalman_filter2(filtered_data, 0, 0, 0) 
                KF_Out = 0
                display_frame = info_frame(parsing_data, filtered_data, fps, KF_Out, CF_out[2], position, position2)
                print(CF_out[2])
                print(position2)
                # print(str(round(position+info_frame[1],2))+","+str(round(position+info_frame[2],2)))
                cv2.imshow("Image", display_frame)
                print("Detection successful")

                # print("Rover spotted at: "+ str(dist_x) +","+ str(dist_y))
                cv2.waitKey(100)
    
            except:
                cv2.imshow("Image", vision_sensor_output)

        elif ERRORCODE == vrep.simx_return_novalue_flag:
            pass
        else:
            print(ERRORCODE)
else:
    vrep.simxFinish(clientID)
cv2.destroyAllWindows()





# cv2.imshow("Image", parsing_data)
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     break