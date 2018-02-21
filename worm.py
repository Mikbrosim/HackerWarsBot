HE = __import__("main")
from time import sleep
import re

def Worm(ips, clearLog, getSoftware, yourIp):
    HE.GetYourSoftware()
    hackedIps = []
    hackedIps.append(HE.YourIp())
    for ip in ips:
        HE.ips.append(ip)
        print(ip)
        print(HE.ips)

    while len(HE.ips) >= 1:
        print ("ips = " + str(HE.ips))
        ip = HE.ips[0]
        if ip in hackedIps:
            HE.ips.remove(ip)
        else:
            HE.ips.remove(ip)
            if HE.Hack(ip, clearLog, getSoftware, getIps = True):
                program(ip)
            hackedIps.append(ip)

def program(ip):
    HE.Upload("Mikbrosim.vddos")
    HE.GetSoftware(ip)
    HE.Install("Mikbrosim.vddos")
