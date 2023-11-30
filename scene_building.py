from abc import ABC, abstractmethod

class SceneBuilding:

    @abstractmethod
    def import_(self, import_file_path, import_format_name):
        pass

    @abstractmethod
    def export(self, export_file_path, export_format_name):
        pass

    @abstractmethod
    def build(self):
        pass