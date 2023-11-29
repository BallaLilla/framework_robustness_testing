from abc import ABC, abstractmethod

class SceneBuilding:

    @abstractmethod
    def import_(self):
        pass

    @abstractmethod
    def export(self):
        pass

    @abstractmethod
    def build(self):
        pass