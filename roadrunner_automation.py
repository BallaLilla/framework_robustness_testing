import shutil
import grpc
from mathworks.roadrunner import roadrunner_service_messages_pb2
from mathworks.roadrunner import roadrunner_service_pb2_grpc

with grpc.insecure_channel('127.0.0.1:54321') as channel:
    api = roadrunner_service_pb2_grpc.RoadRunnerServiceStub(channel)
    
    # Creating new project with default asset
    try:
        shutil.rmtree("C:/Users/balia/Desktop/Szakdolgozat/RoadRunnerClientProject")
    except OSError as e:
        pass
    
    newProjectRequest = roadrunner_service_messages_pb2.NewProjectRequest()
    newProjectRequest.folder_path = "C:/Users/balia/Desktop/Szakdolgozat/RoadRunnerClientProject"
    newProjectRequest.asset_libraries.append("RoadRunner_Asset_Library")
    api.NewProject(newProjectRequest)

    # Creating new scene
    newSceneRequest = roadrunner_service_messages_pb2.NewSceneRequest()
    api.NewScene(newSceneRequest)

    #import custom HD map into RoadRunner

    importRequest = roadrunner_service_messages_pb2.ImportRequest()
    importRequest.file_path = "C:/Users/balia/Desktop/Szakdolgozat/process/import_to_RoadRunner/rrMap.rrhd"
    importRequest.format_name = "RoadRunner HD Map"
    api.Import(importRequest)

    #export custom HD map to CARLA format

    exportRequest = roadrunner_service_messages_pb2.ExportRequest()
    exportRequest.file_path = "C:/Users/balia/Desktop/Szakdolgozat/process/export_from_RoadRunner/rrMap"
    exportRequest.format_name = "CARLA"
    api.Export(exportRequest)

    
    
    print("Siker")
    
 
