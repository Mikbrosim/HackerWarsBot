#Import libraries
from selenium import webdriver
from time import sleep, clock, gmtime, strftime
import datetime
import re
import os

#Setup global vars
global ips
ips = []
global btcAddr
btcAddr = []
global btcPass
btcPass = []

########
# To-Do:
# Make the worm not upload ddosvirus to infected machines
# Find BTC info (it kinda works :D )
# Add input for hackedIps in worm.py
# Cleanup ErrorCheck
########

#Import settings if it exists
try: import settings
except NameError: pass

#Set vars from settings
try: debug = settings.debug
except NameError: debug = False

try: signature = settings.signature
except NameError: signature = ""

try: password = settings.password
except NameError: password = ""

try: userName = settings.userName
except NameError: userName = ""

try: firefox = settings.firefox
except NameError: firefox = False

try: breaker = settings.breaker
except NameError: breaker = "None"

try: cracker = settings.cracker
except NameError: cracker = "None"


#Setup Error strings and paths
class Error:
    crackerNotGoodEnough = "Error! Access denied: your cracker is not good enough."
    noCracker = "Error! You do not have the needed software to perform this action."
    login = "Error! This IP is already on your hacked database."
    invalidIp = "Error! Invalid IP address."
    notHacked = "Error! This IP is not on your Hacked Database."
    notUploaded = "Error! You do not have enough disk space to download this software."
    processNotFound = "Error! Process not found."
    fileHidden = "Error! This software already exists on your root folder."

    filePath = "/html/body/div[5]/div[3]/div/div/div[1]/strong"
    ddosPath = "/html/body/div[5]/div[3]/div/div/div/div[2]/div/div[1]/div/div[2]"
    logPath = "/html/body/div[5]/div[3]/div/div[1]/strong"
    notUploadedPath = "/html/body/div[5]/div[3]/div/div[1]/div[2]/strong"
    loginPath = "/html/body/div[5]/div[3]/div/div[1]/div[2]/strong"

#Setup links to the website
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

def Start():
    #Make a dir called logs if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    #Make log file
    global logName
    logName = "logs\\" + datetime.datetime.now().strftime('%Y-%m-%d_%H;%M.log')

    #Start browser
    global browser

    if firefox == True:
        browser = webdriver.Firefox()
    else:
        chromeOptions = webdriver.chrome.options.Options()
        chromeOptions.add_argument('log-level=3')
        browser = webdriver.Chrome(chrome_options=chromeOptions)

    browser.set_window_size(970, 1045)
    browser.set_window_position(0, 0)
    browser.get('http://legacy.hackerexperience.com/')

    #Insert credentials
    loginButton = FindByXpath("""/html/body/div[2]/div[2]/div/div/div/ul/li[1]/a""")
    userNameField = FindByXpath("""//*[@id="login-username"]""")
    userPasswordField = FindByXpath("""//*[@id="password"]""")
    loginButton.click()
    userNameField.send_keys(userName)
    userPasswordField.send_keys(password)

    #Wait for user to login
    WaitForLoad(Links.home, reload = False, errorCheckBool = False)
    Print ("Logged in")

    #Set the yourIP global var to your ip
    global yourIp
    yourIp = YourIp()

def FindByXpath(xpath,errorExpected = True):
    #Find element by xpath, if errorExpected = false wait then wait for the xpath to be there
    if errorExpected:
        return browser.find_element_by_xpath(xpath)
    else:
        while True:
            try:
                return browser.find_element_by_xpath(xpath)
            except:
                sleep(1)

def RemoveElement(element):
	browser.execute_script("""
	var element = arguments[0];
	element.parentNode.removeChild(element);
	""", element)

def PrintDebug(inputString):
    #Write to log and only print to terminal if script is in debug mode
    inputString = str(RoundTime(datetime.datetime.now().time())) + "   " + str(inputString)
    if debug:
        print(inputString)
    file = open(logName,"a")
    file.write(str(inputString) + "\n")
    file.close

def Print(inputString):
    #Write to log and print to terminal
    inputString = str(RoundTime(datetime.datetime.now().time())) + "   " + str(inputString)
    print(inputString)
    file = open(logName,"a")
    file.write(str(inputString) + "\n")
    file.close

def RoundTime(currentTime, secs = 0):
    #Roundtime to nearest second
    newTime = datetime.datetime(100, 1, 1, currentTime.hour, currentTime.minute, currentTime.second)
    returnTime = newTime + datetime.timedelta(seconds=secs)
    return returnTime.time()

def TimerStart():
    #Start timer / reset the start time
    global firstTime
    firstTime = clock()

def TimerStop():
    #Return time since TimerStart()
    return clock() - firstTime

def NewEstimatedTime(input, times):
    #Generate an estimatedTime
    global estimatedTime
    estimatedTime -= (estimatedTime-input)/times

def ClearLog():
    #Clears user log
    browser.get(Links.log)

    logField = browser.find_element_by_name('log')
    editLogButton = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div[2]/form/input[2]""", errorExpected = False)

    logField.clear()
    editLogButton.click()

    #Wait for the operation to finish and load the log site again
    WaitForLoad(Links.log)
    PrintDebug ("Log has been cleared")

def InternetClearLog(ip = "", getIps = False, getBTCs = False):
    #Clear the log on the connected machine
    PrintDebug ("Clearing log on " + ip)
    browser.get(Links.internetLog)
    try:
        internetLogField = FindByXpath("""//*[@id="content"]/div[3]/div/div[3]/div[2]/div/div/div[2]/form/textarea""")
        internetEditLogButton = FindByXpath("""//*[@id="content"]/div[3]/div/div[3]/div[2]/div/div/div[2]/form/input[2]""")
    except:
        if FindByXpath("/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div", errorExpected = False).text == "No logs":
            PrintDebug("No logs to be cleared on " + ip)
            return
        InternetClearLog(ip, getIps, getBTCs)

    #Get log text
    rawLog = internetLogField.text
    logLines = rawLog.split("\n")

    #Get the BtcPass and BtcAddr
    global btcAddr
    global btcPass
    if getBTCs:
        tempBtcAddr = []
        tempBtcPass = []
        for logLine in logLines:
            try:
                tempBtcAddr.append(re.search("[a-zA-Z0-9]{34}", logLine).group())
                tempBtcPass.append(re.search("[a-zA-Z0-9]{64}", logLine).group())
            except:
                pass
        if len(tempBtcAddr) == len(tempBtcPass):
            for i in range(0,len(tempBtcAddr)):
                if tempBtcAddr[-1] not in btcAddr:
                    btcAddr.append(tempBtcAddr.pop())
                    btcPass.append(tempBtcPass.pop())

    #Get ips from the log
    if getIps:
        for logLine in logLines:
            global ips
            foundIpList = re.findall( r'[0-9]+(?:\.[0-9]+){3}', logLine)
            for foundIp in foundIpList:
                if foundIp in ips:
                    continue
                elif foundIp == yourIp:
                    continue
                else:
                    ips.append(foundIp)

    #Clear the log
    internetLogField.clear()
    internetLogField.send_keys(signature)
    internetEditLogButton.click()

    #Wait the log to be cleared
    if WaitForLoad(Links.internetLog, errorPath = Error.logPath) == False:
        if Error.processNotFound == errorText[1]:
            return False
    PrintDebug ("Log has been cleared on " + ip)

def YourIp():
    #Get your ip
    yourIp = FindByXpath("""/html/body/div[5]/div[1]/div/div[1]/span""", errorExpected = False)
    yourIp = yourIp.text
    return yourIp

def Install(software):
    #Install software locally
    PrintDebug ("Installing " + software)
    GetYourSoftware()
    try:
        i = yourSoftwares.index(software)
        PrintDebug(software + " is not in your softwares")
    except:
        return False
    browser.get(Links.install + yourIds[i])
    WaitForLoad(Links.software)
    PrintDebug (software + " installed")
    return True

def Download(software):
    #Download files from harddisk
    PrintDebug ("Downloading " + software)
    GetYourHarddisk()
    try:
        i = harddiskSoftwares.index(software)
    except:
        PrintDebug(software + " is not in harddisk")
        return False
    browser.get(Links.download + harddiskIds[i])
    #WaitForLoad(Links.software)
    if WaitForLoad(Links.software, errorPath=Error.filePath) == False:
        if Error.fileHidden == errorText[1]:
            PrintDebug(software + " is already on machine")
            return False

    PrintDebug (software + " downloaded")
    return True

def InternetInstall(software,ip=""):
    #Install file on internet machine
    PrintDebug ("Installing " + software + " on " + ip)
    GetInternetSoftware(ip)
    try:
        i = softwares.index(software)
    except:
        return False
    browser.get(Links.internetInstall + ids[i])
    WaitForLoad([Links.internet, Links.internetSoftware])
    PrintDebug (software + " installed" + " on " + ip)
    InternetClearLog(ip)
    return True

def InternetHide(software, ip=""):
    #Hide file on internet machine
    PrintDebug ("Hiding " + software + " on " + ip)
    GetInternetSoftware(ip)
    try:
        i = softwares.index(software)
    except:
        return False
    browser.get(Links.internetHide + ids[i])
    WaitForLoad([Links.internet, Links.internetSoftware])
    PrintDebug (software + " hid" + " on " + ip)
    InternetClearLog(ip)
    return True

def InternetUpload(software, ip=""):
    #Upload file to internet machine
    PrintDebug ("Uploading " + software + " on " + ip)
    GetYourSoftware()
    try:
        i = yourSoftwares.index(software)
        if yourIds[i] == "None":
            0/0
    except:
        Download(software)
        InternetUpload(software, ip)

    browser.get(Links.internetUpload + yourIds[i])
    WaitForLoad([Links.internet, Links.internetSoftware], errorPath = Error.notUploadedPath)
    if errorText[1] == Error.notUploaded:
        PrintDebug (software + " could'nt be uploaded" + " on " + ip)
        return False
    PrintDebug (software + " uploaded" + " on " + ip)
    InternetClearLog(ip)
    return True

def WaitForLoad(link, reload = True, errorCheckBool=True, errorPath = "null"):
    #Wait for a website to load
    if WaitForLoadErrorCheck(errorCheckBool,errorPath):
        return False
    ErrorCheck(errorPath)
    PrintDebug ("Wait for " + str(link) + " has loaded")

    while browser.current_url not in link:
        if reload:
            browser.refresh()
            #RemoveElement(FindByXpath('//*[@id="he2"]'), False)
            #RemoveElement(FindByXpath('//*[@id="gritter-notice-wrapper"]'),False)
        sleep(1)
        if WaitForLoadErrorCheck(errorCheckBool,errorPath):
            return False

    return True

def WaitForLoadErrorCheck(errorCheckBool,errorPath):
    #Function used in WaitForLoad, check if an error is present
    if errorPath != "null":
        if errorCheckBool:
            return ErrorCheck(errorPath)
        else:
            ErrorCheck(errorPath)

def ErrorCheck(errorPath):
    #Get string from the errorPath
    global errorText
    try:
        error = FindByXpath(errorPath)
    except:
        errorText = ["","None"]
        return False
    else:
        error = FindByXpath(errorPath.replace("/strong", ""))
        errorText = error.text.split("\n")
        try:
            PrintDebug(errorText)
            errorText.append(errorText[-1])
        except:
            PrintDebug("Error Return False 2")
            errorText = ["","None"]
            return False
        return True

def GetHDD(MB = True):
    #Get HHD returns float or int
    browser.get(Links.internetSoftware)
    fullHDD = FindByXpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[2]/span/font[2]""", errorExpected = False).text
    usedHDD = FindByXpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[2]/span/font[1]""", errorExpected = False).text
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
    #Get Internetspeed returns int or float
    browser.get(Links.internetSoftware)
    internetSpeed = FindByXpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[1]/span/strong""", errorExpected = False).text
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
    #Get all important data from your harddisk
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
                info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[1]")
                link = info.get_attribute('href')
                id = link.replace("https://legacy.hackerexperience.com/software?id=", "")
            except:
                id = "None"

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[2]")
            software = info.text

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[3]")
            version = info.text

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[4]")
            size = info.text

            harddiskSizes.insert(i, size)
            harddiskVersions.insert(i, version)
            harddiskSoftwares.insert(i, software)
            harddiskIds.insert(i, id)
    except:
        pass

def GetYourSoftware():
    #Get all important data from your software
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
                info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[3]")
                link = info.get_attribute('href')
                id = link.replace("https://legacy.hackerexperience.com/software?action=install&id=", "")
                id = id.replace("https://legacy.hackerexperience.com/software?action=uninstall&id=", "")
            except:
                id = "None"

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[2]")
            software = info.text

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[3]")
            version = info.text

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[4]")
            size = info.text

            yourSizes.insert(i, size)
            yourVersions.insert(i, version)
            yourSoftwares.insert(i, software)
            yourIds.insert(i, id)
    except:
        pass

def GetInternetSoftware(ip = "No ip was given"):
    #Get all important data from the connected machines software
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
                info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[3]")
                link = info.get_attribute('href')
                id = link.replace("https://legacy.hackerexperience.com/internet?view=software&cmd=install&id=", "")
                id = id.replace("https://legacy.hackerexperience.com/internet?view=software&cmd=uninstall&id=", "")
            except:
                id = "None"

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[2]")
            software = info.text

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[3]")
            version = info.text

            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[4]")
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

def DDos(ip, times = 1, hack = True, clearLog = True, getSoftware = True):
    #Launch ddos attack against ip x times

    #If script is supposed to hack then do so
    if hack:
        if Hack(ip, clearLog, getSoftware) == False:
            return False

    #Prepare estimatedTime time
    sleep(2)
    global estimatedTime
    estimatedTime = 305

    #Start ddosing x times
    for i in range(0,times):
        TimerStart()

        Print("")
        estimatedTimeLeft = str(RoundTime(datetime.datetime.now().time(), round(estimatedTime * (times-i))))
        Print ("Starting ddos number " + str(i+1) + "/" + str(times) + " against " + ip)
        Print ("This ETA: " + str(round(estimatedTime)) + " seconds, Total ETA: " + estimatedTimeLeft + " seconds")
        browser.get(Links.ddos)

        sleep(1)

        ipField = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""", errorExpected = False)
        try:
            launchDDosButton = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input""")
        except:
            Print ("To ddos you need to have a breaker")
            try:
                if breaker == "None":
                    Print("BREAKER IF, RETURN")
                    return False
                if not Download(breaker):
                    return False
                browser.get(Links.ddos)
                sleep(1)
                ipField = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""")
                launchDDosButton = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input""")
            except:
                Print("DDOS EXCEPT IS NEEDED, RETURN")
                return False

        ipField.send_keys(ip)
        launchDDosButton.click()
        sleep(2)

        WaitForLoad(Links.software, errorPath = Error.ddosPath)
        '''
        if WaitForLoad(Links.software, errorPath = Error.ddosPath) == False:
            if "Success! DDoS attack against " + ip + " launched." == errorText[1]:
                WaitForLoad(Links.software, errorPath= """//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""")
            else:
                return False
        '''
        Print(ip + " has been DDosed, it took " + str(round(TimerStop())) + " seconds")
        NewEstimatedTime(TimerStop(),i+1)

        sleep(3)
    Print("Done DDosing " + ip)

def Hack(ip = "1.2.3.4", clearLog = True, getSoftware = True, getIps = False, getBTCs = False):
    #Hack host
    browser.get(Links.internetLogout)
    browser.get(Links.internetWithIp + ip)
    browser.get(Links.internetHack)
    browser.get(Links.internetBruteforce)
    if ip != FindByXpath("""/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/form/div/input[1]""", errorExpected = False).get_attribute('value'):
        return False

    if WaitForLoad(Links.internetLogin, errorPath=Error.loginPath) == False:
        if Error.crackerNotGoodEnough == errorText[1]:
            return False
        elif Error.noCracker == errorText[1]:
            if cracker == "None":
                Print("CRACKER IF, RETURN")
                return False
            if Download(cracker):
                Install(cracker)
            else:
                return False

            return Hack(ip, clearLog, getSoftware, getIps, getBTCs)
        else:
            WaitForLoad(Links.internetLogin, errorPath=Error.loginPath)

    loginButton = FindByXpath("""/html/body/div[5]/div[3]/div/div[1]/div[3]/div[3]/form/div[3]/span[3]/input""", errorExpected = False)
    loginButton.click()

    if WaitForLoad(Links.internet, errorPath=Error.loginPath) == False:
        if Error.crackerNotGoodEnough == errorText[1]:
            return False
        elif Error.noCracker == errorText[1]:
            if cracker == "None":
                Print("CRACKER IF, RETURN")
                return False
            if Download(cracker):
                Install(cracker)
            else:
                return False

            return Hack(ip, clearLog, getSoftware, getIps, getBTCs)
        else:
            WaitForLoad(Links.internet, errorPath=Error.loginPath)

    Print ("Hacked " + ip)

    if clearLog:
        InternetClearLog(ip, getIps, getBTCs)

    if getSoftware:
        Print ("Getting software information from " + ip)
        GetInternetSoftware(ip)
    return True

def WriteToFiles(ip, minSoftwareVersion, i):
    #WriteToFiles is used for logging
    if minSoftwareVersion <= float(versions[i]):
        with open("software" + str(minSoftwareVersion) + ".txt", "a") as myfile:
            myfile.write(ip + ": " + softwares[i] + " " + versions[i] + " " + sizes[i] + "\n")

if __name__ == "__main__":
	Start()
