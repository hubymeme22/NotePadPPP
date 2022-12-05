from NotePPPP import NotePPPPClient
from tkinter import *

class PopUp:
    def __init__(self, root: Tk, title: str) -> None:
        self.newWindow = Toplevel(root)
        self.newWindow.title(title)
        self.newWindow.geometry("250x250")

    def displayHiddenClient(self, infoDictionary: dict):
        canvas = Canvas(self.newWindow, width=250, height=250)
        canvas.pack()

        inputIP = Entry(self.newWindow, font=("Consolas", 12), fg="#000000", bd=0, background='white')
        inputPort = Entry(self.newWindow, font=("Consolas", 12), fg="#000000", bd=0, background='white')
        inputNickname = Entry(self.newWindow, font=("Consolas", 12), fg="#000000", bd=0, background='white')
        connectedLabel = Label(self.newWindow)

        inputIP.insert(0, 'Enter IP')
        inputPort.insert(0, 'Enter PORT')
        inputNickname.insert(0, 'Enter nickname')

        # callback for connection
        def connectServer():
            ip = inputIP.get()
            nickname = inputNickname.get()

            try:
                port = int(inputPort.get())
                infoDictionary.update({'ip': ip, 'port': port, 'nickname': nickname, 'notepadCli': NotePPPPClient(ip, port)})

                infoDictionary['notepadCli'].start()
                infoDictionary['notepadCli'].connect(nickname)

                self.newWindow.destroy()
            except:
                print ('[-] Error in connecting')

        buttonConnect = Button(self.newWindow, text="Connect", command=connectServer)
        canvas.create_window(20, 20, anchor=NW, window=inputIP)
        canvas.create_window(20, 50, anchor=NW, window=inputPort)
        canvas.create_window(20, 80, anchor=NW, window=inputNickname)

        canvas.create_window(20, 100, anchor=NW, window=connectedLabel)
        canvas.create_window(20, 130, anchor=NW, window=buttonConnect)

        self.newWindow.resizable(False, False)