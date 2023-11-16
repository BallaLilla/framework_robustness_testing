import shutil
import os
import carla
import subprocess
import time
import psutil


class CARLAClient:
    def __init__(self, ip_address="127.0.0.1", port=2000):
        self.carla_client = carla.Client(ip_address, port)
        self.carla_client.set_timeout(10)
        

    def _generate_opendrive_world(self, xodr_path, vertex_distance=1, max_road_length=3000, wall_height=1, extra_width=0) :  
        # Load an OpenDRIVE file
        if xodr_path :
            print("specified xodr: ", xodr_path)
            if os.path.exists(xodr_path):
                 print("exist")
                 with open(xodr_path, encoding='utf-8') as od_file:
                    try:
                        data = od_file.read()
                    except:
                        raise("Specified xodr cannot be read")
                    try:
                        print("test_to_import_CARLA: ")
                        carla_world = self.carla_client.generate_opendrive_world(
                            data, carla.OpendriveGenerationParameters(
                            vertex_distance=vertex_distance,
                            max_road_length=max_road_length,
                            wall_height=wall_height,
                            additional_width=extra_width,
                            smooth_junctions=False,
                            enable_mesh_visibility=True))
                        
                        settings = carla_world.get_settings()
                        

                        #client_carla_word = self.carla_client.get_world()
                        #client_carla_word.apply_settings(settings) 
                        print("Done")
                    except Exception as e:
                        print(e)
                        return False
            else :
                errorMessage = "Cannot find an OpenDRIVE file %s. " % xodr_path
                return False
        return True
    

    def close_Carla(self):
        try:
            for process in psutil.process_iter(['pid', 'name']):
                if 'CarlaUE4' in process.info['name']:
                    pid = process.info['pid']
                    psutil.Process(pid).terminate()
                    print(f"{process.info['name']} (PID: {pid}) terminated successfully.")
        except Exception as e:
            print(f"Error terminating processes: {e}")


