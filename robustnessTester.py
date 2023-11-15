import argparse
import os
import shutil

from test_settings import read_config_from_file
from ConcreteScenarioParametrizer import parametrizeConcreteScenario
from road_network_generator import generate_concrete_road_network
from roadrunnerhdmapgenerator import generate_road_runner_hd_map

from roadrunner_server import RoadRunnerServer
from roadrunner_client import RoadRunnerClient

from carla_server import CARLAServer
from carla_client import CARLAClient

import subprocess


def parse_arguments():
    parser = argparse.ArgumentParser(description='Robustness testing')
    parser.add_argument('--config_file', dest='config_file', default='config.json', help='Path to the configuration file')
    return parser.parse_args()

def create_output_folder(index):
    test_cases_folder = os.path.relpath(os.path.join(os.path.dirname(__file__), "test_cases"))
    if os.path.exists(test_cases_folder):
       shutil.rmtree(test_cases_folder)
    os.makedirs(test_cases_folder)

    # Generate a folder name based on the index
    folder_name = f"test_case_{index + 1}"

    # Create the output folder (delete and recreate if it already exists)
    folder_path = os.path.join(test_cases_folder, folder_name)
    if os.path.exists(os.path.realpath(folder_path)):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

    return folder_name, folder_path

if __name__ == "__main__":
    args = parse_arguments()

    settings = read_config_from_file(args.config_file)

    for index, road_network in enumerate(settings.road_networks):
        output_folder_name, output_folder_path = create_output_folder(index)
        #print("road_group_type: ", road_network.road_groups[0].type)
        parametrizeConcreteScenario(road_network, output_folder_path)
        concrete_road_network = generate_concrete_road_network(output_folder_path + "/descriptor.xml")
        if settings.scene_building.tool == "RoadRunner":
            pass
            generate_road_runner_hd_map(concrete_road_network, output_folder_path)
            roadrunner_server = RoadRunnerServer(project_path=os.path.dirname(__file__) + "/Server")
            import_file_path = os.path.realpath(output_folder_path + "/rrMap")
            export_file_path = os.path.realpath(output_folder_path + "/rrMap_exported")
            print("import_file_path: ", import_file_path)
            print("export_file_path: ", export_file_path)
            roadrunner_client = RoadRunnerClient(import_file_path=import_file_path, import_format_name=settings.scene_building.import_format, export_file_path=export_file_path, export_format_name=settings.scene_building.export_format)
        if settings.simulator.simulator == "CARLA":
            pass
            #print("starting carla server")
            #carla_server = CARLAServer()
            #print("starting and connecting carla client")
            #carla_client = CARLAClient()
            #print("loading xodr")
            #carla_client._generate_opendrive_world(export_file_path + ".xodr")

            



