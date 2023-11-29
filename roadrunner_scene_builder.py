import subprocess
import sys
import os

from scene_builder import SceneBuilder

from roadrunner_server import RoadRunnerServer
from roadrunner_client import RoadRunnerClient


class RoadRunnerSceneBuilder(SceneBuilder):
    def __init__(self):
         self.roadrunner_server = None
         self.roadrunner_client = None
       
    
    def load_project(self, project_path):
        self.roadrunner_client.load_project(project_path=project_path)

    def create_new_scene(self):
        self.roadrunner_client.create_new_scene()
    

    def import_(self, import_file_path, import_format_name):
        self.roadrunner_client.import_(import_file_path=import_file_path, import_format_name=import_format_name)

    
    def export(self, export_file_path, export_format_name):
        self.roadrunner_client.export(export_file_path=export_file_path, export_format_name=export_format_name)
    
    def exit(self):
        self.roadrunner_client.exit()     


    def prepare(self):
        self.compile_proto_files()
        self.start_server()
        self.client_connect_to_server()


    
    def start_server(self, project_path=None, api_port=54321, timeout=10):
        if project_path is None:
            project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "RoadRunnerProject"))
        self.roadrunner_server = RoadRunnerServer(project_path=project_path, api_port=api_port, timeout=timeout)

    
    def client_connect_to_server(self):
        self.roadrunner_client = RoadRunnerClient("localhost", self.roadrunner_server.api_port)

    
    def compile_proto_files(self):
        process = subprocess.Popen("python roadrunner_setup.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = process.wait()
        output, error = process.communicate()
        if error:
            print(error)
            sys.exit(1)