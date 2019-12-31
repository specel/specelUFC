#!python3

from __future__ import print_function
from __future__ import unicode_literals

import socket, time, requests, json
from packaging import version
from dcsbiosParser import ProtocolParser, StringBuffer, IntegerBuffer
from specelG13Handler import G13Handler

__version__="v1.12.1"

def attemptConnect():
	connected = False
	print("Waiting for DCS connection...")
	while not connected:
		try:
			s.connect(("127.0.0.1", 7778))
			print("Connected")
			connected=True
		except socket.error:
			time.sleep(2)

def checkCurrentVersion():
	try:
		url="https://api.github.com/repos/specel/specelUFC/releases/latest"
		response = requests.get(url)
		if response.status_code==200:
			jsonResponse=response.json()
			onlineVersion=jsonResponse["tag_name"]
			if version.parse(onlineVersion)>version.parse(__version__):
				print("There is updated version of specelUFC: ",onlineVersion, "- get it on https://github.com/specel/specelUFC")
			elif version.parse(onlineVersion)==version.parse(__version__):
				print("This is up-to-date version")
			else:
				print("Something goes wrong: local version:", __version__,", a onlineVersion:",onlineVersion)
		else:
			print("Unable to check version online. Try again later. Status=", response.status_code())
	except Exception as e:
		print("Unable to check version online: ", e)



print("specelUFC ",__version__," https://github.com/specel/specelUFC")
checkCurrentVersion()
while True:
	parser = ProtocolParser()
	g13 = G13Handler(parser)
	g13.infoDisplay(("G13 initialised OK","Waiting for DCS","","specel UFC "+__version__))

	s = socket.socket()
	s.settimeout(None)

	attemptConnect()
	while True:
		try:
			c=s.recv(1)
			parser.processByte(c)
			if g13.shouldActivateNewAC:
				g13.activateNewAC()

			g13.buttonHandle(s)

		except socket.error as e:
			print("Main loop socket error: ", e)
			time.sleep(2)
		
		except Exception as e:
			print("Unexpected error: resetting... : ", e)
			time.sleep(2)
			break
		

	
	del s
	del g13
	del parser

	


