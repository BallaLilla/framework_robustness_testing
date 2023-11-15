import json

class RoadGroup:
    def __init__(self, segment_count, network_function, topography, type, offset_from_ref_line):
        self.segment_count = segment_count
        self.network_function = network_function
        self.topography = topography
        self.type = type
        self.offset_from_ref_line = 0 #offset_from_ref_line

class RoadNetwork:
    def __init__(self, resolution, initial_position_x=0, initial_position_y=0, initial_heading=0, format="RoadRunner HD Map"):
        self.resolution = resolution
        self.initial_position_x = initial_position_x
        self.initial_position_y = initial_position_y
        self.initial_heading = initial_heading
        self.format = format
        self.road_groups = []
    
    def add_road_groups(self, road_group):
        self.road_groups.append(road_group)

class SceneBuilding:
    def __init__(self, tool="RoadRunner", import_format="RoadRunner HD Map", export_format="CARLA"):
        self.tool = tool
        self.import_format = import_format
        self.export_format = export_format

class Simulator:
    def __init__(self, simulator="CARLA"):
        self.simulator = simulator

class Config:
    def __init__(self, road_networks, scene_building, simulator):
        self.road_networks = road_networks
        self.scene_building = scene_building
        self.simulator = simulator

def json_to_config(json_data):
    road_networks_data = json_data.get("road_networks", [])
    road_networks = []

    for road_network_data in road_networks_data:
        road_group_data = road_network_data.get("road_groups", [])[0] if road_network_data.get("road_groups") else {}
        road_group = RoadGroup(**road_group_data) if road_group_data else None

        road_network = RoadNetwork(resolution=road_network_data.get("resolution", 0),
                                   initial_position_x=road_network_data.get("initial_position_x", 0),
                                   initial_position_y=road_network_data.get("initial_position_y", 0),
                                   initial_heading=road_network_data.get("initial_heading", 0),
                                   format=road_network_data.get("format", "RoadRunner HD Map"))
        road_network.add_road_groups(road_group)

        road_networks.append(road_network)

    scene_building_data = json_data.get("scene_building", {})
    scene_building = SceneBuilding(**scene_building_data)

    simulator_data = json_data.get("simulation", {})
    simulator = Simulator(**simulator_data)

    return Config(road_networks, scene_building, simulator)

def read_config_from_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_to_config(json_data)
