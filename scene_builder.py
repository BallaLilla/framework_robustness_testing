from abc import ABC, abstractmethod

class SceneBuilder(ABC):
    
    @abstractmethod
    def build_scene(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

