import sys

sys.path.append('module')
from NotePPPP import NotePPPPServer

if (__name__ == '__main__'):
    server = NotePPPPServer('localhost', 8000)
    server.start()