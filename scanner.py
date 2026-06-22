import socket
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 135: "Windows RPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 8080: "HTTP-Alt",
}

def grab_banner(host, port, timeout=0.5):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((host, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        return banner[:80]
    except:
        return None

def scan_port(args):
    host, port = args
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    try:
        s.connect((host, port))
        service = COMMON_PORTS.get(port, "Unknown")
        banner = grab_banner(host, port)
        return (port, service, banner)
    except:
        return None
    finally:
        s.close()

host = input("Enter IP to scan: ")
print(f"Scanning {host}...\n")

results = []
ports = [(host, port) for port in range(1, 1025)]

with ThreadPoolExecutor(max_workers=100) as executor:
    for result in executor.map(scan_port, ports):
        if result:
            port, service, banner = result
            if banner:
                print(f"Port {port}: OPEN  ({service})")
                print(f"  Banner: {banner}\n")
            else:
                print(f"Port {port}: OPEN  ({service})")
            results.append({
                "port": port,
                "status": "open",
                "service": service,
                "banner": banner
            })

filename = f"scan_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w") as f:
    json.dump({
        "target": host,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open_ports": results
    }, f, indent=4)

print(f"\nScan complete!")
print(f"Results saved to: {filename}")
