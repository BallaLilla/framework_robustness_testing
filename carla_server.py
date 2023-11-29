import os
import psutil
import subprocess
import time

class CARLAServer():
    def __init__(self, timeout=10):
        self.exe_path = os.environ.get("CARLA")
        self.timeout = timeout
        if not self.check_carla_is_running():
            call_string = f"{self.exe_path} -dx11 -carla-server"
            print(call_string)
            self.process = subprocess.Popen(call_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(self.timeout)
        else:
            print("CarlaUE4.exe is already running. No need to start it again.")

    def check_carla_is_running(self):
        for proc in psutil.process_iter():
            try:
                if 'CARLA'.lower() in proc.name().lower():
                    print('CARLA process is running.')
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                print(f"Error checking for CARLA process: {e}")
        return False
    
    def stop(self):
        if self.process is not None:
            print('Terminating CARLA ...')
            carla_parent_process = psutil.Process(self.process.pid)
            for carla_child_process in carla_parent_process.children(recursive=True):
                carla_child_process.terminate()
            self.process.terminate()
            self.process.wait()
            print('CARLA has been closed.')
        else:
            print("CARLA is not running")

    
   