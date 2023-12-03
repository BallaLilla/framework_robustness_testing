import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import shapely

import os


def createOffsetGeometry(offset, actMultiLineStrings, predMultiLineStrings=None):
    offset_line = None
     
    if actMultiLineStrings is None:
        raise Exception("actMultiLineString is None and must be specified")
    
    if offset is None:
        raise Exception("offset is None and must be specified")
    else:
        offset_line = shapely.offset_curve(actMultiLineStrings, offset)
   
    if predMultiLineStrings is not None:
        lastMultiLineString = shapely.get_geometry(predMultiLineStrings, -1)
        last_point = shapely.get_point(lastMultiLineString, -1)
        point_x = shapely.get_x(last_point)
        point_y = shapely.get_y(last_point)

        offset_line_first_segment = shapely.get_geometry(offset_line, 0)
        offset_first_point = shapely.get_point(offset_line_first_segment, 0)
        offset_first_x = shapely.get_x(offset_first_point)
        offset_first_y = shapely.get_y(offset_first_point)

        x_offset = point_x - offset_first_x
        y_offset = point_y - offset_first_y

        offset_line = shapely.affinity.translate(offset_line, xoff=x_offset, yoff=y_offset)

    return offset_line


class SpeedLimit:
    def __init__(self, id, value, position, orientation):
        print("pos: ", position)
        self.id = id
        self.value = value
        self.pos_x = shapely.get_x(position)
        self.pos_y = shapely.get_y(position)
        self.orientation = orientation
        print("SPEED_LIMIT_value: ", self.value)
        print("SPEED_LIMIT_pos_x: ", self.pos_x)
        print("SPEED_LIMIT_pos_y: ", self.pos_y)
        print("SPEED_LIMIT_orientation: ", self.orientation)
        



class Geometry:
    def __init__(self, startX, startY, startHdg, length=None, endX=None, endY=None, endHdg=None):
        self.startX = float(startX)
        self.startY = float(startY)
        self.startHdg = float(startHdg)
        if length is not None:
            self.length = float(length)
        else:
            self.length = length
        if endX is not None:
            self.endX = float(endX)
        else:
            self.endX = endX
        if endY is not None:
            self.endY = float(endY)
        else:
            self.endY = endY
        if endHdg is not None:
            self.endHdg = float(endHdg)
        else:
            self.endHdg = endHdg
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

    def createGeometryFromXMLElement(geometry_element):
        pass


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
    
    def createGeometryFromXMLElement(geometry_element, x, y, hdg):
        length = geometry_element.get("length")
        line = Line(startX=x, startY=y, startHdg=hdg, length=length)
        return line
    


    
   
    
    


class Arc(Geometry):
    def __init__(self, startX, startY, startHdg, curvature, angle=None, length=None, endX=None, endY=None, endHdg=None):
        super().__init__(startX, startY, startHdg, length, endX, endY, endHdg)
        if curvature:
            if curvature == 0:
                raise Exception("Zero curvature is specified. Please use line")
            else:
                self.curvature = float(curvature)
        
        self.radius = 1 / abs(self.curvature)
        if angle:
            self.angle = float(angle)
            self.length = abs(self.angle) * self.radius
        else:
            raise Exception("Angle must be specified")
        
        self.calculateRefLinePoints()
        endPoint= shapely.get_geometry(self.refLinePoints,-1)
        self.endX = shapely.get_x(endPoint)
        self.endY = shapely.get_y(endPoint)
        self.endHdg = self.startHdg + self.angle
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!refLinePoints: ", self.refLinePoints)
        self.createMultiLineStringsFromRefLinePoints()
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!refLine: ", self.refLine)
        
    
    def calculateRefLinePoints(self):
        x = 0.0
        y = 0.0
        self.refLinePoints = []
        for i in range(globals()["resolution"]):
            theta = (i /(globals()["resolution"]-1)) * self.angle
            x_rel= np.sin(np.radians(theta)) * self.radius
            y_rel= (self.radius - np.cos(np.radians(theta)) * self.radius)
            x_rel = np.cos(np.radians(self.startHdg)) * x_rel - np.sin(np.radians(self.startHdg)) * y_rel
            y_rel = np.sin(np.radians(self.startHdg)) * x_rel + np.cos(np.radians(self.startHdg)) * y_rel
            x += x_rel
            y += y_rel
            self.refLinePoints.append(shapely.Point(x, y))
        self.refLinePoints = shapely.multipoints(self.refLinePoints)

   
    
    def createGeometryFromXMLElement(geometry_element, x, y, hdg):
        length = geometry_element.get("length")
        curvature = geometry_element.get("curvature")
        angle = geometry_element.get("angle")
        arc = Arc(startX=x, startY=y, startHdg=hdg, length=length, curvature=curvature, angle=angle)
        return arc
    

    def createOffsetGeometry(self, offset, predStartPoint=None):
        offset_arc = None
        if offset is None:
            raise Exception("offset is None and must be specified")
        else:
            offset_arc = shapely.offset_curve(self.refLine, offset)
            


        if predStartPoint is not None:
           predStartPoint_x = shapely.get_x(predStartPoint)
           predStartPoint_y = shapely.get_y(predStartPoint)
           offset_arc_coords = offset_arc.coords
           offset_arc_x = offset_arc_coords[0]
           offset_arc_y = offset_arc_coords[1]

           x_offset = predStartPoint_x - offset_arc_x
           y_offset = predStartPoint_y - offset_arc_y

           offset_arc = shapely.affinity.translate(offset_arc, x_offset=x_offset, y_offset=y_offset)

        return offset_arc
    

    



        
class Lane:
    def __init__(self, width, type, road, lane_id, section, travel_dir):
        self.width = float(width)
        self.type = type
        self.travel_dir = travel_dir
        self.center_line = None
        self.rightBoundaryObject = None
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
        
        lane_markings = lane_element.findall("lane_marking")
        lane = Lane(width, lane_type, road, lane_id, lane_section, travel_dir)
        for lane_marking in lane_markings:
            lane_marking_ = LaneMarking.createLaneMarkingFromXMLElement(lane_marking)
            lane.add_lane_marking(lane_marking_)
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
    def __init__(self, type_, position = None, id=None):
        self.type = type_
        self.id = id
        self.position = position
        
        
    def createLaneMarkingFromXMLElement(element):
        #assetPath = element.get('asset_path')
        type_ = element.get('type')
        position = element.get('position')
        laneMarking = LaneMarking(type_, position)
        return laneMarking
    
    def get_type(self):
        return self.type
    
    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id
    
    def replace(self, type):
        self.type = type

    

class LaneBoundary:
    def __init__(self, id, line):
        self.id = id
        self.line = line
        self.marking = None

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
    def __init__(self, id, geometry, type, traffic_rule, endX=None, endY=None, endHdg=None):
        self.id = "Road" + str(id)
        self.geometry = geometry
        self.type = type
        self.traffic_rule = traffic_rule
        self.predecessor = None
        self.successor = None
        self.sections = {"right": Section(), "center": Section(), "left": Section()}
        self.rightNeighbour = None
        self.leftNeighbour = None
        self.lane_boundaries = []
        self.speed_limits = []
        
    def createRoadFromXMLElement(road_element, id):
        geometry_element= road_element.find("geometry")
        geo_type = geometry_element.get("type")
        plan_view_geo=None
        if geo_type == "line":
            plan_view_geo = Line.createGeometryFromXMLElement(geometry_element, globals()["x"], globals()["y"], globals()["hdg"])
        elif geo_type == "arc":
            plan_view_geo = Arc.createGeometryFromXMLElement(geometry_element, globals()["x"], globals()["y"], globals()["hdg"])
        type = road_element.get("type")
        traffic_rule = road_element.get("traffic_rule")
        road = Road(id, geometry=plan_view_geo, type=type, traffic_rule=traffic_rule)

        globals()["x"] = road.geometry.endX
        print("globals()[x]: ",  globals()["x"])
        globals()["y"] = road.geometry.endY
        print("globals()[y]: ",  globals()["y"])
        globals()["hdg"] = road.geometry.endHdg
        print("globals()[hdg]: ",  globals()["hdg"])
        
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
                    elif section_element.tag == "median_section":
                        if self.sections["center"].get_lane_count() + 1 > 1:
                            raise Exception("Only one center lane can be specified")
                        else:
                            lane_id = 0
                            lane_section = "center"

                    
                    lane = Lane.createLaneFromXMLElement(element, self, lane_id, lane_section)
                    self.sections[lane_section].add_lane(lane)
        self.sections["right"].orderLanesAscending()
        self.sections["center"].orderLanesAscending()
        self.sections["left"].orderLanesAscending()



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
        boundaries = []
        all_lanes = self.get_all_lanes()
        for lane in all_lanes:
            # create lane center line
            predMultiLineString = None
            center_line_offset = None
            if lane.predecessor:
                predMultiLineString = lane.predecessor.center_line
            center_line_offset = self.calculate_center_line_offset_from_roadCenterLine(lane.offsetFromCenterLane)
            lane.center_line = createOffsetGeometry(offset=center_line_offset, actMultiLineStrings=self.geometry.refLine, predMultiLineStrings=predMultiLineString)
            
            #Creating boundaries
            lane_boundary_id = ""
            if lane.section == "right":
                if lane.rightNeighbour:
                    lane_boundary_id = lane.rightNeighbour.id
                else:
                    lane_boundary_id = lane.id
                lane_boundary_id += "___"
                lane_boundary_id += lane.id
                lane_boundary_id += " boundary"
                if lane.predecessor:
                    predMultiLineString=lane.predecessor.rightBoundaryObject.line
            
                lane_boundaryObject = createOffsetGeometry(offset=-lane.width/2,actMultiLineStrings=lane.center_line ,predMultiLineStrings=predMultiLineString)
                lane_boundary = LaneBoundary(lane_boundary_id, lane_boundaryObject)
                boundaries.append(lane_boundary) 
                lane.rightBoundaryObject = lane_boundary
                if lane.rightNeighbour:
                    lane.rightNeighbour.leftBoundaryObject = lane_boundary
                
            if lane.section == "left":
                lane_boundary_id = lane.id + "___"
                if lane.leftNeighbour:
                    lane_boundary_id_ = lane.leftNeighbour.id
                else:
                    lane_boundary_id_ = lane.id
                lane_boundary_id += lane_boundary_id_
                
                lane_boundary_id += " boundary"
                if lane.predecessor:
                    predMultiLineString=lane.predecessor.leftBoundaryObject.line
        
                lane_boundaryObject = createOffsetGeometry(offset=lane.width/2, actMultiLineStrings=lane.center_line, predMultiLineStrings=predMultiLineString)
                lane_boundary = LaneBoundary(lane_boundary_id, lane_boundaryObject)
                boundaries.append(lane_boundary)
                lane.leftBoundaryObject = lane_boundary
                if lane.leftNeighbour:
                    lane.leftNeighbour.rightBoundaryObject = lane_boundary

            if lane.section == "center":
                    #right
                    if lane.rightNeighbour:
                        lane_boundary_id = lane.rightNeighbour.id
                    else:
                        lane_boundary_id = lane.id
                    lane_boundary_id += "___"
                    lane_boundary_id += lane.id
                    lane_boundary_id += " boundary"
                    if lane.predecessor:
                        predMultiLineString=lane.predecessor.rightBoundaryObject.line
                
                    lane_boundaryObject = createOffsetGeometry(offset=-lane.width/2,actMultiLineStrings=lane.center_line ,predMultiLineStrings=predMultiLineString)
                    lane_boundary = LaneBoundary(lane_boundary_id, lane_boundaryObject)
                    boundaries.append(lane_boundary) 
                    lane.rightBoundaryObject = lane_boundary
                    if lane.rightNeighbour:
                        lane.rightNeighbour.leftBoundaryObject = lane_boundary
                    
        
                    #left
                    lane_boundary_id = lane.id + "___"
                    if lane.leftNeighbour:
                        lane_boundary_id_ = lane.leftNeighbour.id
                    else:
                        lane_boundary_id_ = lane.id
                    lane_boundary_id += lane_boundary_id_
                    
                    lane_boundary_id += " boundary"
                    if lane.predecessor:
                        predMultiLineString=lane.predecessor.leftBoundaryObject.line
            
                    lane_boundaryObject = createOffsetGeometry(offset=lane.width/2, actMultiLineStrings=lane.center_line, predMultiLineStrings=predMultiLineString)
                    lane_boundary = LaneBoundary(lane_boundary_id, lane_boundaryObject)
                    boundaries.append(lane_boundary)
                    lane.leftBoundaryObject = lane_boundary
                    if lane.leftNeighbour:
                        lane.leftNeighbour.rightBoundaryObject = lane_boundary
                
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
            lane_markings = lane.get_lane_markings()
            for lane_marking in lane_markings:
                if lane_marking.position == "right" and lane.section == "right":
                    boundary = lane.rightBoundaryObject
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")
                if lane_marking.position == "right" and lane.section == "center" and lane.width > 0:
                    boundary = lane.rightBoundaryObject
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")
                if lane.section == "center" and lane.width == 0:
                    boundary = lane.rightBoundaryObject
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")

                    boundary = lane.leftBoundaryObject
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")
                    
                if lane_marking.position == "left" and lane.section == "left":
                    boundary = lane.leftBoundaryObject
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")
                if lane_marking.position == "left" and lane.section == "center" and lane.width > 0:
                    boundary = lane.leftBoundaryObject
                    for lane_boundary in self.get_lane_boundaries():
                        if boundary.id == lane_boundary.id:
                            lane_boundary.set_marking(lane_marking)
                            lane_marking.set_id(boundary.id + "_marking")



    def add_speed_limit(self, value, side, offset):
        print("ADDING SPEED LIMIT")
        if side == "left" or side =="both":
            mostLeftLane = self.get_all_lanes()[-1]
            position = createOffsetGeometry(offset=offset, actMultiLineStrings=mostLeftLane.leftBoundaryObject.line)
            position = shapely.get_geometry(position, -1)
            position = shapely.get_point(position, -1)
            orientation = self.geometry.startHdg + 90
            self.speed_limits.append(SpeedLimit(id=self.id + "_left_speed_limit_" + str(value), value=value, position=position, orientation=orientation))

        if side == "right" or side == "both":
            mostLeftLane = self.get_all_lanes()[0]
            position = createOffsetGeometry(offset=offset, actMultiLineStrings=mostLeftLane.rightBoundaryObject.line)
            position = shapely.get_geometry(position, 0)
            position = shapely.get_point(position, 0)
            orientation = self.geometry.startHdg - 90
            self.speed_limits.append(SpeedLimit(id=self.id + "_right_speed_limit_" + str(value), value=value, position=position, orientation=orientation))


            

            



class RoadNetwork:
    def __init__(self):
        self.roads = []

    def build_from_xml(xmlFile):
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        globals()["resolution"] = int(root.get('resolution'))
        globals()["x"] = float(root.get('x'))
        globals()["y"] = float(root.get('y'))
        globals()["hdg"] = float(root.get('hdg'))
       
        roadNetwork = RoadNetwork()
        for road_element in root.findall("road"):
            road = Road.createRoadFromXMLElement(road_element, len(roadNetwork.roads))
            roadNetwork.roads.append(road)
        
            lanes_element = road_element.find("lanes")
            road.classify_and_create_lanes(lanes_element)
            road.set_neighbours()
            #road_bounadries = road.get_lane_boundaries()
        roadNetwork.link_roads()
        roadNetwork.link_lanes()
        for road in roadNetwork.roads:
            #road.build_geometry()
            road.create_and_set_lane_boundaries()
            road.link_marking_and_boundaries()

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
    

    def get_item_by_id(self, item_id):
        print("keresett_id: ", item_id)
        for road in self.roads:
            if road.id == item_id:
                return road
            for lane in road.get_all_lanes():
                if lane.id == item_id:
                    return lane
                rightBoundaryObj = lane.rightBoundaryObject
                if rightBoundaryObj.id == item_id:
                    return rightBoundaryObj
                rightBoundaryObjMarking = rightBoundaryObj.get_marking()
                if rightBoundaryObjMarking is not None:
                    if rightBoundaryObjMarking.id == item_id:
                        return rightBoundaryObjMarking
                    
                leftBoundaryObj = lane.leftBoundaryObject
                if leftBoundaryObj.id == item_id:
                    return leftBoundaryObj
                leftBoundaryObjMarking = leftBoundaryObj.get_marking()
                if leftBoundaryObjMarking is not None:
                    if leftBoundaryObjMarking.id == item_id:
                        return leftBoundaryObjMarking
        print("Nincs ilyen")
        return None
                

        

def generate_concrete_road_network(descriptor_xml_path):

    
    global x, y, hdg, resolution
    
    road_network = RoadNetwork.build_from_xml(descriptor_xml_path)
    for road in road_network.roads:
        print("road_id", road.id)
        print("     refLine: ", road.geometry)
        if road.successor:
            print("     successor_id: ", road.successor.id)
        if road.predecessor:
            print("     predecessor_id: ", road.predecessor.id)
        for section in road.sections:
            for lane in road.sections[section].get_lanes():
                print("\n         lane_id", lane.id)
                #print("         lane_geo", lane.center_line)
                print("         lane_right_boundaryObject_id", lane.rightBoundaryObject.id)
                marking = lane.rightBoundaryObject.get_marking()
                print("         lane_right_boundary_marking_id", marking.id)
                print("         lane_right_boundary_marking_type", marking.type)
                print("         lane_left_boundaryObject_id", lane.leftBoundaryObject.id)
                marking = lane.leftBoundaryObject.get_marking()
                print("         lane_left_boundary_marking_id", marking.id)
                print("         lane_left_boundary_marking_type", marking.type)
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
            lane_marking = boundary.get_marking()
            #print("____marking ", lane_marking.id)
            #print("____marking_type ", lane_marking.type)
            #print("____marking_pos ", lane_marking.position)


        for speed_limit in road.speed_limits:
            print("____SPEED_LIMIT", speed_limit.id)
            #print("____marking ", lane_marking.id)
            #print("____marking_type ", lane_marking.type)
            #print("____marking_pos ", lane_marking.position)
        

    print("x:", globals()["x"])
    print("y:", globals()["y"])
    print("hdg:", globals()["hdg"])



    return road_network