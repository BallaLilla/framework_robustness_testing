import random
import xml.etree.ElementTree as ET
import xml.dom.minidom

from outdoor_primary_main_concretizer import OutdoorPrimaryMainRoadProfileStrategy
import geometryStrategy


def choose_segment_type():
    segment_types = ["line", "arc"]
    return random.choice(segment_types)


def concretize_road_netork(network_setting, output_folder_path):
    road_network = ET.Element("road_network", x=str(network_setting.initial_position_x),
                                             y=str(network_setting.initial_position_y),
                                             hdg=str(network_setting.initial_heading),
                                             resolution=str(network_setting.resolution)
                                            )
    tree = ET.ElementTree(road_network)

    # TODO: later will be modified when several road groups will be handled
    category = "outdoor_primary_main"
    topography = "A"
    traffic_rule = "RHT"

    parametrizer = None
    
   
    for i in range(network_setting.segment_count):
        parametrizer = OutdoorPrimaryMainRoadProfileStrategy(topography=topography)
        design_speed = parametrizer.get_design_speed()


        road_element = ET.SubElement(road_network, "road", type=category, traffic_rule=traffic_rule)
        geometry_type = choose_segment_type()
        geometry_strategy_ = None
        geometry_element = None
        if geometry_type == "arc":
            geometry_attributes = geometryStrategy.RandomArcGeometryStrategyBetweenBoundary(min_radius=parametrizer.get_min_curve_radius(design_speed)/100, max_radius=parametrizer.get_min_curve_radius(design_speed) + 10, min_angle=3, max_angle=180).determine_values()
        elif geometry_type == "line":
            geometry_attributes = geometryStrategy.RandomLineGeometryStrategyBetweenBoundary(min_length=100, max_length=parametrizer.get_max_straight_length(design_speed)/100).determine_values()
        geometry_element = ET.SubElement(road_element, "geometry")
        for key, value in geometry_attributes.items():
            geometry_element.set(key, str(value))

        road_profile = parametrizer.determine_parameters()
        lanes_element = ET.SubElement(road_element, "lanes")
        right_lane_section = ET.SubElement(lanes_element, "right_section")
        for i in range(road_profile.lane_count_right_side):
            lane_type = "driving"
            lane_width = road_profile.lane_widths_right_side[i]
            lane_element = ET.SubElement(right_lane_section, "lane", type=lane_type, width=str(lane_width))
            lane_marking_type = road_profile.lame_boundary_markings_right_side[i]
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="right" ,type=lane_marking_type)
        median_lane_section = ET.SubElement(lanes_element, "median_section")
        lane_type = "median"
        lane_width = road_profile.median_lane_width
        lane_element = ET.SubElement(median_lane_section, "lane", type=lane_type, width=str(lane_width))
        if lane_width == 0:
            lane_marking_type = road_profile.median_lane_boundary_markings[0]
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="center" ,type=lane_marking_type)
        else:
            lane_marking_type = road_profile.median_lane_boundary_markings[0]
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="right" ,type=lane_marking_type)
            lane_marking_type = road_profile.median_lane_boundary_markings[0]
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="left" ,type=lane_marking_type)
        left_lane_section = ET.SubElement(lanes_element, "left_section")
        for i in range(road_profile.lane_count_left_side):
            lane_type = "driving"
            lane_width = road_profile.lane_widths_left_side[i]
            lane_element = ET.SubElement(left_lane_section, "lane", type=lane_type, width=str(lane_width))
            lane_marking_type = road_profile.lame_boundary_markings_left_side[i]
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="left" ,type=lane_marking_type)

    output_file_path = output_folder_path + "/descriptor.xml"

    xml_str = ET.tostring(road_network, encoding='utf-8')
    reparsed = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = reparsed.toprettyxml(indent="  ")

    with open(output_file_path, "wb") as file:
        file.write(pretty_xml_str.encode('utf-8'))



