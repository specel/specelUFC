#!python3

from __future__ import print_function
from __future__ import unicode_literals

import socket, time
from dcsbiosParser import ProtocolParser, StringBuffer, IntegerBuffer
from specelG13Handler import G13Handler

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

while True:
	parser = ProtocolParser()
	g13 = G13Handler(parser)

	s = socket.socket()
	s.settimeout(None)

	attemptConnect()
	while True:
		try:
			c=s.recv(1)
			parser.processByte(c)

			g13.buttonHandle(s)

		except socket.error as e:
			print("Main loop socket error: ", e)
			time.sleep(2)
		except Exception as e:
			print("Unexpected error: resetting...")
			break
	print("End of main loop")


