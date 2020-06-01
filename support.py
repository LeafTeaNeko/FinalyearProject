# import numpy as np
import math
import cv2
import socket
import sim as vrep
FONT = cv2.FONT_HERSHEY_PLAIN

object_data = []
rover_data = []

def get_quadrant(gyrodata):
    rotation =  gyrodata
    quadrant = math.pi*rotation
    return quadrant

# def OAR(Lidar, state, quadrant):
#     if Lidar<400 & state==1:
#         object_data.append(quadrant, Lidar)
#     return None

# def Aggregator_Gyro(clientID, Gyro1, Gyro2, Gyro3, Gyro4, Gyro5, mode):
#     ERRORCODE, gyro1 = vrep.simxGetStringSignal(clientID, "myGyroData#1", mode)
#     ERRORCODE, gyro2 = vrep.simxGetStringSignal(clientID, "myGyroData#2", mode)
#     ERRORCODE, gyro3 = vrep.simxGetStringSignal(clientID, "myGyroData#3", mode)
#     ERRORCODE, gyro4 = vrep.simxGetStringSignal(clientID, "myGyroData#4", mode)
#     ERRORCODE, gyro5 = vrep.simxGetStringSignal(clientID, "myGyroData#5", mode)
#     return gyro1, gyro2, gyro3, gyro4, gyro5

# def Aggregator_Accel(clientID, Accel1, Accel2, Accel3, Accel4, Accel5, mode):
#     ERRORCODE, Accel1 = vrep.simxGetStringSignal(clientID, "myaccData#1", mode)
#     ERRORCODE, Accel2 = vrep.simxGetStringSignal(clientID, "myaccData#2", mode)
#     ERRORCODE, Accel3 = vrep.simxGetStringSignal(clientID, "myaccData#3", mode)
#     ERRORCODE, Accel4 = vrep.simxGetStringSignal(clientID, "myaccData#4", mode)
#     ERRORCODE, Accel5 = vrep.simxGetStringSignal(clientID, "myaccData#5", mode)
#     return Accel1, Accel2, Accel3, Accel4, Accel5

# def Aggregator_Mag(clientID, Mag1, Mag2, Mag3, Mag4, Mag5, mode):
#     ERRORCODE, Mag1 = vrep.simxGetStringSignal(clientID, "Magref1", mode)
#     ERRORCODE, Mag2 = vrep.simxGetStringSignal(clientID, "Magref2", mode)
#     ERRORCODE, Mag3 = vrep.simxGetStringSignal(clientID, "Magref3", mode)
#     ERRORCODE, Mag4 = vrep.simxGetStringSignal(clientID, "Magref4", mode)
#     ERRORCODE, Mag5 = vrep.simxGetStringSignal(clientID, "Magref5", mode)
#     return Mag1, Mag2, Mag3, Mag4, Mag5

# def Aggregator_VS(clientID, VS1, VS2, VS3, VS4, VS5, mode):
#     ERRORCODE, resolution, VS1_image = vrep.simxGetVisionSensorImage(clientID, v1, 0, mode)
#     ERRORCODE, resolution, VS2_image = vrep.simxGetVisionSensorImage(clientID, v2, 0, mode)
#     ERRORCODE, resolution, VS3_image = vrep.simxGetVisionSensorImage(clientID, v3, 0, mode)
#     ERRORCODE, resolution, VS4_image = vrep.simxGetVisionSensorImage(clientID, v4, 0, mode)
#     ERRORCODE, resolution, VS5_image = vrep.simxGetVisionSensorImage(clientID, v5, 0, mode)

#     return VS1_image, VS2_image, VS3_image, VS4_image, VS5_image

# def Aggregator_Lidar(clientID, L1, L2, L3, L4, L5, mode):
#     ERRORCODE, detectionState, detectedPoint_lidar1, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, L1, mode)
#     ERRORCODE, detectionState, detectedPoint_lidar2, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, L2, mode)
#     ERRORCODE, detectionState, detectedPoint_lidar3, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, L3, mode)
#     ERRORCODE, detectionState, detectedPoint_lidar4, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, L4, mode)
#     ERRORCODE, detectionState, detectedPoint_lidar5, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, L5, mode)    
#     return L1, L2, L3, L4, L5

def PtC(Distance, Angle):
    x = Distance*math.cos(Angle)
    y = Distance*math.sin(Angle)
    return x,y


def info_frame(parsing_data, filtered_data, fps, KF_out, CF_out, Selfref, pos):
    Camera_based_distance = round((1/2*(math.tan(0.52)*parsing_data[4]))*10, 2)
    cv2.putText(parsing_data[0], "VS_Dist: " + str(Camera_based_distance), (10, 30), FONT, 2, (71,99,225), 2)
    KF_output = next(filtered_data)
    # print(KF_output)
    cv2.putText(parsing_data[0], "LS_Dist: " + str(KF_output*100), (10, 60), FONT, 2, (71,99,225), 2)
    cv2.putText(parsing_data[0], "FPS: " + str(round(fps, 2)), (10, 150), FONT, 2, (255,69,0), 2)
    cv2.putText(parsing_data[0], "State: "+str(parsing_data[5]), (10, 120), FONT, 2, (71, 99, 225), 2)
    if parsing_data[5]==1:
        dist_x, dist_y = PtC( KF_output,CF_out)
        cv2.putText(parsing_data[0], "Local Coordinates: "+str(round(dist_x,2))+","+str(round(dist_y,2)), (10, 180), FONT, 2, (71, 99, 225), 2)
        cv2.putText(parsing_data[0], "Global Coordinates: "+str(round(Selfref[0]+dist_x,2))+","+str(round(Selfref[1]+dist_y,2)), (10, 210), FONT, 2, (71, 99, 225), 2)
        cv2.putText(parsing_data[0], "Global Coordinates: "+str(round(pos[0],2))+","+str(round(pos[1],2)), (10, 240), FONT, 2, (71, 99, 225), 2)

        

    # cv2.putText(parsing_data[0], "KF_Dist: "+str((KF_output*1.005)+0.01), (10, 90), FONT, 2, (71, 99, 225), 2)
    return parsing_data[0], dist_x, dist_y

def tcp_tx(payload):
    TCP_IP = 'localhost'   
    TCP_PORT = 50007            
    # BUFFER_SIZE = 32            
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connection address: ', addr)  
    while 1:
        data = conn.recv(1024)
        if not data: break
        conn.sendall(payload.encode('utf-8'))
    conn.close() 
    return None

def kalman_filter2(data, x, y, z):
    Output = data
    return Output

# def roverID(frame,color):
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
#     lower_red = np.array([110,50,50]) 
#     upper_red = np.array([130,255,255])
#     if cv2.inRange(hsv, lower_red, upper_red)
#     return None