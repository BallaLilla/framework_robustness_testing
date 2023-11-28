import subprocess
import sys
import shutil
import grpc
import mathworks.roadrunner.roadrunner_service_messages_pb2 as roadrunner_service_messages_pb2
import mathworks.roadrunner.roadrunner_service_pb2_grpc as roadrunner_service_pb2_grpc
import os
import time

from scene_builder import SceneBuilder


class RoadRunnerSceneBuilder(SceneBuilder):
       
       
    def build_scene(self, project_path, import_file_path, import_format_name, export_file_path, export_format_name):
        with grpc.insecure_channel("localhost: " + str(self.server_api_port)) as channel:
           api = roadrunner_service_pb2_grpc.RoadRunnerServiceStub(channel)

           # create new project
           print("Load project")
           loadProjectRequest = roadrunner_service_messages_pb2.LoadProjectRequest()
           loadProjectRequest.folder_path =  project_path
           api.LoadProject(loadProjectRequest)

           # create new scene
           print("New scene creation")
           newSceneRequest = roadrunner_service_messages_pb2.NewSceneRequest()
           api.NewScene(newSceneRequest)
           
           
           # import file into scene
           print("Import")
           importRequest = roadrunner_service_messages_pb2.ImportRequest()
           importRequest.file_path = import_file_path
           importRequest.format_name = import_format_name
           api.Import(importRequest)

           # export scene
           print("export")
           exportRequest = roadrunner_service_messages_pb2.ExportRequest()
           exportRequest.file_path = export_file_path
           exportRequest.format_name = export_format_name
           api.Export(exportRequest)

           print("exit")
           exitRequest = roadrunner_service_messages_pb2.ExitRequest()
           api.Exit(exitRequest)

    def prepare(self):
        self.compile_proto_files()
        self.start_server()


    
    def start_server(self, project_path=None, api_port=54321):
        self.server_api_port = api_port
        if project_path is None:
            project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "RoadRunnerProject"))
        self.project_path = project_path
        callString = "AppRoadRunner --apiPort " + str(api_port) + " --projectPath " + project_path
        print(callString)
        self.process = subprocess.Popen(callString)
        time.sleep(10)


    
    def compile_proto_files(self):
        process = subprocess.Popen("python roadrunner_setup.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = process.wait()
        output, error = process.communicate()
        if error:
            print(error)
            sys.exit(1)



