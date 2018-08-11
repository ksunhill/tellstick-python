#!/usr/bin/env python
# -*- coding: utf-8 -*-



import socket, re, sys

PORT = 42314
HOST = ""
VERSIONS = ['X']

if len(sys.argv) <= 1:
	print "[-] Missing command string"
	exit()

UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
UDP.setblocking(True)
UDP.settimeout(3)

UDP.bind((HOST, PORT))

print "[*] Searching for TellStick Net"
UDP.sendto("D", ('255.255.255.255',30303))

ip = "192.168.1.11"


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
    exit()

print "[*] Sending command"
cmd = sys.argv[1]
msg = "4:sendh1:S%X:%ss" % (len(cmd), cmd)
# print "... %s" % msg
UDP.sendto(msg, (ip, PORT))
