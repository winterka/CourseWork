import socket
import threading
from tendo import singleton
import win32api
import datetime

me = singleton.SingleInstance()
HEADER = 2048
PORT = 8083
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
ENCODING = "utf-8"
DISCONNECT_MSG = "!DIS"

server_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_a.bind(ADDR)


def timestamp():
    time = datetime.datetime.now()
    time = f"[{time.strftime('%H:%M:%S')}]"
    return time


def task1():
    res = []
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    out = (f"Количество жестких дисков - {len(drives)} \n")
    for i in range(len(drives)):
        fs = win32api.GetVolumeInformation(str(drives[i]))[4]
        #print(f"Файловая система диска {drives[i]} - {fs}")
        res.append(f"{drives[i]} file systen is {fs} \n")
        out += str(res[i])
    out += timestamp()
    return out


def task2():
    return (f"Количетсво логических процессоров {win32api.GetSystemInfo()[5]} \n{timestamp()}")


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
            if msg == "!task2":  # Команда на второй таск
                res = bytes(task2(), encoding=ENCODING)
                conn.send(res)
                print("Response sent")
            if msg == "!task1":  # Команда на первый таск
                res = bytes(task1(), encoding=ENCODING)
                conn.send(res)
                print("Response sent")

            print(f"[{addr}] {msg} {timestamp()}")
    conn.close()


def start_server():
    server_a.listen()
    print(f"[LISTENING] Server Alpha is listening on {SERVER}")
    while True:
        conn, addr = server_a.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        conn.send(b"[INFO] Commands:\n"
                  b"!task1 - Drives and their file system\n"
                  b"!task2 - Count of logical processors")


if __name__ == '__main__':
    print("[LAUNCHING] Server Alpha is starting...")
    start_server()
