#!python3

from __future__ import print_function
from __future__ import unicode_literals

import socket, time
from dcsbiosParser import ProtocolParser, StringBuffer, IntegerBuffer
from specelG13Handler import G13Handler

parser = ProtocolParser()
g13 = G13Handler(parser)

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
			print("Connection error (Is DCS running? Are you in cockpit?): ", e)
			time.sleep(2)

attemptConnect()
while True:
	try:
		#parse bytes
		c = s.recv(1)
		parser.processByte(c)

		#send button commands
		g13.buttonHandle(s)

	except socket.error as e:
		print("Main loop socket error: ", e)
		time.sleep(2)

	except Exception as e:
		print("Unexpected error. If DCS crashed, restart this software, otherwise - ignore. Error: ", e)
		time.sleep(2)

