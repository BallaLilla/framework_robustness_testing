from abc import ABC, abstractmethod

class SceneBuilder(ABC):
    
    @abstractmethod
    def build_scene(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def load_project(self):
        pass

    @abstractmethod
    def create_new_scene(self):
        pass

    @abstractmethod
    def import_(self):
        pass

    @abstractmethod
    def export(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    def build_scene(self, project_path, import_file_path, import_format_name, export_file_path, export_format_name):
        self.load_project(project_path=project_path)
        self.create_new_scene()
        self.import_(import_file_path=import_file_path, import_format_name=import_format_name)
        self.export(export_file_path=export_file_path, export_format_name=export_format_name)
        self.exit()

