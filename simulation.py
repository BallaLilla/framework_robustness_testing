from abc import abstractmethod

class Simulation:
    @abstractmethod
    def load_scene(scene_path):
        pass

    @abstractmethod
    def make_record(log_path, duration):
        pass