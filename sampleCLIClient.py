import sys

sys.path.append('module')
from NotePPPP import NotePPPPClient

if (__name__ == '__main__'):
    clientObj = NotePPPPClient('localhost', 8000)

    # sample callback
    def whenMessage(args):
        nickname = args[0]
        message = args[1]
        print (f'\nfrom ({nickname}) recieved: {message}')

    nickname = input('Enter Nickname: ')
    updated = clientObj.callbackUpdate('MSG', whenMessage)

    print (f'Updated = {updated}')

    clientObj.connect(nickname)
    clientObj.start()

    while True:
        message = input('Enter message: ')
        clientObj.message(message)