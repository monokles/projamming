import socket
import time
from threading import Timer
import os
import threading
from sample_manager import SampleManager
import signal

HOST = ''
PORT = 31415

running = True

def sig_handle(signal, frame):
    print("Closing program...")
    running = False

class ConnectionThread(threading.Thread):
    playbackQueue = []

    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.remote_ip = ip
        self.port = port
        self.socket = socket

    @staticmethod
    def playFromQueue():
        for i in ConnectionThread.playbackQueue:
            SampleManager.playFromFile(i)
        ConnectionThread.playbackQueue = []        
        if running is True:
            Timer(0.125, ConnectionThread.playFromQueue, ()).start()

    def parseCommand(self, command):
        num = ord(command)
        print("[+] Playing command: " + format(num, 'x'))
        print("[+]  |-: " + command)
        if num in (10, 13): # newline
            return
        ConnectionThread.playbackQueue.append("bytes/" + format(num, 'x'))
        # SampleManager.playFromFile("bytes/" + format(num, 'x'))
    def run(self):
        print('[+] Connnected to {}'.format(self.remote_ip))
        self.socket.send("\nWelcome to the Projamming system. Jam away!\n\n")
        while running:
            receive_data = self.socket.recv(1)
            if not receive_data:
                self.socket.close()
                print("[+] Closing connection with {}".format(self.remote_ip))
                return
            print("[+]received {}".format(receive_data))
            self.parseCommand(receive_data)



# set up server to create a new thread for all connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

threads = []

Timer(0.125, ConnectionThread.playFromQueue, ()).start()
SampleManager.init()
print("Server is now online.\n")

while running:
    s.listen(1)
    (socket, (ip, port)) = s.accept()
    thread = ConnectionThread(ip, port, socket)
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()
