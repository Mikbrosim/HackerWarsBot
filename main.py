import pickle, re, os, datetime, colorama
from selenium import webdriver
from time import sleep, clock, gmtime, strftime

#Setup global vars
global ips
ips = []
global btcAddr
btcAddr = []
global btcPass
btcPass = []

########
# To-Do:
########

class Links:
    #Setup links to the website
    base = 'https://legacy.hackerexperience.com/'
    log = base + 'log'
    index = base + 'index'
    home = base + 'index.php'
    ddos = base + 'list?action=ddos'
    software = base + 'software'
    internet = base + 'internet'
    harddisk = base + 'software?page=external'
    hardware = base + 'hardware'
    processes = base + 'processes'
    download = harddisk + "&action=download&id="
    install = software + '?action=install&id='
    uninstall = software + '?action=uninstall&id='
    delete = software + '?action=del&id='
    hide = software + '?action=hide&id='
    information = software + '?id='
    internetWithIp = internet + '?ip='
    internetHack = internet + '?action=hack'
    internetBruteforce = internet + '?action=hack&method=bf'
    internetLogin = internet + '?action=login'
    internetLog = internet + '?view=logs'
    internetSoftware = internet + '?view=software'
    internetLogout = internet + '?view=logout'
    internetInstall = internetSoftware + '&cmd=install&id='
    internetUninstall = internetSoftware + '&cmd=uninstall&id='
    internetInformation = internetSoftware + '&id='
    internetUpload = internetSoftware + '&cmd=up&id='
    internetHide = internetSoftware + '&cmd=hide&id='

#Setup Error strings
class Error:
    crackerNotGoodEnough = "Error! Access denied: your cracker is not good enough."
    noCracker = "Error! You do not have the needed software to perform this action."
    login = "Error! This IP is already on your hacked database."
    invalidIp = "Error! Invalid IP address."
    notHacked = "Error! This IP is not on your Hacked Database."
    notUploaded = "Error! You do not have enough disk space to download this software."
    processNotFound = "Error! Process not found."
    fileHidden = "Error! This software already exists on your root folder."
    identicalLog = "Error! Identical logs."
    alreadyClearingLog = "Error! There already is a log edit in progress. Delete or complete it before."

#Setup Error paths
class ErrorPath:
    file = "/html/body/div[5]/div[3]/div/div/div[1]/strong"
    ddos = "/html/body/div[5]/div[3]/div/div/div/div[2]/div/div[1]/div/div[2]/strong"
    internetLog = "/html/body/div[5]/div[3]/div/div[1]/strong"
    notUploaded = "/html/body/div[5]/div[3]/div/div[1]/div[2]/strong"
    login = "/html/body/div[5]/div[3]/div/div[1]/div[2]/strong"
    log = '//*[@id="content"]/div[3]/div/div/div[1]/strong'
    process = '//*[@id="content"]/div[3]/div/div[1]/strong'

def Main():
    MakeLog()
    ImportSettings()
    StartBrowser()
    LogIn()
    Print(GetInfectedIps())

def StartBrowser():
    Print("# Starting Browser #")
    global browser
    chromeOptions = webdriver.chrome.options.Options()
    chromeOptions.add_argument('--log-level=3')
    browser = webdriver.Chrome(chrome_options=chromeOptions)

    browser.set_window_size(970, 1045)
    browser.set_window_position(0, 0)
    browser.get(Links.base)

    #Removes the devtools message
    colorama.init()
    print("\u001b[1A",end="")
    print("\033[K",end="")
    print("\u001b[1A",end="")
    Print("")

def LogIn():
    Print("# Logging In #")
    if LoadCookies() == False:
        SaveCookies()
    browser.get(Links.home)
    Print("")

def ImportSettings():
    Print("# Importing Settings #")
    global debug, signature, password, userName, firefox, breaker, cracker
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
    Print("")

def LoadCookies():
    #Trys to log in using cookies.
    #It returns True if log in was successfull and False if it fails to do so
    PrintLog("Loading cookies")
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
    except:
        PrintLog("Error loading cookies")
        return False
    else:
        PrintLog("Loaded cookies correctly")
        browser.get(Links.hardware)
        sleep(5)
        if browser.current_url == Links.index:
            Print("Couldn't log in with cookies, please log in manually")
            return False
        else:
            Print("Successfully logged in with cookies")
            return True

def SaveCookies():
    #Log in
    loginButton = FindByXpath('/html/body/div[2]/div[2]/div/div/div/ul/li[1]/a')
    userNameField = FindByXpath('//*[@id="login-username"]')
    userPasswordField = FindByXpath('//*[@id="password"]')
    loginButton.click()
    userNameField.send_keys(userName)
    userPasswordField.send_keys(password)

    #Wait for user to login
    WaitForLoad(Links.home, reload = False, errorCheck = False)
    Print("Saving cookies in 5 seconds")
    sleep(5)
    pickle.dump(browser.get_cookies() , open("cookies.pkl","wb"))
    Print("Saved cookies")

def MakeLog():
    #Make a dir called logs if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    #Make log file
    global logName
    logName = "logs\\" + datetime.datetime.now().strftime('%Y-%m-%d_%H;%M.log')

def PrintLog(inputString):
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

def WaitForLoad(link, reload = True, errorCheck = True, errorPath = None):
    def WaitForLoadLoop(errorCheck,errorPath):
        #Loop used in WaitForLoad
        if reload:
            browser.refresh()
            RemoveElement('//*[@id="he2"]')
            RemoveElement('//*[@id="gritter-notice-wrapper"]')
        sleep(1)
        ErrorCheck(ErrorPath.process)
        if errorText[1] == Error.processNotFound:
            PrintLog("Process not found, getting link")
            browser.get(link)

        if WaitForLoadErrorCheck(errorCheck, errorPath):
            return False

    def WaitForLoadErrorCheck(errorCheck, errorPath = None):
        #Function used in WaitForLoad, check if an error is present
        if errorPath != None:
            if errorCheck:
                return ErrorCheck(errorPath)
            else:
                ErrorCheck(errorPath)

    def ErrorCheck(errorPath = None):
        #Get string from the errorPath
        global errorText
        try:
            error = FindByXpath(errorPath, False)
        except:
            errorText = ["","None"]
            return False
        else:
            error = FindByXpath(errorPath.replace("/strong", ""))
            errorText = error.text.replace("×","x").split("\n")
            try:
                if errorText[0] == "x":
                    PrintLog(errorText)
                errorText.append(errorText[-1])
            except:
                PrintLog("ERRORMAYBE Return False 2")
                errorText = ["","None"]
                return False
            else:
                return True

    #Check if an error has appeared
    if WaitForLoadErrorCheck(errorCheck, errorPath):
        return False

    #Wait for a website to load
    Print ("Waiting for " + str(link) + " to load")
    if type(link) == type(''):
        while browser.current_url != link:
            if WaitForLoadLoop(errorCheck,errorPath):
                return False
    elif type(link) == type([]):
        while browser.current_url not in link:
            if WaitForLoadLoop(errorCheck,errorPath):
                return False
    else:
        Print("ERROR IN WAITFORLOAD")

    return True

def FindByXpath(xpath, shouldWait = False):
    #Find and return element by xpath
    if shouldWait == False:
        return browser.find_element_by_xpath(xpath)
    else:
        counter = 0
        while True:
            try:
                return browser.find_element_by_xpath(xpath)
            except:
                if counter > 10:
                    Print("Stuck on FindByXpath: " + xpath)
                counter+=1
                sleep(1)

def RemoveElement(xpath):
    try:
        element = FindByXpath(xpath)
    except:
        #Couldn't remove element
        pass
    else:
        try:
        	browser.execute_script("""
        	var element = arguments[0];
        	element.parentNode.removeChild(element);
        	""", element)
        except:
            #Couldn't remove element
            pass

def GetElementLen(xpath1,xpath2, shouldWait = False):
    i = 1
    while i < 1000:
        try:
            FindByXpath(xpath1 + str(i) + xpath2, shouldWait = shouldWait)
        except:
            return i-1
        else:
            i+=1
    Print("ERRORMAYBE Something went wrong in GetElementLen")

def YourIp():
    #Get your ip
    yourIp = FindByXpath('//*[@id="content-header"]/div/div[1]/span', shouldWait = True)
    yourIp = yourIp.text
    return yourIp

def WriteToFiles(ip, minSoftwareVersion, i):
    #WriteToFiles is used for logging
    try:
        float(versions[i])
    except:
        return False
    else:
        if minSoftwareVersion <= float(versions[i]):
            with open("software" + str(minSoftwareVersion) + ".txt", "a") as myfile:
                myfile.write(ip + ": " + softwares[i] + " " + versions[i] + " " + sizes[i] + "\n")
        return True

def GetIpsFromLog(logLines):
    #Get ips from the log
    for logLine in logLines:
        global ips
        foundIpList = re.findall( r'[0-9]+(?:\.[0-9]+){3}', logLine)
        for foundIp in foundIpList:
            if foundIp in ips:
                continue
            elif foundIp == YourIp():
                continue
            else:
                ips.append(foundIp)

def GetBTCFromLog(logLines):
    global btcAddr
    global btcPass
    tempBtcAddr = []
    tempBtcPass = []
    for logLine in logLines:
        try:
            tempBtcAddr.append(re.search("[a-zA-Z0-9]{34} ", logLine).group())
            tempBtcPass.append(re.search("[a-zA-Z0-9]{64}", logLine).group())
        except:
            pass
    if len(tempBtcAddr) == len(tempBtcPass):
        for i in range(0,len(tempBtcAddr)):
            if tempBtcAddr[-1] not in btcAddr:
                btcAddr.append(tempBtcAddr.pop())
                btcPass.append(tempBtcPass.pop())

def GetInfectedIps():
    browser.get(Links.ddos)
    ipsInText = FindByXpath('//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[2]/div/div[2]').text
    foundIpList = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ipsInText)
    ips = []
    for foundIp in foundIpList:
        ips.append(foundIp)
    return ips

def ClearLog():

    #Clears user log
    browser.get(Links.log)

    logField = FindByXpath('//*[@id="content"]/div[3]/div/div/div/div[2]/div[2]/form/textarea', shouldWait = True)
    editLogButton = FindByXpath('//*[@id="content"]/div[3]/div/div/div/div[2]/div[2]/form/input[2]', shouldWait = True)

    logField.clear()
    editLogButton.click()

    #ErrorHandling stage (identical logs and a clear log in progress)
    while WaitForLoad(Links.log, errorPath = ErrorPath.log) == False:
        #Identical logs
        if errorText[1] == Error.identicalLog:
            Print("Your log had already been cleared")
            return False

        #AlreadyClearingLog
        if errorText[1] == Error.alreadyClearingLog:
            Print("There is already a clear log in progress")
            browser.get(Links.processes)
            proccesCount = GetElementLen('//*[@id="content"]/div[3]/div/div/div[2]/ul/li[',']/div[1]')

            #Loop through all processes
            for i in range(0+1,proccesCount+1):
                element = FindByXpath('//*[@id="content"]/div[3]/div/div/div[2]/ul/li[' + str(i) + ']/div[1]')
                if element.text == "Edit log at localhost":
                    completeButton = FindByXpath('//*[@id="content"]/div[3]/div/div/div[2]/ul/li[' + str(i) + ']/div[3]/div[2]/form/input[2]')
                    completeButton.click()
                    break
            else:
                PrintLog("ERRORMAYBE An error has accored in ClearLog during the errorhandling stage")
                return False
            break

        sleep(1)

    Print("Your log has been cleared")
    return True

def GetHDD(MB = True, internet = True):
    #Get HHD returns float or int
    if internet:
        browser.get(Links.internetSoftware)
        fullHDD = FindByXpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[2]/span/font[2]""", shouldWait = True).text
        usedHDD = FindByXpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[2]/span/font[1]""", shouldWait = True).text
    else:
        browser.get(Links.software)
        fullHDD = FindByXpath('//*[@id="softwarebar"]/div/span/font[2]', shouldWait = True).text
        usedHDD = FindByXpath('//*[@id="softwarebar"]/div/span/font[1]', shouldWait = True).text

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

def GetInternetSpeed(Mbit = True, internet = True):
    #Get Internetspeed returns int or float
    if internet:
        browser.get(Links.internetSoftware)
        internetSpeed = FindByXpath("""/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[1]/span/strong""", shouldWait = True).text
    else:
        browser.get(Links.hardware)
        internetSpeed = FindByXpath('//*[@id="content"]/div[3]/div/div/div/div[2]/ul/li[4]/div[2]', shouldWait = True).text.replace("\n"," ")
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

    Print("Getting harddisk software")

    baseXpath = "/html/body/div[5]/div[3]/div/div/div/div[2]/div[1]/table/tbody/"
    softwareCount = GetElementLen(baseXpath + 'tr[',']')
    for i in range(1,softwareCount+1):
        try:
            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[1]")
        except:
            continue
        id = info.get_attribute('href').replace(Links.information, "")

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

    Print("Getting your software")

    baseXpath = "/html/body/div[5]/div[3]/div/div/div/div[2]/div/table/tbody/"
    softwareCount = GetElementLen(baseXpath + 'tr[',']')
    for i in range(1,softwareCount+1):
        try:
            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[1]")
        except:
            continue
        id = info.get_attribute('href').replace(Links.install, "")
        id = id.replace(Links.uninstall, "")
        id = id.replace(Links.delete,"")
        id = id.replace(Links.hide,"")
        id = id.replace(Links.information,"")

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

    Print("Getting software information from " + ip)

    baseXpath = "/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div[1]/table/tbody/"
    softwareCount = GetElementLen(baseXpath + 'tr[',']')
    for i in range(1,softwareCount+1):
        try:
            info = FindByXpath(baseXpath + "tr[" + str(i) + "]/td[5]/a[1]")
        except:
            continue
        id = info.get_attribute('href').replace(Links.internetInstall, "")
        id = id.replace(Links.internetUninstall, "")
        id = id.replace(Links.internetHide,"")
        id = id.replace(Links.internetInformation,"")

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

def Install(software):
    #Install software locally
    Print("Installing " + software)
    GetYourSoftware()
    try:
        i = yourSoftwares.index(software)
        Print(software + " is not in your softwares")
    except:
        return False
    browser.get(Links.install + yourIds[i])
    WaitForLoad(Links.software)
    Print(software + " installed")
    return True

def Download(software):
    #Download files from harddisk
    Print("Downloading " + software)
    GetYourHarddisk()
    try:
        i = harddiskSoftwares.index(software)
    except:
        Print(software + " is not in harddisk")
        return False
    browser.get(Links.download + harddiskIds[i])
    #WaitForLoad(Links.software)
    if WaitForLoad(Links.software, errorPath=ErrorPath.file) == False:
        if Error.fileHidden == errorText[1]:
            Print(software + " is already on machine")
            return False

    Print(software + " downloaded")
    return True

def InternetInstall(software,ip=""):
    #Install file on internet machine
    Print("Installing " + software + " on " + ip)
    GetInternetSoftware(ip)
    try:
        i = softwares.index(software)
    except:
        return False
    browser.get(Links.internetInstall + ids[i])
    WaitForLoad([Links.internet, Links.internetSoftware])
    Print(software + " installed" + " on " + ip)
    InternetClearLog(ip)
    return True

def InternetHide(software, ip=""):
    #Hide file on internet machine
    Print("Hiding " + software + " on " + ip)
    GetInternetSoftware(ip)
    try:
        i = softwares.index(software)
    except:
        return False
    browser.get(Links.internetHide + ids[i])
    WaitForLoad([Links.internet, Links.internetSoftware])
    Print(software + " hid" + " on " + ip)
    InternetClearLog(ip)
    return True

def InternetUpload(software, ip=""):
    #Upload file to internet machine
    Print("Uploading " + software + " on " + ip)
    GetYourSoftware()
    try:
        i = yourSoftwares.index(software)
        if yourIds[i] == "None":
            0/0
    except:
        return "Download"

    browser.get(Links.internetUpload + yourIds[i])
    WaitForLoad([Links.internet, Links.internetSoftware], errorPath = ErrorPath.notUploaded)
    if errorText[1] == Error.notUploaded:
        Print(software + " couldn't be uploaded, not enough space on " + ip + "??")
        return False
    Print(software + " uploaded" + " on " + ip)
    InternetClearLog(ip)
    return True

def InternetClearLog(ip = "", getIps = False, getBTCs = False):
    #Clear the log on the connected machine
    Print("Clearing log on " + ip)
    browser.get(Links.internetLog)
    try:
        internetLogField = FindByXpath("""//*[@id="content"]/div[3]/div/div[3]/div[2]/div/div/div[2]/form/textarea""")
        internetEditLogButton = FindByXpath("""//*[@id="content"]/div[3]/div/div[3]/div[2]/div/div/div[2]/form/input[2]""")
    except:
        if FindByXpath("/html/body/div[5]/div[3]/div/div[3]/div[2]/div/div", shouldWait = True).text == "No logs":
            Print("Can't clear logs on " + ip)
            return
        Print("ERRORMAYBE InternetClearLog gets called again")
        InternetClearLog(ip, getIps, getBTCs)

    #Get log text
    rawLog = internetLogField.text
    logLines = rawLog.split("\n")

    #Clear the log
    internetLogField.clear()
    internetLogField.send_keys(signature)
    internetEditLogButton.click()



    #Wait the log to be cleared
    while WaitForLoad(Links.internetLog, errorPath = ErrorPath.internetLog) == False:
        if Error.processNotFound == errorText[1]:
            break

    if getBTCs:
        GetBTCFromLog(logLines)

    if getIps:
        GetIpsFromLog(logLines)

    Print("Log has been cleared on " + ip)

def Hack(ip = "1.2.3.4", clearLog = True, getSoftware = True, getIps = False, getBTCs = True):

    def WaitForLoadCalls(link):
        if WaitForLoad(link, errorPath=ErrorPath.login) == False:
            if Error.crackerNotGoodEnough == errorText[1]:
                Print("You're cracker isn't good enough to hack " + ip)
                return False
            elif Error.noCracker == errorText[1]:
                if cracker == "None":
                    Print("No cracker set in settings.py")
                    return False
                if Download(cracker):
                    Install(cracker)
                else:
                    return False

                return Hack(ip, clearLog, getSoftware, getIps, getBTCs)
            elif Error.login == errorText[1]:
                Print("Ip already in database")
            elif "Error!" == errorText[1]:
                Print("Retrying the hack")
                Hack(ip,clearLog,getSoftware,getIps,getBTCs)
            else:
                PrintLog("ERRORMAYBE Couldn't handle this error: " + errorText[1])
                WaitForLoad(link, errorPath=ErrorPath.login)

    #Hack host
    #Start by logging out if logged in to another IP
    browser.get(Links.internetLogout)
    #Then proceed to go to the ip requested
    browser.get(Links.internetWithIp + ip)
    #Enter the hacking GUI
    browser.get(Links.internetHack)
    #Start bruteforcing
    browser.get(Links.internetBruteforce)

    #Check if the ip still exists
    #This should return false if
    ipInputField = FindByXpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/form/div/input[1]',shouldWait = False)
    if ip != ipInputField.get_attribute('value'):
        return False

    if WaitForLoadCalls(Links.internetLogin) == False:
        return False

    loginButton = FindByXpath('//*[@id="loginform"]/div[3]/span[3]/input', shouldWait = True)
    sleep(1)
    loginButton.click()

    if WaitForLoadCalls(Links.internet) == False:
        return False

    Print("Hacked " + ip)

    if clearLog:
        InternetClearLog(ip, getIps, getBTCs)

    if getSoftware:
        GetInternetSoftware(ip)

    return True

def DDos(ip, times = 1, hack = True, clearLog = True, getSoftware = True):
    #Launch ddos attack against ip x times

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

    #If function is supposed to hack then do so
    if hack:
        if Hack(ip, clearLog, getSoftware) == False:
            Print("Failed hacking " + ip + " during the start of a ddos")
            return False
        else:
            Print("Successfully hacked " + ip)

    #Prepare estimatedTime time
    sleep(2)
    global estimatedTime
    estimatedTime = 305

    #Start ddosing x times
    for i in range(times):
        TimerStart()

        Print("")
        estimatedTimeLeft = str(RoundTime(datetime.datetime.now().time(), round(estimatedTime * (times-i))))
        Print ("Starting ddos number " + str(i+1) + "/" + str(times) + " against " + ip)
        Print ("This ETA: " + str(round(estimatedTime)) + " seconds, Total ETA: " + estimatedTimeLeft + " seconds")
        browser.get(Links.ddos)

        sleep(1)

        ipField = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""", shouldWait = True)
        try:
            launchDDosButton = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input""")
        except:
            Print ("To ddos you need to have a breaker")
            try:
                if breaker == "None":
                    Print("No breaker set in settings.py")
                    return False
                if not Download(breaker):
                    return False
                browser.get(Links.ddos)
                sleep(1)
                ipField = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input""")
                launchDDosButton = FindByXpath("""//*[@id="content"]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input""")
            except:
                PrintLog("ERRORMAYBE DDOS EXCEPT IS NEEDED, RETURNING FALSE")
                return False

        ipField.send_keys(ip)
        launchDDosButton.click()
        sleep(2)

        Print("DDOS launched")
        WaitForLoad(Links.software, errorPath = ErrorPath.ddos)

        Print(ip + " has been DDosed, it took " + str(round(TimerStop())) + " seconds")
        NewEstimatedTime(TimerStop(),i+1)

        sleep(3)
    Print("Done DDosing " + ip)

if __name__ == "__main__":
	Main()
