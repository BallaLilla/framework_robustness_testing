import carla
import os

class CARLAClient:
    def __init__(self, ip_address = "localhost", port=2000, timeout=10):
        self.carla_client = carla.Client(ip_address, port)
        self.carla_client.set_timeout(timeout)

    def make_record(self, log_path, duration):
        print('Making record.....')
        self.carla_client.start_recorder(log_path+".log", duration)
        self.carla_client.stop_recorder()
    
    def load_scene(self, scene_path):
        if not scene_path:
            print("Scene path must be specified for loading into the simulator")
            return False

        xodr_files = [f for f in os.listdir(os.path.dirname(scene_path)) if f.endswith('.xodr')]

        if not xodr_files:
            print("No .xodr files found in the specified scene path")
            return False
        
        xodr_file = xodr_files[0]
        xodr_file_path = os.path.realpath(os.path.join(os.path.dirname(scene_path),xodr_file))
        print("xodr_file: ", xodr_file_path)
        with open(xodr_file_path, encoding='utf-8') as od_file:
            try:
                data = od_file.read()
            except OSError:
                print('file could not be readed.')
                
            print('load opendrive map %r.' % os.path.basename(xodr_file_path))
            vertex_distance =0.001  # in meters
            max_road_length = 5000.0 # in meters
            wall_height = 1.0      # in meters
            extra_width = 0.0     # in meters
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
            except Exception as e:
                print('Error loading the OpenDRIVE file. Error: ' + repr(e))
