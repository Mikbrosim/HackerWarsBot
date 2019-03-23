HE = __import__("main")
from time import sleep
import re

def Worm(ips, clearLog, getSoftware, hackedIps = []):
    HE.GetYourSoftware()
    hackedIps.append(HE.YourIp())
    for ip in ips:
        HE.ips.append(ip)
    for ip in HE.GetInfectedIps():
        if ip not in hackedIps:
            hackedIps.append(ip)

    while len(HE.ips) >= 1:
        HE.PrintLog ("ips = " + str(HE.ips))
        ip = HE.ips[0]
        if ip in hackedIps:
            HE.ips.remove(ip)
        else:
            HE.ips.remove(ip)
            HE.Print("Starting worm on " + ip)
            if HE.Hack(ip, clearLog, getSoftware, getIps = True, getBTCs = True):
                Program(ip, hackedIps)
            hackedIps.append(ip)

def Program(ip, hackedIps):
    ddosVirus = "Mikbrosim.vddos"
    HE.Print("Infecting " + ip)
    if HE.GetHDD()>= 11:
        internetUpload = HE.InternetUpload(ddosVirus, ip)
        if internetUpload == True:
            HE.InternetInstall(ddosVirus, ip)

        elif internetUpload == "Download":
            if HE.Download(ddosVirus):
                if HE.InternetUpload(ddosVirus, ip):
                    HE.InternetInstall(ddosVirus, ip)

    HE.Print("Done infecting " + ip)
    HE.PrintLog("btcAddr " + str(HE.btcAddr))
    HE.PrintLog("btcPass " + str(HE.btcPass))
    HE.PrintLog("Ips to hack " + str(HE.ips))
    HE.PrintLog("Hacked ips " + str(hackedIps))
