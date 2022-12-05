import socket

'''
This class acts as parser for packets recieved by the
client/server.

Copyright (c) 2022 HueHueberry
Author: Hubert F. Espinola I
'''
class ProtoCommandParser:
    def __init__(self, packet: str) -> None:
        self.packet = packet.split('[*$%]')
        self.command = None
        self.args = None

    # gets the command from the packet
    def getCommand(self) -> str:
        if (self.command != None):
            return self.command

        if (len(self.packet) >= 1):
            self.command = self.packet[0]
            return self.command
        else:
            return ''

    # same as the command
    def getKeyword(self) -> str:
        return self.getCommand()

    # retrieves the argument/s
    def getArgs(self) -> list:
        if (len(self.packet) >= 2):
            self.args = self.packet[1:]
            return self.args
        else:
            return []