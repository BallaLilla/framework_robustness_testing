from abc import ABC, abstractmethod
from scene_building import SceneBuilding

class SceneBuilder(SceneBuilding):
    
    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def exit(self):
        pass