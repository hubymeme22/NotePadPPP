'''

NotePPPP is a simple class that handles both NotePPPP client and server
the client and server are communicating via NotePPPPProtocol which is an
application-level protocol. Made from the love of trolling and trippings
as a BSU student.

Copyright (c) 2022 HueHueberry
Author: Hubert F. Espinola I (HueHueberry)

'''
from Protocol import ProtoCommandParser
from Exec import ExecCmd, nullFunction
from datetime import datetime
import socket
import threading


'''
This class acts as the server which stores client
details for recieving data, forwards message and so on.
'''
class NotePPPPServer:
    def __init__(self, ip: str, port: int):
        # server info
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # clients and threading details
        self.cliList = {}
        self.threadTracks = {}

        # server status
        self.listening = True
        self.isEncrypted = False

    # wait for client's nickname before accepting
    def __confirmClient(self, cli_sock: socket.socket):
        data = cli_sock.recv(1024).decode()
        data = data.replace(' ', '')
        data = data.replace('\n', '')

        if (len(data) > 0):
            self.cliList[data] = {}
            self.cliList[data]['socket'] = cli_sock
            self.cliList[data]['handled'] = True

            print (f'[*] New Client added ({data})')
            th = threading.Thread(target=self.__handleClientRequests, args=(data,))
            th.start()

            # sends confirmation to client
            cli_sock.send('OK'.encode())
        else:
            print (f'[-] Client connection failed')
            cli_sock.close()

    # after confirmed handle this client
    def __handleClientRequests(self, cliNick: str):
        print (f'[+] Client ({cliNick}) handled in thread')

        clientSocket = self.cliList[cliNick]['socket']
        commandExec = ExecCmd(clientSocket, self.cliList)

        while self.cliList[cliNick]['handled']:
            packet = clientSocket.recv(1024).decode()
            parser = ProtoCommandParser(packet)

            commandExec.addComs(parser)
            commandExec.execute()

    # listens and saves client if nickname is assigned
    def __listenClient(self):
        while True:
            try:
                cli_sock, address = self.socket.accept()
                th = threading.Thread(target=self.__confirmClient, args=(cli_sock,))

                self.threadTracks[cli_sock] = th
                th.start()

            except Exception as e:
                print (f'[Error] {e}')

    # starts the server
    def start(self):
        print (f'[*] Starting server at {self.ip}:{self.port}')
        self.socket.bind((self.ip, self.port))
        self.socket.listen(25)

        print (f'[*] Listening client at port {self.port}')
        th = threading.Thread(target=self.__listenClient, args=())
        th.start()

        self.threadTracks['main'] = th

    # stops server listening for more client
    def stop(self):
        print ('[!] Server listens to last client...')
        self.listening = False

    # for getting client details
    def getSpecifiedClient(self, cliNick: str) -> dict:
        if (cliNick in self.cliList):
            return self.cliList[cliNick]
        return {}

'''
Client class for communicating to server
'''
class NotePPPPClient:
    def __init__(self, ip: str, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commandExec = ExecCmd(self.socket)

        # client details
        self.ip = ip
        self.port = port
        self.nickname = None
        self.isConnected = False
        self.loopUpdate = True

        # initialize with sample message
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.messageLog = [{'Author': [current_time, 'Hello everybody! Welcome to NotepadPPP!']}]

    # constantly recieves from server's updates
    def __recieveUpdate(self):
        while self.loopUpdate:
            try:
                packet = self.socket.recv(1024).decode()
                parser = ProtoCommandParser(packet)

                added = self.commandExec.addComs(parser)
                self.commandExec.execute()
            except Exception as e:
                print (f'[Error __recieveUpdate] {e}')
                self.stop()

    # connect with the server
    def connect(self, nickname: str):
        self.nickname = nickname

        try:
            self.socket.connect((self.ip, self.port))
            self.socket.send(nickname.encode())
            response = self.socket.recv(1024).decode()

            self.isConnected = (response == 'OK')
            return self.isConnected
        except Exception as e:
            print (f'[Error Client.connect] {e}')

    # starts constant recieving
    def start(self):
        self.loopUpdate = True
        th = threading.Thread(target=self.__recieveUpdate, args=())
        th.start()

    # stops constant recieving
    def stop(self):
        self.loopUpdate = False

    # client callback updater
    def callbackUpdate(self, key, callback=nullFunction):
        if (key not in self.commandExec.cliCallbacks):
            return False

        # the callback for this recieves a message
        # ex, callback(message)
        self.commandExec.cliCallbacks[key] = callback
        return True

    ############################
    #  Client Functionalities  #
    ############################
    def message(self, message: str):
        self.socket.send(f'FWD[*$%]{message}'.encode())