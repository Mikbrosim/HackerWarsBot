from selenium import webdriver
from time import sleep
import re

global ips
ips = []

class OtherVars:
    userName = "Mikbrosim5"
    signature ="You was hacked by... NameError: name 'userName' is not defined"

class Error:
    crackerNotGoodEnough = "Error! Access denied: your cracker is not good enough."
    login = "Error! This IP is already on your hacked database."
    loginPath = """/html/body/div[5]/div[3]/div/div[1]/div[2]"""
    invalidIp = "Error! Invalid IP address."
    notHacked = "Error! This IP is not on your Hacked Database."
    ddosPath = """/html/body/div[5]/div[3]/div/div/div[1]/strong"""
    processNotFound = "Error! Process not found."
    logPath = """/html/body/div[5]/div[3]/div/div[1]/strong"""


class Links:
    log = 'https://legacy.hackerexperience.com/log'
    home = 'https://legacy.hackerexperience.com/index.php'
    ddos = 'https://legacy.hackerexperience.com/list?action=ddos'
    software = 'https://legacy.hackerexperience.com/software'
    internet = 'https://legacy.hackerexperience.com/internet'
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
    global browser
    browser = webdriver.Firefox()
    browser.set_window_size(970, 1045)
    #browser.maximize_window()
    browser.set_window_position(0, 0)
    browser.get('http://legacy.hackerexperience.com/')

    loginButton = browser.find_element_by_xpath("""/html/body/div[2]/div[2]/div/div/div/ul/li[1]/a""")
    userNameField = browser.find_element_by_xpath("""//*[@id="login-username"]""")
    loginButton.click()
    userNameField.send_keys(OtherVars.userName)

    WaitForLoad(Links.home, reload = False, errorCheckBool = False)
    print ("Logged in")

    global yourIp
    yourIp = browser.find_element_by_xpath("""/html/body/div[5]/div[1]/div/div[1]/span""")
    yourIp = yourIp.text

def ClearLog():
    browser.get(Links.log)

    logField = browser.find_element_by_name('log')
    editLogButton = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div[2]/form/input[2]""")

    logField.clear()
    editLogButton.click()

    WaitForLoad(Links.log)
    print ("Log has been cleared")

def InternetClearLog(ip = "", getIps = False):
    browser.get(Links.internetLog)
    internetLogField = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div[3]/div[2]/div/div/div[2]/form/textarea""")
    internetEditLogButton = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div[3]/div[2]/div/div/div[2]/form/input[2]""")

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
    internetLogField.send_keys(OtherVars.signature)
    internetEditLogButton.click()

    if WaitForLoad(Links.internetLog, errorPath = Error.logPath) == False:
        if Error.processNotFound == errorText[1]:
            return False
    print ("Log has been cleared on " + ip)

def Install(software):
    print ("Installing " + software)
    i = softwares.index(software)
    browser.get(Links.internetInstall + ids[i])
    WaitForLoad(Links.internetSoftware)
    print (software + " installed")
    InternetClearLog()
    return True

def Hide(software):
    print ("Hiding " + software)
    i = softwares.index(software)
    browser.get(Links.internetHide + ids[i])
    WaitForLoad(Links.internetSoftware)
    print (software + " hid")
    InternetClearLog()
    return True

def Upload(software):
    print ("Uploading " + software)
    i = yourSoftwares.index(software)
    browser.get(Links.internetUpload + yourIds[i])
    WaitForLoad(Links.internetSoftware)
    print (software + " uploaded")
    InternetClearLog()
    return True

def WaitForLoad(link, reload = True, errorCheckBool=True, errorPath = "null"):
    if errorCheckBool:
        if ErrorCheck(errorPath):
            return False
    while browser.current_url != link:
        if reload:
            browser.refresh()
        sleep(1)
        if errorCheckBool:
            if errorPath == "null":
                print("errorPath = null cant check for errors")
            else:
                if ErrorCheck(errorPath):
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
        errorText = error.text.split("\n")
        print(errorText[1])
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
    try:
        while True:
            i += 1
            baseXpath = "/html/body/div[5]/div[3]/div/div/div/div[2]/div/table/tbody/"

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

            yourSizes.insert(i, size)
            yourVersions.insert(i, version)
            yourSoftwares.insert(i, software)
            yourIds.insert(i, id)
    except:
        pass


def DDos(ip, times = 1, hack = True, clearLog = True, getSoftware = True):
    if hack:
        Hack(ip, clearLog, getSoftware)

    sleep(2)
    for i in range(0,times):
        browser.get(Links.ddos)

        sleep(1)

        ipField = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""")
        launchDDosButton = browser.find_element_by_xpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input""")

        ipField.send_keys(ip)
        launchDDosButton.click()
        sleep(2)

        if WaitForLoad(Links.software, errorPath = Error.ddosPath) == False:
            continue
        print (ip + " has been DDosed")

        sleep(3)
    print("Done DDosing " + ip)

def Hack(ip = "1.2.3.4", clearLog = True, getSoftware = True, getIps = False):
    browser.get(Links.internetLogout)
    browser.get(Links.internetWithIp + ip)
    browser.get(Links.internetHack)
    browser.get(Links.internetBruteforce)

    if WaitForLoad(Links.internetLogin, errorPath=Error.loginPath) == False:
        if Error.crackerNotGoodEnough == errorText[1]:
            return False

    loginButton = browser.find_element_by_xpath("""//*[@id="loginform"]/div[3]/span[3]/input""")
    loginButton.click()

    if WaitForLoad(Links.internet, errorPath=Error.loginPath) == False:
        if Error.crackerNotGoodEnough == errorText[1]:
            return False
    print ("Hacked " + ip)

    if clearLog:
        print ("Clearing log on " + ip)
        InternetClearLog(ip, getIps)

    if getSoftware:
        print ("Getting software information from " + ip)
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
    try:
        while True:
            i += 1
            baseXpath = "/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[1]/table/tbody/"

            try:
                info = browser.find_element_by_xpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[1]")
                link = info.get_attribute('href')
                id = link.replace("https://legacy.hackerexperience.com/internet?view=software&id=", "")
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
