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

    def simulate(self, scene_path, log_path, duration):
        self.load_scene(scene_path=scene_path)
        self.make_record(log_path=log_path, duration=duration)
