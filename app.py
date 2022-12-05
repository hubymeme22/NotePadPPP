import sys

sys.path.append('module')
from tkinter import *
from NotePPPP import NotePPPPClient
from clientPopup import PopUp

HEIGHT = 500
WIDTH  = 600
ALTPRESSED = False
CONNECTED = False

# defult values
information = {
    'ip': 'localhost',
    'port': 8080,
    'notepadCli': None
};

rootParent = Tk()
rootParent.title('Notepad')
rootParent.geometry(f'{WIDTH}x{HEIGHT}')

# functions for event listeners
def displayConnectWindow(event):
    global ALTPRESSED

    # Alt + c for connection
    if (str(event.keysym) == 'Alt_L'):
        print ('AltPressed!')
        ALTPRESSED = True
        return

    # for displaying server connection
    if (ALTPRESSED and str(event.keysym) == 'c'):
        PopUp(rootParent, 'Connect to Server').displayHiddenClient(information)
        ALTPRESSED = False
    else:
        ALTPRESSED = False

# binding event listeners
rootParent.bind('<Key>', displayConnectWindow)

# main canvas
simpleCanvas = Canvas(rootParent, bg="red", height=HEIGHT, width=WIDTH, highlightthickness=0)
simpleCanvas.pack(expand=True)

# text box for notepad editting
noteText = Text(simpleCanvas, font=('Consolas', 15), height=HEIGHT, width=WIDTH, highlightthickness=0)
noteText.pack(expand=True)

rootParent.mainloop()
