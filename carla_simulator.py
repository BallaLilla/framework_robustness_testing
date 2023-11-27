import os
import time
import subprocess
import psutil
import logging
import carla

from simulator import Simulator

class CARLASimulator(Simulator):

    def __init__(self):
        self.exe_path = os.environ.get("CARLA")
        self.process = None
        self.timeout = 10
        self.carla_client = None

    
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
            self.process.wait()  # Wait for the process to complete termination
            print('CARLA has been closed.')
        else:
            print("CARLA is not running")


    def start_server(self):
        if not self.check_carla_is_running():
            call_string = f"{self.exe_path} -dx11 -carla-server"
            print(call_string)
            self.process = subprocess.Popen(call_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #time.sleep(self.timeout)
        else:
            print("CarlaUE4.exe is already running. No need to start it again.")


    def connect_client_to_server(self, ip_address = "localhost", port=2000, timeout=10):
        self.carla_client = carla.Client(ip_address, port)
        self.carla_client.set_timeout(timeout)
    

    def prepare_simulation(self):
        self.start_server()
        self.connect_client_to_server()


    def make_record(self, file_path, duration=1):
        print('Making record.....')
        self.carla_client.start_recorder(file_path, duration)
        self.carla_client.stop_recorder()
        

    def load_scene(self, scene_path):
        if scene_path:
            if os.path.exists(scene_path):
                _, file_extension = os.path.splitext(scene_path)
                if file_extension.lower() != '.xodr':
                    print('Error: The provided file is not an OpenDRIVE file.')
                    return False
                else:
                    with open(scene_path, encoding='utf-8') as od_file:
                        try:
                            data = od_file.read()
                        except OSError:
                            print('Error reading the specified OpenDRIVE file %r.' % os.path.basename(scene_path))
                            return False
                            
                        vertex_distance = 2.0
                        max_road_length = 500.0
                        wall_height = 0
                        extra_width = 0.6
                        try:
                            self.carla_world = self.carla_client.generate_opendrive_world(
                                data, carla.OpendriveGenerationParameters(
                                vertex_distance=vertex_distance,
                                max_road_length=max_road_length,
                                wall_height=wall_height,
                                additional_width=extra_width,
                                smooth_junctions=True,
                                enable_mesh_visibility=True))
                            print('Opendrive world has been generated.')
                        except RuntimeError as e:
                            print('Error loading the OpenDRIVE file. Error: ' + repr(e))
                            return False
                    return True
            else:
                print("Specified scene path does not exist")
            
        else:
            print("Scene path must be specified for loading into simulator")
            return False

