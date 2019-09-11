# Script that outputs the network interfaces on a system with the corresponding IP addresses in CIDR format.  

import subprocess
from ipaddress import IPv4Network

ipv4 = ipv4nm = ipv6 = ipv6nm = iFace = None

def countBits(x):
    x = int(x,16)
    count = 0
    while (x):
        count += x & 1
        x >>= 1
    return count

def foundSomething():
    if ipv4 != None or ipv4nm != None or ipv6 != None or ipv6nm != None or iFace != None:
        return True

def init():
    ipv4 = None
    ipv4nm = None
    ipv6 = None
    ipv6nm = None
    iFace = None

job = subprocess.run("ifconfig", stdout=subprocess.PIPE).stdout.decode('utf-8')
lines = job.splitlines()

for line in lines:
    # print(line)
    if line.find(" flags=") != -1 and line.find("\t") == -1:
        #new iface:
        if foundSomething():
            print("{} - {}/{} - {}/{}".format(iFace,ipv4,ipv4nm,ipv6,ipv6nm))
        else:
            init()
        iFace = line.split(" flags=")[0]

    if line.find("inet ") != -1:
        # print (line)
        ipv4 = line.split("inet ")[1].split(" netmask")[0]
        ipv4nm = countBits(line.split(" ")[3])

    if line.find("scopeid ") != -1: #ipv6
        ipv6 = line.split(" ")[1].split("%")[0]
        ipv6nm = line.split(" ")[3]

print("{} - {}/{} - {}/{}".format(iFace,ipv4,ipv4nm,ipv6,ipv6nm))
