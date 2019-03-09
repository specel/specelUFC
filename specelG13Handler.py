#!python3

import GLCD_SDK
from PIL import Image, ImageFont, ImageDraw
from ctypes import c_ubyte
import socket
from specelFA18Handler import FA18Handler

class G13Handler:

	def __init__(self, parserHook):

		#init all hornet stuff using new class:
		self.currentAC = FA18Handler(self, parserHook)

		self.isAlreadyPressed=False

		#display parameters
		self.width=160
		self.height=43

		#GLCD Init
		GLCD_SDK.initDLL("C:\\Program Files\\Logitech Gaming Software\\LCDSDK_8.57.148\\Lib\\GameEnginesWrapper\\x86\\LogitechLcdEnginesWrapper.dll")
		GLCD_SDK.LogiLcdInit("Python",GLCD_SDK.TYPE_MONO)
	
	def updateDisplay(self, pixels):
		#put bitmap array into display
		if GLCD_SDK.LogiLcdIsConnected(GLCD_SDK.TYPE_MONO):
			GLCD_SDK.LogiLcdMonoSetBackground((c_ubyte * (self.width *self.height))(*pixels))
			GLCD_SDK.LogiLcdUpdate()
		else:
			print("LCD is not connected")


	def ClearDisplay(self, TrueClear=0):
		GLCD_SDK.LogiLcdMonoSetBackground((c_ubyte * (self.width *self.height))(*[0]*(self.width *self.height)))
		if TrueClear:
			for i in range(4):
				GLCD_SDK.LogiLcdMonoSetText(i,"")
		GLCD_SDK.LogiLcdUpdate()

	def checkButtons(self):
		if GLCD_SDK.LogiLcdIsButtonPressed(GLCD_SDK.MONO_BUTTON_0):
			if not self.isAlreadyPressed:
				self.isAlreadyPressed=True
				return 1
			else:
				return 0

		elif GLCD_SDK.LogiLcdIsButtonPressed(GLCD_SDK.MONO_BUTTON_1):
			if not self.isAlreadyPressed:
				self.isAlreadyPressed=True
				return 2
			else:
				return 0

		elif GLCD_SDK.LogiLcdIsButtonPressed(GLCD_SDK.MONO_BUTTON_2):
			if not self.isAlreadyPressed:
				self.isAlreadyPressed=True
				return 3
			else:
				return 0

		elif GLCD_SDK.LogiLcdIsButtonPressed(GLCD_SDK.MONO_BUTTON_3):
			if not self.isAlreadyPressed:
				self.isAlreadyPressed=True
				return 4
			else:
				return 0
		else:	
			self.isAlreadyPressed=False
			return 0
	
	def buttonHandle(self, socket):
		button = self.checkButtons()
		if not button==0:
			socket.send(bytes(self.currentAC.buttonHandleSpecificAC(button),"utf-8"))

	def initHornet(self):
		raise NotImplementedError("init hornet jeszcze nie działa")
	

