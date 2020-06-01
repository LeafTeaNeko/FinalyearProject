import b0RemoteApi
import math

with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient','b0RemoteApi',60) as client:    

    def data_callback(msg):
        print(msg)
        if type(msg[1])==bytes:
            msg[1]=msg[1].decode('ascii') # python2/python3 differences

    client.simxCallScriptFunction('getData@GyroSensor','sim.scripttype_childscript',None,client.simxDefaultSubscriber(data_callback));

    client.simxStartSimulation(client.simxServiceCall())

    while True:
        client.simxSpinOnce()
    client.simxStopSimulation(client.simxServiceCall())