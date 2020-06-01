import math

dt = 1/10 #0.1 readings per second
RPY = [0,0,0]                               


def Formatting(inp, maxlength):  #Both inputs are numbers
    #This function checks if a numbers polarity, and outputs a string of maxLength with the correct polarity
    polarity = "-"
    if inp > 0:
        polarity = "+"
        
    tempVal = abs(inp)
    outp = str(tempVal)
    
    #This functions pads zeros to the start of inp till it reaches maxlength
    if len(str(tempVal)) < maxlength:
        for i in range(maxlength - len(str(tempVal))):
            outp = "0" + outp
    
    #THis is all done so that when the package is transmitted, the elements can have uniform string length
    return polarity + outp

def ComplementaryFilter(Accel_data, gyro_data, Mag_data, RPYaw):
    #Integrating the gyro data
    RPYaw[0] += gyro_data[0]*dt
    RPYaw[1] -= gyro_data[1]*dt
    
    rollXL = math.degrees(math.atan2(Accel_data[1], Accel_data[2]))
    pitchXL = math.degrees(math.atan2(-1*Accel_data[0], math.sqrt(Accel_data[1]**2+Accel_data[2]**2)))

    #Getting the yaw angle from the Magnetometer
    MagYaw = math.degrees(math.atan2(-1*(Mag_data[1]), (Mag_data[0])))
   
    ratio = 0.50    #The percentage of Gyro data vs Accelerometer data
    RPYaw[0] = RPYaw[0]*ratio + rollXL*(1-ratio)    #applying a low pass filter to the accelerometer, and a high pass filter to the gyroscope
    RPYaw[1] = RPYaw[1]*ratio + pitchXL*(1-ratio)   
    #Calculating the Yaw from the Magnetometer data (this is noisy but accurate)
    RPYaw[2] = MagYaw
    
    RPY[0]= RPYaw[0] #Roll
    RPY[1] = RPYaw[1] #Pitch
    RPY[2] = RPYaw[2] #Yaw
    
    return RPY

