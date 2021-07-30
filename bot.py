import re
import time
import modules
import importlib
import graphics as graphicsTools

# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException

# Stop the webdriver from closing on keyboard interrupt
# Inspiration from https://stackoverflow.com/a/49323296
import WebdriverKeyboardInterruptSecured
webdriver.common.service.Service.start = WebdriverKeyboardInterruptSecured.start

#####
## Setup optional variables related to settings
####
try: import settings
except NameError: pass

try: password = settings.password
except NameError: password = ""

try: username = settings.username
except NameError: username = ""

try: format = settings.format
except NameError: format = True

try: transferBank = settings.transferBank
except NameError: transferBank = "HEBC"

try: missionBank = settings.missionBank
except NameError: missionBank = "First International Bank"

try: missionCrackerVersion = settings.missionCrackerVersion
except NameError: missionCrackerVersion = 2.9

try: secondBTCaddr = settings.secondBTCaddr
except NameError: secondBTCaddr = ""

#####
## Hooks for the Modules
####
class Hooks:
    def __init__(self, gui, driver):
        self.gui = gui
        self.driver = driver
        self.ipRegex = r"(?:[^\d\.]|^)(\d{1,3}(?:\.\d{1,3}){3})(?:[^\d\.]|$)"
        self.bot = modules.Bot(self.gui, self.driver, format, transferBank, missionBank, missionCrackerVersion, secondBTCaddr)

    def Reload(self):
        importlib.reload(modules)
        print("reloaded modules")

        del self.bot
        self.bot = modules.Bot(self.gui, self.driver, format, transferBank, missionBank, missionCrackerVersion, secondBTCaddr)

    def ClearLog(self):
        self.bot.ClearLocalLog()
        print("DONE")

    def Hack(self):
        searchIp = re.search(self.ipRegex, self.gui.HACKipInputField.text)
        if searchIp == None:
            print("No valid ip given to HACK")
            return False

        self.bot.Hack(ip = searchIp.group(1), clearLog = self.gui.HACKclearLogCheckbox.value, infect = self.gui.HACKinfectCheckbox.value)
        return True
        print("DONE")

    def DDOS(self):
        searchIp = re.search(self.ipRegex, self.gui.DDOSipInputField.text)
        if searchIp == None:
            print("No valid ip given to DDOS")
            return False

        batch = self.gui.DDOSbatchInputField.text
        if not batch.isdigit():
            print('"' + batch + '"' + " isn't a valid amount of times to DDOS \nan int is required")
            return False

        self.bot.DDOS(ip = searchIp.group(1), batch = int(batch), hack = self.gui.DDOShackCheckbox.value, clearLog = self.gui.DDOSclearLogCheckbox.value)
        print("DONE")

    def Worm(self):
        ipsToHack = {ip for ip in re.findall(self.ipRegex, self.gui.WORMipsToHackTextField.text)}
        hackedIps = {ip for ip in re.findall(self.ipRegex, self.gui.WORMipsHackedTextField.text)}

        if len(ipsToHack) == 0:
            print("No valid entry ips given to WORM")
            return False

        self.bot.Worm(ipsToHack = ipsToHack, hackedIps = hackedIps, clearLog = self.gui.WORMclearLogCheckbox.value)
        print("DONE")

    def MissionMedium(self):
        while True:
            if (not self.bot.MissionCheckBankStatus()) or (not self.gui.MISSIONloopCheckbox.value):
                break
        print("DONE")

    def MissionVeryEasy(self):
        while True:
            if (not self.bot.MissionDeleteSoftware()) or (not self.gui.MISSIONloopCheckbox.value):
                break
        print("DONE")

    def MissionHard(self):
        while True:
            if (not self.bot.MissionTransferMoney()) or (not self.gui.MISSIONloopCheckbox.value):
                self.bot.MoneyTransferChainEnd()
                break
        print("DONE")

    def BankAccountCleaner(self):
        batch = self.gui.BANKbatchInputField.text
        if not batch.isdigit():
            print('"' + batch + '"' + " isn't a valid amount of times to Clean \nan int is required")
            return False

        self.bot.BankAccountCleaner(int(batch))
        print("DONE")

    def LocalBankCleaner(self):
        self.bot.LocalBankCleaner()
        print("DONE")

#####
## GUI
####
class GUI:
    colorRed = "#ff676b"
    colorGreen = "#1AE62B"
    colorYellow = "#FFA500"
    colorBlue = "#D4EBF2"

    def __init__(self):
        self.webdriver = WebDriver(self)
        self.hooks = Hooks(self, self.webdriver.driver)
        self.webdriver.bot = self.hooks.bot

        self.window = graphicsTools.Window()
        self.window.overlay = 5
        self.width = self.window.root.winfo_screenwidth()
        self.height = self.window.root.winfo_screenheight()
        self.window.geometry = (self.width-self.width/4, 0, self.width/4, self.height)
        self.graphics = self.window.graphics
        self.graphics.backgroundColor('#fafafa')

        self.checkboxColors = [GUI.colorRed, GUI.colorGreen]
        self.border = 5

        self.graphics.Button(self.graphics, 0.01, 0.01, 0.07, 0.06, "Clear Log", self.hooks.ClearLog, self.border)

        self.graphics.Button(self.graphics, 0.19, 0.01, 0.24, 0.06, "Reload", self.hooks.Reload, self.border)
        self.graphics.CheckBox(self.graphics, 0.12, 0.01, 0.17, 0.06, text="Dock", width = self.border, colors=self.checkboxColors, value = True, func = self.dock)

        self.graphics.Button(self.graphics, 0.01, 0.10, 0.07, 0.15, "Hack", self.hooks.Hack, self.border)
        self.HACKipInputField = self.graphics.InputField(self.graphics, 0.08, 0.10, 0.18, 0.15, text="1.2.3.4", width = self.border, backgroundColor = GUI.colorBlue)
        self.HACKclearLogCheckbox = self.graphics.CheckBox(self.graphics, 0.01,0.16,0.07,0.21, text="Clear Log", width = self.border, colors=self.checkboxColors, value = True)
        self.HACKinfectCheckbox = self.graphics.CheckBox(self.graphics, 0.08,0.16,0.14,0.21, text="Infect", width = self.border, colors=self.checkboxColors, value = False)

        self.graphics.Button(self.graphics, 0.01, 0.25, 0.07, 0.30, "DDOS", self.hooks.DDOS, self.border)
        self.DDOSipInputField = self.graphics.InputField(self.graphics, 0.08, 0.25, 0.18, 0.30, text="xxx.xxx.xxx.xxx", width = self.border, backgroundColor = GUI.colorBlue)
        self.DDOSbatchInputField = self.graphics.InputField(self.graphics, 0.19, 0.25, 0.24, 0.30, text="batch", width = self.border, backgroundColor = GUI.colorBlue)
        self.DDOShackCheckbox = self.graphics.CheckBox(self.graphics, 0.01,0.31,0.07,0.36, text="Hack", width = self.border, colors=self.checkboxColors)
        self.DDOSclearLogCheckbox = self.graphics.CheckBox(self.graphics, 0.08,0.31,0.14,0.36, text="Clear Log", width = self.border, colors=self.checkboxColors, value = True)

        self.graphics.Button(self.graphics, 0.01, 0.40, 0.08, 0.45, "Start Worm", self.hooks.Worm, self.border)
        self.WORMclearLogCheckbox = self.graphics.CheckBox(self.graphics, 0.09,0.40,0.15,0.45, text="Clear Log", width = self.border, colors=self.checkboxColors, value = True)
        self.WORMipsToHackTextField = self.graphics.TextField(self.graphics, 0.01, 0.46, 0.12, 0.64, text="ips to hack", scale=.5, width = self.border, backgroundColor = GUI.colorBlue)
        self.WORMipsHackedTextField = self.graphics.TextField(self.graphics, 0.13, 0.46, 0.24, 0.64, text="hacked ips", scale=.5, width = self.border, backgroundColor = GUI.colorBlue)

        self.graphics.Button(self.graphics, 0.01, 0.69, 0.13, 0.74, "Remote Bank Cleaner", self.hooks.BankAccountCleaner, self.border)
        self.BANKbatchInputField = self.graphics.InputField(self.graphics, 0.14, 0.69, 0.19, 0.74, text="batch", width = self.border, backgroundColor = GUI.colorBlue)
        self.graphics.Button(self.graphics, 0.01, 0.75, 0.13, 0.80, "Local Bank Cleaner", self.hooks.LocalBankCleaner, self.border)


        self.graphics.Button(self.graphics, 0.01, 0.85, 0.06, 0.90, "Check", self.hooks.MissionMedium, self.border)
        self.graphics.Button(self.graphics, 0.07, 0.85, 0.12, 0.90, "Delete", self.hooks.MissionVeryEasy, self.border)
        self.graphics.Button(self.graphics, 0.13, 0.85, 0.18, 0.90, "Transfer", self.hooks.MissionHard, self.border)
        self.MISSIONloopCheckbox = self.graphics.CheckBox(self.graphics, 0.01, 0.91, 0.06, 0.96, text="Loop", width = self.border, colors=self.checkboxColors)

    def loop(self):
        while True:
            self.graphics.update()
            time.sleep(.1)

    def dock(self, value):
        if value:
            self.graphics.update()
            posX,posY,sizeX,sizeY = self.window.geometry
            self.window.geometry = (posX//self.width*self.width + self.width-self.width/4, posY//self.height*self.height, self.width/4, self.height)
            self.window.overlay = 5
        else:
            self.window.overlay = 0

#####
## WebDriver
####
class WebDriver:
    def __init__(self, gui):
        self.gui = gui

        #####
        ## Removes the infobar stating
        ## Chrome is being controlled by automated test software
        #####
        options = Options()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches",["enable-automation"])

        self.driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
        self.driver.get("https://hackerwars.io/")

    def login(self):
        loginbutton = self.bot.FindElementByXpath("/html/body/div[2]/div[2]/div/div/div/ul/li[1]/a")
        loginbutton.click()

        usernameField = self.bot.FindElementByXpath("/html/body/div[3]/div/div/div[2]/div/form/input[1]")
        usernameField.send_keys(username)

        passwordField = self.bot.FindElementByXpath("/html/body/div[3]/div/div/div[2]/div/form/input[2]")
        passwordField.send_keys(password)

        print("Waiting for login")

        self.bot.WaitForURL("home")

        print("Logged in")

        self.bot.BitcoinLogin()

gui = GUI()
gui.graphics.update()
gui.webdriver.login()
latestTime = time.time()
while True:
    try:
        gui.loop()
    except Exception as ex:
        print("CAUGHT:",ex)
    except KeyboardInterrupt:
        if time.time() - latestTime < 1:
            print("Stopping...")
            gui.webdriver.driver.quit()
            gui.graphics.stop()
            break
        else:
            print("KeyboardInterrupt!","\nDo another KeyboardInterrupt within a second to stop program")
            latestTime = time.time()
