from abc import ABC, abstractmethod

class RoadProfile():
    def __init__(self) -> None:
        self.lane_count_right_side = None
        self.lane_count_left_side = None
        self.lane_widths_right_side = []
        self.lane_widths_left_side = []
        self.lame_boundary_markings_right_side = []
        self.lame_boundary_markings_left_side = []
        self.median_lane_width = None
        self.median_lane_boundary_markings = []



class RoadProfilStrategy(ABC):
    def __init__(self, topography):
        self.topography = topography
        self.road_profile = RoadProfile()

    
    @abstractmethod
    def determine_parameters(self):
        return self.road_profile

    
    def get_design_speed(self):
        if self.category == "outdoor_highway" and self.topography == "A":
            return 130
        elif self.category == "outdoor_highway" and self.topography == "B":
            return 110
        elif self.category == "outdoor_highway" and self.topography == "C":
            return 110
        elif self.category == "outdoor_freeway" and self.topography == "A":
            return 110
        elif self.category == "outdoor_freeway" and self.topography == "B":
            return 90
        elif self.category == "outdoor_freeway" and self.topography == "C":
            return 90
        elif self.category == "outdoor_primary_main" and self.topography == "A":
            return 90
        elif self.category == "outdoor_primary_main" and self.topography == "B":
            return 90
        elif self.category == "outdoor_primary_main" and self.topography == "C":
            return 80
        elif self.category == "outdoor_secondary_main" and self.topography == "A":
            return 90
        elif self.category == "outdoor_secondary_main" and self.topography == "B":
            return 70
        elif self.category == "outdoor_secondary_main" and self.topography == "C":
            return 60
        
        #TODO: handling other combinations


    def get_max_straight_length(self, design_speed):
        if design_speed <= 30:
            return 600
        elif design_speed <= 40:
            return 800
        elif design_speed <= 50:
            return 1000
        elif design_speed <= 60:
            return 1200
        elif design_speed <= 70:
            return 1400
        elif design_speed <= 80:
            return 1600
        elif design_speed <= 100:
            return 2000
        elif design_speed <= 130:
            return 2600
        
    
    def get_min_curve_radius(self, design_speed):
        if design_speed <= 30:
            return 30
        elif design_speed <= 40:
            return 60
        elif design_speed <= 50:
            return 100
        elif design_speed <= 60:
            return 150
        elif design_speed <= 70:
            return 200
        elif design_speed <= 80:
            return 300
        elif design_speed <= 100:
            return 500
        elif design_speed <= 130:
            return 900
    