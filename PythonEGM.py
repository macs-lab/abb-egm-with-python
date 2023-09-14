# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 12:50:49 2023

@author: Jonas Beachy, University of Washington
"""


import egm_pb2 as egm
import socket

#computer_ip = '192.168.125.50' #For use on physical controller (need static IP on a local network)
computer_ip= "127.0.0.1" #For simulation in robotstudio
robot_port=6510
num=0

#Sets up a client to recieve UDP messages
robot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Binds the client to listen on your IP and port (same as specified in Controller-Configuration-
robot_socket.bind((computer_ip, robot_port))


def CreateSensorMessage(egmSensor):
    headerOne=egmSensor.header
    headerOne.seqno=num
    headerOne.mtype=egm.EgmHeader.MessageType.MSGTYPE_CORRECTION
    
    
    
    #to change pos and orientation of robot, change values below
    planned=egmSensor.planned
    pose=planned.cartesian
    pos=pose.pos
    quat=pose.orient
    pos.x=100.0
    pos.y=0.0
    pos.z=300.0
    
    quat.u0=1.0
    quat.u1=0.0
    quat.u2=0.0 
    quat.u3=0.0
    
    return egmSensor



def CreateSensorPathCorr(egmPathCorr):   
    
    #Create a header
    hdr = egmPathCorr.header
    hdr.seqno = num
    #hdr.Tm = (uint)DateTime.Now.Ticks;
    hdr.mtype = egm.EgmHeader.MessageType.MSGTYPE_PATH_CORRECTION
   
    #create some sensor data for EGMPathCorr
    Corr = egmPathCorr.pathCorr
    pc = Corr.pos

    
    pc.x = 0;
    pc.y  = 0;
    pc.z  = 10;

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
    # egmSensor=egm.EgmSensor()
    # egmSensor=CreateSensorMessage(egmSensor)
    
    # #To create Path Correction message 
    # egmPathCorr=egm.EgmSensorPathCorr()
    # egmPathCorr=CreateSensorPathCorr(egmPathCorr)
    
    

    #To Serialize with protocol buffer and transmit message to Controller (either message type)
    # mess=egmPathCorr.SerializeToString()
    # robot_socket.sendto(mess, addr)
    
    num+=1
