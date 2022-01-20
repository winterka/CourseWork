import socket
import threading
import datetime
from time import sleep

import win32api
from tendo import singleton

me = singleton.SingleInstance()
HEADER = 2048
PORT = 8084
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
ENCODING = "utf-8"
DISCONNECT_MSG = "!DIS"

server_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_b.bind(ADDR)


def timestamp():
    time = datetime.datetime.now()
    time = f"[{time.strftime('%H:%M:%S')}]"
    return time



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(ENCODING)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(ENCODING)
            if msg == DISCONNECT_MSG:
                connected = False
                print(f"[CONNECTION INTERRUPTED] {addr} disconnected.")
                break
            if msg == "!task3":
                #disk = conn.recv(HEADER).decode(ENCODING)
                ram_total = task3()
                f = conn.recv(HEADER).decode(ENCODING)
                res = bytes(convertor(ram_total,f,0), encoding=ENCODING)
                conn.send(res)
            if msg == "!task4":
                ram_avail = task4()
                f = conn.recv(HEADER).decode(ENCODING)
                res = bytes(convertor(ram_avail,f,0), encoding=ENCODING)
                conn.send(res)
            print(f"[{addr}] {msg}")
    conn.close()


def convertor_float(f, prec):
    return ("%." + str(prec) + "f") % f

def convertor(size, size_out, prec):
    assert size_out.upper() in {"B", "KB", "MB", "GB"}, "sizeOut type error"
    if size_out == "B":
        return (f"{size} B\n{timestamp()}")
    elif size_out == "MB":
        return f"{(convertor_float((size / 1024.0 ** 2), prec))} MB\n{timestamp()}"
    elif size_out == "GB":
        return f"{convertor_float((size / 1024.0 ** 3), prec)} GB\n{timestamp()}"


def task3():
    return win32api.GlobalMemoryStatusEx()['TotalPhys']

def task4():
    return win32api.GlobalMemoryStatusEx()['AvailPhys']


def start_server():
    server_b.listen()
    print(f"[LISTENING] Server Beta is listening on {SERVER}")
    while True:
        conn, addr = server_b.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        conn.send(b"[INFO] Commands:\n"
                  b"!task3 - Total phys. memory\n"
                  b"!task2 - Avail phys. memory")


if __name__ == '__main__':
    print("[LAUNCHING] Server Beta is starting...")
    start_server()
