import subprocess
import os
import time


class CARLAServer:
    def __init__(self):
        self.exe_path = r"C:\Users\balia\Desktop\szakdolgozat\robustness_testing\CARLA_0.9.14\WindowsNoEditor\CarlaUE4.exe".replace(os.sep, '/')
        
        
        callString = self.exe_path + " -dx11"
        print(callString)
        server_is_started = subprocess.Popen(callString)
        time.sleep(60)


        if server_is_started:
            Exception("CARLA server cannot be strated")

