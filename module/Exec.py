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
    def __init__(self, cliSock: socket.socket, cliMap: dict={}) -> None:
        self.cliSock = cliSock
        self.cliMap = cliMap

        # current command
        self.command = None
        self.nickname = ''

        # nickname retrieval
        for nickname in self.cliMap:
            if (self.cliSock == self.cliMap[nickname]['socket']):
                self.nickname = nickname
                break

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
    def forward(self, args: list):
        message = args[0]
        for nickname in self.cliMap:
            try:
                cliSocket = self.cliMap[nickname]['socket']
                if (cliSocket != self.cliSock):
                    print (f'[MESSAGE] from {self.nickname} to {nickname}')
                    cliSocket.send(f'MSG[*$%]{self.nickname}[*$%]{message}'.encode())
            except Exception as e:
                print (e)

    ####################
    #  Client Actions  #
    ####################
    # when message is recieved by client
    def message(self, args: list):
        message = args[1]
        self.cliCallbacks['MSG'](args)