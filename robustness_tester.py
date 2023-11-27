import argparse
import os
import shutil
import copy

from test_settings import read_config_from_file
from road_network_parametrizer import parametrize_road_netork
from concrete_road_network_generator import generate_concrete_road_network
from roadrunner_hd_map_adapter import generate_roadrunner_hd_map
from roadrunner_server import RoadRunnerServer
from roadrunner_client import RoadRunnerClient
from carla_server import CARLAServer
from carla_client import CARLAClient
import mutation as mutation


def parse_arguments():
    parser = argparse.ArgumentParser(description='Robustness testing')
    parser.add_argument('--config_file', dest='config_file', default='config.json',
                        help='Path to the configuration file')
    return parser.parse_args()


def create_output_folder(test_input_folder_path, road_network_index):
    road_network_folder_name = f"road_network_{road_network_index + 1}"
    road_network_folder_path = os.path.join(test_input_folder_path, road_network_folder_name)
    if os.path.exists(os.path.realpath(road_network_folder_path)):
        shutil.rmtree(road_network_folder_path)
    os.makedirs(road_network_folder_path)
    return road_network_folder_path


def create_mutation_output_folder(road_network_folder_path, mutation_group):
    mutation_group_folder_name = f"mutation_group_{mutation_group}"
    mutation_group_folder_path = os.path.join(road_network_folder_path, mutation_group_folder_name)
    if os.path.exists(os.path.realpath(mutation_group_folder_path)):
        shutil.rmtree(mutation_group_folder_path)
    os.makedirs(mutation_group_folder_path)
    return mutation_group_folder_path




if __name__ == "__main__":
    args = parse_arguments()

    settings = read_config_from_file(args.config_file)

    test_input_folder_path = os.path.relpath(os.path.join(os.path.dirname(__file__), "test_input"))
    if os.path.exists(test_input_folder_path):
        shutil.rmtree(test_input_folder_path)
    os.makedirs(test_input_folder_path)

    for index, road_network in enumerate(settings.road_networks):
        road_network_folder_path = create_output_folder(test_input_folder_path, index)
        parametrize_road_netork(road_network, road_network_folder_path)
        concrete_road_network = generate_concrete_road_network(road_network_folder_path + "/descriptor.xml")

        if road_network.format == "RoadRunner HD Map":
            generate_roadrunner_hd_map(concrete_road_network, road_network_folder_path)


        if settings.scene_building.tool == "RoadRunner":
            
            roadrunner_server = RoadRunnerServer(project_path=os.path.realpath(os.path.join(os.path.dirname(__file__), "Server")))
            import_file_path = os.path.realpath(road_network_folder_path + "/rrMap")
            export_file_path = os.path.realpath(road_network_folder_path + "/rrMap_exported")
            roadrunner_client = RoadRunnerClient(import_file_path=import_file_path,
                                                 import_format_name=settings.scene_building.import_format,
                                                 export_file_path=export_file_path,
                                                 export_format_name=settings.scene_building.export_format)

        if settings.simulator.simulator == "CARLA":
            carla_server = CARLAServer()
            carla_client = CARLAClient()
            carla_client._generate_opendrive_world(export_file_path + ".xodr")
            carla_client.make_record(os.path.join(os.path.dirname(import_file_path), "record.log"))
                 
            

        
        for i in range(len(road_network.mutation_groups)):
            mutated_network = None
            mutated_network_path = create_mutation_output_folder(road_network_folder_path, mutation_group=i + 1)
            mutation_group = road_network.mutation_groups[i]
            for m in range(len(mutation_group.mutations)):
                mutation_ = mutation_group.mutations[m]
                if mutation_.type == "laneMarkingReplacer":
                    concrete_mutation = mutation.LaneMarkingReplacer(id=mutation_.params.get("id"), type=mutation_.type, newLaneType=mutation_.params.get("new_type"))
                if m == 0:
                    mutated_network = concrete_mutation.apply(copy.deepcopy(concrete_road_network))
                else:
                    mutated_network = concrete_mutation.apply(copy.deepcopy(mutated_network))

                    

                if settings.scene_building.tool == "RoadRunner":
                    generate_roadrunner_hd_map(mutated_network, mutated_network_path)
                    roadrunner_server = RoadRunnerServer(project_path=os.path.realpath(os.path.join(os.path.dirname(__file__), "Server")))
                    import_file_path = os.path.realpath(mutated_network_path + "/rrMap")
                    export_file_path = os.path.realpath(mutated_network_path + "/rrMap_exported")
                    roadrunner_client = RoadRunnerClient(import_file_path=import_file_path,
                                                        import_format_name=settings.scene_building.import_format,
                                                        export_file_path=export_file_path,
                                                        export_format_name=settings.scene_building.export_format)

                if settings.simulator.simulator == "CARLA":
                    carla_server = CARLAServer()
                    carla_client = CARLAClient()
                    carla_client._generate_opendrive_world(export_file_path + ".xodr")
                    carla_client.make_record(os.path.join(os.path.dirname(import_file_path), "record.log"))
                   
        
       
    carla_client.close_Carla()