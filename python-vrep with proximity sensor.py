
#py 3.7.6 and Spyder 4.1.2

import sim as vrep
import cv2
import numpy as np
from ATF import alphatrimmer

vrep.simxFinish(-1)

# font 
font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
org = (50, 50) 
  
# fontScale 
fontScale = 1
   
# Blue color in BGR 
color = (255, 0, 0) 
  
# Line thickness of 2 px 
thickness = 2
   

clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

returnCode,Lidar = vrep.simxGetObjectHandle( clientID, 'Lidar', vrep.simx_opmode_blocking)
returnCode,Sonar = vrep.simxGetObjectHandle( clientID, 'sonar', vrep.simx_opmode_blocking)

if clientID!=-1:
    res, v1 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    returnCode, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
    returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Sonar,vrep.simx_opmode_streaming);
    returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Lidar,vrep.simx_opmode_streaming);
    while (vrep.simxGetConnectionId(clientID) != -1):
        returnCode, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
        returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Sonar,vrep.simx_opmode_buffer);
        returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Lidar,vrep.simx_opmode_buffer);
        norm_distance = np.linalg.norm(detectedPoint_lidar)

        filtered_data = alphatrimmer(7,2,str(norm_distance))
        
            
        if returnCode == vrep.simx_return_ok:
            img = np.array(image,dtype=np.uint8)
            img.resize([resolution[1],resolution[0],3])
            output = cv2.rotate(img, cv2.ROTATE_180)
            out = cv2.VideoWriter('output.avi', -1, 20.0, (1024,512))
            cv2.imshow('img',output)
            output_filter = next(filtered_data)
            # cv2.putText(image, str(filtered_data), org, font,  fontScale, color, thickness, cv2.LINE_AA)
            print(output_filter*100)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        elif returnCode == vrep.simx_return_novalue_flag:
            pass
        else:                 
          print (returnCode)
else:
  vrep.simxFinish(clientID)
cv2.destroyAllWindows()

