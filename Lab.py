addr = "78.100.240.0/25"

addr = addr.split('/')

ip = addr[0]
mask = int(addr[1])

ip = ip.split('.')
ip = (int(ip[0]) << 24) | (int(ip[1]) << 16) | (int(ip[2]) << 8) | int(ip[3])

ip_mask = int(mask * "1" + (32-mask) * "0", 2)

net_ip = ip & ip_mask
not_mask = ~ip_mask
broadcast = net_ip | ~ip_mask & 0xFFFFFFFF

host_number = max(0, 2**(32-mask)-2)

host1 = net_ip + 1 if mask < 31 else None
host_last = broadcast - 1 if mask < 31 else None

def ip_to_str(ip):
    return f"{(ip >> 24) & 0xFF}.{(ip >> 16) & 0xFF}.{(ip >> 8) & 0xFF}.{ip & 0xFF}"

def print_ip():
    print(f"Adres IP sieci: {ip_to_str(net_ip)}")
    print(f"Maska podsieci: {ip_to_str(ip_mask)}")
    print(f"Ilość hostów w sieci: {host_number}")
    print(f"Pierwszy adres IP hosta: {ip_to_str(host1) if host1 else 'Brak dostępnych hostów'}")
    print(f"Ostatni adres IP hosta: {ip_to_str(host_last) if host_last else 'Brak dostępnych hostów'}")
    print(f"Adres broadcast: {ip_to_str(broadcast)}")

print_ip()