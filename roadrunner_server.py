import subprocess
import shutil
import os
import time

IP_address = "127.0.0.1"
port = "54321"

class RoadRunnerServer:
    def __init__(self, project_path):
        self.installation_path = "C:/Program Files/RoadRunner R2023b/bin/win64"
        self.project_path = project_path.replace(os.sep, '/')
        print("self_proj_path: ", self.project_path)
        print("RoadRunner server init")
        
        callString = "AppRoadRunner --apiPort " + port + " --projectPath " + self.project_path
        print(callString)
        self.process = subprocess.Popen(callString)
        time.sleep(10)
       
