
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:12:25 2020
@author: Abdul
"""

import numpy as np 
Count = 0

D_t = 1#Time interval, assuming 1 sec for now
accx = 0 #from rover unit
accy = 0 # from rover unit

A = np.array([[1 ,0, D_t, 0], [0, 1, 0, D_t], [0, 0, 1, 0], [0, 0, 0, 1]])
X_previous = np.array([[4260],[0], [282], [0]])
B = np.array([[0.5*(D_t^2), 0], [0, 0.5*(D_t^2)], [D_t, 0], [0, D_t]])
U_K = np.array([[accx],[accy]])
W_K = np.zeros((4,4))
Q = np.array([[0.5*(D_t^2), 0.5*(D_t^2), D_t, D_t]])
#Q = np.identity(4)
Q_K = Q.transpose()
#R = np.array([[2, 0, 0, 0], [0, 2, 0, 0], ]) # Elements are arbitrary
flag = True

def Predicted_State(X_previous,A, B, U_K, W_K):
    X_Predicted =  A.dot(X_previous)+ B.dot(U_K)+ W_K
    return X_Predicted

def Process_Covariance(Q_K, A):
    error_posx = 5#insert theoritical error in position, X direction
    error_posy = 0#insert theoritical error in position, Y direction
    error_velx = 5#insert theoritical error in velocity, X direction
    error_vely = 0 #insert theoritical error in velocity, Y direction
    P_previous = np.array([[error_posx^2, 0 , 0, 0], [0, error_posy^2, 0, 0], [0, 0, error_velx^2, 0], [0, 0, 0, error_vely^2]])
    P_K = A.dot(P_previous).dot(A.transpose())+ Q_K
    return P_K

def Kalman_Gain(P_K):
    H = np.identity(4)
    H_transpose = H.transpose()
#    K_G = (P_K.dot(H_transpose))./(H.dot(P_K).dot(H_transpose)+ R)
    Per = H.dot(P_K)
    Per = Per.dot(H_transpose)
#    Per = Per + R
    K_G = np.divide(P_K.dot(H_transpose), Per )
    return K_G

def New_Measurements(Y_K):
    C = np.identity(4)
    Z_K = np.zeros(4)
    Y_new = C.dot(Y_K) + Z_K
    return Y_new

def Current_State(X_Predicted, K_G, Y_new):
    H = np.identity(4)
    process = Y_new-H.dot(X_Predicted)
    X_Current = X_Predicted + K_G.dot(process)
    return X_Current # Values of importance

def Update_Covariance(P_K, K_G):
    H = np.identity(4)
    I = np.identity(4)
    New_Covariance = (I - K_G.dot(H)).dot(P_K)
    return New_Covariance

def kalman_filter(New_readings_pos_X, New_readings_pos_Y, New_readings_velx, New_readings_vely):
    Y_K = [New_readings_pos_X, New_readings_pos_Y, New_readings_velx, New_readings_vely]
    # FIRST_VALUES = Predicted_State(X_previous,A, B, U_K, W_K)
    # print("Entered Prediction loop: %f\n", FIRST_VALUES)
    if Count == 0:
        P_K = Process_Covariance(Q_K, A)        
    # print("Entered P_K loop: \n", P_K)
#    Kalman_Gain(Process_Covariance(Q_K, A),R)
    # GAIN_VALUES= Kalman_Gain(Process_Covariance(Q_K, A))
    # print("Entered Kalman_gain loop: \n", GAIN_VALUES)
    # NEW_VALUES = New_Measurements(Y_K)
    # print("Updated new measurements: \n",NEW_VALUES )
    New_Pos = Current_State(Predicted_State(X_previous,A, B, U_K, W_K), Kalman_Gain(P_K), New_Measurements(Y_K))
    # print("New_pos calculated")
    # Updated_covar = Update_Covariance(P_K, Kalman_Gain(P_K))
    # Count = Count + 1
    # if Count>1:
    #     P_K = Updated_covar
    # stored = New_Pos.flatten()
    # print("New Pos: "+ str(stored[1])+","+ str(stored[9]))
    # print(New_readings_pos_X)
    # New_add = np.array([[New_readings_pos_X],[0], [New_readings_velx], [0]])
    return New_Pos

# kalman_filter(New_Measurements_pos, 0, New_Measurements_vel, 0)













