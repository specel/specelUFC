#!python3
#test

from aircraft import AircraftHandler
from dcsbiosParser import StringBuffer


class FA18Handler(AircraftHandler):

    def __init__(self, displayHandler):
        super(FA18Handler, self).__init__(displayHandler)
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
        
        self.bufferScratchpadString1Display = StringBuffer(self.g13.parser, 0x744e  , 2, lambda s: self.setData(1,s))
        self.bufferScratchpadString2Display = StringBuffer(self.g13.parser, 0x7450  , 2, lambda s: self.setData(2,s))
        self.bufferScratchpadNumberDisplay = StringBuffer(self.g13.parser, 0x7446  , 8, lambda s: self.setData(3,s))
        self.bufferOptionDisplay1 = StringBuffer(self.g13.parser, 0x7432    , 4, lambda s: self.setData(11,s))
        self.bufferOptionDisplay2 = StringBuffer(self.g13.parser, 0x7436    , 4, lambda s: self.setData(12,s))
        self.bufferOptionDisplay3 = StringBuffer(self.g13.parser, 0x743a    , 4, lambda s: self.setData(13,s))
        self.bufferOptionDisplay4 = StringBuffer(self.g13.parser, 0x743e   , 4, lambda s: self.setData(14,s))
        self.bufferOptionDisplay5 = StringBuffer(self.g13.parser, 0x7442   , 4, lambda s: self.setData(15,s))
        self.bufferCOMM1Display = StringBuffer(self.g13.parser, 0x7424   , 2, lambda s: self.setData(21,s))
        self.bufferCOMM2Display = StringBuffer(self.g13.parser, 0x7426   , 2, lambda s: self.setData(22,s))
        self.bufferOptionCueing1 = StringBuffer(self.g13.parser, 0x7428   , 1, lambda s: self.setData(31,s))
        self.bufferOptionCueing2 = StringBuffer(self.g13.parser, 0x742a   , 1, lambda s: self.setData(32,s))
        self.bufferOptionCueing3 = StringBuffer(self.g13.parser, 0x742c   , 1, lambda s: self.setData(33,s))
        self.bufferOptionCueing4 = StringBuffer(self.g13.parser, 0x742e   , 1, lambda s: self.setData(34,s))
        self.bufferOptionCueing5 = StringBuffer(self.g13.parser, 0x7430   , 1, lambda s: self.setData(35,s))
        self.bufferFuelTotal = StringBuffer(self.g13.parser, 0x748a    , 6, lambda s: self.setData(40,s))

    def updateDisplay(self):
        super(FA18Handler, self).updateDisplay()

        #Scrachpad
        self.g13.draw.text((0,0), (self.ScratchpadString1Display+""+ self.ScratchpadString2Display+""+self.ScratchpadNumberDisplay), 1, self.g13.font2)
        self.g13.draw.line((0,20,115,20),1, 1)

        #comm1
        self.g13.draw.rectangle((0,29,20,42),0,1)
        self.g13.draw.text((2,29), self.COMM1Display, 1, self.g13.font2)

        #comm2
        offsetComm2=44
        self.g13.draw.rectangle((139-offsetComm2,29,159-offsetComm2,42),0,1)
        self.g13.draw.text((140-offsetComm2,29), self.COMM2Display, 1, self.g13.font2)

        #option display 1..5 with cueing
        pos=0
        offset=8
        self.g13.draw.text((120,pos), "1"+self.OptionCueing1+self.OptionDisplay1, 1, self.g13.font1)
        pos+=offset
        self.g13.draw.text((120,pos), "2"+self.OptionCueing2+self.OptionDisplay2, 1, self.g13.font1)
        pos+=offset
        self.g13.draw.text((120,pos), "3"+self.OptionCueing3+self.OptionDisplay3, 1, self.g13.font1)
        pos+=offset
        self.g13.draw.text((120,pos), "4"+self.OptionCueing4+self.OptionDisplay4, 1, self.g13.font1)
        pos+=offset
        self.g13.draw.text((120,pos), "5"+self.OptionCueing5+self.OptionDisplay5, 1, self.g13.font1)

        #Fuel Totaliser
        self.g13.draw.text((36,29), self.FuelTotal, 1, self.g13.font2)

        #make it array and set proper values
        pixels = list(self.g13.img.getdata())
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
