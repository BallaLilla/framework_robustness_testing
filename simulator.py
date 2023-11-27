from abc import ABC, abstractmethod

class Simulator(ABC):

    @abstractmethod
    def prepare_simulation(self):
        pass

    @abstractmethod
    def make_record(self, log_path, duration):
        pass

    @abstractmethod
    def load_scene(self, scene_path):
        pass

    @abstractmethod
    def stop(self):
        pass
