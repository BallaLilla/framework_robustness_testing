import os
import subprocess
import time
import psutil


class RoadRunnerServer:
    def __init__(self, project_path=None, api_port=54321, timeout=10):
        self.api_port = api_port
        if project_path is None:
            project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "RoadRunnerProject"))
        self.project_path = project_path
        if self.roadrunner_is_running:
            self.kill()
        callString = "AppRoadRunner --apiPort " + str(api_port) + " --projectPath " + project_path
        print(callString)
        self.process = subprocess.Popen(callString, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(timeout)

    def roadrunner_is_running(self):
        for proc in psutil.process_iter():
            try:
                if 'RoadRunner'.lower() in proc.name().lower():
                    print('RoadRunner process is running.')
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                print(f"Error checking for RoadEunner process: {e}")
        return False
    
    def kill(self):
        for proc in psutil.process_iter():
            try:
                if 'RoadRunner'.lower() in proc.name().lower():
                    for child_process in proc.children(recursive=True):
                        child_process.terminate()
                    proc.terminate()
                    proc.wait()
                    print('RoadRunner has been closed.')
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                print(f"Error checking for RoadEunner process: {e}")
        
            

    
    