class AircraftHandler:
    def __init__(self, displayHandler):
        self.g13 = displayHandler

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
        self.g13.draw.rectangle((0, 0, self.g13.width, self.g13.height), 0, 0)

    def setData(self, selector, value, update=True):
        setattr(self, selector, value)
        if update:
            self.updateDisplay()
