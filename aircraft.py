from abc import abstractmethod

from PIL import Image, ImageFont, ImageDraw


class AircraftHandler(object):
    def __init__(self, displayHandler, parser):
        self.g13 = displayHandler
        self.parser = parser
        self.width = 160
        self.height = 43
        self.img = Image.new('1', (self.width, self.height), 0)
        self.draw = ImageDraw.Draw(self.img)
        self.font1 = ImageFont.truetype("consola.ttf", 11)
        self.font2 = ImageFont.truetype("consola.ttf", 16)

    def buttonHandleSpecificAC(self, buttonPressed):
        if buttonPressed == 1:
            return "UFC_COMM1_CHANNEL_SELECT -3200\n"
        elif buttonPressed == 2:
            return "UFC_COMM1_CHANNEL_SELECT +3200\n"
        elif buttonPressed == 3:
            return "UFC_COMM2_CHANNEL_SELECT -3200\n"
        elif buttonPressed == 4:
            return "UFC_COMM2_CHANNEL_SELECT +3200\n"

    @abstractmethod
    def updateDisplay(self):
        pass

    @abstractmethod
    def setData(self, selector, value, update=True):
        pass
