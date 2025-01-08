# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 12:50:49 2023

@author: Jonas Beachy, University of Washington
"""


import egm_pb2 as egm
import socket

#computer_ip = '192.168.125.50' or whatever IP address is #For use on physical controller (need static IP on a local network)
computer_ip= "127.0.0.1" #For simulation in robotstudio
robot_port=6510
num=0

#Sets up a client to receive UDP messages
robot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Binds the client to listen on your IP and port (same as specified in Controller-Configuration-
robot_socket.bind((computer_ip, robot_port))


def CreateSensorMessage(egmSensor, pos, quat):
    headerOne=egmSensor.header
    headerOne.seqno=num
    headerOne.mtype=egm.EgmHeader.MessageType.MSGTYPE_CORRECTION
    
    #to change the position and/or orientation of the robot, change values of input vectors
    planned=egmSensor.planned
    pose=planned.cartesian
    Position=pose.pos
    Quaternion=pose.orient
    Position.x=pos[0]
    Position.y=pos[1]
    Position.z=pos[2]
    
    Quaternion.u0=quat[0]
    Quaternion.u1=quat[1]
    Quaternion.u2=quat[2]
    Quaternion.u3=quat[3]
    
    return egmSensor



def CreateSensorPathCorr(egmPathCorr, pos):   
    
    #Create a header
    hdr = egmPathCorr.header
    hdr.seqno = num
    #hdr.Tm = (uint)DateTime.Now.Ticks;
    hdr.mtype = egm.EgmHeader.MessageType.MSGTYPE_PATH_CORRECTION
   
    #create some sensor data for EGMPathCorr
    Corr = egmPathCorr.pathCorr
    pc = Corr.pos
    pc.x = pos[0]
    pc.y  = pos[1]
    pc.z  = pos[2]

    Corr.age=1
    
    return egmPathCorr


print(f"Listening on {computer_ip}:{robot_port}")

while True:
    data, addr = robot_socket.recvfrom(1024)  # Buffer size is 1024 bytes
    
    print(f"Received message from {addr}")

    #Reads-in and deserializes the protocol buffer message from controller
    message=egm.EgmRobot()
    message.ParseFromString(data)
    
    #print(message)
    
    Seq=message.header.seqno
    Time=message.header.tm
    CurX=message.feedBack.cartesian.pos.x
    CurY=message.feedBack.cartesian.pos.y
    CurZ=message.feedBack.cartesian.pos.z
    
    print(f"SeqNum={Seq}, Time={Time}, X={CurX}, Y={CurY}, Z={CurZ}")
    
    ####Setup for message back to Robot Controller (see readme and EGM manual for specifics)####
    
    # #To create Position Guidance message
    Pos=[100,100,300] #[x,y,z] chords
    Quat=[1,0,0,0] #[q0,q1,q2,q3] quaternion
    egmSensor=egm.EgmSensor()
    egmSensor=CreateSensorMessage(egmSensor,Pos,Quat)
    
    # #To create Path Correction message 
    # Pos=[0,0,20] # y,z adjustments off of the planned path
    # egmPathCorr=egm.EgmSensorPathCorr()
    # egmPathCorr=CreateSensorPathCorr(egmPathCorr,Pos)
    
    # #To Serialize with protocol buffer and transmit message to Controller (either message type)
    mess=egmSensor.SerializeToString()
    # mess=egmPathCorr.SerializeToString()
    
    robot_socket.sendto(mess, addr)
    
    num+=1
