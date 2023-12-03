import random

from abc import ABC, abstractmethod

class GeometryStrategy(ABC):
    @abstractmethod
    def determine_values(self):
        pass

class LineGeometryStrategy(GeometryStrategy):
    def __init__(self):
        self.dict = {"type":"line", "length": None}
    
    def determine_values(self):
        return self.dict.copy()

class RandomLineGeometryStrategyBetweenBoundary(LineGeometryStrategy):
    def __init__(self, min_length, max_length):
        super().__init__()
        self.min_length = min_length
        self.max_length = max_length
    
    def determine_values(self):
        self.dict["length"] = random.uniform(self.min_length, self.max_length)
        return self.dict.copy()

class ArcGeometryStrategy(GeometryStrategy):
    def __init__(self):
        self.dict = {"type":"arc", "curvature": None, "angle": None}
    
    def determine_values(self):
        return self.dict.copy()

class RandomArcGeometryStrategyBetweenBoundary(ArcGeometryStrategy):
    def __init__(self, min_radius, max_radius, min_angle, max_angle):
        super().__init__()
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_angle = min_angle
        self.max_angle = max_angle
    
    def determine_values(self):
        self.dict["curvature"] = 1 / random.uniform(self.min_radius, self.max_radius)
        self.dict["angle"] = random.uniform(self.min_angle, self.max_angle)
        return self.dict.copy()

    
        