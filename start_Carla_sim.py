import subprocess

pathToCarlaExe = "C:/Users/balia/Desktop/Szakdolgozat/CARLA_0.9.14/WindowsNoEditor/CarlaUE4.exe"

# Start Carla simulator
runCarlaCommand = (pathToCarlaExe + ' -dx11')
subprocess.run(runCarlaCommand, check=True)
