import socket
import argparse
import onetimepad
import json
import pickle


def recv_all(sock, data_leght):
    r_data = b""
    while len(r_data) < data_leght:
        temp = sock.recv(data_leght-len(r_data))
        if not temp:
            break
        r_data += temp
    return r_data


class EnbeddedData:
    def __init__(self, sourcefile, jsonfile):
        self.data = sourcefile
        self.json = jsonfile


class Server:

    def change_text(self, source, jsonfile):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('127.0.0.1', 3040))
        soc.listen(5)
        print('Listening at', soc.getsockname())

        while True:
            sc, address = soc.accept()
            print('We have accepted a connection from', address)
            print(' Socket name:', sc.getsockname())

            message = recv_all(sc, 1024)
            obj = pickle.loads(message)
            text = obj.data
            json_file = obj.json
            data = json.loads(json_file)
            print('Plain text is ', text)

            cipher = ''

            for word in text.split():
                if word in data:
                    word = data[word]
                    cipher += word + ' '
                else:
                    cipher += word + ' '

            print("Cipher text is ", cipher)
            sc.sendall(cipher.encode('utf-8'))

            sc.close()
            print('Cipher text is sent, socket closed')

    def encode_decode(self, source, my_key):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('127.0.0.1', 3036))
        soc.listen(5)
        print('Listening at', soc.getsockname())
        flag = True
        while True:
            sc, address = soc.accept()
            print('We have accepted a connection from', address)
            print(' Socket name:', sc.getsockname())

            message = recv_all(sc, 1024)
            obj = pickle.loads(message)
            text = obj.data
            key = obj.json

            if(flag):
                print('Plain text is ', text)
                cipher = onetimepad.encrypt(
                    text, key)
                print("Cipher text is", repr(cipher))
                sc.sendall(cipher.encode('utf-8'))
            else:
                print("Cipher text is ", text)
                plain = onetimepad.decrypt(
                    text, key)
                print("Plain text is", repr(plain))
                sc.sendall(plain.encode('utf-8'))

            sc.close()
            flag = not flag


class Client:

    def change_text(self, source, jsonfile):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('127.0.0.1', 3040))
        print('Client has been assigned ', soc.getsockname())

        file = open(source, 'r')
        source_file = ""
        while True:
            source = file.read(1024)
            if not source:
                break
            source_file += source
        file.close()

        file = open(jsonfile, 'r')
        json_file = ""
        while True:
            json = file.read(1024)
            if not json:
                break
            json_file += json
        file.close()

        ed = EnbeddedData(source_file, json_file)
        sender_data = pickle.dumps(ed)

        soc.sendall(sender_data)
        soc.shutdown(socket.SHUT_WR)

        reply = recv_all(soc, 1024)
        print('Server said ', reply)

        soc.close()

    def encode_decode(self, source, keyfile):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('127.0.0.1', 3036))
        print('Client has been assigned ', soc.getsockname())

        file = open(source, 'r')
        source_file = ""
        while True:
            source = file.read(1024)
            if not source:
                break
            source_file += source
        file.close()

        file = open(keyfile, 'r')
        key_file = ""
        while True:
            key = file.read(1024)
            if not key:
                break
            key_file += key
        file.close()

        ed = EnbeddedData(source_file, key_file)
        sender_data = pickle.dumps(ed)

        soc.sendall(sender_data)
        soc.shutdown(socket.SHUT_WR)

        reply = recv_all(soc, 1024)
        print('Server said ', reply)

        soc.close()


def main():

    choises = {'server': Server, 'client': Client}
    functions = {'change_text': 'change_text',
                 'encode_decode': 'encode_decode'}
    parser = argparse.ArgumentParser(description="Text service")
    parser.add_argument("role", choices=choises)
    parser.add_argument('function', choices=functions)
    parser.add_argument('source')
    parser.add_argument('second_arg')

    args = parser.parse_args()

    clss = choises[args.role]()
    func = functions[args.function]

    method = getattr(clss, func)
    method(args.source, args.second_arg)


if __name__ == '__main__':
    main()
