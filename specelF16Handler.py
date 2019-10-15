#!python3
#test

from PIL import Image, ImageFont, ImageDraw
#import specelG13Handler
from dcsbiosParser import ProtocolParser, StringBuffer, IntegerBuffer

class F16Handler:

    def __init__(self, displayHandler, parser):
        self.g13 = displayHandler
        self.parser = parser

        self.DEDLine1=""
        self.DEDLine2=""
        self.DEDLine3=""
        self.DEDLine4=""
        self.DEDLine5=""

        
        self.bufferDEDLine1= StringBuffer(parser, 0x44fc, 50, lambda s: self.setData("DEDLine1", s))
        self.bufferDEDLine2= StringBuffer(parser, 0x452e, 50, lambda s: self.setData("DEDLine2", s))
        self.bufferDEDLine3= StringBuffer(parser, 0x4560, 50, lambda s: self.setData("DEDLine3", s))
        self.bufferDEDLine4= StringBuffer(parser, 0x4592, 50, lambda s: self.setData("DEDLine4", s))
        self.bufferDEDLine5= StringBuffer(parser, 0x45c4, 50, lambda s: self.setData("DEDLine5", s))

        #self.g13 = displayHandler
        self.width=160
        self.height=43

        self.img = Image.new('1',(self.width,self.height),0)
        self.draw = ImageDraw.Draw(self.img)
        self.font1 = ImageFont.truetype("consola.ttf",11)
        self.font2 = ImageFont.truetype("consola.ttf",16)

    def updateDisplay(self):
        #clear bitmap
        self.draw.rectangle((0,0,self.width, self.height),0,0)

        '''print(self.DEDLine1)
        print(self.DEDLine2)
        print(self.DEDLine3)
        print(self.DEDLine4)
        print(self.DEDLine5)'''


        pos=0
        offsetpos=8
        self.draw.text((0,pos), self.DEDLine1, 1, self.font1)
        pos=pos+offsetpos
        self.draw.text((0,pos), self.DEDLine2, 1, self.font1)
        pos=pos+offsetpos
        self.draw.text((0,pos), self.DEDLine3, 1, self.font1)
        pos=pos+offsetpos
        self.draw.text((0,pos), self.DEDLine4, 1, self.font1)
        pos=pos+offsetpos
        self.draw.text((0,pos), self.DEDLine5, 1, self.font1)

        
        #make it array and set proper values
        pixels = list(self.img.getdata())
        for i in range(0,len(pixels)):
        	pixels[i]*=128

        self.g13.updateDisplay(pixels)
        
    def setData(self, selector, value, update=True):
		#programming noob here, but it's pretty clear how to use this monster
        if	selector=="DEDLine1":
            self.DEDLine1 = value
        elif selector=="DEDLine2":
            self.DEDLine2 = value
        elif selector=="DEDLine3":
            self.DEDLine3 = value
        elif selector=="DEDLine4":
            self.DEDLine4 = value
        elif selector=="DEDLine5":
            self.DEDLine5 = value
        else:
        	print("No such selector: ", selector)

        if update:
        	self.updateDisplay()
    
    def buttonHandleSpecificAC(self, buttonPressed):
        if buttonPressed==1:
        	return "UFC_COMM1_CHANNEL_SELECT -3200\n"
        elif buttonPressed==2:
        	return "UFC_COMM1_CHANNEL_SELECT +3200\n"
        elif buttonPressed==3:
        	return "UFC_COMM2_CHANNEL_SELECT -3200\n"
        elif buttonPressed==4:
        	return "UFC_COMM2_CHANNEL_SELECT +3200\n"
