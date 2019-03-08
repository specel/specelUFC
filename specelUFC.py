#!python3

from __future__ import print_function
from __future__ import unicode_literals

import socket, time
from dcsbiosParser import ProtocolParser, StringBuffer, IntegerBuffer
from specelG13Handler import G13Handler

parser = ProtocolParser()
g13 = G13Handler()

# Hornets data subscription
ScratchpadString1Display = StringBuffer(parser, 0x5446  , 2, lambda s: g13.setData(1,s))
ScratchpadString2Display = StringBuffer(parser, 0x5448  , 2, lambda s: g13.setData(2,s))
ScratchpadNumberDisplay = StringBuffer(parser, 0x543e  , 8, lambda s: g13.setData(3,s))
OptionDisplay1 = StringBuffer(parser, 0x542a  , 4, lambda s: g13.setData(11,s))
OptionDisplay2 = StringBuffer(parser, 0x542e  , 4, lambda s: g13.setData(12,s))
OptionDisplay3 = StringBuffer(parser, 0x5432  , 4, lambda s: g13.setData(13,s))
OptionDisplay4 = StringBuffer(parser, 0x5436  , 4, lambda s: g13.setData(14,s))
OptionDisplay5 = StringBuffer(parser, 0x543a  , 4, lambda s: g13.setData(15,s))
COMM1Display = StringBuffer(parser, 0x541c  , 2, lambda s: g13.setData(21,s))
COMM2Display = StringBuffer(parser, 0x541e  , 2, lambda s: g13.setData(22,s))
OptionCueing1 = StringBuffer(parser, 0x5420  , 1, lambda s: g13.setData(31,s))
OptionCueing2 = StringBuffer(parser, 0x5422  , 1, lambda s: g13.setData(32,s))
OptionCueing3 = StringBuffer(parser, 0x5424  , 1, lambda s: g13.setData(33,s))
OptionCueing4 = StringBuffer(parser, 0x5426  , 1, lambda s: g13.setData(34,s))
OptionCueing5 = StringBuffer(parser, 0x5428  , 1, lambda s: g13.setData(35,s))
FuelTotal = StringBuffer(parser, 0x5482  , 6, lambda s: g13.setData(40,s))

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket()
s.settimeout(None)

def attemptConnect():
	connected = False

	while not connected:
		try:
			s.connect(("127.0.0.1", 7778))
			print("Connected")
			connected=True
		except socket.error as e:
			print("Connection error: ", e)
			time.sleep(2)

attemptConnect()
while True:
	try:
		#parse bytes
		c = s.recv(1)
		parser.processByte(c)

		#send button commands
		button = g13.checkButtons()
		if button==1:
			s.send(bytes("UFC_COMM1_CHANNEL_SELECT -3200\n","utf-8"))
		elif button==2:
			s.send(bytes("UFC_COMM1_CHANNEL_SELECT +3200\n","utf-8"))
		elif button==3:
			s.send(bytes("UFC_COMM2_CHANNEL_SELECT -3200\n","utf-8"))
		elif button==4:
			s.send(bytes("UFC_COMM2_CHANNEL_SELECT +3200\n","utf-8"))


	except socket.error as e:
		print("Main loop socket error: ", e)
		time.sleep(2)

	except:
		print("Unexpected error")
		time.sleep(2)

