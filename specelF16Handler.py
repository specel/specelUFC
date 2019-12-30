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

        self.g13.updateDisplay(self.g13.img)
