HE = __import__("main")
from time import sleep
import re


def Worm(ips, clearLog, getSoftware, yourIp):
    HE.GetYourSoftware()
    hackedIps = []
    hackedIps.append(HE.yourIp)
    print (HE.yourIp)
    for ip in ips:
        HE.ips.append(ip)
        print(ip)
        print(HE.ips)
    while len(HE.ips) >= 1:
        ip = HE.ips[0]
        print("if " + ip + " in " + str(hackedIps))
        print("youtIp is " + HE.yourIp)
        if ip in hackedIps:
            HE.ips.remove(ip)
            print (ip + " is in this list " + hackedIps)
        else:
            HE.ips.remove(ip)
            if HE.Hack(ip, clearLog, getSoftware, getIps = True):
                program(ip)
            hackedIps.append(ip)

def program(ip):
    if HE.Upload("Mikbrosim.vddos"):
        HE.GetSoftware(ip)
        HE.Install("Mikbrosim.vddos")
    else:
        HE.GetSoftware(ip)
