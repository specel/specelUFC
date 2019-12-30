from PIL import Image, ImageFont, ImageDraw


class AircraftHandler:
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
            return "UFC_COMM1_CHANNEL_SELECT DEC\n"
        elif buttonPressed == 2:
            return "UFC_COMM1_CHANNEL_SELECT INC\n"
        elif buttonPressed == 3:
            return "UFC_COMM2_CHANNEL_SELECT DEC\n"
        elif buttonPressed == 4:
            return "UFC_COMM2_CHANNEL_SELECT INC\n"

    def updateDisplay(self):
        # clear bitmap
        self.draw.rectangle((0, 0, self.width, self.height), 0, 0)

    def setData(self, selector, value, update=True):
        setattr(self, selector, value)
        if update:
            self.updateDisplay()
