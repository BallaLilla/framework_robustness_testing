import argparse
import os
import shutil
import copy
import time
import csv

from test_settings import read_config_from_file
from road_network_concretizer import concretize_road_netork
from concrete_road_network_generator import generate_concrete_road_network

from roadrunner_hd_map_converter import RoadRunnerHDMapConverter

from roadrunner_scene_builder import RoadRunnerSceneBuilder

import mutation as mutation

from carla_simulator import CARLASimulator


def parse_arguments():
    parser = argparse.ArgumentParser(description='Robustness testing')
    parser.add_argument('--config_file', dest='config_file', default='config.json',
                        help='Path to the configuration file')
    parser.add_argument('--segment_count', dest='segment_count', type=int, 
                        help='If a segment count is specified, the network will consist of the corresponding number of segments. If not, the value in the configuration file will be used.')
    parser.add_argument('--resolution', dest='resolution', type=int,
                        help='If resolution is specified, each road network segment will consist of the corresponding number of control points. If not, the value in the configuration file will be used.')
    parser.add_argument('--measure_generation', dest='measure_generation', action='store_true',
                        help='Measure network generation runtime if set.')
    parser.add_argument('--measure_scene_building', dest='measure_scene_building', action='store_true',
                        help='Measure scene building runtime if set.')
    parser.add_argument('--measure_simulation', dest='measure_simulation', action='store_true',
                        help='Measure simulation runtime if set.')
    parser.add_argument('--measure_mutation', dest='measure_mutation', action='store_true',
                        help='Measure mutation runtime if set.')
    return parser.parse_args()


def create_output_folder(test_input_folder_path):
    road_network_folder_name = f"road_network"
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


def build_scene(scene_building_settings, road_network_file_path):
    scene_builder = None
    import_file_path = os.path.realpath(road_network_file_path)
    #print("import_path: ", import_file_path)
    import_format_name=scene_building_settings.import_format
    export_format_name=scene_building_settings.export_format
    export_file_path = os.path.realpath(os.path.dirname(road_network_file_path) + "/road_network")
    if scene_building_settings.tool == "RoadRunner Scene Builder":
        scene_builder = RoadRunnerSceneBuilder()
        project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "RoadRunnerProject"))
    scene_builder.prepare()
    scene_builder.import_(import_file_path=import_file_path, import_format_name=import_format_name)
    scene_builder.build()
    scene_builder.export(export_file_path=export_file_path, export_format_name=export_format_name)
    scene_builder.exit()
    print("export_file_path", export_file_path)
    return export_file_path

    


def simulate(scene_path, simulation_settings):
    #print("sim_scene_path", scene_path)
    simulator = None
    if simulation_settings.simulator == "CARLA":
        simulator = CARLASimulator()
    simulator.prepare_simulation()
    log_path = os.path.join(os.path.dirname(scene_path), "record")
    simulator.load_scene(scene_path=scene_path)
    simulator.make_record(log_path=log_path, duration=1)
    simulator.stop()







if __name__ == "__main__":
    args = parse_arguments()

    settings = read_config_from_file(args.config_file)
    
    if args.segment_count:
        settings.road_network.segment_count = args.segment_count
    
    if args.resolution:
        settings.road_network.resolution = args.resolution

    test_input_folder_path = os.path.relpath(os.path.join(os.path.dirname(__file__), "test_input"))
    if os.path.exists(test_input_folder_path):
        shutil.rmtree(test_input_folder_path)
    os.makedirs(test_input_folder_path)

    converter = None
    if settings.road_network_format == "RoadRunner HD Map":
            converter = RoadRunnerHDMapConverter()

    road_network = settings.road_network

    road_network_folder_path = create_output_folder(test_input_folder_path)

    if args.measure_generation:
        start_time = time.time()

    concretize_road_netork(road_network, road_network_folder_path)
    print("The segments of the road network have been concretized")
    concrete_road_network = generate_concrete_road_network(road_network_folder_path + "/descriptor.xml")
    print("The concrete road network has been generated")
    concrete_road_network_file_path = converter.convert_road_network_to_specified_format(concrete_road_network, road_network_folder_path)
    print("The concrete road network has been converted")

    if args.measure_generation:
        end_time = time.time()
        runtime_network_gen = end_time - start_time
        csv_file_path = "runtime_generation_data.csv"
        with open(csv_file_path, "a") as csv_file:
            csv_file.write(f"{args.segment_count}\t{args.resolution}\t{runtime_network_gen}\n")

    
    if args.measure_scene_building:
        start_time = time.time()

    scene_path = build_scene(scene_building_settings=settings.scene_building, road_network_file_path=concrete_road_network_file_path)

    if args.measure_scene_building:
        end_time = time.time()
        runtime_scene_building = end_time - start_time
        csv_file_path = "runtime_scene_building_data.csv"
        with open(csv_file_path, "a") as csv_file:
            csv_file.write(f"{args.segment_count}\t{args.resolution}\t{runtime_scene_building}\n")


    
    if args.measure_simulation:
        start_time = time.time()

    simulate(scene_path=scene_path, simulation_settings=settings.simulation)

    if args.measure_simulation:
        end_time = time.time()
        runtime_simulation = end_time - start_time
        csv_file_path = "runtime_simulation_data.csv"
        with open(csv_file_path, "a") as csv_file:
            csv_file.write(f"{args.segment_count}\t{args.resolution}\t{runtime_simulation}\n")
   


    for i in range(len(road_network.mutation_groups)):
        mutated_network = None
        mutated_network_path = create_mutation_output_folder(road_network_folder_path, mutation_group=i + 1)
        mutation_group = road_network.mutation_groups[i]
        for m in range(len(mutation_group.mutations)):
            mutation_ = mutation_group.mutations[m]
            if mutation_.type == "LaneMarkingReplacer":
                concrete_mutation = mutation.LaneMarkingReplacer(id=mutation_.params.get("id"), type=mutation_.type, newLaneType=mutation_.params.get("new_type"))
            elif mutation_.type == "SpeedLimitPlacer":
                    concrete_mutation = mutation.SpeedLimitPlacer(id=mutation_.params.get("id"), type=mutation_.type, speedLimitValue=mutation_.params.get("value"), side=mutation_.params.get("side"), offset=mutation_.params.get("offset"))
            if m == 0:
                if args.measure_mutation:
                    start_time = time.time()
                mutated_network = concrete_mutation.apply(copy.deepcopy(concrete_road_network))
                if args.measure_mutation:
                    end_time = time.time()
                    runtime_mut_op = end_time - start_time
            else:
                if args.measure_mutation:
                    start_time = time.time()
                mutated_network = concrete_mutation.apply(copy.deepcopy(mutated_network))
                if args.measure_mutation:
                    end_time = time.time()
                    runtime_mut_op = end_time - start_time

                    csv_file_path = "runtime_mutation_data.csv"
                    with open(csv_file_path, "a", newline='') as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter='\t')
                        if mutation_.type == "LaneMarkingReplacer":
                            csv_writer.writerow([
                                args.segment_count,
                                args.resolution,
                                mutation_.type,
                                concrete_mutation.id,
                                runtime_mut_op
                            ])
                        elif mutation_.type == "SpeedLimitPlacer":
                            csv_writer.writerow([
                                args.segment_count,
                                args.resolution,
                                mutation_.type,
                                concrete_mutation.id,
                                runtime_mut_op
                            ])

            mutated_road_network_file_path = converter.convert_road_network_to_specified_format(mutated_network, mutated_network_path)

            scene_path = build_scene(scene_building_settings=settings.scene_building, road_network_file_path=mutated_road_network_file_path)

            simulate(scene_path=scene_path, simulation_settings=settings.simulation)