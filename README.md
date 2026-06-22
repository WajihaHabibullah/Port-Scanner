# Port Scanner

A lightweight network port scanner built in Python, inspired by Nmap. Performs TCP connect scanning, service detection, banner grabbing, and saves results as JSON reports.



## Features

- TCP connect scan on any target IP
- Service name detection (FTP, SSH, HTTP, SMB, etc.)
- Banner grabbing — identifies software and version running on open ports
- Multi-threaded scanning — 100 ports scanned simultaneously for fast results
- JSON report generation with timestamp



## How It Works

The scanner sends TCP connection requests to each port on the target host and analyzes the response:

| Response | Status |
|---|---|
| Connection accepted | `OPEN` |
| Connection refused | `CLOSED` |
| No response / timeout | `FILTERED` |

For every open port, a banner grab is attempted — the scanner sends an HTTP HEAD request and reads the service response, revealing software name and version (e.g. `Apache/2.4`, `OpenSSH_8.2`, `Pure-FTPd`).



## Technologies Used

- Python 3
- `socket` — TCP connection and banner grabbing
- `concurrent.futures.ThreadPoolExecutor` — multi-threading
- `json` — report generation
- `datetime` — timestamped output files


## Installation

No external dependencies required — uses Python standard library only.

```bash
git clone https://github.com/WajihaHabibullah/Port-Scanner.git
cd Port-Scanner
python scanner.py
```


## Usage

```bash
python scanner.py
Enter IP to scan: 127.0.0.1
```

You can scan:
- `127.0.0.1` — your own machine (localhost)
- Any IP on your local network (e.g. `192.168.1.1`)
- Any public IP you have permission to scan


## Sample Output

```
Scanning 192.168.1.100...

Port 21: OPEN  (FTP)
  Banner: 220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------

Port 22: OPEN  (SSH)

Port 80: OPEN  (HTTP)
  Banner: HTTP/1.1 302 Found
          Server: Apache

Port 143: OPEN  (IMAP)
  Banner: * OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS]

Port 443: OPEN  (HTTPS)
  Banner: HTTP/1.1 302 Found
          Server: Apache

Scan complete!
Results saved to: scan_192.168.1.100_20260622_145826.json
```


## Sample JSON Report

{
    "target": "192.168.1.100",
    "scan_time": "2026-06-22 14:58:26",
    "open_ports": [
        {
            "port": 21,
            "status": "open",
            "service": "FTP",
            "banner": "220---------- Welcome to Pure-FTPd [privsep] [TLS]"
        },
        {
            "port": 22,
            "status": "open",
            "service": "SSH",
            "banner": null
        },
        {
            "port": 80,
            "status": "open",
            "service": "HTTP",
            "banner": "HTTP/1.1 302 Found\nServer: Apache"
        }
    ]
}



## Real World Application

Banner grabbing reveals exact software versions running on a target. These version numbers can then be cross-referenced with public vulnerability databases (CVE) to identify known security issues — this is the core workflow of the **reconnaissance phase** in penetration testing.

Example from a real scan:
- Scanner found `Exim 4.99.4` on port 26
- Cross-referenced with NVD (nvd.nist.gov)
- Confirmed server was running the latest patched version — no action needed



## Legal & Ethical Notice

> Only scan systems you own or have **explicit written permission** to test.
> Unauthorized port scanning may be illegal under cybersecurity laws including Pakistan's PECA 2016.
> This tool is intended for educational purposes and authorized security assessments only.



## Author

**Wajiha Habibullah**  
CS Student — NUCES FAST, Karachi  
[github.com/WajihaHabibullah](https://github.com/WajihaHabibullah)



## Related Projects

- [DNS Query Resolver](https://github.com/WajihaHabibullah/DNS-Query-Resolver-)
