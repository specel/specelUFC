#!python3
from math import log2
from platform import architecture
from sys import maxsize

import GLCD_SDK
from PIL import Image, ImageFont, ImageDraw
from ctypes import c_ubyte, sizeof, c_void_p
from specelFA18Handler import FA18Handler
from specelF16Handler import F16Handler
from dcsbiosParser import StringBuffer


class G13Handler:

	def __init__(self, parserHook):
		##init all hornet stuff using new class - will change to autodetect someday:
		#self.currentAChook = FA18Handler(self, parserHook)

		self.bufferAC = StringBuffer(parserHook,0x0000,16, lambda v: self.setAC(v))
		self.parser = parserHook
		self.currentAC= None
		self.currentACHook = None
		self.shouldActivateNewAC= False

		self.isAlreadyPressed=False

		#display parameters
		self.width=160
		self.height=43

		#GLCD Init
		arch = 'x64' if all([architecture()[0] == '64bit', maxsize > 2 ** 32, sizeof(c_void_p) > 4]) else 'x86'
		GLCD_SDK.initDLL("C:\\Program Files\\Logitech Gaming Software\\LCDSDK_8.57.148\\Lib\\GameEnginesWrapper\\{}\\LogitechLcdEnginesWrapper.dll".format(arch))
		GLCD_SDK.LogiLcdInit("Python",GLCD_SDK.TYPE_MONO)

		self.img = Image.new('1',(self.width,self.height),0)
		self.draw = ImageDraw.Draw(self.img)
		self.font1 = ImageFont.truetype("consola.ttf",11)
		self.font2 = ImageFont.truetype("consola.ttf",16)
		
#### for new A/C implementation, make sure that setAC() makes shouldActivateNewAC=true, and then activateNewAC creates needed handler###
	def setAC(self, value):
		if not value == self.currentAC:
			self.currentAC=value
			if value in ("FA-18C_hornet", "AV8BNA", "F-16C_50"):
				print(f'Detected AC: {value}')
				self.infoDisplay()
				self.shouldActivateNewAC = True
			else:
				## FIXME a może tylko tyo zostawić, żeby po prostu zaczynał aktywaować nowy moduł, a weryfikację zostawić w metodzie poniżej?
				print(f'Unknown AC data: {value}')
				self.infoDisplay(('Unknown AC data:', self.currentAC))

	def activateNewAC(self):
		self.shouldActivateNewAC=False
		if self.currentAC=="FA-18C_hornet":
			self.currentACHook = FA18Handler(self)
		elif self.currentAC=="AV8BNA":
			self.infoDisplay(("AV8BNA", "not implemented yet"))
		elif self.currentAC=="F-16C_50":
			self.currentACHook = F16Handler(self)

			

	def infoDisplay(self, message=""):
		#clear bitmap
		self.draw.rectangle((0,0,self.width, self.height),0,0)
		#self.ClearDisplay()

		if message=="":
			self.draw.text((0,0), self.currentAC, 1, self.font1)
		else:
			y=0
			#self.draw.text((0,0), message, 1, self.font1)
			for line in message:
				self.draw.text((0,y), line, 1, self.font1)
				y=y+10

		self.updateDisplay(self.img)
		'''
		if GLCD_SDK.LogiLcdIsConnected(GLCD_SDK.TYPE_MONO):
			GLCD_SDK.LogiLcdMonoSetBackground((c_ubyte * (self.width *self.height))(*pixels))
			GLCD_SDK.LogiLcdUpdate()
		else:
			print("LCD is not connected")
		'''

	def updateDisplay(self, img):
		pixels = list(img.getdata())
		for i, _ in enumerate(pixels):
			pixels[i] *= 128

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
		for btn in (GLCD_SDK.MONO_BUTTON_0, GLCD_SDK.MONO_BUTTON_1, GLCD_SDK.MONO_BUTTON_2, GLCD_SDK.MONO_BUTTON_3):
			if GLCD_SDK.LogiLcdIsButtonPressed(btn):
				if not self.isAlreadyPressed:
					self.isAlreadyPressed = True
					return int(log2(btn)) + 1
				return 0
		self.isAlreadyPressed = False
		return 0
	
	def buttonHandle(self, socket):
		button = self.checkButtons()
		if button:
			socket.send(bytes(self.currentACHook.buttonHandleSpecificAC(button),"utf-8"))

	

