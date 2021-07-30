# HackerWarsBot
A bot made to play the game HackerWars, in earlier days known has HackerExperience
I hope this bot can be of use :D
![image](https://user-images.githubusercontent.com/34891657/127701068-3ccbd840-90ac-4685-85b1-906fcdb4be57.png)
## Features
- Clear local log
- Dock the GUI to turn it into and overlay
- **Reload** the code on the fly
- Hack an ip with the option to infect and clear the log upon success
- DDOS an ip a specific number of times, with the option to hack the target beforehand (clearlog is only implemented to clear the log upon hack)
- **[Worm](#worm)**, go from server to server scouring the log and infecting the servers
- **Clean the database of hacked bank accounts** (works best with bank accounts from missions, could break otherwise D: )
- **Clean local banks accounts**, transfers money from one account to the other closing and reopening the accounts afterwars
- Complete missions
	- Very easy (Delete software)
	- Medium (Check balance)
	- Hard (Transfer money)
- 	**Gather software information**
- **Automatic bitcoin login** (You can remove this feature in [bot.py](https://github.com/Mikbrosim/HackerExperienceBot/blob/95180f16822b96f4d16f476545f07c378e44695a/bot.py#L237))

## Requirements
- Chrome
- Python 3
- Selenium
- Tkinter
- An account on  https://hackerwars.io/

## Settings
Create a file called "settings.py" in your directory.
The bellow variables can be used in your "settings.py"
```
# Username for autologin
username = ""

# Password for autologin
password = ""

# Whether or not the bot is allowed to format the hardrive, upon not being able to download a file successfully
format = True

# The bank name used as a reciever in money transfers
transferBank = "HEBC"

# The bank name used to recieve rewards from missions
missionBank = "First International Bank"

# The highest version of a cracker allowed for download if no cracker on local server
missionCrackerVersion = 2.9

# If used, the bot will automatically transfer bitcoins to the second BTC address after buying them
secondBTCaddr = ""
```

## How the worm works
Start the worm by inputting a text containing one or more ips with the option to avoid some other ips
If able to obtain access to the remote server, the worm then scours through the log, in order for it to obtain more ips to infect. After looking through the log, the bot then proceeds to infect the server.

How the worm and infection is carried out can be edited in the last two functions in the file modules.py [Worm](https://github.com/Mikbrosim/HackerExperienceBot/blob/95180f16822b96f4d16f476545f07c378e44695a/modules.py#L1141) [Infect](https://github.com/Mikbrosim/HackerExperienceBot/blob/95180f16822b96f4d16f476545f07c378e44695a/modules.py#L1155)

## How to use
Just run bot.py with python3
