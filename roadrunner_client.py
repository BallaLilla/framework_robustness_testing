import shutil
import grpc
import mathworks.roadrunner.roadrunner_service_messages_pb2 as roadrunner_service_messages_pb2
import mathworks.roadrunner.roadrunner_service_pb2_grpc as roadrunner_service_pb2_grpc
import os

IP_address = "127.0.0.1"
server_port = "54321"


    

class RoadRunnerClient:
    def __init__(self, import_file_path, import_format_name, export_file_path, export_format_name):
         with grpc.insecure_channel("localhost: " + server_port) as channel:
           api = roadrunner_service_pb2_grpc.RoadRunnerServiceStub(channel)

           # create new project
           print("Creating new project")
           newProjectRequest = roadrunner_service_messages_pb2.NewProjectRequest()
           dummy_path = os.path.realpath(os.path.dirname(__file__) + "/Dummy").replace(os.sep, '/')
           if os.path.exists(dummy_path):
               shutil.rmtree(dummy_path)

           print("dummy_path: ", dummy_path)
           newProjectRequest.folder_path =  dummy_path
           newProjectRequest.asset_libraries.append("RoadRunner_Asset_Library")
           api.NewProject(newProjectRequest)

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

           exitRequest = roadrunner_service_messages_pb2.ExitRequest()
           api.Exit(exitRequest)



    

        