from abc import ABC, abstractmethod

class Simulator(ABC):
    
    @abstractmethod
    def simulate(self):
        pass
