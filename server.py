import socket
from PyQt5.QtWidgets import *
import sys


# Create a socket allows to connect
def socket_create():
    try:
        global host
        global port 
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: ", str(msg))

# Bind socket to port and wait for connection from client
def socket_bind():
    try:
        global host
        global port 
        global s
        #print("Binding socket to port: ", str(port))
        s.bind((host, port))
        s.listen(1)
    except socket.error as msg:
        QMessageBox.warning(None, 'Warning', "Socket binding error: " + str(msg) +"\n"+"Retrying...")
        socket_bind()

# Establishing a connection with client (socket must be a listening for them)
def socket_accept():
    global conn
    global address
    conn, address = s.accept()
    #print("Connection has been established | " +" IP " + address[0] + " | Port "+str(address[1]))
    send_commands(conn)
    conn.close()

def close_server():
    global conn
    global s
    conn.close()
    s.close()
    sys.exit()

# Send commands
def send_commands(conn):
    conn.send(str.encode('dsb.py'))
    conn.send(str.encode('dir'))
    client_response = str(conn.recv(1024), "utf-8")
    #print(client_response, end="")



def main_module():
    socket_create()
    socket_bind()
    socket_accept()