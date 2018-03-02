from selenium import webdriver
from time import sleep, clock, gmtime, strftime
import datetime
import re
import os

global ips
ips = []

debug = False

try:
    import settings
    debug = settings.debug
except:
    pass


########
# To-Do:
# Fix the worm functions (download, upload, install)
# Add input for hackedIps in worm.py
########

class Error:
    crackerNotGoodEnough = "Error! Access denied: your cracker is not good enough."
    noCracker = "Error! You do not have the needed software to perform this action."
    login = "Error! This IP is already on your hacked database."
    loginPath = """/html/body/div[5]/div[3]/div/div[1]/div[2]/strong"""
    invalidIp = "Error! Invalid IP address."
    notHacked = "Error! This IP is not on your Hacked Database."
    ddosPath = """/html/body/div[5]/div[3]/div/div/div[1]/strong"""
    processNotFound = "Error! Process not found."
    logPath = """/html/body/div[5]/div[3]/div/div[1]/strong"""
    notUploadedPath = "/html/body/div[5]/div[3]/div/div[1]/div[2]/strong"
    notUploaded = "Error! You do not have enough disk space to download this software."


class Links:
    log = 'https://legacy.hackerexperience.com/log'
    home = 'https://legacy.hackerexperience.com/index.php'
    ddos = 'https://legacy.hackerexperience.com/list?action=ddos'
    software = 'https://legacy.hackerexperience.com/software'
    internet = 'https://legacy.hackerexperience.com/internet'
    harddisk = 'https://legacy.hackerexperience.com/software?page=external'
    download = harddisk + "&action=download&id="
    install = software + '?action=install&id='
    internetWithIp = internet + '?ip='
    internetHack = internet + '?action=hack'
    internetBruteforce = internet + '?action=hack&method=bf'
    internetLogin = internet + '?action=login'
    internetLog = internet + '?view=logs'
    internetSoftware = internet + '?view=software'
    internetLogout = internet + '?view=logout'
    internetInstall = internet + '?view=software&cmd=install&id='
    internetUpload = internet + '?view=software&cmd=up&id='
    internetHide = internet + '?view=software&cmd=hide&id='

def Main():
    Start()

def Start():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    global logName
    logName = "logs\\" + datetime.datetime.now().strftime('%Y-%m-%d_%H;%M.log')

    global browser
    browser = webdriver.Firefox()
    browser.set_window_size(970, 1045)
    #browser.maximize_window()
    browser.set_window_position(0, 0)
    browser.get('http://legacy.hackerexperience.com/')

    loginButton = browser.find_element_by_xpath("""/html/body/div[2]/div[2]/div/div/div/ul/li[1]/a""")
    userNameField = browser.find_element_by_xpath("""//*[@id="login-username"]""")
    userPasswordField = browser.find_element_by_xpath("""//*[@id="password"]""")
    loginButton.click()
    userNameField.send_keys(settings.userName)
    try:
        userPasswordField.send_keys(settings.password)
    except:
        pass

    WaitForLoad(Links.home, reload = False, errorCheckBool = False)
    Print ("Logged in")

    global yourIp
    yourIp = YourIp()

def PrintDebug(inputString):
    inputString = str(RoundTime(datetime.datetime.now().time())) + "   " + str(inputString)
    if debug:
        print(inputString)
    file = open(logName,"a")
    file.write(str(inputString) + "\n")
    file.close

def Print(inputString):
    inputString = str(RoundTime(datetime.datetime.now().time())) + "   " + str(inputString)
    print(inputString)
    file = open(logName,"a")
    file.write(str(inputString) + "\n")
    file.close

def RoundTime(ct, secs = 0):
    ct = datetime.datetime(100, 1, 1, ct.hour, ct.minute, ct.second)
    ct = ct + datetime.timedelta(seconds=secs)
    return ct.time()

def TimerStart():
    global firstTime
    firstTime = clock()

def TimerStop():
    return clock() - firstTime

def NewEta(input, times):
    global etaTime
    etaTime -= (etaTime-input)/times
    PrintDebug (etaTime)

def ClearLog():
    browser.get(Links.log)

    logField = browser.find_element_by_name('log')
    editLogButton = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div[2]/form/input[2]""")

    logField.clear()
    editLogButton.click()

    WaitForLoad(Links.log)
    Print ("Log has been cleared")


def InternetClearLog(ip = "", getIps = False):
    browser.get(Links.internetLog)
    try:
        internetLogField = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div[3]/div[2]/div/div/div[2]/form/textarea""")
        internetEditLogButton = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div[3]/div[2]/div/div/div[2]/form/input[2]""")
    except:
        InternetClearLog(ip, getIps)
        return

    if getIps:
        rawLog = internetLogField.text
        global ips
        logLines = rawLog.split("\n")
        for logLine in logLines:
            foundIpList = re.findall( r'[0-9]+(?:\.[0-9]+){3}', logLine)
            for foundIp in foundIpList:
                if foundIp in ips:
                    continue
                elif foundIp == yourIp:
                    continue
                else:
                    ips.append(foundIp)

    internetLogField.clear()
    try:
        internetLogField.send_keys(settings.signature)
    except:
        pass
    internetEditLogButton.click()

    if WaitForLoad(Links.internetLog, errorPath = Error.logPath) == False:
        if Error.processNotFound == errorText[1]:
            return False
    Print ("Log has been cleared on " + ip)

def YourIp():
    yourIp = browser.find_element_by_xpath("""/html/body/div[5]/div[1]/div/div[1]/span""")
    yourIp = yourIp.text
    return yourIp

def Install(software):
    PrintDebug ("Installing " + software)
    GetYourSoftware()
    try:
        i = yourSoftwares.index(software)
    except:
        return False
    browser.get(Links.install + yourIds[i])
    WaitForLoad(Links.software)
    PrintDebug (software + " installed")
    return True

def Download(software):
    PrintDebug ("Downloading " + software)
    GetYourHarddisk()
    try:
        i = harddiskSoftwares.index(software)
    except:
        return False
    browser.get(Links.download + harddiskIds[i])
    WaitForLoad(Links.software)
    PrintDebug (software + " downloaded")
    return True

def InternetInstall(software,ip):
    PrintDebug ("Installing " + software)
    GetSoftware(ip)
    try:
        i = softwares.index(software)
    except:
        return False
    browser.get(Links.internetInstall + ids[i])
    WaitForLoad([Links.internet, Links.internetSoftware])
    PrintDebug (software + " installed")
    InternetClearLog()
    return True

def InternetHide(software):
    PrintDebug ("Hiding " + software)
    GetSoftware(ip)
    try:
        i = softwares.index(software)
    except:
        return False
    browser.get(Links.internetHide + ids[i])
    WaitForLoad([Links.internet, Links.internetSoftware])
    PrintDebug (software + " hid")
    InternetClearLog()
    return True

def InternetUpload(software):
    PrintDebug ("Uploading " + software)
    GetYourSoftware()
    try:
        i = yourSoftwares.index(software)
    except:
        Download(software)
        InternetUpload(software)
    browser.get(Links.internetUpload + yourIds[i])
    WaitForLoad([Links.internet, Links.internetSoftware], errorPath = Error.notUploadedPath)
    if errorText[1] == Error.notUploaded:
        PrintDebug (software + " could'nt be uploaded")
        return False
    PrintDebug (software + " uploaded")
    InternetClearLog()
    return True

def WaitForLoadErrorCheck(errorCheckBool,errorPath):
    if errorPath != "null":
        if errorCheckBool:
            if ErrorCheck(errorPath):
                return True
        else:
            ErrorCheck(errorPath)

def WaitForLoad(link, reload = True, errorCheckBool=True, errorPath = "null"):
    if WaitForLoadErrorCheck(errorCheckBool,errorPath):
        return False
    ErrorCheck(errorPath)
    PrintDebug ("Wait for " + str(link) + " has loaded")
    if isinstance(link, list):
        while browser.current_url not in link:
            if reload:
                browser.refresh()
            sleep(1)
            if WaitForLoadErrorCheck(errorCheckBool,errorPath):
                return False
    else:
        while browser.current_url != link:
            if reload:
                browser.refresh()
            sleep(1)
            if WaitForLoadErrorCheck(errorCheckBool,errorPath):
                return False
    return True

def ErrorCheck(errorPath):
    global errorText
    try:
        error = browser.find_element_by_xpath(errorPath)
    except:
        pass
        return False
    else:
        error = browser.find_element_by_xpath(errorPath.replace("/strong", ""))
        errorText = error.text.split("\n")
        try:
            PrintDebug(errorText[1])
        except:
            pass
        return True

def GetHDD(MB = True):
    browser.get(Links.internetSoftware)
    fullHDD = browser.find_element_by_xpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[2]/span/font[2]""").text
    usedHDD = browser.find_element_by_xpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[2]/span/font[1]""").text
    if "GB" in fullHDD:
        fullHDD = float(fullHDD.replace(" GB", ""))
        fullHDD *= 1000
    else:
        fullHDD = float(fullHDD.replace(" MB", ""))

    if "GB" in usedHDD:
        usedHDD = float(usedHDD.replace(" GB", ""))
        usedHDD *= 1000
    else:
        usedHDD = float(usedHDD.replace(" MB", ""))

    if MB:
        return int(fullHDD - usedHDD)
    else:
        return (fullHDD - usedHDD)/1000

def GetInternetSpeed(Mbit = True):
    browser.get(Links.internetSoftware)
    internetSpeed = browser.find_element_by_xpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[1]/span/strong""").text
    if "Gbit" in internetSpeed:
        internetSpeed = int(internetSpeed.replace(" Gbit", ""))
        internetSpeed *= 1000
    else:
        internetSpeed = int(internetSpeed.replace(" Mbit", ""))

    if Mbit:
        return internetSpeed
    else:
        return internetSpeed/1000

def GetYourHarddisk():
    browser.get(Links.harddisk)
    global harddiskIds
    global harddiskSoftwares
    global harddiskVersions
    global harddiskSizes
    harddiskIds = ["None"]
    harddiskSoftwares = ["None"]
    harddiskVersions = ["None"]
    harddiskSizes = ["None"]
    i = 0
    PrintDebug("Getting harddisk software")
    try:
        while True:
            i += 1
            baseXpath = "/html/body/div[5]/div[3]/div/div/div/div[2]/div[1]/table/tbody/"

            try:
                info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[1]")
                link = info.get_attribute('href')
                id = link.replace("https://legacy.hackerexperience.com/software?id=", "")
            except:
                id = "None"

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[2]")
            software = info.text

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[3]")
            version = info.text

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[4]")
            size = info.text

            harddiskSizes.insert(i, size)
            harddiskVersions.insert(i, version)
            harddiskSoftwares.insert(i, software)
            harddiskIds.insert(i, id)
    except:
        pass

def GetYourSoftware():
    browser.get(Links.software)
    global yourIds
    global yourSoftwares
    global yourVersions
    global yourSizes
    yourIds = ["None"]
    yourSoftwares = ["None"]
    yourVersions = ["None"]
    yourSizes = ["None"]
    i = 0
    PrintDebug("Getting your software")
    try:
        while True:
            i += 1
            baseXpath = "/html/body/div[5]/div[3]/div/div/div/div[2]/div/table/tbody/"

            try:
                info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[3]")
                link = info.get_attribute('href')
                id = link.replace("https://legacy.hackerexperience.com/software?action=install&id=", "")
                id = id.replace("https://legacy.hackerexperience.com/software?action=uninstall&id=", "")
            except:
                id = "None"

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[2]")
            software = info.text

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[3]")
            version = info.text

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[4]")
            size = info.text

            yourSizes.insert(i, size)
            yourVersions.insert(i, version)
            yourSoftwares.insert(i, software)
            yourIds.insert(i, id)
    except:
        pass


def DDos(ip, times = 1, hack = True, clearLog = True, getSoftware = True):
    if hack:
        if Hack(ip, clearLog, getSoftware) == False:
            return False

    sleep(2)
    global etaTime
    etaTime = 300

    for i in range(0,times):
        TimerStart()

        print("")
        etaTimeLeft = str(RoundTime(datetime.datetime.now().time(), round(etaTime * (times-i))))
        Print ("Starting ddos number " + str(i+1) + "/" + str(times) + " against " + ip)
        Print ("This ETA: " + str(round(etaTime)) + " seconds, Total ETA: " + etaTimeLeft + " seconds")
        browser.get(Links.ddos)

        sleep(1)

        ipField = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""")
        try:
            launchDDosButton = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input""")
        except:
            Print ("To ddos you need to have a breaker")
            try:
                Download(settings.breaker)
                browser.get(Links.ddos)
                sleep(1)
                ipField = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""")
                launchDDosButton = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input""")
            except:
                pass
                return

        ipField.send_keys(ip)
        launchDDosButton.click()
        sleep(2)

        if WaitForLoad(Links.software, errorPath = Error.ddosPath) == False:
            if "Success! DDoS attack against " + ip + " launched." == errorText[1]:
                WaitForLoad(Links.software, errorPath= """//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""")
            else:
                return False
        Print(ip + " has been DDosed, it took " + str(round(TimerStop())) + " seconds")
        NewEta(TimerStop(),i+1)

        sleep(3)
    Print("Done DDosing " + ip)

def Hack(ip = "1.2.3.4", clearLog = True, getSoftware = True, getIps = False):
    browser.get(Links.internetLogout)
    browser.get(Links.internetWithIp + ip)
    browser.get(Links.internetHack)
    browser.get(Links.internetBruteforce)
    if ip != browser.find_element_by_xpath("""/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/form/div/input[1]""").get_attribute('value'):
        return False

    if WaitForLoad(Links.internetLogin, errorPath=Error.loginPath) == False:
        if Error.crackerNotGoodEnough == errorText[1]:
            return False
        elif Error.noCracker == errorText[1]:
            return False
        else:
            WaitForLoad(Links.internetLogin, errorPath=Error.loginPath)

    loginButton = browser.find_element_by_xpath("""/html/body/div[5]/div[3]/div/div[1]/div[3]/div[3]/form/div[3]/span[3]/input""")
    loginButton.click()

    if WaitForLoad(Links.internet, errorPath=Error.loginPath) == False:
        if Error.crackerNotGoodEnough == errorText[1]:
            return False
        elif Error.noCracker == errorText[1]:
            return False
        else:
            WaitForLoad(Links.internet, errorPath=Error.loginPath)

    Print ("Hacked " + ip)

    if clearLog:
        Print ("Clearing log on " + ip)
        InternetClearLog(ip, getIps)

    if getSoftware:
        Print ("Getting software information from " + ip)
        GetSoftware(ip)
    return True

def GetSoftware(ip = "No ip was given"):
    browser.get(Links.internetSoftware)
    global ids
    global softwares
    global versions
    global sizes
    ids = ["None"]
    softwares = ["None"]
    versions = ["None"]
    sizes = ["None"]
    i = 0
    PrintDebug("Getting software from " + ip)
    try:
        while True:
            i += 1
            baseXpath = "/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[1]/table/tbody/"

            try:
                info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[3]")
                link = info.get_attribute('href')
                id = link.replace("https://legacy.hackerexperience.com/internet?view=software&cmd=install&id=", "")
                id = id.replace("https://legacy.hackerexperience.com/internet?view=software&cmd=uninstall&id=", "")
            except:
                id = "None"

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[2]")
            software = info.text

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[3]")
            version = info.text

            info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[4]")
            size = info.text

            sizes.insert(i, size)
            versions.insert(i, version)
            softwares.insert(i, software)
            ids.insert(i, id)
            WriteToFiles(ip, 2, i)
            for j in range(1,10):
                WriteToFiles(ip, j*10, i)
    except:
        pass

def WriteToFiles(ip, minSoftwareVersion, i):
    if minSoftwareVersion <= float(versions[i]):
        with open("software" + str(minSoftwareVersion) + ".txt", "a") as myfile:
            myfile.write(ip + ": " + softwares[i] + " " + versions[i] + " " + sizes[i] + "\n")

if __name__ == "__main__":
	Main()
