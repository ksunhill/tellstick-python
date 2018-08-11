#!/usr/bin/env python
# -*- coding: utf-8 -*-



import socket, re, tellstick

PORT = 42314
HOST = ""
VERSIONS = ['X','K']

UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
UDP.setblocking(True)
UDP.settimeout(3)

UDP.bind((HOST, PORT))

print "[*] Searching for TellStick Net"
UDP.sendto("D", ('255.255.255.255',30303))

ip = None

while True:
    try:
        (msg, (ip, port)) = UDP.recvfrom(2048)
    except socket.error, e:
        break
    info = re.findall('(.+):(.+):(.+):(.+)', msg)[0]
    print "[*] Found %s on %s. Firmware version %s" % (info[0], ip, info[3])

    if(info[3] in VERSIONS):
        print "[+] Version approved, let's use it!"
        break
    else:
        print "[-] Not approved firmware, keep looking"

if(ip == None):
    print "[-] No TellStick Net found."
    print "[*] Waiting for broadcast"
    UDP.close()
    UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP.bind(('', PORT))
    while True:
        try:
            (msg, (ip, port)) = UDP.recvfrom(2048)
        except socket.error:
            pass

        version = re.findall("Telldus TellStick Net v(.+)", msg)[0][0]
        if version  in VERSIONS:
            print "[+] Found an approved firmware"
            UDP.close()
            UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDP.bind((HOST, PORT))
            break

print "[*] Sending reglistener command"
UDP.sendto("B:reglistener", (ip, 42314))

msg = None

while True:
    try:
        (msg, (ip, port)) = UDP.recvfrom(2048)
    except socket.error:
        pass

    if msg:
        try:
            print "[+] Received: %s" % msg
            print "... %s" % str(tellstick.parse(msg))
        except Exception, e:
            print "[-] Exception: %s" % e
        msg = None


