import grpc
import mathworks.roadrunner.roadrunner_service_messages_pb2 as roadrunner_service_messages_pb2
import mathworks.roadrunner.roadrunner_service_pb2_grpc as roadrunner_service_pb2_grpc

class RoadRunnerClient:
    def __init__(self, ip_address, api_port):
        self.channel = grpc.insecure_channel(ip_address + ":"  + str(api_port))
        self.api = roadrunner_service_pb2_grpc.RoadRunnerServiceStub(self.channel)

    def load_project(self, project_path):
        print("Load project")
        loadProjectRequest = roadrunner_service_messages_pb2.LoadProjectRequest()
        loadProjectRequest.folder_path =  project_path
        self.api.LoadProject(loadProjectRequest)

    def create_new_scene(self):
        print("New scene creation")
        newSceneRequest = roadrunner_service_messages_pb2.NewSceneRequest()
        self.api.NewScene(newSceneRequest)

    def import_(self, import_file_path, import_format_name):
        print("Import")
        importRequest = roadrunner_service_messages_pb2.ImportRequest()
        importRequest.file_path = import_file_path
        importRequest.format_name = import_format_name
        self.api.Import(importRequest)

    def export(self, export_file_path, export_format_name):
        print("Export")
        exportRequest = roadrunner_service_messages_pb2.ExportRequest()
        exportRequest.file_path = export_file_path
        exportRequest.format_name = export_format_name
        self.api.Export(exportRequest)
    
    def exit(self):
        print("exit")
        exitRequest = roadrunner_service_messages_pb2.ExitRequest()
        self.api.Exit(exitRequest)
        self.channel.close()
        self.api = None
        self.channel = None