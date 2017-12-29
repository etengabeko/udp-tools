#!/usr/bin/env python3

import argparse
import binascii
import socket
import sys

class Sender:
    infile = None
    isHexToBin = False

    def __init__(self, filename = None):
        if filename:
            self.infile = open(filename, "rb")

    def setHexToBin(self, enabled):
        self.isHexToBin = enabled

    def start(self, address, port):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while True:
                sended = None
                if self.infile:
                    sended = self.infile.readline()
                    if not sended:
                        break;
                else:
                    sended = input("Input sending content: ").encode()

                if sended[-1] == ord("\n"):
                    sended = sended[:-1]

                if not sended:
                    continue

                if self.isHexToBin:
                    sended = binascii.unhexlify(sended)

                sock.sendto(sended, (address, port))
        except:
            print(sys.exc_info()[1])

        finally:
            if sock:
                sock.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, required=True, help="send to port number")
    parser.add_argument("-i", "--iface", action="store", help="sending interface address")
    parser.add_argument("-f", "--file", action="store", help="input filename")
    parser.add_argument("--from-hex", action="store_true", dest="fromHex", help="convert hex to bin")

    arguments = parser.parse_args()

    print("port = {}, iface = {}, file = {}, fromHex = {}".format(arguments.port,
                                                                  arguments.iface if arguments.iface else "None",
                                                                  arguments.file  if arguments.file  else "None",
                                                                  arguments.fromHex))
    receiver = Sender(arguments.file if arguments.file else None)
    receiver.setHexToBin(arguments.fromHex)
    receiver.start(arguments.iface if arguments.iface else "localhost",
                   arguments.port)

if __name__ == "__main__":
    main()
