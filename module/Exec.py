'''
This class decides what has to be done on the commands
recieved from client/server by mapping the commands to
the callbacks

Copyright (c) 2022 HueHueberry
Author: Hubert F. Espinola I (HueHueberry)

'''
from Protocol import ProtoCommandParser
import socket

def nullFunction():
    pass

class ExecCmd:
    def __init__(self, cliSock: socket.socket, cliMap: dict) -> None:
        self.cliSock = cliSock
        self.cliMap = cliMap

        # current command
        self.command = None

        # for executing functions
        self.execMap = {
            'NULL': nullFunction,
            'FWD' : self.forward,
            'MSG' : self.message
        }

        # callbacks when client recieves the ff. information
        self.cliCallbacks = {
            'MSG': nullFunction
        }

    # push command on 
    def addComs(self, commandParserObj: ProtoCommandParser) -> bool:
        command = commandParserObj.getCommand()
        if (command == ''):
            return False
        else:
            self.command = commandParserObj
            return True

    # executes the command received
    def execute(self) -> None:
        if (self.command == None):
            return

        # executes the command recieved
        command = self.command.getCommand()
        args = self.command.getArgs()
        self.execMap[command](args)

    ####################
    #  Server Actions  #
    ####################
    # forwards all the message to other clients
    def forward(self, message: str):
        for nickname in self.cliMap:
            try:
                cliSocket = self.cliMap[nickname]
                if (cliSocket != self.cliSock):
                    cliSocket.send(f'MSG[*$%]{message}')
            except Exception as e:
                print (e)

    ####################
    #  Client Actions  #
    ####################
    # when message is recieved by client
    def message(self, message: str):
        self.cliCallbacks['MSG'](message)
        print (f'Message: {message}')