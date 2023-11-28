from abc import ABC, abstractmethod

class Converter(ABC):
    @abstractmethod
    def processMultiLineSegmentList(self, multilinestrings, settable):
        pass

    @abstractmethod
    def processLaneType(self, laneType, settable):
        pass

    @abstractmethod
    def processTravelDir(self, travelDir, settable):
        pass

    @abstractmethod
    def convert_road_network_to_specified_format(self, road_network, output_folder_path):
        pass


