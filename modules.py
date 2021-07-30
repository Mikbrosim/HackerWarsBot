from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException, NoSuchWindowException
import re
import time
import json
from html.parser import HTMLParser

links = {
    "base" : "https://hackerwars.io/",

    "home" : "index",
    "ddos" : "list?action=ddos",
    "finances" : "finances",
    "internet" : "internet",
    "missions" : "missions",
    "bankHack" : "internet?action=hack&type=bank",
    "bankLogin" : "internet?action=login&type=bank",
    "processes" : "processes",
    "bankLogout" : "internet?bAction=logout",
    "bankAccounts" : "list?show=bankaccounts",
    "bankRegister" : "internet?action=register",
    "internetHack" : "internet?action=hack",
    "internetLogin" : "internet?action=login",
    "internetLogout" : "internet?view=logout",
    "internetWithIp" : "internet?ip=",
    "internetBruteforce" : "internet?action=hack&method=bf",

    "localLog" : "log",
    "localHide" : "software?action=hide&id=",
    "localDelete" : "software?action=del&id=",
    "localInstall" : "software?action=install&id=",
    "localProcess" : "processes?pid=",
    "localHardware" : "hardware",
    "localSoftware" : "software",
    "localHarddisk" : "software?page=external",
    "localUninstall" : "software?action=uninstall&id=",
    "localInformation" : "?id=",
    "localHarddiskDownload" : "software?page=external&action=download&id=",
    "localProcessesRunning" : "processes?page=running",
    "localSoftwareInformation" : "software?id=",

    "internetLog" : "internet?view=logs",
    "internetHide" : "internet?view=software&cmd=hide&id=",
    "internetUpload" : "internet?view=software&cmd=up&id=",
    "internetDelete" : "internet?view=software&cmd=del&id=",
    "internetInstall" : "internet?view=software&cmd=install&id=",
    "internetSoftware" : "internet?view=software",
    "internetUninstall" : "internet?view=software&cmd=uninstall&id=",
    "internetInformation" : "internet?view=software&id="
    }

class Bot:
    def __init__(self, gui, driver, format, transferBank, missionBank, missionCrackerVersion, secondBTCaddr):
        self.gui = gui
        self.driver = driver

        self.format = format
        self.transferBank = transferBank
        self.missionBank = missionBank
        self.missionCrackerVersion = missionCrackerVersion
        self.secondBTCaddr = secondBTCaddr


        self.ipRegex = r"(?:[^\d\.]|^)(\d{1,3}(?:\.\d{1,3}){3})(?:[^\d\.]|$)"
        self.btcRegex = r"([a-zA-Z0-9]{34}) using key ([a-zA-Z0-9]{64})"

        self.btc = dict()
        self.ips = set()
        self.hackedIps = set()

    def FindElementByXpath(self, *xPaths):
        # Make sure the same xPath isn't being spammed
        if not hasattr(self, "lastXPaths"):
            self.lastXPaths = []
        if self.lastXPaths != xPaths:
            print("Waiting for " + str(xPaths))
            self.lastXPaths = xPaths

        while True:
            for xPath in xPaths:
                try:
                    element = self.driver.find_element_by_xpath(xPath)
                except NoSuchElementException:
                    time.sleep(.1)
                else:
                    return element
            # I hate doing it this way, but I didn't wanna think too long before making this little fix to the issue of people deleting my cracker
            try:
                if self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div[1]/div[2]").text == "Error! You do not have the cracker needed to keep logged in - disconnected.":
                    self.DownloadLocalSoftwareByType("crc", missionCrackerVersion)
            except (NoSuchElementException, StaleElementReferenceException):
                pass

    def ClickElementBeforePopup(self, xpath):
        # Wait for window to popup
        button = self.FindElementByXpath(xpath)
        while True:
            try:
                button.click()
            except ElementClickInterceptedException:
                break
            except StaleElementReferenceException:
                break
            else:
                time.sleep(.1)

    @property
    def currentUrl(self):
        try:
            return self.driver.current_url.replace(".php","")

        except NoSuchWindowException:
            # In case of original window being closen
            self.driver.switch_to.window(self.driver.window_handles[0])
            return self.driver.current_url.replace(".php","")

    @currentUrl.setter
    def currentUrl(self, value):
        try:
            value = self.TransLink(value)
            self.driver.get(value)

        except NoSuchWindowException:
            # In case of original window being closen
            self.driver.switch_to.window(self.driver.window_handles[0])

            value = self.TransLink(value)
            self.driver.get(value)

    @property
    def localIp(self):
        i = 0
        localIp = ""
        while localIp == "":
            localIp = self.FindElementByXpath("/html/body/div[4]/div[1]/div/div[1]/span").text
            if i > 100:
                print("COULDN'T OBTAIN LOCAL IP WITHIN 100 TRIES",i)
                break
            i += 1
        return localIp

    @property
    def remoteIp(self):
        self.currentUrl = self.TransLink("internetLog")
        try:
            self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div[3]/div[1]/ul/li[3]")
        except NoSuchElementException:
            return ""
        else:
            return self.FindElementByXpath("/html/body/div[4]/div[3]/div[1]/div[1]/div/div/div[1]/form/div/input[1]").get_attribute("value")

    def TransLink(self, linkName):
        if linkName in links:
            linkName = links["base"] + links[linkName]
        return linkName

    def WaitForURL(self, linkName):
        print("Waiting for " + self.TransLink(linkName))
        while self.TransLink(linkName) != self.currentUrl:
            time.sleep(.1)

    def Database(self, key, value):
        try:
            db = json.load(open("./softwares.json", "r"))
        except FileNotFoundError:
            db = {}
        finally:
            db[key] = value
            json.dump(db , open("./softwares.json", "w+"))

    class SoftwareCarver(HTMLParser):
        def __init__(self):
            self.softwares = dict()
            super().__init__()

        def handle_starttag(self, tag, attrs):
            if tag == "tr":
                self.datas = list()
                self.software = dict()
                self.software["installed"] = False
            elif tag == "b":
                self.data.append("b")
            elif tag == "td":
                self.data = list()
            for attr in attrs:
                if tag == "tr":
                    if attr[0] == "id":
                        self.software["id"] = attr[1]
                    if attr[0] == "class":
                        self.software["installed"] = attr[1] == "installed"
                elif tag == "span":
                    if attr[0] == "class":
                        result = re.search(r'[^-]*-(\d+)', attr[1])
                        if result:
                            self.software["icon"] = result.group(1)
                elif tag == "a":
                    if attr[0] == "href":
                        result = re.search(r'id=(\d+)', attr[1])
                        if result:
                            self.software["id"] = result.group(1)

        def handle_endtag(self, tag):
            if tag == "tr":
                fileName = self.datas[1][-1].split(".")
                self.software["name"] = ".".join(fileName[:-1])
                self.software["type"] = fileName[-1]
                self.software["viruscontrol"] = ("b" in self.datas[1] and self.software["type"] in ["vddos","vspam","vwarez","vminer"])
                if len(self.datas[2]) > 0:
                    self.software["version"] = self.datas[2][-1]
                    self.software["version"] = float(self.software["version"]) if self.software["version"] != "" else 1
                else:
                    self.software["version"] = 1.0
                if len(self.datas[3]) > 0:
                    self.software["size"] = self.datas[3][-1]
                    self.software["size"] = float(self.software["size"].replace("GB","")) * 1000 + 100 if "GB" in self.software["size"] else self.software["size"].replace("MB","")
                    self.software["size"] = float(self.software["size"]) if self.software["size"] != "" else 1
                else:
                    self.software["size"] = 1
                self.softwares[self.software["id"]] = dict(self.software)

            if tag == "td":
                self.datas.append([x for x in self.data if x.strip()])

        def handle_data(self, data):
            self.data.append(data)

        def feed(self,tableHTML):
            tableHTML = tableHTML.replace("\n","")
            if tableHTML == "":
                return {}
            super().feed(tableHTML)
            try:
                return self.softwares
            except Exception as ex:
                print(tableHTML)
                print("CAUGHT:",ex)

    def GetLocalSoftware(self):
        #Get all important data from local software
        self.currentUrl = self.TransLink("localSoftware")
        try:
            table = self.FindElementByXpath('/html/body/div[4]/div[3]/div/div/div/div[2]/div/table/tbody').get_attribute('innerHTML')
        except StaleElementReferenceException:
            print("ERROR","StaleElementReferenceException", "RERUNNING","GetLocalSoftware")
            return self.GetLocalSoftware()

        return self.SoftwareCarver().feed(table)

    def GetRemoteSoftware(self):
        # Make sure logged in to remote
        remoteIp = self.remoteIp
        if remoteIp == "":
            return {}

        #Get all important data from remote software
        self.currentUrl = self.TransLink("internetSoftware")
        try:
            table = self.FindElementByXpath('/html/body/div[4]/div[3]/div/div[3]/div[2]/div/div[1]/table/tbody').get_attribute('innerHTML')
        except StaleElementReferenceException:
            print("ERROR","StaleElementReferenceException", "RERUNNING","GetRemoteSoftware")
            return self.GetRemoteSoftware()

        return self.SoftwareCarver().feed(table)

    def GetLocalHarddisk(self):
        #Get all important data from your software
        self.currentUrl = self.TransLink("localHarddisk")
        table = self.FindElementByXpath('/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]/table/tbody').get_attribute('innerHTML')
        return self.SoftwareCarver().feed(table)

    def GetLocalProcesses(self):
        processes = {}
        self.currentUrl = "processes"
        table = self.FindElementByXpath('/html/body/div[4]/div[3]/div[1]/div/div[2]').find_elements_by_tag_name("li")
        for item in table:
            text = item.find_element_by_class_name("proc-desc").text

            process = item.find_element_by_class_name("process")
            id = process.get_attribute("data-process-id")
            timeLeft = process.get_attribute("data-process-timeleft")

            processes[id] = {"id":id, "timeLeft":timeLeft, "text":text, "element":process}
        return processes

    def GetRemoteInternet(self):
        if self.remoteIp != "":
            self.currentUrl = self.TransLink("internetSoftware")
            internetSpeed = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[1]/span/strong").text
            internetSpeed = int(internetSpeed.replace("Mbit","")) if "Mbit" in internetSpeed else int(internetSpeed.replace("Gbit",""))*1000
            return internetSpeed
        else:
            return 0

    def GetRemainingLocalHDD(self):
        self.currentUrl = self.TransLink("localSoftware")

        totalSoftware = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[3]/div/div/span/font[2]").text
        totalSoftware = float(totalSoftware.replace("GB","")) * 1000 + 100 if "GB" in totalSoftware else float(totalSoftware.replace("MB",""))

        usageSoftware = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[3]/div/div/span/font[1]").text
        usageSoftware = float(usageSoftware.replace("GB","")) * 1000 + 100 if "GB" in usageSoftware else float(usageSoftware.replace("MB",""))

        return totalSoftware-usageSoftware

    def GetRemainingRemoteHDD(self):
        if self.remoteIp != "":
            self.currentUrl = self.TransLink("internetSoftware")

            totalSoftware = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[2]/span/font[2]").text
            totalSoftware = float(totalSoftware.replace("GB","")) * 1000 + 100 if "GB" in totalSoftware else float(totalSoftware.replace("MB",""))

            usageSoftware = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[3]/div[2]/div/div[2]/div/div[2]/span/font[1]").text
            usageSoftware = float(usageSoftware.replace("GB","")) * 1000 + 100 if "GB" in usageSoftware else float(usageSoftware.replace("MB",""))

            return totalSoftware-usageSoftware
        else:
            return 0

    def GetRemainingLocalRam(self):
        self.currentUrl = self.TransLink("localProcessesRunning")
        totalRam = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/span/font[2]").text
        totalRam = float(totalRam.replace("GB","")) * 1000 + 100 if "GB" in totalRam else float(totalRam.replace("MB",""))

        ramUsage = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/span/font[1]").text
        ramUsage = float(ramUsage.replace("GB","")) * 1000 + 100 if "GB" in ramUsage else float(ramUsage.replace("MB",""))
        return totalRam - ramUsage

    def GetBankAccount(self, bankName):
        self.currentUrl = self.TransLink("finances")
        table = self.FindElementByXpath('/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]').find_elements_by_class_name("span4")
        for item in table:
            name = item.find_element_by_xpath("./div/div[2]/div/strong[1]")
            if name.text == bankName:
                bank = item.find_element_by_xpath("./div/div[1]/a[2]")
                localAccountIp = bank.get_attribute("href").replace(self.TransLink("internetWithIp"),"")
                account = item.find_element_by_xpath("./div/div[2]/div")
                localAccountNumber = account.text.replace(" ","").split("#")[-1]
                return localAccountNumber, localAccountIp

    def DeleteLocalProcess(self, processId):
        print("Deleting",processId)
        self.currentUrl = self.TransLink("localProcess") + processId + "&del=1"
        self.WaitForURL(self.TransLink("processes"))

    def DeleteRemoteSoftware(self, softwareId):
        remoteIp = self.remoteIp
        print("REMOTEIP:",remoteIp)
        # Must be logged in to remote
        if remoteIp == "":
            print("Not logged in to remote")
            return False

        self.currentUrl = self.TransLink("internetDelete") + softwareId
        self.WaitForURL(self.TransLink("internetSoftware"))
        return True

    def ClearLocalLog(self):
        """
        print(self.localIp)
        return
        #"""

        # Make sure no other local log cleaning is in progress
        processes = self.GetLocalProcesses()
        for processId in processes:
            if processes[processId]['text'] == "Edit log at localhost":
                self.DeleteLocalProcess(processId)

        self.currentUrl = "localLog"
        logField = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]/form/textarea[2]")

        # Make sure log isn't cleaned already
        if logField.text == "":
            print("Local log already cleared")
            return

        logField.clear()
        editLogButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]/form/input[2]")
        editLogButton.click()

        self.WaitForURL("localLog")
        print("Local log cleared")
        return True

    def ClearRemoteLog(self):
        remoteIp = self.remoteIp
        # Must be logged in to remote
        if remoteIp == "":
            print("Not logged in to remote")
            return False

        # Make sure no other local log cleaning is in progress
        processes = self.GetLocalProcesses()
        for processId in processes:
            print(processes[processId]['text'])
            if processes[processId]['text'] == "Edit log at " + remoteIp:
                self.DeleteLocalProcess(processId)


        self.currentUrl = self.TransLink("internetLog")
        logField = self.FindElementByXpath("/html/body/div[4]/div[3]/div[1]/div[3]/div[2]/div[1]/div/div/form/textarea[2]")

        # Make sure log isn't cleaned already
        if logField.text == "" or logField.text == "Download Center doesnt record logs.":
            print("Remote log already cleared")
            return

        logText = logField.text
        logField.clear()
        editLogButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div[1]/div[3]/div[2]/div[1]/div/div/form/input[2]")
        editLogButton.click()
        self.WaitForURL("internetLog")

        # Carve out the log text
        result = re.findall(self.btcRegex, logText)
        if len(result) != 0:
            print(result)
            for btc in result:
                self.btc[btc[0]] = btc[1]

        self.ips.update(set(re.findall(self.ipRegex, logText))-self.hackedIps)

        print("Remote log cleared")
        return True

    def UploadToRemote(self, softwareId):
        if self.remoteIp == "":
            return False

        # Make sure enough space on remote harddrive
        software = self.GetLocalSoftware()
        if softwareId not in software:
            print("SoftwareId",softwareId,"not in local software")
            return False

        remainingHDD = self.GetRemainingRemoteHDD()
        if software[softwareId]["size"] > remainingHDD:
            return False

        self.currentUrl = self.TransLink("internetUpload") + softwareId
        # THERE ISN'T USED ANY WAIT FOR LOAD, BEACUSE THE "ERROR TEXT"
        # MESSAGE IS BEING SHOWN ON DIFFERENT PAGES
        # THEREFORE IT IS WAITING FOR THE LOGOUT BUTTON TO SHOW
        self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[3]/div[1]/ul/li[3]/a")

        errorText = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]").text.split("\n")[-1]
        if errorText == "Success! Software successfully uploaded.":
            return True
        elif errorText == "Error! The remote client already have this software.":
            return True
        elif errorText == "Error! This software does not exist anymore. The task was deleted.":
            harddiskSoftware = self.GetLocalHarddisk()
            for harddiskSoftwareId in harddiskSoftware:
                if harddiskSoftware[harddiskSoftwareId]["name"] == software[softwareId]["name"]:
                    if self.DownloadLocalSoftware(harddiskSoftwareId):
                        software = self.GetLocalSoftware()
                        for softwareId in software:
                            if software[softwareId]["name"] == harddiskSoftware[harddiskSoftwareId]["name"]:
                                return self.UploadToRemote(softwareId)
            return False
        elif errorText == "Error! You do not have the cracker needed to keep logged in - disconnected.":
            return False
        else:
            print("Errror Text",errorText)
            return False

    def InstallLocalSoftware(self, softwareId):
        # Make sure enough RAM is avaiable
        #""" Making sure that enough RAM is avaiable returns False, and thereby could trigger a redownload
        self.currentUrl = self.TransLink("localSoftwareInformation") + softwareId
        softwareRamUsage = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[3]/td[2]").text
        softwareRamUsage = float(softwareRamUsage.replace("GB","")) * 1000 + 100 if "GB" in softwareRamUsage else float(softwareRamUsage.replace("MB",""))

        if softwareRamUsage > self.GetRemainingLocalRam():
            return False
        #"""

        # Install software
        self.currentUrl = self.TransLink("localInstall") + softwareId
        self.WaitForURL(self.TransLink("localSoftware"))
        errorText = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div[1]").text.split("\n")[-1]
        if errorText == "Success! Software installed.":
            return True

        elif errorText == "Error! This software does not exist anymore. The task was deleted.":
            return False

    def InstallRemoteSoftware(self, softwareId):
        self.currentUrl = self.TransLink("internetInstall") + softwareId
        self.WaitForURL(self.TransLink("internetSoftware"))
        errorText = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]","/html/body/div[4]/div[3]/div/div/div[1]").text.split("\n")[-1]
        if errorText == "Success! Software installed.":
            return True

        elif errorText == "Error! This software does not exist anymore. The task was deleted.":
            return False

        elif errorText == "Error! This software does not exists.":
            return False

    def DownloadLocalSoftware(self, softwareId):
        # Make sure enough space on local harddrive
        harddiskSoftware = self.GetLocalHarddisk()
        if harddiskSoftware[softwareId]["size"] > self.GetRemainingLocalHDD():
            print("Not enough space", harddiskSoftware[softwareId]["size"], self.GetRemainingLocalHDD())
            return False

        # Download form harddisk
        self.currentUrl = self.TransLink("localHarddiskDownload") + softwareId
        self.WaitForURL(self.TransLink("localSoftware"))
        errorText = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div[1]").text.split("\n")[-1]
        print(errorText)
        if errorText == "Success! Software downloaded from external HD.":
            return True

        elif errorText == "Error! This software already exists on your root folder.":
            if self.format:
                formatButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[3]/div/ul/li[3]/a")
                formatButton.click()

                confirmButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[3]/div/span/div/form/div[2]/input[2]")
                confirmButton.click()

                return self.DownloadLocalSoftware(softwareId)
            return False

    def DownloadLocalSoftwareByType(self, type, maximumVersion = 0):
        softwares = self.GetLocalSoftware()
        for softwareId in softwares:
            if type == softwares[softwareId]['type']:
                if type == "vbrk":
                    return True
                success = self.InstallLocalSoftware(softwareId)
                if not success:
                    print("Couldn't install " + type)
                    return False
                return True

        # Donwload cracker if no cracker on local server
        else:
            # Downlaod cracker from harddisk
            harddisk = self.GetLocalHarddisk()
            for softwareId in harddisk:
                if type == harddisk[softwareId]['type'] and (maximumVersion == 0 or maximumVersion >= harddisk[softwareId]['version']):
                    success = self.DownloadLocalSoftware(softwareId)
                    if not success:
                        print("Couldn't download " + type + " from harddisk")
                        return False
                    break
            else:
                print("No " + type + " on harddisk")
                return False

            if type == "vbrk":
                return True
            # Install the downloaded cracker
            softwares = self.GetLocalSoftware()
            for softwareId in softwares:
                if type == softwares[softwareId]['type']:
                    success = self.InstallLocalSoftware(softwareId)
                    if not success:
                        print("Couldn't install " + type)
                        return False
                    return True

    def BankCrack(self, accountNumber, accountIp):
        # Start by logging out if logged in to another IP
        self.currentUrl = self.TransLink("internetLogout")
        self.currentUrl = self.TransLink("bankLogout")
        self.currentUrl = self.TransLink("internetWithIp") + accountIp
        self.currentUrl = self.TransLink("bankHack")
        accountField = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/input")
        accountField.send_keys(accountNumber.replace("#",""))
        hackButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/form/div[2]/button")
        hackButton.click()

        #self.WaitForURL(self.TransLink("bankLogin"))
        try:
            while "%" in self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]").text.split("\n")[-1]:
                time.sleep(.1)
        except StaleElementReferenceException:
            pass


        errorText = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]").text.split("\n")[-1]
        if errorText == "Error! Access denied: your cracker is not good enough.":
            softwares = self.GetLocalSoftware()
            for softwareId in softwares:
                if "crc" == softwares[softwareId]['type'] and softwares[softwareId]["installed"]:
                    print("Cracker not good enough")
                    return False
            else:
                self.DownloadLocalSoftwareByType("crc", self.missionCrackerVersion)
                return self.BankCrack(accountNumber, accountIp)

        elif errorText == "Error! You do not have the needed software to perform this action.":
            self.DownloadLocalSoftwareByType("crc", self.missionCrackerVersion)
            return self.BankCrack(accountNumber, accountIp)

        elif errorText == "Error! This bank account does not exists.":
            self.currentUrl = self.TransLink("bankAccounts")
            accountList = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul").find_elements_by_tag_name("li")
            for account in accountList:
                accountId = account.find_element_by_xpath("./div[1]/div[1]/span").text
                if accountId == accountNumber:
                    # Wait for window to popup
                    button = account.find_element_by_xpath("./div[4]/span")
                    while True:
                        try:
                            button.click()
                        except ElementClickInterceptedException:
                            break
                        except StaleElementReferenceException:
                            break
                        else:
                            time.sleep(.1)

                    confirmButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/span/div/form/div[2]/input[3]")
                    confirmButton.click()
                    break
            return "bank account does not exists"
        else:
            print(errorText)

        accountField = self.FindElementByXpath('//*[@id="loginform"]/div[1]/div/div/input')
        localAccountText = self.FindElementByXpath('//*[@id="loginform"]/div[3]/span[1]')
        if accountField.get_attribute("value") != accountNumber:
            print("You are trying to login to the wrong account", accountField.get_attribute("value"), "instead of", accountNumber)
            return self.BankCrack(accountNumber, accountIp)

        loginButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[3]/div[3]/form/div[3]/span[3]/input")
        loginButton.click()
        return True

    def BankTransfer(self, fromNumber, fromIp, toNumber, toIp):
        response = self.BankCrack(fromNumber, fromIp)
        if response != True:
            return response

        toField = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/form/div[1]/div[2]/input")
        toField.send_keys(toNumber)

        ipField = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/form/div[1]/div[4]/input")
        ipField.send_keys(toIp)

        amount = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[1]/ul/li/div[2]/strong").text

        moneyField = self.FindElementByXpath('//*[@id="money"]')
        moneyField.clear()
        moneyField.send_keys(amount)

        transferButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/form/div[2]/button")
        transferButton.click()

        errorText = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]").text.split("\n")[-1]
        if errorText == "Error! This account does not exists.":
            self.currentUrl = self.TransLink("bankAccounts")
            accountList = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul").find_elements_by_tag_name("li")
            for account in accountList:
                accountId = account.find_element_by_xpath("./div[1]/div[1]/span").text
                if accountId == toNumber:
                    # Wait for window to popup
                    button = account.find_element_by_xpath("./div[4]/span")
                    while True:
                        try:
                            button.click()
                        except ElementClickInterceptedException:
                            break
                        except StaleElementReferenceException:
                            break
                        else:
                            time.sleep(.1)

                    confirmButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/span/div/form/div[2]/input[3]")
                    confirmButton.click()
                    break
            return "uncleaned"


        self.oldAccountNumber = toNumber
        self.oldAccountIp = toIp
        return True

    def BitcoinLogin(self):
        # Make sure no other local log cleaning is in progress
        processes = self.GetLocalProcesses()
        for processId in processes:
            if processes[processId]['text'] == "Edit log at localhost":
                self.DeleteLocalProcess(processId)

        self.currentUrl = "localLog"
        logField = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]/form/textarea[2]")

        # Make sure log isn't cleaned already
        if logField.text == "":
            logField.send_keys(" ")
        else:
            logField.clear()

        editLogButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]/form/input[2]")
        editLogButton.click()

        while self.TransLink("localProcess") not in self.currentUrl:
            time.sleep(0.1)

        # Retrieve log process link
        logProcess = self.currentUrl

        processes = self.GetLocalProcesses()
        for processId in processes:
            if processes[processId]['text'] == "Edit log at localhost":
                percentText = processes[processId]['element'].find_element_by_class_name("percent")
                while percentText.text != "100%":
                    time.sleep(.1)

        # Get the address of the bitcoin market
        self.currentUrl = self.TransLink("internetWithIp") + "1.2.3.4"
        ipList = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div").text
        bitcoinMarketIp = re.search(r"(\d{1,3}(?:\.\d{1,3}){3}) - Bitcoin Market", ipList).group(1)

        # Get local bitcoin adress
        self.currentUrl = self.TransLink("internetWithIp") + bitcoinMarketIp

        self.ClickElementBeforePopup('//*[@id="btc-login"]')

        self.currentUrl = logProcess
        self.WaitForURL("localLog")
        return True

    def LocalBankCleaner(self):
        self.currentUrl = self.TransLink("finances")
        table = self.FindElementByXpath('/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]').find_elements_by_class_name("span4")
        accounts = []
        for item in table:
            name = item.find_element_by_xpath("./div/div[2]/div/strong[1]")
            bank = item.find_element_by_xpath("./div/div[1]/a[2]")
            localAccountIp = bank.get_attribute("href").replace(self.TransLink("internetWithIp"),"")
            account = item.find_element_by_xpath("./div/div[2]/div")
            localAccountNumber = account.text.replace(" ","").split("#")[-1]
            if name.text != self.transferBank:
                accounts.append((localAccountNumber, localAccountIp))

        i = 0
        for localAccountNumber, localAccountIp in accounts:
            i+=1
            if i == 1:
                self.MoneyTransferChainStart(localAccountNumber, localAccountIp)
            else:
                if not self.BankTransfer(self.oldAccountNumber, self.oldAccountIp, localAccountNumber, localAccountIp):
                    break
                self.ReRegisterBankAccount()


        self.BankTransfer(localAccountNumber, localAccountIp, self.localAccountNumber, self.localAccountIp)
        self.ReRegisterBankAccount()

        del self.oldAccountNumber
        del self.oldAccountIp
        self.MoneyTransferChainEnd()

    def ReRegisterBankAccount(self):
        # Requires account being logged in
        # This function has no checks right now

        # Delete current account
        self.ClickElementBeforePopup('//*[@id="bendacc"]')
        confirmButton = self.FindElementByXpath('//*[@id="modal-submit"]')
        confirmButton.click()

        # Create new account
        self.currentUrl = self.TransLink("bankRegister")
        createAccount = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/form/input[2]")
        createAccount.click()

    def MoneyTransferChainStart(self, startAccountNumber, startAccountIp):
        # Get current account id and ip
        self.localAccountNumber, self.localAccountIp = self.GetBankAccount(self.transferBank)
        if "uncleaned" == self.BankTransfer(self.localAccountNumber, self.localAccountIp, startAccountNumber, startAccountIp):
            return False

        self.ReRegisterBankAccount()

        # Get new account id and ip
        self.localAccountNumber, self.localAccountIp = self.GetBankAccount(self.transferBank)

    def MoneyTransferChainEnd(self):
        if hasattr(self, "oldAccountNumber") and hasattr(self, "oldAccountIp"):
            if not self.BankTransfer(self.oldAccountNumber, self.oldAccountIp, self.localAccountNumber, self.localAccountIp):
                return False

            del self.oldAccountNumber
            del self.oldAccountIp

        # Get the address of the bitcoin market
        self.currentUrl = self.TransLink("internetWithIp") + "1.2.3.4"
        ipList = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div").text
        bitcoinMarketIp = re.search(r"(\d{1,3}(?:\.\d{1,3}){3}) - Bitcoin Market", ipList).group(1)

        # Get local bitcoin adress
        self.currentUrl = self.TransLink("internetWithIp") + bitcoinMarketIp

        self.ClickElementBeforePopup('//*[@id="btc-buy"]/a')

        # Open dropdown
        accountDropdown = self.FindElementByXpath('/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/span/div/form/div[1]/span/div/a/span[1]')
        accountDropdown.click()

        # Select the correct account
        for choice in self.FindElementByXpath('//*[@id="select2-drop"]/ul').find_elements_by_tag_name("li"):
            choiceText = choice.text
            if choiceText[1:10] == self.localAccountNumber:
                choice.click()
                btcValue = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/span/div/form/div[1]/div[1]/div[3]/span/span[2]/span")

                # Calculate the buyable amount
                btcValue = int(btcValue.text)
                accountValue = int(choiceText[13:-1].replace(",",""))
                btcAmount = int((10*accountValue) // btcValue)/10

                if btcAmount == 0:
                    return False

                # Buy that amount
                btcField = self.FindElementByXpath('//*[@id="btc-amount"]')
                btcField.clear()
                btcField.send_keys(str(btcAmount))

                buyButton = self.FindElementByXpath('//*[@id="btc-submit"]')
                buyButton.click()
                break
        else:
            return False

        # Transfer bitcoins to a second adresses if specified
        if hasattr(self, "secondBTCaddr") and self.secondBTCaddr != "":
            self.currentUrl = self.TransLink("internetWithIp") + bitcoinMarketIp

            self.ClickElementBeforePopup('//*[@id="btc-transfer"]/a')

            destinationField = self.FindElementByXpath('//*[@id="btc-to"]')
            destinationField.send_keys(self.secondBTCaddr)
            transferButton = self.FindElementByXpath('//*[@id="btc-submit"]')
            transferButton.click()


        return True

    def BankAccountCleaner(self, batch = 90):
        j = 16
        for i in range(batch):
            j-=1
            self.currentUrl = self.TransLink("bankAccounts")
            accountList = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul").find_elements_by_tag_name("li")
            if len(accountList) > 1:
                startTime = time.localtime()
                # REMOVE FIRST ACCOUNT IF $0 on it
                amount = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul/li[1]/div[2]/div[1]").text
                if amount == "$0":
                    self.ClickElementBeforePopup("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul/li[1]/div[4]/span")

                    confirmButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/span/div/form/div[2]/input[3]")
                    confirmButton.click()
                    continue

                # REMOVE Seccond ACCOUNT IF $0 on it
                amount = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul/li[2]/div[2]/div[1]").text
                if amount == "$0":
                    self.ClickElementBeforePopup("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul/li[2]/div[4]/span")

                    confirmButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/span/div/form/div[2]/input[3]")
                    confirmButton.click()
                    continue

                # This function is very fast xD
                # Sleep in order to not act to suspecious :P
                print("\nBatch",i,"out of",batch,"\nWaiting",j,"seconds\n")
                if j > 0:
                    time.sleep(j)
                j=16
                accountId = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul/li[1]/div[1]/div[1]/span").text
                accountIp = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul/li[1]/div[3]/div[2]/a").get_attribute("href").replace(self.TransLink("internetWithIp"),"")

                nextId = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul/li[2]/div[1]/div[1]/span").text
                nextIp = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/ul/li[2]/div[3]/div[2]/a").get_attribute("href").replace(self.TransLink("internetWithIp"),"")

                if i == 0:
                    self.MoneyTransferChainStart(accountId, accountIp)
                response = self.BankTransfer(accountId, accountIp, nextId, nextIp)
                if response == False or response == "uncleaned":
                    break
            else:
                break
        self.MoneyTransferChainEnd()

    def MissionBase(text):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                self.missionAccountNumber, self.missionAccountIp = self.GetBankAccount(self.missionBank)
                self.currentUrl = self.TransLink("missions")

                currentMission = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[1]/ul/li[2]")
                if currentMission.get_attribute("class") == "link active":
                    print("MISSION ALREADY IN PROGRESS")
                    return False

                table = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div[1]/div/div[2]/table/tbody").find_elements_by_tag_name("tr")
                for item in table:
                    mission = item.find_element_by_xpath('./td[2]/a')
                    if mission.text == text:
                        self.currentUrl = mission.get_attribute("href")

                        acceptButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/span[1]")
                        loop = True
                        while loop:
                            try:
                                acceptButton.click()
                                confirmButton = self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/span[2]/div/form/div[2]/input[3]")
                            except NoSuchElementException:
                                pass
                            except ElementClickInterceptedException:
                                loop = False

                        confirmButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/span[2]/div/form/div[2]/input[3]")
                        confirmButton.click()

                        if not func(self, *args, **kwargs):
                            return False

                        self.ClickElementBeforePopup("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/span[1]")

                        # Open dropdown
                        while True:
                            try:
                                accountDropdown = self.FindElementByXpath('/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/span[2]/div/form/div[1]/span/div/a/span[1]')
                                accountDropdown.click()
                                break
                            except StaleElementReferenceException:
                                print("STALE!?!?!?!")

                        # Select the correct account
                        for choice in self.FindElementByXpath('//*[@id="select2-drop"]/ul').find_elements_by_tag_name("li"):
                            choiceText = choice.text
                            if choiceText[1:10] == self.missionAccountNumber:
                                choice.click()
                                break

                        confirmButton = self.FindElementByXpath('//*[@id="modal-submit"]')
                        confirmButton.click()
                        break
                else:
                    return False
                return True
            return wrapper
        return decorator

    @MissionBase("Transfer money")
    def MissionTransferMoney(self):
        fromDetails = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]")
        fromNumber = fromDetails.text[1:10]
        fromIp = fromDetails.text[10:]

        toDetails = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody/tr[3]/td[2]")
        toNumber = toDetails.text[1:10]
        toIp = toDetails.text[10:]

        if hasattr(self, "oldAccountNumber") and hasattr(self, "oldAccountIp"):
            if not self.BankTransfer(self.oldAccountNumber, self.oldAccountIp, fromNumber, fromIp):
                return False
        else:
            self.MoneyTransferChainStart(fromNumber, fromIp)

        if not self.BankTransfer(fromNumber, fromIp, toNumber, toIp):
            return False

        self.currentUrl = self.TransLink("missions")

        return True

    @MissionBase("Check bank status")
    def MissionCheckBankStatus(self):
        accountDetails = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]")

        accountNumber = accountDetails.text[1:10]
        accountIp = accountDetails.text[10:]

        if not self.BankCrack(accountNumber, accountIp):
            return False

        amountText = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[1]/ul/li/div[2]/strong")
        amount = amountText.text
        print(amount)

        self.currentUrl = self.TransLink("bankLogout")

        self.currentUrl = self.TransLink("missions")
        balanceField = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/form/div/div/input")
        balanceField.send_keys(amount)

        return True

    @MissionBase("Delete software")
    def MissionDeleteSoftware(self):
        victimIp = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/a")
        victimIp = victimIp.get_attribute("href").replace(self.TransLink("internetWithIp"),"")
        fileName = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]","/html/body/div[4]/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]")
        fileName = fileName.text.split(".")[0]

        self.Hack(victimIp, False, False)

        loop = True
        while loop:
            softwares = self.GetRemoteSoftware()
            for softwareID in softwares:
                if softwares[softwareID]["name"] == fileName:
                    self.DeleteRemoteSoftware(softwareID)
                    loop = False
                    break
            else:
                minutesTillReset = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[3]/div[2]/div/div[2]/div/strong[1]").text
                time.sleep(int(minutesTillReset)*60)


        self.currentUrl = self.TransLink("missions")

        return True

    def Hack(self, ip, clearLog, infect):
        # Hack host
        # Make sure your not hacking yourself
        localIp = self.localIp
        if ip == localIp:
            return False
        else:
            print("Hacking",ip)

        # Start by logging out if logged in to another IP
        self.currentUrl = self.TransLink("internetLogout")

        # Then proceed to go to the ip requested
        self.currentUrl = self.TransLink("internetWithIp") + ip
        text = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[1]").text
        if "Login" not in text:
            print("Invalid ip", ip)
            self.Database(ip, "Invalid ip")
            return False

        # Try to login
        self.currentUrl = self.TransLink("internetLogin")

        loginButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/form/div[3]/span/input")
        loginButton.click()

        if self.currentUrl == self.TransLink("internetLogin") + "&user=&pass=":
            # Use brute force
            self.currentUrl = self.TransLink("internetBruteforce")

            # Wait for the next section to be ready
            while self.TransLink("localProcess") in self.currentUrl:
                time.sleep(.1)

            if self.currentUrl == self.TransLink("internet"):
                errorText = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[2]").text.split("\n")[-1]
                # No cracker installed
                if errorText == "Error! You do not have the needed software to perform this action.":
                    # Install cracker if on local server
                    if self.DownloadLocalSoftwareByType("crc", self.missionCrackerVersion):
                        return self.Hack(ip, clearLog)
                    else:
                        return False

                # Cracker not good enough
                elif errorText == "Error! Access denied: your cracker is not good enough.":
                    print("Cracker not good enough")
                    self.Database(ip, "Cracker not good enough")
                    return False

                # UNKNOWN ERROR?
                else:
                    print(errorText)

            elif self.currentUrl == self.TransLink("internetLogin"):
                loginButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div[1]/div[3]/div[2]/div/form/div[3]/span[3]/input")
                loginButton.click()

        if self.currentUrl == self.TransLink("internet"):
            try:
                errorText = self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div[1]/div[2]").text.split("\n")[-1]
                if errorText == "Error! You do not have the needed software to perform this action.":
                    # Install cracker if on local server
                    if self.DownloadLocalSoftwareByType("crc", self.missionCrackerVersion):
                        return self.Hack(ip, clearLog)
                    else:
                        print("COULDN'T OBTAIN ACCES TO",ip)
                        return False
                elif errorText == "Error! Access denied: your cracker is not good enough.":
                    print("Cracker not good enough")
                    self.Database(ip, "Cracker not good enough")
                    return False
                else:
                    print(errorText)
            except NoSuchElementException:
                pass

        # Successfully entered remote
        if clearLog:
            self.ClearRemoteLog()

        # Retrieve software
        self.Database(ip, self.GetRemoteSoftware())

        print("HACKED",ip)
        if infect:
            self.Infect()
        return True

    def DDOS(self, ip, batch, hack, clearLog):
        print(ip,batch,hack,clearLog)
        if hack:
            self.Hack(ip, clearLog)

        for i in range(batch):
            self.currentUrl = self.TransLink("ddos")

            ipField = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input")
            ipField.send_keys(ip)

            try:
                self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input")
            except NoSuchElementException:
                if not self.DownloadLocalSoftwareByType("vbrk"):
                    return False
                else:
                    self.currentUrl = self.TransLink("ddos")
                    ipField = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[1]/div/input")
                    ipField.send_keys(ip)

            ddosButton = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[1]/div/div[3]/form/div[2]/div/input")
            ddosButton.click()

            self.WaitForURL(self.TransLink("localSoftware"))

    def Worm(self, ipsToHack, hackedIps, clearLog):
        self.currentUrl = self.TransLink("ddos")
        runningDDOS = self.FindElementByXpath("/html/body/div[4]/div[3]/div/div/div/div[2]/div/div[2]/div/div[2]")
        hackedIps.update(set(re.findall(self.ipRegex,runningDDOS.text)))
        self.ips.update(ipsToHack)
        self.hackedIps = set(hackedIps)

        while len(self.ips) != 0:
            print("\n\n\nHACKED IPS",hackedIps,"\nBTC",self.btc,"\nIps to Hack",self.ips,"\n\n\n")
            ip = self.ips.pop()
            if ip not in self.hackedIps:
                hackedIps.update({ip})
                self.Hack(ip, clearLog, infect = True)

    def Infect(self):
        # Skip if already infected with the virus
        print("Check if remote infected with the virus")
        remoteSoftware = self.GetRemoteSoftware()
        for remoteSoftwareId in remoteSoftware:
            if remoteSoftware[remoteSoftwareId]["type"] == "vddos" and remoteSoftware[remoteSoftwareId]["viruscontrol"]:
                print("vDDOS detected, skipping vDDOS")
                break
        else:
            # Make sure local has a copy of the virus, if not, then install
            print("No vDDOS detected, installing")
            print("Make sure local has a copy of the virus, if not, then install")
            localSoftware = self.GetLocalSoftware()
            for localSoftwareId in localSoftware:
                if localSoftware[localSoftwareId]["type"] == "vddos" and not localSoftware[localSoftwareId]["installed"]:
                    break
            else:
                localHarddisk = self.GetLocalHarddisk()
                for localHarddiskId in localHarddisk:
                    if localHarddisk[localHarddiskId]["type"] == "vddos":
                        self.DownloadLocalSoftware(localHarddiskId)
                        localSoftware = self.GetLocalSoftware()
                        for localSoftwareId in localSoftware:
                            if localSoftware[localSoftwareId]["type"] == "vddos" and not localSoftware[localSoftwareId]["installed"]:
                                break
                        break

            # Upload the virus if not present on remote
            print("Upload the virus if not present on remote")
            remoteSoftware = self.GetRemoteSoftware()
            for remoteSoftwareId in remoteSoftware:
                if localSoftware[localSoftwareId]["name"] == remoteSoftware[remoteSoftwareId]["name"] and not remoteSoftware[remoteSoftwareId]["installed"]:
                    break
            else:
                if not self.UploadToRemote(localSoftwareId):
                    return

            # Install the virus
            print("Install the virus")
            remoteSoftware = self.GetRemoteSoftware()
            for remoteSoftwareId in remoteSoftware:
                if localSoftware[localSoftwareId]["name"] == remoteSoftware[remoteSoftwareId]["name"] and not remoteSoftware[remoteSoftwareId]["installed"]:
                    self.InstallRemoteSoftware(remoteSoftwareId)
                    break


        # INSTALL OTHER PRESSENT VIRUSSES
        print("INSTALL OTHER PRESSENT VIRUSSES")
        remoteSoftware = self.GetRemoteSoftware()
        controlled = {remoteSoftware[remoteSoftwareId]["type"] for remoteSoftwareId in remoteSoftware if remoteSoftware[remoteSoftwareId]["viruscontrol"]}
        installAble= {remoteSoftware[remoteSoftwareId]["type"] for remoteSoftwareId in remoteSoftware if remoteSoftware[remoteSoftwareId]["type"] in {"vddos","vspam","vwarez","vminer"} and not remoteSoftware[remoteSoftwareId]["installed"]} - controlled
        print("installAble viruses", installAble)
        for remoteSoftwareId in remoteSoftware:
            software = remoteSoftware[remoteSoftwareId]
            if software["type"] in installAble and not software["installed"]:
                # Clear log before installing, in case the install takes some time
                self.ClearRemoteLog()
                print("Installing", software["type"])
                self.InstallRemoteSoftware(remoteSoftwareId)
                installAble -= {software["type"]}

        # CleanLog
        self.ClearRemoteLog()
