from abc import ABC, abstractmethod

class Simulator(ABC):

    @abstractmethod
    def prepare_simulation(self):
        pass

    @abstractmethod
    def make_record(self):
        pass

    @abstractmethod
    def load_scene(self):
        pass

    @abstractmethod
    def stop(self):
        pass
