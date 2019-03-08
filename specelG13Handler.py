#!python3

import GLCD_SDK
from PIL import Image, ImageFont, ImageDraw
from ctypes import c_ubyte
import socket

class G13Handler:

	def __init__(self):
		self.ScratchpadString1Display=""
		self.ScratchpadString2Display=""
		self.ScratchpadNumberDisplay=""
		self.OptionDisplay1=""
		self.OptionDisplay2=""
		self.OptionDisplay3=""
		self.OptionDisplay4=""
		self.OptionDisplay5=""
		self.COMM1Display=""
		self.COMM2Display=""
		self.OptionCueing1=""
		self.OptionCueing2=""
		self.OptionCueing3=""
		self.OptionCueing4=""
		self.OptionCueing5=""
		self.FuelTotal=""
		self.SelectorList=[1,2,3,11,12,13,14,15,21,22,31,32,33,34,35] #outdated
		self.isAlreadyPressed=False

		#display parameters
		self.width=160
		self.height=43

		self.img = Image.new('1',(self.width,self.height),0)
		self.draw = ImageDraw.Draw(self.img)
		self.font1 = ImageFont.truetype("consola.ttf",11)
		self.font2 = ImageFont.truetype("consola.ttf",16)

		#GLCD Init
		GLCD_SDK.initDLL("C:\\Program Files\\Logitech Gaming Software\\LCDSDK_8.57.148\\Lib\\GameEnginesWrapper\\x86\\LogitechLcdEnginesWrapper.dll")
		GLCD_SDK.LogiLcdInit("Python",GLCD_SDK.TYPE_MONO)


	
	def updateDisplay(self):
		#clear bitmap
		self.draw.rectangle((0,0,self.width, self.height),0,0)

		#Scrachpad
		self.draw.text((0,0), (self.ScratchpadString1Display+""+ self.ScratchpadString2Display+""+self.ScratchpadNumberDisplay), 1, self.font2)
		self.draw.line((0,20,115,20),1, 1)

		#comm1
		self.draw.rectangle((0,29,20,42),0,1)
		self.draw.text((2,29), self.COMM1Display, 1, self.font2)

		#comm2
		offsetComm2=44
		self.draw.rectangle((139-offsetComm2,29,159-offsetComm2,42),0,1)
		self.draw.text((140-offsetComm2,29), self.COMM2Display, 1, self.font2)

		#option display 1..5 with cueing
		pos=0
		offset=8
		self.draw.text((120,pos), "1"+self.OptionCueing1+self.OptionDisplay1, 1, self.font1)
		pos+=offset
		self.draw.text((120,pos), "2"+self.OptionCueing2+self.OptionDisplay2, 1, self.font1)
		pos+=offset
		self.draw.text((120,pos), "3"+self.OptionCueing3+self.OptionDisplay3, 1, self.font1)
		pos+=offset
		self.draw.text((120,pos), "4"+self.OptionCueing4+self.OptionDisplay4, 1, self.font1)
		pos+=offset
		self.draw.text((120,pos), "5"+self.OptionCueing5+self.OptionDisplay5, 1, self.font1)

		#Fuel Totaliser
		self.draw.text((36,29), self.FuelTotal, 1, self.font2)

		#make it array
		pixels = list(self.img.getdata())
		for i in range(0,len(pixels)):
			pixels[i]*=128

		#put bitmap array into display
		if GLCD_SDK.LogiLcdIsConnected(GLCD_SDK.TYPE_MONO):
			GLCD_SDK.LogiLcdMonoSetBackground((c_ubyte * (self.width *self.height))(*pixels))
			GLCD_SDK.LogiLcdUpdate()
		else:
			print("LCD is not connected")
	
	def setData(self, selector, value, update=True):
		#programming noob here, but it's pretty clear how to use this monster
		if	selector==1:
			modifiedString=value
			modifiedString=modifiedString.replace('`','1')
			modifiedString=modifiedString.replace('~','2')
			self.ScratchpadString1Display=modifiedString
		elif	selector==2:
			modifiedString=value
			modifiedString=modifiedString.replace('`','1')
			modifiedString=modifiedString.replace('~','2')
			self.ScratchpadString2Display=modifiedString
		elif	selector==3:
			self.ScratchpadNumberDisplay=value
		elif	selector==11:
			self.OptionDisplay1=value
		elif	selector==12:
			self.OptionDisplay2=value
		elif	selector==13:
			self.OptionDisplay3=value
		elif	selector==14:
			self.OptionDisplay4=value
		elif	selector==15:
			self.OptionDisplay5=value
		elif	selector==21:
			# for unknown reason dcs_bios returns symbols instead '1' and '2' from comm channel display, so here we can correct this
			modifiedString=value
			modifiedString=modifiedString.replace('`','1')
			modifiedString=modifiedString.replace('~','2')
			self.COMM1Display=modifiedString
		elif	selector==22:
			modifiedString=value
			modifiedString=modifiedString.replace('`','1')
			modifiedString=modifiedString.replace('~','2')
			self.COMM2Display=modifiedString
		elif	selector==31:
			self.OptionCueing1=value
		elif	selector==32:
			self.OptionCueing2=value
		elif	selector==33:
			self.OptionCueing3=value
		elif	selector==34:
			self.OptionCueing4=value	
		elif	selector==35:
			self.OptionCueing5=value	
		elif	selector==40:
			self.FuelTotal=value
		else:
			print("No such selector: ", selector)
		
		if update:
			self.updateDisplay()
	
	def setData2(self, *data):
		#receive tuple with ufc data in order as in SelectorList - used to arrange data on screen
		x=0
		for arg in data:
			self.setData(self.SelectorList[x],arg,False)
			x+=1
		print("")
		self.updateDisplay()

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
		if button==1:
			socket.send(bytes("UFC_COMM1_CHANNEL_SELECT -3200\n","utf-8"))
		elif button==2:
			socket.send(bytes("UFC_COMM1_CHANNEL_SELECT +3200\n","utf-8"))
		elif button==3:
			socket.send(bytes("UFC_COMM2_CHANNEL_SELECT -3200\n","utf-8"))
		elif button==4:
			socket.send(bytes("UFC_COMM2_CHANNEL_SELECT +3200\n","utf-8"))

	def initHornet(self, parser):
		raise NotImplementedError()
	

