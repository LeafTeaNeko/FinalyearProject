# import sim as vrep
# import numpy as np
# import matplotlib.pyplot as plt

# vrep.simxFinish(-1)

# clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

# if clientID!=-1:
#     print("connected to Vrep Remote API")
# else:
#     print("Could not connect to VREP") 

# Errorcode,Lidar = vrep.simxGetObjectHandle( clientID, 'Lidar', vrep.simx_opmode_blocking)
# Errorcode,Sonar = vrep.simxGetObjectHandle( clientID, 'sonar', vrep.simx_opmode_blocking)
# Errorcode,camera = vrep.simxGetObjectHandle( clientID, 'Vision_sensor', vrep.simx_opmode_blocking)

# Errorcode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Lidar,vrep.simx_opmode_streaming)
# ErrorCode, resolution, image = vrep.simxGetVisionSensorImage(clientID, camera, 0, vrep.simx_opmode_streaming)

# returnCode, detectionState, detectedPoint_sonar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Sonar,vrep.simx_opmode_buffer);
# returnCode, detectionState, detectedPoint_lidar, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID,Lidar,vrep.simx_opmode_buffer);
# [returnCode, resolution, image]=vrep.simxGetVisionSensorImage( clientID, camera, 0, vrep.simx_opmode_buffer);
# im = np.array(image, dtype=np.uint8);
# im.resize([resolution[0],resolution[1],3]);
# plt.imshow(im,origin='lower')

# vrep.simxFinish(clientID);
#================================================================================================================================
# import sim as vrep
# import numpy as np
# import matplotlib.pyplot as plt

# vrep.simxFinish(-1)

# clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

# if clientID!=-1:
#     res, v1 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_blocking)
#     err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
#     # while (vrep.simxGetConnectionId(clientID) != -1):
#     err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
#     #     if err == vrep.simx_return_ok:
#     img = np.array(image,dtype=np.uint8)
#     img.resize([resolution[1],resolution[0],3])
#     plt.imshow(img)
#     #         #cv2.imshow('image',img)
#     #     elif err == vrep.simx_return_novalue_flag:
#     #         pass
#     #     else:
#     #       print (err)
# else:
#   vrep.simxFinish(clientID)

# #cv2.destroyAllWindows()

#================================================================================================================================


import sim as vrep
import time
import cv2
import numpy as np

vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID!=-1:
    res, v1 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
    while (vrep.simxGetConnectionId(clientID) != -1):
        err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        if err == vrep.simx_return_ok:
            img = np.array(image,dtype=np.uint8)
            img.resize([resolution[1],resolution[0],3])
            output = cv2.rotate(img, cv2.ROTATE_180)
            cv2.imshow('image',output)
            out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1024,512))
            out.write(output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        elif err == vrep.simx_return_novalue_flag:
            pass
        else:
          print (err)
else:
  vrep.simxFinish(clientID)

cv2.destroyAllWindows()