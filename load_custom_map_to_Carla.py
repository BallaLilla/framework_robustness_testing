import os
import subprocess


pathToMaps = "C:/Users/balia/Desktop/Szakdolgozat/process/export_from_RoadRunner"
pathToCarlaConfig = "C:/Users/balia/Desktop/Szakdolgozat/CARLA_0.9.14/WindowsNoEditor/PythonAPI/util/config.py"


# Get list of all xodr files
mapFiles = list()
for root, dirs, files in os.walk(pathToMaps):
    for file in files:
        if file.endswith(".xodr"):
            mapFiles.append(os.path.join(root,file))

# Generate map loader command
for file in mapFiles:
    command = ("python " + pathToCarlaConfig + " -x " + file)
    print("Loading map files...")
    print("Executing command:\n\n" + command + "\n")
    out = subprocess.run(command, check=True)

