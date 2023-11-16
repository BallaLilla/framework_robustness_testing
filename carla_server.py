import subprocess
import os
import time
import psutil


class CARLAServer:
    def __init__(self):
        self.exe_path = r"C:\Users\balia\Desktop\szakdolgozat\robustness_testing\CARLA_0.9.14\WindowsNoEditor\CarlaUE4.exe".replace(os.sep, '/')
        is_carla_running = any('CarlaUE4' in process.info['name'] for process in psutil.process_iter(['name']))
        
        if not is_carla_running:
            callString = self.exe_path + " -dx11"
            print(callString)
            server_is_started = subprocess.Popen(callString)
            time.sleep(15)
        else:
            print("CarlaUE4.exe is already running. No need to start it again.")