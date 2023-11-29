import os
import time
import subprocess
import psutil
import logging
import carla

from simulator import Simulator

from carla_server import CARLAServer
from carla_client import CARLAClient

class CARLASimulator(Simulator):

    def __init__(self):
        
        self.carla_server = None 
        self.carla_client = None

    def start_server(self):
        self.carla_server = CARLAServer()
    
    def client_connect_server(self):
        self.carla_client = CARLAClient()


    def prepare_simulation(self):
        self.start_server()
        self.client_connect_server()


    def make_record(self, log_path, duration):
        self.carla_client.make_record(log_path=log_path, duration=duration)
    

    def load_scene(self, scene_path):
        self.carla_client.load_scene(scene_path=scene_path)

    def stop(self):
        self.carla_server.stop()