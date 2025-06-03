import socket
import select
import sys

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9999
ADDR = (SERVER_IP, SERVER_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)

nickname = input("Podaj swój nick: ")
sock.sendto(b'\0' + nickname.encode('utf-8'), ADDR)

print("Dołączono. Możesz pisać wiadomości:")

try:
    while True:
        rlist, _, _ = select.select([sock, sys.stdin], [], [])

        for ready in rlist:
            if ready == sock:
                data, _ = sock.recvfrom(1024)
                print(data.decode('utf-8'))
            elif ready == sys.stdin:
                msg = input()
                if msg.strip() == "":
                    sock.sendto(b'', ADDR)
                    print("Rozłączono.")
                    sys.exit(0)
                sock.sendto(b'\1' + msg.encode('utf-8'), ADDR)
except KeyboardInterrupt:
    sock.sendto(b'', ADDR)
    print("\nZamknięto klienta.")
