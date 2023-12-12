from concretizer import RoadProfilStrategy

class OutdoorPrimaryMainRoadProfileStrategy(RoadProfilStrategy):
    def __init__(self, topography):
        super().__init__(topography)
        self.category = "outdoor_primary_main"

    
    def determine_parameters(self):
        design_speed = self.get_design_speed()
        if design_speed > 80:
            self.road_profile.lane_count_right_side = 1
            self.road_profile.lane_count_left_side = 1
            self.road_profile.lane_widths_right_side = [3.5] * self.road_profile.lane_count_right_side
            self.road_profile.lane_widths_left_side = [3.5] * self.road_profile.lane_count_left_side
            self.road_profile.lame_boundary_markings_right_side = ["SolidSingleWhite"] * self.road_profile.lane_count_right_side
            self.road_profile.lame_boundary_markings_left_side = ["SolidSingleWhite"] * self.road_profile.lane_count_left_side
            self.road_profile.median_lane_width = 0
            self.road_profile.median_lane_boundary_markings = ["DashedSingleWhite"]
        
        elif design_speed > 70:
            self.road_profile.lane_count_right_side = 2
            self.road_profile.lane_count_left_side = 2
            self.road_profile.lane_widths_right_side = [3.5] * self.road_profile.lane_count_right_side
            self.road_profile.lane_widths_left_side = [3.5] * self.road_profile.lane_count_left_side
            self.road_profile.lame_boundary_markings_right_side = ["SolidSingleWhite"] * self.road_profile.lane_count_right_side
            self.road_profile.lame_boundary_markings_left_side = ["SolidSingleWhite"] * self.road_profile.lane_count_left_side
            self.road_profile.median_lane_width = 0
            self.road_profile.median_lane_boundary_markings = ["DashedSingleWhite"]

        elif design_speed > 60:
            self.road_profile.lane_count_right_side = 2
            self.road_profile.lane_count_left_side = 2
            self.road_profile.lane_widths_right_side = [3.25] * self.road_profile.lane_count_right_side
            self.road_profile.lane_widths_left_side = [3.25] * self.road_profile.lane_count_left_side
            self.road_profile.lame_boundary_markings_right_side = ["SolidSingleWhite"] * self.road_profile.lane_count_right_side
            self.road_profile.lame_boundary_markings_left_side = ["SolidSingleWhite"] * self.road_profile.lane_count_left_side
            self.road_profile.median_lane_width = 0
            self.road_profile.median_lane_boundary_markings = ["DashedSingleWhite"]

        return self.road_profile
    

