HE = __import__("main")
Worm = __import__("worm")
from tkinter import *
import tkinter.messagebox as tm
import re

class Graphics(Frame):
        def __init__(self, master):
            super().__init__(master)
            HE.Start()
            self.ClearLogGUI()
            self.HackGUI()
            self.DDosGUI()
            self.WormGUI()
            self.pack()

        def ClearLogGUI(self):
            self.clearLogButton = Button(self, text="Clear Log", command = self.ClearLog)
            self.clearLogButton.grid(row=0, column=0, sticky=W)

        def HackGUI(self):
            self.hackIpLabel = Label(self, text="Ip:  ")
            self.hackIpEntry = Entry(self)

            self.hackIpLabel.grid(row=1, column=1, sticky=E)
            self.hackIpEntry.grid(row=1, column=2, sticky=W)

            self.hackTKClearLog = BooleanVar()
            self.hackClearLogCheckbox = Checkbutton(self, text="Clear Log", variable = self.hackTKClearLog)
            self.hackClearLogCheckbox.grid(row=1, column=3)
            self.hackClearLogCheckbox.select()
            self.hackTKGetSoftware = BooleanVar()
            self.hackGetSoftwareCheckbox = Checkbutton(self, text="Get Software", variable = self.hackTKGetSoftware)
            self.hackGetSoftwareCheckbox.grid(row=1, column=4)
            self.hackGetSoftwareCheckbox.select()


            self.hackButton = Button(self, text="Hack", command = self.Hack)
            self.hackButton.grid(row=1, column=0, sticky=W)

        def DDosGUI(self):
            self.ddosIpLabel = Label(self, text="Ip:  ")
            self.ddosIpEntry = Entry(self)

            self.ddosIpLabel.grid(row=2, column=1, sticky=E)
            self.ddosIpEntry.grid(row=2, column=2, sticky=W)

            self.ddosTimesLabel = Label(self, text="Times:  ")
            self.ddosTimesEntry = Entry(self)

            self.ddosTimesLabel.grid(row=2, column=3, sticky=E)
            self.ddosTimesEntry.grid(row=2, column=4, sticky=W)
            self.ddosTimesEntry.insert(END, '1')


            self.ddosTKHack = BooleanVar()
            self.ddosClearLogCheckbox = Checkbutton(self, text="Hack", variable = self.ddosTKHack)
            self.ddosClearLogCheckbox.grid(row=2, column=5)
            self.ddosClearLogCheckbox.select()

            self.ddosTKClearLog = BooleanVar()
            self.ddosClearLogCheckbox = Checkbutton(self, text="Clear Log", variable = self.ddosTKClearLog)
            self.ddosClearLogCheckbox.grid(row=2, column=6)
            self.ddosClearLogCheckbox.select()

            self.ddosTKGetSoftware = BooleanVar()
            self.ddosGetSoftwareCheckbox = Checkbutton(self, text="Get Software", variable = self.ddosTKGetSoftware)
            self.ddosGetSoftwareCheckbox.grid(row=2, column=7)
            self.ddosGetSoftwareCheckbox.select()


            self.ddosButton = Button(self, text="DDos", command = self.DDos)
            self.ddosButton.grid(row=2, column=0, sticky=W)

        def WormGUI(self):
            self.wormIpLabel = Label(self, text="Text containing ips:  ")
            self.wormIpLabel.grid(row=4, column=0, columnspan = 7, sticky=W)

            self.wormTKClearLog = BooleanVar()
            self.wormClearLogCheckbox = Checkbutton(self, text="Clear Log", variable = self.wormTKClearLog)
            self.wormClearLogCheckbox.grid(row=3, column=1)
            self.wormClearLogCheckbox.select()
            self.wormTKGetSoftware = BooleanVar()
            self.wormGetSoftwareCheckbox = Checkbutton(self, text="Get Software", variable = self.wormTKGetSoftware)
            self.wormGetSoftwareCheckbox.grid(row=3, column=2)
            self.wormGetSoftwareCheckbox.select()

            self.wormText = Text(self, width = 50, height = 50, wrap = WORD)
            self.wormText.grid(row = 5, column = 0, columnspan = 7, sticky = W)

            self.wormButton = Button(self, text="Start Worm", command = self.Worm)
            self.wormButton.grid(row=3, column=0, sticky=W)


        def ClearLog(self):
            HE.PrintDebug ("ClearLog()")
            #tm.showinfo("Task", "Clearing Log")
            HE.ClearLog()

        def Hack(self):
            self.ip = self.hackIpEntry.get()
            self.clearLog = self.hackTKClearLog.get()
            self.getSoftware = self.hackTKGetSoftware.get()
            if self.ip == "":
                tm.showerror("Task", 'You cant hack "none" ip')
                return
            HE.PrintDebug ('Hack("' + self.ip + '", ' + str(self.clearLog) + ", " + str(self.getSoftware) + ")")
            HE.Hack(self.ip, self.clearLog, self.getSoftware)
            #tm.showinfo("Task", "Hacking: " + self.ip)

        def DDos(self):
            self.ip = self.ddosIpEntry.get()
            self.times = self.ddosTimesEntry.get()
            self.hack = self.ddosTKHack.get()
            self.clearLog = self.ddosTKClearLog.get()
            self.getSoftware = self.ddosTKGetSoftware.get()
            if self.ip == "":
                tm.showerror("Task", 'You cant DDos "none" ip')
                return
            try:
                int(self.times)
            except:
                tm.showerror("Task", "You cant DDos " + self.ip + " " + self.times + " times")
                return
            HE.PrintDebug ('DDos("' + self.ip + '", ' + self.times + ", " + str(self.hack) + ", " + str(self.clearLog) + ", " + str(self.getSoftware) + ")")
            HE.DDos(self.ip, int(self.times), self.hack, self.clearLog, self.getSoftware)

        def Worm(self):
            self.inputWithIps = self.wormText.get("1.0",'end-1c')
            self.clearLog = self.wormTKClearLog.get()
            self.getSoftware = self.wormTKGetSoftware.get()
            if self.inputWithIps == "":
                tm.showerror("Task", 'You cant start a worm on "none" ip')
                return
            self.ips = []
            inputLine = self.inputWithIps
            #inputLines = self.inputWithIps.split("\n")
            #for inputLine in inputLines:
            foundIpList = re.findall( r'[0-9]+(?:\.[0-9]+){3}', inputLine)
            for foundIp in foundIpList:
                if foundIp == HE.yourIp:
                    continue
                else:
                    self.ips.append(foundIp)
            HE.PrintDebug ('Worm("' + str(self.ips) + '", ' + str(self.clearLog) + ", " + str(self.getSoftware) + ")")
            Worm.Worm(self.ips, self.clearLog, self.getSoftware, HE.yourIp)


root = Tk()
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
root.geometry('705x935+' + str(int(ws/2+50)) + "+25")
root.title("HE bot")
try:
    root.iconbitmap('HE bot.ico')
except:
    pass
lf = Graphics(root)
root.mainloop()
