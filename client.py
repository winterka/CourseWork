import socket
import threading
from time import sleep

HEADER = 2048
PORT = int(input("[CONNECTING] Choose server(Alpha: 8083 | Beta: 8084) "))
ENCODING = "utf-8"
DISCONNECT_MSG = "!DIS"
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = '192.168.1.64'
ADDR = (SERVER, PORT)
print(ADDR)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(ENCODING)
    msg_len = len(message)
    send_len = str(msg_len).encode(ENCODING)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)
    if msg == '!task1':
        listen_server()
    if msg == '!task2':
        listen_server()
    if msg == '!task3':
        f = str(input("Введите единицы для перевода "))
        client.send(str(f).encode(ENCODING))
        listen_server()
    if msg == '!task4':
        f = str(input("Введите единицы для перевода "))
        client.send(str(f).encode(ENCODING))
        listen_server()




def listen_server():
    data = client.recv(HEADER)
    if data:
        print(data.decode(ENCODING))
        data=''


def listening():
    listen_thread = threading.Thread(target=listen_server())
    listen_thread.start()
    while True:
        send(str(input(">")))


if __name__=='__main__':
    listening()


