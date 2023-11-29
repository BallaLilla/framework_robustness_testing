from abc import ABC, abstractmethod

from simulation import Simulation

class Simulator(Simulation):

    @abstractmethod
    def prepare_simulation(self):
        pass

    @abstractmethod
    def stop(self):
        pass

