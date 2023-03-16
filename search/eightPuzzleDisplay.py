from graphicsUtils import *
from eightpuzzle import *

BACKGROUND_COLOR = formatColor(0, 0, 0)
PUZZLE_TEXT_COLOR = formatColor(0, 0, 0)
TEXT_COLOR = formatColor(1, 1, 1)
SQUARE_COLOR = formatColor(1, 1, 1)


class Graphics:

    def __init__(self, width=600, height=600, size=3):
        self.size = size
        self.messageBoxHeight = 30
        self.enableMessageBox = 1
        self.windowWidth = width
        self.windowHeight = height
        self.make_window(self.windowWidth, self.windowHeight + self.getMessageBoxHeight())

        self.drawSquares()

    def make_window(self, width, height):
        begin_graphics(width, height,
                       BACKGROUND_COLOR,
                       "AI: Eight Puzzle Problem")

    def getMessageBoxHeight(self):
        return self.messageBoxHeight * self.enableMessageBox

    def drawMessage(self, message, refreshGraphics=1, ):
        text((5, 5), TEXT_COLOR, message, "Times", 24, "bold")
        if refreshGraphics: refresh()

    def drawSquares(self, refreshGraphics=1):
        normalizedSize = min(self.windowHeight, self.windowWidth)
        startX = normalizedSize / (self.size * 2)
        startY = normalizedSize / (self.size * 2) + self.getMessageBoxHeight()
        position = [startX, startY]
        increment = normalizedSize / self.size
        for i in range(self.size):
            for j in range(self.size):
                square(self.to_screen(position), increment / 2 - 1, SQUARE_COLOR, 1)
                position[0] += increment
            position[1] += increment
            position[0] = startX
        if refreshGraphics: refresh()

    def drawState(self, state, refreshGraphics=1):
        normalizedSize = min(self.windowHeight, self.windowWidth)
        startX = normalizedSize / (self.size ** 2)
        startY = normalizedSize / (self.size ** 2) + self.getMessageBoxHeight()
        position = [startX, startY]
        increment = normalizedSize / self.size

        for i in range(self.size):
            for j in range(self.size):
                if state.cells[i][j] != 0:
                    text(self.to_screen(position), PUZZLE_TEXT_COLOR, str(state.cells[i][j]), "Times", increment / 2, "bold")
                position[0] += increment
            position[1] += increment
            position[0] = startX
        if refreshGraphics: refresh()

    def updatePuzzleGraphics(self, state, message):
        clear_screen()
        self.drawSquares(0)
        self.drawState(state, 0)
        self.drawMessage(message, 0)
        refresh()

    def to_screen(self, point):
        return (point[0], point[1])

    def finish(self):
        end_graphics()

SAVE_POSTSCRIPT = True
POSTSCRIPT_OUTPUT_DIR = 'frames'
FRAME_NUMBER = 0

def saveFrame():
    "Saves the current graphical output as a postscript file"
    global SAVE_POSTSCRIPT, FRAME_NUMBER, POSTSCRIPT_OUTPUT_DIR
    if not SAVE_POSTSCRIPT: return
    if not os.path.exists(POSTSCRIPT_OUTPUT_DIR): os.mkdir(POSTSCRIPT_OUTPUT_DIR)
    name = os.path.join(POSTSCRIPT_OUTPUT_DIR, 'frame_%08d.ps' % FRAME_NUMBER)
    FRAME_NUMBER += 1
    writePostscript(name)  # writes the current canvas
