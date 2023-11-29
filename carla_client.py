import carla
import os

class CARLAClient:
    def __init__(self, ip_address = "localhost", port=2000, timeout=10):
        self.carla_client = carla.Client(ip_address, port)
        self.carla_client.set_timeout(timeout)

    def make_record(self, log_path, duration):
        print('Making record.....')
        self.carla_client.start_recorder(log_path, duration)
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


