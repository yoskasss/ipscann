import socket
import os
from multiprocessing import Pool

def ping_ip(ip):
    """Belirli bir IP adresini ping ile kontrol et."""
    response = os.system(f"ping -c 1 -w 1 {ip}")  # Linux/Mac için '-c 1', Windows için '-n 1'
    if response == 0:
        return ip
    else:
        return None

def get_local_ips_and_hostnames():
    """Yerel ağdaki IP'leri ve hostnameleri al"""
    local_ip = socket.gethostbyname(socket.gethostname())
    network = '.'.join(local_ip.split('.')[:-1]) + '.'

    # Tüm cihaz IP'lerini taramak için 1'den 254'e kadar olan aralığı kullan
    ip_range = [f"{network}{i}" for i in range(1, 255)]

    # Paralel ping işlemleri
    with Pool(20) as p:
        alive_ips = p.map(ping_ip, ip_range)

    devices = []
    for ip in alive_ips:
        if ip is not None:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = "Unknown"
            devices.append((ip, hostname))

    return devices

# Tüm cihazları listele
devices = get_local_ips_and_hostnames()
print("Yerel ağdaki cihazlar:")
for ip, hostname in devices:
    print(f"IP: {ip}, Hostname: {hostname}")
