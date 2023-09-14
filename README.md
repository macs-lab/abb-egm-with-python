# abb-egm-with-python
A script that allows for interfacing with ABB's Externally Guided Motion (EGM) option in python


This repo contains the files needed to get EGM communication working with an ABB robot controller. 

The main file is PythonEGM.py. This script sets up a UDP listening client to receive and deserialize the EGM messages from the controller. It also includes examples of assembling and serializing Position Guidance messages and Path Correction messages to sent back to the controller for those applications.


You must include the egm_pb2 file in the PythonEGM.py script. This file contains the necessary information for the protocol buffer to serialize and deserialize messages based on the message structure in the .proto file.
The raw egm.proto(found on ABB controller) file is included. When compiled for use in python language the egm.proto file becomes egm_pb2.py.



Basic knowledge of working with protocol buffers is necessary.
In python, information about adding data to message structure, serializing and sending messages, and parsing serialized messages can be found at: https://protobuf.dev/getting-started/pythontutorial/

Basic knowledge of socket communication is also necessary.
This particular setup uses UDP to continuously send and receive messages. More information about socket communication can be found at: https://docs.python.org/3/library/socket.html





Necessary setup to prepare ABB Controller for EGM:

Configuration:
	-Motion
		-External Motion Interface Data
			-Level: must be set to Path for use with Path Correction, Raw or Filtered for Position Guidance
			-Position Gain:	determines motion responsiveness, higher values equal faster response (Position Guidance Only)
			-Filter Bandwidth: value used to filter the speed contribution from EGM (Position Guidance Only)
			-Ramp Time: determines how fast the speed should be ramped to zero after motion is complete (Position Guidance Only)
	-Communication
		-Type: must turn type to UDPUC standard
		-Remote Address: The ip address of the sensor(computer)
		-Remote Port Number: The port number of the sensor(computer)



An example RAPID module is included for position streaming. For examples using Position Guidance or Path Correction, as well as information on EGM RAPID commands and general setup information consult the ABB EGM manual: https://library.e.abb.com/public/4c9bfa6a4e9542bf9386c87f5377a27f/3HAC073319%20AM%20Externally%20Guided%20Motion%20RW6-en.pdf?x-sign=W42ZwkRuP3q1Dr78NoMTFHI0DdPMmb7ezINcsvqB/Ij7YxK7rdtzREC7RSoHvQJW  

Written with RobotWare 6.14 - Effectiveness may vary in other versions, but should work for most.


Author: Jonas Beachy, University of Washington
