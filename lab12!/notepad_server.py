import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9999))

users = {} 
print("Serwer działa na porcie 9999...")

while True:
    data, addr = sock.recvfrom(1024)

    if not data:
        if addr in users:
            print(f"Użytkownik {users[addr]} się rozłączył.")
            del users[addr]
        continue

    msg_type = data[0:1]
    content = data[1:].decode('utf-8', errors='ignore')

    if msg_type == b'\0':
        users[addr] = content
        print(f"Użytkownik {content} dołączył z adresu {addr}.")
    elif msg_type == b'\1':
        if addr in users:
            nick = users[addr]
            full_message = f"{nick}: {content}".encode('utf-8')
            for user_addr in users:
                if user_addr != addr:
                    sock.sendto(full_message, user_addr)
        else:
            print(f"Nieznany użytkownik {addr} próbował wysłać wiadomość.")
    else:
        print(f"Nieprawidłowy typ wiadomości od {addr}.")
