import socket
import time
import signal

HOST = '192.168.13.37'
PORT = 31415


# close connection when the user fires a SIGINT
def closefunc(signal, frame):
    print("Closing connection...s")
    s.close()
    exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to {}:{} ...".format(HOST, PORT))
s.connect((HOST, PORT))
signal.signal(signal.SIGINT, closefunc)

# Wait until the server sends 2 newlines to inform us that we can send data
while True:
    bytes = s.recv(2)
    if(bytes == b'\n\n'):
        print("Connection established!")
        break

# Actual loop
while True:
    s.sendall('z')
    time.sleep(0.25)
    s.sendall('a')
    time.sleep(0.25)
    s.sendall('q')
    time.sleep(0.25)
    s.sendall('zp')
    time.sleep(0.25)
    s.sendall('ao')
    time.sleep(0.25)
    s.sendall('q')
    time.sleep(0.25)
    s.sendall('z')
    time.sleep(0.25)
    s.sendall('a')
    time.sleep(0.25)
    s.sendall('q')
    time.sleep(0.25)
    s.sendall('zp')
    time.sleep(0.25)
    s.sendall('ao')
    time.sleep(0.25)
    s.sendall('ui7')
    time.sleep(0.25)

