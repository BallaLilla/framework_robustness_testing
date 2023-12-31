import json

class Mutation:
    def __init__(self, type, **kwargs):
        self.type = type
        self.params = kwargs

class MutationGroup:
    def __init__(self, mutation_group_id, mutations):
        self.mutation_group_id = mutation_group_id
        self.mutations = [Mutation(**mutation) for mutation in mutations]

class RoadNetwork:
    def __init__(self, resolution, segment_count, initial_position_x=0, initial_position_y=0, initial_heading=0, format="RoadRunner HD Map"):
        self.resolution = resolution
        self.initial_position_x = initial_position_x
        self.initial_position_y = initial_position_y
        self.initial_heading = initial_heading
        self.segment_count = segment_count
        self.mutation_groups = []


    def add_mutation_group(self, mutation_group):
        self.mutation_groups.append(mutation_group)

class SceneBuilding:
    def __init__(self, tool="RoadRunner Scene Builder", import_format="RoadRunner HD Map", export_format="CARLA"):
        self.tool = tool
        self.import_format = import_format
        self.export_format = export_format

class Simulation:
    def __init__(self, simulator="CARLA"):
        self.simulator = simulator

class Config:
    def __init__(self, road_network, road_network_format, scene_building, simulation):
        self.road_network = road_network
        self.scene_building = scene_building
        self.simulation = simulation
        self.road_network_format = road_network_format

def json_to_config(json_data):
    road_network_data = json_data.get("road_network")

    resolution = road_network_data.get("resolution", 10)
    segment_count = road_network_data.get("segment_count", 1)
    initial_pos_x = road_network_data.get("initial_position_x", 0)
    initial_pos_y = road_network_data.get("initial_position_y", 0)
    initial_heading = road_network_data.get("initial_heading", 0)
        
    road_network = RoadNetwork(resolution=resolution, segment_count=segment_count, initial_position_x=initial_pos_x,
                                   initial_position_y=initial_pos_y, initial_heading=initial_heading)
        
    mutation_groups = road_network_data.get("mutation_groups", [])
    for mutation_group_data in mutation_groups:
        mutation_group_id = mutation_group_data.get("mutation_group_id", "")
        mutations = mutation_group_data.get("mutations", [])
        mutation_group = MutationGroup(mutation_group_id=mutation_group_id, mutations=mutations)
        road_network.add_mutation_group(mutation_group)

    road_network_format = json_data.get("format", "RoadRunner HD Map")
    scene_building_data = json_data.get("scene_building", {})
    scene_building = SceneBuilding(**scene_building_data)

    simulator_data = json_data.get("simulation", {})
    simulation = Simulation(**simulator_data)

    return Config(road_network, road_network_format, scene_building, simulation)

def read_config_from_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_to_config(json_data)
