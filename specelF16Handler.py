#!python3
#test

from aircraft import AircraftHandler
from dcsbiosParser import StringBuffer


class F16Handler(AircraftHandler):

    def __init__(self, displayHandler):
        super(F16Handler, self).__init__(displayHandler)
        self.DEDLine1=""
        self.DEDLine2=""
        self.DEDLine3=""
        self.DEDLine4=""
        self.DEDLine5=""
        
        self.bufferDEDLine1= StringBuffer(self.g13.parser, 0x44fc, 50, lambda s: self.setData("DEDLine1", s))
        self.bufferDEDLine2= StringBuffer(self.g13.parser, 0x452e, 50, lambda s: self.setData("DEDLine2", s))
        self.bufferDEDLine3= StringBuffer(self.g13.parser, 0x4560, 50, lambda s: self.setData("DEDLine3", s))
        self.bufferDEDLine4= StringBuffer(self.g13.parser, 0x4592, 50, lambda s: self.setData("DEDLine4", s))
        self.bufferDEDLine5= StringBuffer(self.g13.parser, 0x45c4, 50, lambda s: self.setData("DEDLine5", s))

    def updateDisplay(self):
        super(F16Handler, self).updateDisplay()

        '''print(self.DEDLine1)
        print(self.DEDLine2)
        print(self.DEDLine3)
        print(self.DEDLine4)
        print(self.DEDLine5)'''


        pos=0
        offsetpos=8
        self.g13.draw.text((0,pos), self.DEDLine1, 1, self.g13.font1)
        pos=pos+offsetpos
        self.g13.draw.text((0,pos), self.DEDLine2, 1, self.g13.font1)
        pos=pos+offsetpos
        self.g13.draw.text((0,pos), self.DEDLine3, 1, self.g13.font1)
        pos=pos+offsetpos
        self.g13.draw.text((0,pos), self.DEDLine4, 1, self.g13.font1)
        pos=pos+offsetpos
        self.g13.draw.text((0,pos), self.DEDLine5, 1, self.g13.font1)

        
        #make it array and set proper values
        pixels = list(self.g13.img.getdata())
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
