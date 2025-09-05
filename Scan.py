import os
import sys
import time
import socket
import threading
from time import sleep
from pyfiglet import Figlet

GREEN = '\033[32m'
BLUE = '\033[36m'
RED = '\033[31m'
YELLOW = '\033[33m'
RESET = '\033[0m'
 
 
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    f = Figlet(font='big')
    ascii_art = f.renderText('HR Team')
    print(GREEN + ascii_art + RESET)

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389]
COMMON_PORTS_NAMES = ["FTP", "SSH", "Telnet", "SMTP", "DNS", "HTTP", "POP3", "IMAP", "HTTPS", "SMB", "RDP"]

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return True
        else:
            return False
    except:
        return False

def perform_scan(host):
    open_ports = []

    def worker(port):
        if scan_port(host, port):
            open_ports.append(port)

    threads = []
    for port in COMMON_PORTS:
        t = threading.Thread(target=worker, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return open_ports

def main():
    while True:
        clear_screen()
        display_banner()
        print(f"{YELLOW}1. {YELLOW}Nmap Scan{RESET}")
        print(f"{YELLOW}2. {YELLOW}Exit{RESET}")
        choice = input(f"{YELLOW}Select an option (1 or 2): {RESET}")

        if choice == '1':
            url_input = input(f"{GREEN}Enter the website URL to scan: {RESET}")
            print(f"{BLUE}Resolving host...{RESET}")
            try:
                host_ip = socket.gethostbyname(url_input)
                print(f"{BLUE}Host resolved: {host_ip}{RESET}")
            except socket.gaierror:
                print(f"{RED}Error: Unable to resolve hostname.{RESET}")
                input("Press Enter to continue...")
                continue

            print(f"{BLUE}Starting scan on {host_ip}...{RESET}")
            open_ports = perform_scan(host_ip)

            if open_ports:
                print(f"{BLUE}Open Ports:{RESET}")
                for port in sorted(open_ports):
                    print(f" - Port {port}: ", end='')
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result = sock.connect_ex((host_ip, port))
                        sock.close()
                        if result == 0:
                            print("Open")
                        else:
                            print("Closed")
                    except:
                        print("Error")
            else:
                print(f"{YELLOW}No common ports are open on {host_ip}.{RESET}")

            input("Press Enter to continue...")
        elif choice == '2':
            break

if __name__ == "__main__":
    main()
