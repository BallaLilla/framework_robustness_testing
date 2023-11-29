from abc import ABC, abstractmethod
from scene_building import SceneBuilding

class SceneBuilder(SceneBuilding):
    
    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def load_project(self):
        pass

    @abstractmethod
    def create_new_scene(self):
        pass

    @abstractmethod
    def exit(self):
        pass