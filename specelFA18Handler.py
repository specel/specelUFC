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
        
        self.bufferScratchpadString1Display = StringBuffer(self.g13.parser, 0x744e, 2, lambda s: self.setData('ScratchpadString1Display',s))
        self.bufferScratchpadString2Display = StringBuffer(self.g13.parser, 0x7450, 2, lambda s: self.setData('ScratchpadString2Display',s))
        self.bufferScratchpadNumberDisplay = StringBuffer(self.g13.parser, 0x7446, 8, lambda s: self.setData('ScratchpadNumberDisplay',s))
        self.bufferOptionDisplay1 = StringBuffer(self.g13.parser, 0x7432, 4, lambda s: self.setData('OptionDisplay1',s))
        self.bufferOptionDisplay2 = StringBuffer(self.g13.parser, 0x7436, 4, lambda s: self.setData('OptionDisplay2',s))
        self.bufferOptionDisplay3 = StringBuffer(self.g13.parser, 0x743a, 4, lambda s: self.setData('OptionDisplay3',s))
        self.bufferOptionDisplay4 = StringBuffer(self.g13.parser, 0x743e, 4, lambda s: self.setData('OptionDisplay4',s))
        self.bufferOptionDisplay5 = StringBuffer(self.g13.parser, 0x7442, 4, lambda s: self.setData('OptionDisplay5',s))
        self.bufferCOMM1Display = StringBuffer(self.g13.parser, 0x7424, 2, lambda s: self.setData('COMM1Display',s))
        self.bufferCOMM2Display = StringBuffer(self.g13.parser, 0x7426, 2, lambda s: self.setData('COMM2Display',s))
        self.bufferOptionCueing1 = StringBuffer(self.g13.parser, 0x7428, 1, lambda s: self.setData('OptionCueing1',s))
        self.bufferOptionCueing2 = StringBuffer(self.g13.parser, 0x742a, 1, lambda s: self.setData('OptionCueing2',s))
        self.bufferOptionCueing3 = StringBuffer(self.g13.parser, 0x742c, 1, lambda s: self.setData('OptionCueing3',s))
        self.bufferOptionCueing4 = StringBuffer(self.g13.parser, 0x742e, 1, lambda s: self.setData('OptionCueing4',s))
        self.bufferOptionCueing5 = StringBuffer(self.g13.parser, 0x7430, 1, lambda s: self.setData('OptionCueing5',s))
        self.bufferFuelTotal = StringBuffer(self.g13.parser, 0x748a, 6, lambda s: self.setData('FuelTotal',s))

    def updateDisplay(self):
        super(FA18Handler, self).updateDisplay()

        #Scrachpad
        self.g13.draw.text((0,0), self.ScratchpadString1Display+self.ScratchpadString2Display+self.ScratchpadNumberDisplay, 1, self.g13.font2)
        self.g13.draw.line((0,20,115,20),1, 1)

        #comm1
        self.g13.draw.rectangle((0,29,20,42),0,1)
        self.g13.draw.text((2,29), self.COMM1Display, 1, self.g13.font2)

        #comm2
        offsetComm2=44
        self.g13.draw.rectangle((139-offsetComm2,29,159-offsetComm2,42),0,1)
        self.g13.draw.text((140-offsetComm2,29), self.COMM2Display, 1, self.g13.font2)

        #option display 1..5 with cueing
        for i in range(1, 6):
            offset = (i - 1) * 8
            self.g13.draw.text((120, offset),
                               f'{i}{getattr(self, f"OptionCueing{i}")}{getattr(self, f"OptionDisplay{i}")}',
                               1, self.g13.font1)

        #Fuel Totaliser
        self.g13.draw.text((36,29), self.FuelTotal, 1, self.g13.font2)

        self.g13.updateDisplay(self.g13.img)
        
    def setData(self, selector, value, update=True):
        if selector in ('ScratchpadString1Display', 'ScratchpadString2Display', 'COMM1Display', 'COMM2Display'):
            value = value.replace('`', '1').replace('~', '2')
        super().setData(selector, value, update)
