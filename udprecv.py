#!/usr/bin/env python3

import argparse
import binascii
import socket
import sys

kReceiveBufferSize = 2048

class Receiver:
    outfile = None
    isBinToHex = False

    def __init__(self, filename = None):
        if filename:
            self.outfile = open(filename, "wb")

    def setBinToHex(self, enabled):
        self.isBinToHex = enabled

    def start(self, address, port):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((address, port))
            while True:
                received = sock.recvfrom(kReceiveBufferSize)[0]
                if self.outfile:
                    self.outfile.write(binascii.hexlify(received) if self.isBinToHex else received)
                    if not received[-1] == ord("\n"):
                        self.outfile.write(b"\n")
                else:
                    if received[-1] == ord("\n"):
                        received = received[:-1]
                    print(binascii.hexlify(received) if self.isBinToHex else received)
        
        except:
            print(sys.exc_info()[1])

        finally:
            if sock:
                sock.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, required=True, help="listening port number")
    parser.add_argument("-i", "--iface", action="store", help="listening interface address")
    parser.add_argument("-f", "--file", action="store", help="output filename")
    parser.add_argument("--to-hex", action="store_true", dest="toHex", help="convert bin to hex")

    arguments = parser.parse_args()

    print("port = {}, iface = {}, file = {}, toHex = {}".format(arguments.port,
                                                                arguments.iface if arguments.iface else "None",
                                                                arguments.file  if arguments.file  else "None",
                                                                arguments.toHex))
    receiver = Receiver(arguments.file if arguments.file else None)
    receiver.setBinToHex(arguments.toHex)
    receiver.start(arguments.iface if arguments.iface else "localhost",
                   arguments.port)

if __name__ == "__main__":
    main()
