#!python3
#test

from PIL import Image, ImageFont, ImageDraw
#import specelG13Handler
from dcsbiosParser import ProtocolParser, StringBuffer, IntegerBuffer

class FA18Handler:

    def __init__(self, displayHandler, parser):
        self.g13 = displayHandler
        self.parser = parser

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
        
        self.bufferScratchpadString1Display = StringBuffer(parser, 0x5446  , 2, lambda s: self.setData(1,s))
        self.bufferScratchpadString2Display = StringBuffer(parser, 0x5448  , 2, lambda s: self.setData(2,s))
        self.bufferScratchpadNumberDisplay = StringBuffer(parser, 0x543e  , 8, lambda s: self.setData(3,s))
        self.bufferOptionDisplay1 = StringBuffer(parser, 0x542a  , 4, lambda s: self.setData(11,s))
        self.bufferOptionDisplay2 = StringBuffer(parser, 0x542e  , 4, lambda s: self.setData(12,s))
        self.bufferOptionDisplay3 = StringBuffer(parser, 0x5432  , 4, lambda s: self.setData(13,s))
        self.bufferOptionDisplay4 = StringBuffer(parser, 0x5436  , 4, lambda s: self.setData(14,s))
        self.bufferOptionDisplay5 = StringBuffer(parser, 0x543a  , 4, lambda s: self.setData(15,s))
        self.bufferCOMM1Display = StringBuffer(parser, 0x541c  , 2, lambda s: self.setData(21,s))
        self.bufferCOMM2Display = StringBuffer(parser, 0x541e  , 2, lambda s: self.setData(22,s))
        self.bufferOptionCueing1 = StringBuffer(parser, 0x5420  , 1, lambda s: self.setData(31,s))
        self.bufferOptionCueing2 = StringBuffer(parser, 0x5422  , 1, lambda s: self.setData(32,s))
        self.bufferOptionCueing3 = StringBuffer(parser, 0x5424  , 1, lambda s: self.setData(33,s))
        self.bufferOptionCueing4 = StringBuffer(parser, 0x5426  , 1, lambda s: self.setData(34,s))
        self.bufferOptionCueing5 = StringBuffer(parser, 0x5428  , 1, lambda s: self.setData(35,s))
        self.bufferFuelTotal = StringBuffer(parser, 0x5482  , 6, lambda s: self.setData(40,s))

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

        #make it array and set proper values
        pixels = list(self.img.getdata())
        for i in range(0,len(pixels)):
        	pixels[i]*=128

        self.g13.updateDisplay(pixels)
        
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
    
    def buttonHandleSpecificAC(self, buttonPressed):
        if buttonPressed==1:
        	return "UFC_COMM1_CHANNEL_SELECT -3200\n"
        elif buttonPressed==2:
        	return "UFC_COMM1_CHANNEL_SELECT +3200\n"
        elif buttonPressed==3:
        	return "UFC_COMM2_CHANNEL_SELECT -3200\n"
        elif buttonPressed==4:
        	return "UFC_COMM2_CHANNEL_SELECT +3200\n"
