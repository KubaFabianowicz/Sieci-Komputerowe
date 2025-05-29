import socket
import os
import sys

DEFAULT_PORT = 80
BUFFER_SIZE = 1024
HTTP_HEADER_TEMPLATE = (
    "HTTP/1.0 200 OK\r\n"
    "Content-Type: text/plain; charset=UTF-8\r\n"
    "Connection: close\r\n"
    "Content-Length: {length}\r\n"
    "\r\n"
)

def get_uptime():
    with open("/proc/uptime", "r") as f:
        return f.read().split()[0] + "\n"

def main():
    if os.getuid() == 0:
        print("Nie uruchamiaj tego programu jako root!", file=sys.stderr)
        sys.exit(1)

    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    print(f"Serwer działa na porcie {port}...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Połączono z {addr}")

            request = client_socket.recv(BUFFER_SIZE)  
            print(f"Otrzymano zapytanie:\n{request.decode(errors='ignore')}")

            uptime = get_uptime()
            response_headers = HTTP_HEADER_TEMPLATE.format(length=len(uptime))
            response = response_headers + uptime

            client_socket.sendall(response.encode("utf-8"))
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()
            print("Zamknięto połączenie.\n")

    except KeyboardInterrupt:
        print("\nZamykam serwer.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()


#uruchomienie
#python3 serwer.py 8080
#testowanie
#nc localhost 8080
# 0.0.0.0 akceptuje polaczenia z zewnatrz
# 127.0.0.1 - tylko polaczenie lokalne, z zewnatrz nikt sie nie polaczy