import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import shapely
from roadrunnerhdmapgenerator import generate




class Geometry:
    def __init__(self, startX, startY, startHdg, length=None, endX=None, endY=None, endHdg=None):
        self.startX = float(startX)
        self.startY = float(startY)
        self.startHdg = float(startHdg)
        self.length = length
        if self.length is not None:
            self.length = float(self.length)
        self.endX = endX
        if self.endX is not None:
            self.endX = float(self.endX)
        self.endY = endY
        if self.endY is not None:
            self.endY = float(self.endY)
        self.endHdg = endHdg
        if self.endHdg is not None:
            self.endHdg = float(self.endHdg)
        self.refLine = None
        self.refLinePoints = []

    
    def createMultiLineStringsFromRefLinePoints(self):
        multiLineStrings = []
        if self.refLinePoints is not None:
            for i in range(shapely.get_num_geometries(self.refLinePoints)-1):
                prev_point = shapely.get_geometry(self.refLinePoints, i)
                next_point = shapely.get_geometry(self.refLinePoints, i+1)
                lineString = shapely.LineString([prev_point, next_point])
                multiLineStrings.append(lineString)
        self.refLine = shapely.multilinestrings(multiLineStrings)

class Line(Geometry):
    def __init__(self, startX, startY, startHdg, length=None, endX=None, endY=None, endHdg=None):
        super().__init__(startX, startY, startHdg, length, endX, endY, endHdg)
        if self.length is not None and self.endX is None and self.endY is None:
            self.calculateRefLinePointsFromLengthAndStartPoint()
            endPoint= shapely.get_geometry(self.refLinePoints,-1)
            self.endX = shapely.get_x(endPoint)
            self.endY = shapely.get_y(endPoint)
        elif self.endX is not None and self.endY is not None and self.length is None:
            self.calculateRefLinePointsFromStartPointAndEndPoint()
        else:
            raise Exception("Length or end position(x, y) must be given to create line segment.")
        self.endHdg = self.startHdg
        self.createMultiLineStringsFromRefLinePoints()
            
        globals()["x"] = self.endX
        globals()["y"] = self.endY
        globals()["hdg"] = self.endHdg
    
    def calculateRefLinePointsFromLengthAndStartPoint(self):
        self.refLinePoints = []
        samples = np.linspace(start=0.0, stop=self.length, num=globals()["resolution"])
        for sample in (samples):
            x = self.startX + np.cos(np.radians(self.startHdg))*sample
            y = self.startY + np.sin(np.radians(self.startHdg))*sample
            self.refLinePoints.append(shapely.Point(x,y))
        self.refLinePoints = shapely.multipoints(self.refLinePoints)

    def calculateRefLinePointsFromStartPointAndEndPoint(self):
        self.length = np.sqrt((self.endX - self.startX) **2 + (self.endX - self.startX) + (self.endY - self.startY) ** 2)
        self.calculateRefLinePointsFromLengthAndStartPoint()

       
        
class Lane:
    def __init__(self, width, type, road, lane_id, section, travel_dir):
        self.width = float(width)
        self.type = type
        self.travel_dir = travel_dir
        self.center_line = None
        self.rightBoundary = None
        self.rightBoundaryObject = None
        self.leftBoundary = None
        self.leftBoundaryObject = None
        self.section = section
        self.road = road
        self.id = self.road.id + "_Lane" + str(lane_id)
        self.offsetFromCenterLane = lane_id
        self.successor = None
        self.predecessor = None
        self.rightNeighbour = None
        self.leftNeighbour = None
        self.lane_markings = []

    
    def add_lane_marking(self, lane_marking):
        self.lane_markings.append(lane_marking)

    def createLaneFromXMLElement(lane_element, road, lane_id, lane_section):
        width = lane_element.get("width")
        lane_type = lane_element.get("type")
        travel_dir = lane_element.get("direction")
        if travel_dir is None:
            if lane_section == "right" and road.traffic_rule == "RHT":
                travel_dir = "forward"
            elif road.traffic_rule == "RHT" and lane_section == "left":
                travel_dir = "backward"
            elif lane_section == "right" and road.traffic_rule == "LHT":
                travel_dir = "backward"
            elif lane_section == "left" and road.traffic_rule == "LHT":
                travel_dir = "forward"
        
        lane_marking = lane_element.find("lane_marking")
        lane_marking = LaneMarking.createLaneMarkingFromXMLElement(lane_marking)
        lane = Lane(width, lane_type, road, lane_id, lane_section, travel_dir)
        lane.add_lane_marking(lane_marking)
        return lane
    
    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type

    def get_travel_dir(self):
        return self.travel_dir
    
    def get_center_line(self):
        return self.center_line
    
    def get_right_boundary(self):
        return self.rightBoundary
    
    def get_left_boundary(self):
        return self.leftBoundary
    
    def get_lane_markings(self):
        return self.lane_markings
    
    def get_section(self):
        return self.section
    
    def get_successor(self):
        return self.successor
    
    def get_predecessor(self):
        return self.predecessor
    

class LaneMarking:
    def __init__(self, type_,assetPath=None, position = None, id=None):
        self.type = type_
        if assetPath:
            self.assetPath = assetPath
        else:
            raise("AssetPath must be specified")
        self.id = id
        self.position = position
        
        
    def createLaneMarkingFromXMLElement(element):
        assetPath = element.get('asset_path')
        type_ = element.get('type')
        position = element.get('position')
        laneMarking = LaneMarking(type_, assetPath, position)
        return laneMarking
    
    def get_assetPath(self):
        return self.assetPath
    
    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id
    

class LaneBoundary:
    def __init__(self, id, line, marking=None):
        self.id = id
        self.line = line
        self.marking = marking

    def get_id(self):
        return self.id
    
    def get_line(self):
        return self.line
    
    def get_marking(self):
        return self.marking
    
    def set_marking(self, marking):
        self.marking = marking
    
    

class Section:
    def __init__(self):
        self.lanes = []

    def add_lane(self, lane):
        self.lanes.append(lane)

    def get_lane_count(self):
        return len(self.lanes)

    def get_lanes(self):
        return self.lanes
    
    def orderLanesAscending(self):
        self.lanes.sort(key=lambda lane: lane.offsetFromCenterLane)


    
class Road:
    def __init__(self, id, actPosX, actPosY, actHdg, geometry, type, traffic_rule, length=None, endX=None, endY=None, endHdg=None):
        self.id = "Road" + str(id)
        if length:
            self.length = float(length)
        if geometry == "line":
            self.geometry = Line(startX=actPosX, startY=actPosY, startHdg=actHdg, length=length, endX=endX, endY=endY)
        self.type = type
        self.traffic_rule = traffic_rule
        self.predecessor = None
        self.successor = None
        self.sections = {"right": Section(), "center": Section(), "left": Section()}
        self.rightNeighbour = None
        self.leftNeighbour = None
        self.lane_boundaries = []
        
    def createRoadFromXMLElement(road_element, id):
        length = road_element.get("length")
        geometry = road_element.get("geometry")
        type = road_element.get("type")
        traffic_rule = road_element.get("traffic_rule")
        road = Road(id, actPosX=globals()["x"], actPosY=globals()["y"], actHdg=globals()["hdg"], geometry=geometry, type=type, traffic_rule=traffic_rule, length=length)
        return road
    
    def get_all_lanes(self):
        lanes = []
        lanes.extend(self.sections["right"].get_lanes())
        lanes.extend(self.sections["center"].get_lanes())
        lanes.extend(self.sections["left"].get_lanes())       
        return lanes

    def classify_and_create_lanes(self, lanes_element):
        for section_element in lanes_element:
            for element in section_element:
                if element.tag == "lane":
                    if section_element.tag == "right_section":
                        lane_id = -1 * (self.sections["right"].get_lane_count() + 1)
                        lane_section = "right"
                    elif section_element.tag == "left_section":
                        lane_id = self.sections["left"].get_lane_count() + 1
                        lane_section = "left"
                    elif section_element.tag == "center_section":
                        if self.sections["center"].get_lane_count() > 0:
                            raise Exception("Only one center lane can be specified")
                        else:
                            lane_id = 0
                            lane_section = "center"

                    lane = Lane.createLaneFromXMLElement(element, self, lane_id, lane_section)
                    self.sections[lane_section].add_lane(lane)
        self.sections["right"].orderLanesAscending()
        self.sections["center"].orderLanesAscending()
        self.sections["left"].orderLanesAscending()

    def build_geometry(self):
        for lane in self.get_all_lanes():
            center_line_offset = self.calculate_center_line_offset_from_roadCenterLine(lane.offsetFromCenterLane)
            lane.center_line = shapely.offset_curve(self.geometry.refLine, center_line_offset)
            lane.rightBoundary = shapely.offset_curve(lane.center_line, -lane.width/2)
            lane.leftBoundary = shapely.offset_curve(lane.center_line, lane.width/2)


    def calculate_center_line_offset_from_roadCenterLine(self, offset):
        centerLaneWidth = self.sections["center"].get_lanes()[0].width
        if offset == 0:
            center_line_offset = 0
        elif offset > 0:
            center_line_offset = (centerLaneWidth / 2)
            for i in range(0, offset-1, 1):
                center_line_offset += self.sections["left"].get_lanes()[i].width
            center_line_offset += self.sections["left"].get_lanes()[offset-1].width / 2
        elif offset < 0:
            center_line_offset = -1*(centerLaneWidth / 2)
            for i in range(0, offset*-1-1, 1):
                center_line_offset -= self.sections["right"].get_lanes()[i].width
            center_line_offset -= self.sections["right"].get_lanes()[offset*-1-1].width/2
        return center_line_offset
    
    def create_and_set_lane_boundaries(self):
        print("lane_boundary CREATION AND SETTING")
        boundaries = []
        all_lanes = self.get_all_lanes()
        for lane in all_lanes:
            print("\nlane_id: ", lane.id)
            lane_boundary_id = ""
            if lane.section == "right":
                print("right")
                if lane.rightNeighbour:
                    lane_boundary_id = lane.rightNeighbour.id
                else:
                    lane_boundary_id = lane.id
                lane_boundary_id += "___"
                lane_boundary_id += lane.id
                lane_boundary_id += " boundary"
                print("lane_b_id: ", lane_boundary_id)
                lane_boundary = LaneBoundary(lane_boundary_id, lane.rightBoundary)
                boundaries.append(lane_boundary) 
                lane.rightBoundaryObject = lane_boundary
                if lane.rightNeighbour:
                    lane.rightNeighbour.leftBoundaryObject = lane_boundary
                
            elif lane.section == "left":
                print("left")
                lane_boundary_id = lane.id + "___"
                if lane.leftNeighbour:
                    lane_boundary_id_ = lane.leftNeighbour.id
                else:
                    lane_boundary_id_ = lane.id
                lane_boundary_id += lane_boundary_id_
                
                lane_boundary_id += " boundary"
                print("b_id: ", lane_boundary_id)
                lane_boundary = LaneBoundary(lane_boundary_id, lane.leftBoundary)
                boundaries.append(lane_boundary)
                lane.leftBoundaryObject = lane_boundary
                if lane.leftNeighbour:
                    lane.leftNeighbour.rightBoundaryObject = lane_boundary

            elif lane.section == "center":
                print("center")
                if lane.width == 0:
                    #right
                    lane_boundary_id = lane.rightNeighbour.id + "___" + lane.id
                    print("right_b_: ", lane_boundary_id)
                    lane_boundary = LaneBoundary(lane_boundary_id, lane.center_line)
                    boundaries.append(lane_boundary)
                    if lane.rightNeighbour:
                        lane.rightNeighbour.leftBoundaryObject = lane_boundary
                    lane.rightBoundaryObject = lane_boundary
        
                    #left
                    lane_boundary_id = lane.id + "___" + lane.leftNeighbour.id
                    print("left_b_: ", lane_boundary_id)
                    lane_boundary = LaneBoundary(lane_boundary_id, lane.center_line)
                    boundaries.append(lane_boundary)
                    if lane.leftNeighbour:
                        lane.leftNeighbour.rightBoundaryObject = lane_boundary
                    lane.leftBoundaryObject = lane_boundary

    
        self.lane_boundaries = boundaries

        
    
    def set_neighbours(self):
        lanes = self.get_all_lanes()
        for i in range(len(lanes)):
            if i > 0:
                lanes[i].rightNeighbour = lanes[i-1]
                lanes[i-1].leftNeighbour = lanes[i]
            if i < len(lanes)-1:
                lanes[i].lefttNeighbour = lanes[i+1]
                lanes[i+1].rightNeighbour = lanes[i]

    def get_lane_boundaries(self):
        return self.lane_boundaries
    
    def link_marking_and_boundaries(self):
        for lane in self.get_all_lanes():
            print("___lane_id: ", lane.id)
            lane_markings = lane.get_lane_markings()
            for lane_marking in lane_markings:
                print("___lane_marking_id: ", lane_marking.id)
                if lane_marking.position == "right" and lane.section == "right":
                    print("___lane_marking_pos: ", "right")
                    boundary = lane.rightBoundaryObject
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            print("match: ", lane_boundary.id)
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")
                elif lane_marking.position == "center" and lane.section == "center" and lane.width == 0:
                    print("___lane_marking_pos: ", "center")
                    boundary = lane.rightBoundaryObject #Lehetne a bal oldali boundaryObject teljesen mindegy ugyanaz a geometriája mindkettőnek
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            print("match: ", lane_boundary.id)
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")
                if lane_marking.position == "left" and lane.section == "left":
                    print("___lane_marking_pos: ", "left")
                    boundary = lane.leftBoundaryObject
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            print("match: ", lane_boundary.id)
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")
                    
            



class RoadNetwork:
    def __init__(self, vendor=None, format=None):
        self.vendor = vendor
        self.format = format
        self.roads = []

    def build_from_xml(xmlFile):
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        vendor = root.get('vendor')
        format = root.get('format')
        roadNetwork = RoadNetwork(vendor, format)
        for road_element in root.findall("road"):
            road = Road.createRoadFromXMLElement(road_element, len(roadNetwork.roads))
            roadNetwork.roads.append(road)
        
            lanes_element = road_element.find("lanes")
            road.classify_and_create_lanes(lanes_element)
            road.build_geometry()
            road.set_neighbours()
            road.create_and_set_lane_boundaries()
            road_bounadries = road.get_lane_boundaries()
            #for boundary in road_bounadries:
                #print("boundary_id: ", boundary.get_id())
            road.link_marking_and_boundaries()
        roadNetwork.link_roads()
        roadNetwork.link_lanes()
        return roadNetwork
    
    def link_roads(self):
        for i in range(len(self.roads)):
            pred_road = None
            suc_road = None
            act_road = self.roads[i]
            
            if i > 0:
                pred_road = self.roads[i-1]
                act_road.predecessor = pred_road
            
            if i < len(self.roads) - 1:
                suc_road = self.roads[i+1]
                act_road.successor = suc_road
            
            if pred_road:
                pred_road.successor = act_road
            
            if suc_road:
                suc_road.predecessor = act_road

    def link_lanes_by_section(self, section):
        for i in range(len(self.roads)):
            pred_road = None
            suc_road = None
            act_road = self.roads[i]

            if i > 0:
                pred_road = self.roads[i - 1]
                act_all_lanes = act_road.sections[section].get_lanes()
                pred_all_lanes = pred_road.sections[section].get_lanes()
                for l in range(len(act_all_lanes)):
                    if (l < len(pred_all_lanes)):
                        act_all_lanes[l].predecessor = pred_all_lanes[l]
                        pred_all_lanes[l].successor = act_all_lanes[l]

            if i < len(self.roads) - 1:
                suc_road = self.roads[i + 1]
                act_all_lanes = act_road.sections[section].get_lanes()
                suc_all_lanes = suc_road.sections[section].get_lanes()
                for l in range(len(act_all_lanes)):
                    if (l < len(suc_all_lanes)):
                        act_all_lanes[l].successor = suc_all_lanes[l]
                        suc_all_lanes[l].predecessor = act_all_lanes[l]
                        
    def link_lanes(self):
        self.link_lanes_by_section("right")
        self.link_lanes_by_section("center")
        self.link_lanes_by_section("left")

    def get_roads(self):
        return self.roads

        

def main():

    global x, y, hdg, resolution
    x = 0
    y = 0.0
    hdg = 0.0
    resolution = 5
    
    road_network = RoadNetwork.build_from_xml("road_network_descriptor.xml")
    for road in road_network.roads:
        print("road_id", road.id)
        print("     refLine: ", road.geometry.refLine)
        if road.successor:
            print("     successor_id: ", road.successor.id)
        if road.predecessor:
            print("     predecessor_id: ", road.predecessor.id)
        for section in road.sections:
            for lane in road.sections[section].get_lanes():
                print("\n         lane_id", lane.id)
                print("         lane_geo", lane.center_line)
                print("         lane_right_boundary", lane.rightBoundary)
                print("         lane_right_boundary", lane.rightBoundaryObject.get_id())
                if lane.rightBoundaryObject.get_marking():
                    print("         lane_right_boundary_marking_id", lane.rightBoundaryObject.get_marking().id)
                    print("         lane_right_boundary_marking_asset", lane.rightBoundaryObject.get_marking().get_assetPath())
                print("         lane_left_boundary", lane.leftBoundary)
                print("         lane_left_boundary", lane.leftBoundaryObject.get_id())
                if lane.leftBoundaryObject.get_marking():
                    print("         lane_left_boundary_marking_id", lane.leftBoundaryObject.get_marking().id)
                    print("         lane_left_boundary_marking_asset", lane.leftBoundaryObject.get_marking().get_assetPath())
                if lane.successor:
                    print("         lane_suc_id", lane.successor.id)
                if lane.predecessor:
                    print("         lane_pred_id", lane.predecessor.id)
                print("         lane_type", lane.type)
                print("         lane_travel_dir", lane.travel_dir)
                print("         lane_width", lane.width)
                print("         lane_section", lane.section)
                print("         lane_offset", lane.offsetFromCenterLane)
                if lane.rightNeighbour:
                    print("         right_neighbour", lane.rightNeighbour.id)
                if lane.leftNeighbour:
                    print("         left_neighbour", lane.leftNeighbour.id)

        for boundary in road.lane_boundaries:
            print("____boundary_id ", boundary.id)
            print("____geo: ", boundary.line)

    print("x:", globals()["x"])
    print("y:", globals()["y"])
    print("hdg:", globals()["hdg"])

    generate(road_network)


main()