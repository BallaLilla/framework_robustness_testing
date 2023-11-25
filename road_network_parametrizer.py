import random
import xml.etree.ElementTree as ET
import xml.dom.minidom



def get_design_speed(type, topography, network_function):
    # csak belterület
    if type == "highway" and topography == "A":
        return 110
    elif type == "highway" and (topography == "B" or topography == "C"):
        return 90
    elif type == "highway1" and topography == "A":
        return 90
    elif type == "highway1" and (topography == "B" or topography == "C"):
        return 80
    elif network_function == "a" and topography == "A":
        return 80
    elif network_function == "a" and topography == "B":
        return 70
    elif network_function == "a" and topography == "C":
        return 60
    elif network_function == "b" and topography == "A":
        return 70
    elif network_function == "b" and topography == "B":
        return 60
    elif network_function == "b" and topography == "C":
        return 50
    elif network_function == "b" and topography == "D":
        return 40
    elif network_function == "c" and topography == "A":
        return 60
    elif network_function == "c" and topography == "B":
        return 50
    elif network_function == "c" and (topography == "C" or topography == "D"):
        return 40
    elif network_function == "d" and (topography == "A" or topography == "B"):
        return 40
    elif network_function == "d" and topography == "C":
        return 30
    #elif network_function == "d" and topography == "D":
        #return None
    
    else:
        return 30



def get_max_straight_length(design_speed):
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
    
def get_min_curve_radius(design_speed):
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
    
def choose_segment_type():
    segment_types = ["line", "arc"]
    return random.choice(segment_types)

def random_angle():
    return random.uniform(3.0, 180.0)

def get_lane_number_per_section(network_function):
    if network_function == "a":
        return random.randint(1, 4)
    elif network_function == "b":
        return random.randint(1, 3)
    elif network_function == "c":
        return random.randint(1, 2)
    elif network_function == "d":
        return 1
    else:
        raise Exception("Invalid network function")
    

def get_lane_type(section):
    if section == "median":
        return "median"
    else:
        return "driving"
    
def get_lane_width(lane_type):
    if lane_type == "median":
        return random.randint(0, 2)
    else:
        return random.randint(2, 4)
   
    
def median_lane_length():
    return 0

def choose_random_lane_marking():
    lane_markings = ["SolidSingleWhite", "SolidSingleYellow", "DashedDoubleWhite", "DashedDoubleYellow", "DashedShortSingleWhite", "DashedShortSingleYellow", "DashedSingleWhite", "DashedSingleYellow",
                    "DashedSolidWhite", "DashedSolidYellow", "SolidDoubleWhite", "SolidDoubleYellow"]
    return random.choice(lane_markings)




def parametrize_road_netork(network_setting, output_folder_path):
    road_network = ET.Element("road_network", x=str(network_setting.initial_position_x),
                                             y=str(network_setting.initial_position_y),
                                             hdg=str(network_setting.initial_heading),
                                             resolution="1000",
                                            )
    tree = ET.ElementTree(road_network)

    # TODO: later will be modified when several road groups will be handled
    category = "main"
    network_function = "a"
    topography = "A"
    traffic_rule = "RHT"

    
    design_speed = get_design_speed(type=category, topography=topography, network_function=network_function)
    for i in range(network_setting.segment_count):
        road_element = ET.SubElement(road_network, "road", type=category, traffic_rule=traffic_rule)
        geometry_type = choose_segment_type()
        print("i: ", i)
        print("type: ", geometry_type)
        geometry_element = None
        if geometry_type == "arc":
            radius = get_min_curve_radius(design_speed=design_speed) / 100
            curvature = 1 / radius
            angle = random_angle()
            geometry_element = ET.SubElement(road_element, "geometry", type=geometry_type, curvature=str(curvature), angle=str(angle))
        elif geometry_type == "line":
            length = get_max_straight_length(design_speed=design_speed) / 100
            geometry_element = ET.SubElement(road_element, "geometry", type=geometry_type, length=str(length))
        lanes_element = ET.SubElement(road_element, "lanes")
        right_lane_section = ET.SubElement(lanes_element, "right_section")
        right_lane_number = get_lane_number_per_section(network_function)
        for i in range(right_lane_number):
            lane_type = get_lane_type("right")
            lane_width = get_lane_width(lane_type)
            lane_element = ET.SubElement(right_lane_section, "lane", type=lane_type, width=str(lane_width))
            lane_marking_type = choose_random_lane_marking()
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="right" ,type=lane_marking_type)
        median_lane_section = ET.SubElement(lanes_element, "median_section")
        lane_type = get_lane_type("median")
        lane_width = get_lane_width(lane_type)
        lane_element = ET.SubElement(median_lane_section, "lane", type=lane_type, width=str(lane_width))
        if lane_width == 0:
            lane_marking_type = choose_random_lane_marking()
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="center" ,type=lane_marking_type)
        else:
            lane_marking_type = choose_random_lane_marking()
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="right" ,type=lane_marking_type)
            lane_marking_type = choose_random_lane_marking()
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="left" ,type=lane_marking_type)
        left_lane_section = ET.SubElement(lanes_element, "left_section")
        left_lane_number = get_lane_number_per_section(network_function)
        for i in range(left_lane_number):
            lane_type = get_lane_type("left")
            lane_width = get_lane_width(lane_type)
            lane_element = ET.SubElement(left_lane_section, "lane", type=lane_type, width=str(lane_width))
            lane_marking_type = choose_random_lane_marking()
            lane_marking_element = ET.SubElement(lane_element, "lane_marking", position="left" ,type=lane_marking_type)

    output_file_path = output_folder_path + "/descriptor.xml"

    xml_str = ET.tostring(road_network, encoding='utf-8')
    reparsed = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = reparsed.toprettyxml(indent="  ")

    with open(output_file_path, "wb") as file:
        file.write(pretty_xml_str.encode('utf-8'))

