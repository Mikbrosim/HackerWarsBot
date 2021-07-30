import json

try:
    db = json.load(open("./softwares.json", "r"))

    # CLEAN DATABASE
    db = {ip:db[ip] for ip in db if db[ip] != "Invalid ip"}
    json.dump(db , open("./softwares.json", "w+"))

except FileNotFoundError:
    db = {}
finally:
    print("Hacked Ips\n",[ip for ip in db if db[ip] != "Cracker not good enough"])
    print("\nCracker not good enought to access\n",[ip for ip in db if db[ip] == "Cracker not good enough"],"\n")

    # Extract best
    bestversions = {"crc":0,"hash":0,"fwl":0,"vcol":0,"hdr":0,"skr":0,"vbrk":0,"av":0,"ftp":0,"ssh":0}
    bestsoftwares = {}

    for ip in db:
        softwares = db[ip]
        if isinstance(softwares, dict):
            for softwareId in softwares:
                software = softwares[softwareId]
                for softwareType in bestversions:
                    if softwareType not in ["ftp","ssh"]:
                        if software["type"] == softwareType and float(software["version"]) > bestversions[softwareType]:
                            bestversions[softwareType] = float(software["version"])
                            bestsoftwares[softwareType] = "\t".join([softwareType, str(software["version"]), ip, softwareId, software["name"]])
                    else:
                        softwareIcon = "14" if softwareType == "ssh" else "13"
                        if "icon" not in software:
                            continue
                        if software["icon"] == softwareIcon and float(software["version"]) > bestversions[softwareType]:
                            bestversions[softwareType] = float(software["version"])
                            bestsoftwares[softwareType] = "\t".join([softwareType, str(software["version"]), ip, softwareId, software["name"]])

    for softwareType in bestsoftwares:
        print(bestsoftwares[softwareType])



    #"""
    # Print with threshold
    print()
    for ip in db:
        softwares = db[ip]
        if isinstance(softwares, dict):
            for softwareId in softwares:
                software = softwares[softwareId]
                if software["type"] == "crc" and float(software["version"]) >= 2.5:
                    print("\t".join([softwares[softwareId]["type"], str(software["version"]), ip, software["name"], str(software["size"])]))
    #"""
