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
