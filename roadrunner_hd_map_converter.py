import mathworks.scenario.scene.hd.hd_map_pb2 as hd_map_pb2
import mathworks.scenario.scene.hd.hd_map_header_pb2 as hd_map_header_pb2
import mathworks.scenario.scene.hd.hd_lanes_pb2 as hd_lanes_pb2
import mathworks.scenario.scene.hd.common_attributes_pb2 as common_attributes_pb2
import mathworks.scenario.scene.hd.hd_lane_markings_pb2 as hd_lane_markings_pb2
import mathworks.scenario.common.geometry_pb2 as geometry_pb2
import mathworks.scenario.scene.hd.hd_static_objects_pb2 as hd_static_objects_pb2
import google.protobuf.internal.encoder as encoder
import google.protobuf.internal.decoder as decoder

from converter import Converter
import shapely
import math

import subprocess
import sys

class RoadRunnerHDMapConverter(Converter):

    def processMultiLineSegmentList(self, multilinestrings, settable):
        for i in range(shapely.get_num_geometries(multilinestrings)):
            LineSegment = shapely.get_geometry(multilinestrings, i)
            startPoint = shapely.get_point(LineSegment, 0)
            endPoint = shapely.get_point(LineSegment, 1)
            startPoint_x = shapely.get_x(startPoint)
            startPoint_y = shapely.get_y(startPoint)
            endPoint_x = shapely.get_x(endPoint)
            endPoint_y = shapely.get_y(endPoint)
            if i==0:
                rr_point = geometry_pb2.Vector3(x=startPoint_x, y=startPoint_y, z=0)
                settable.append(rr_point)
            rr_point = geometry_pb2.Vector3(x=endPoint_x, y=endPoint_y, z=0)
            settable.append(rr_point)

    def processLaneType(self, laneType, settable):
        if laneType == "driving":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_DRIVING
        elif laneType == "unspecified":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_UNSPECIFIED
        elif laneType == "shoulder":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_SHOULDER
        elif laneType == "border":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_BORDER
        elif laneType == "restricted":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_RESTRICTED
        elif laneType == "parking":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_PARKING
        elif laneType == "curb":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_CURB
        elif laneType == "sidewalk":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_SIDEWALK
        elif laneType == "biking":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_BIKING
        elif laneType == "median":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_MEDIAN
        elif laneType == "none":
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_NONE
        else:
            settable = hd_lanes_pb2.LaneType.LANE_TYPE_NONE
        return settable
    
    def processTravelDir(self, travelDir, settable):
        if travelDir == "unspecified":
            settable = hd_lanes_pb2.TravelDir.TRAVEL_DIR_UNSPECIFIED
        elif travelDir == "undirected":
            settable = hd_lanes_pb2.TravelDir.TRAVEL_DIR_UNDIRECTED
        elif travelDir == "forward":
            settable = hd_lanes_pb2.TravelDir.TRAVEL_DIR_FORWARD
        elif travelDir == "backward":
            settable = hd_lanes_pb2.TravelDir.TRAVEL_DIR_BACKWARD
        elif travelDir == "bidirectional":
            settable = hd_lanes_pb2.travelDir.TRAVEL_DIR_BIDIRECTIONAL
        else:
            settable = hd_lanes_pb2.TravelDir.TRAVEL_DIR_UNSPECIFIED
        return settable


    def writeRRHD(self, filepath, headerMessage, HDMap):
        fileStream = open(filepath, 'wb')
        headerBytes = headerMessage.SerializeToString()
        headerLengthVarint = encoder._VarintBytes(len(headerBytes))
        fileStream.write(headerLengthVarint)
        fileStream.write(headerBytes)
        HDMapBytes = HDMap.SerializeToString()
        HDMapLengthVarint = encoder._VarintBytes(len(HDMapBytes))
        fileStream.write(HDMapBytes)
        fileStream.close()

            
    def compile_proto_files(self):
        process = subprocess.Popen("python roadrunner_setup.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = process.wait()
        output, error = process.communicate()
        if error:
            print(error)
            sys.exit(1)
    

    def convert_road_network_to_specified_format(self, road_network, output_folder_path):

        #self.compile_proto_files()

        roadrunnerConverter = RoadRunnerHDMapConverter()
        rrMap = hd_map_pb2.HDMap()
        speed_limits = [10, 20, 30, 60]

        for speed_limit_value in speed_limits:
            speed_limit_type_def_id = f"speed_limit_{speed_limit_value}"
            asset_path = f"Assets/speed_limit_{speed_limit_value}.rrpa"

            speed_limit_type_def = hd_static_objects_pb2.StaticObjectTypeDefinition(
                id=speed_limit_type_def_id,
                asset_path=common_attributes_pb2.RelativeAssetPath(asset_path=asset_path)
            )
            rrMap.static_object_types.append(speed_limit_type_def)

        for road in road_network.get_roads():
            for speed_limit in road.speed_limits:
                geoOrientedBoundingBox = geometry_pb2.GeoOrientedBoundingBox()
                #geoOrientedBoundingBox.center = geometry_pb2.Vector3()
                geoOrientedBoundingBox.center.x = speed_limit.pos_x
                geoOrientedBoundingBox.center.y = speed_limit.pos_y
                geoOrientedBoundingBox.center.z = 0
                
                geoOrientedBoundingBox.dimension.length = 0.5
                geoOrientedBoundingBox.dimension.width = 0.02588
                geoOrientedBoundingBox.dimension.height = 1.774

                geoOrientedBoundingBox.geo_orientation.geo_angle.roll =  0
                geoOrientedBoundingBox.geo_orientation.geo_angle.pitch =  0
                geoOrientedBoundingBox.geo_orientation.geo_angle.heading = math.radians(speed_limit.orientation)

                
                for static_object_type in rrMap.static_object_types:
                    if static_object_type.id == f"speed_limit_"+str(speed_limit.value):
                        speed_limit_static_object = hd_static_objects_pb2.StaticObject(id=speed_limit.id, geometry=geoOrientedBoundingBox, object_type_ref =common_attributes_pb2.Reference(id=static_object_type.id))
                rrMap.static_objects.append(speed_limit_static_object)

            for laneBoundary in road.get_lane_boundaries():
                rrLaneBoundary = hd_lanes_pb2.LaneBoundary(id=laneBoundary.id)
                roadrunnerConverter.processMultiLineSegmentList(laneBoundary.get_line(), rrLaneBoundary.geometry.values)
                lane_marking = None
                rrLaneBoundaryParamAttrib = hd_lanes_pb2.ParametricAttribution(span=common_attributes_pb2.ParametricRange(span_start=0, span_end=1))

                lane_marking = laneBoundary.get_marking()
                if lane_marking is not None:
                    rrLaneBoundaryMarking = hd_lane_markings_pb2.LaneMarking(asset_path = common_attributes_pb2.RelativeAssetPath(asset_path="Assets/Markings/" + lane_marking.get_type() + ".rrlms"))
                    if laneBoundary.get_marking().get_id():
                        rrLaneBoundaryMarking.id = laneBoundary.get_marking().get_id()
                    
                    rrLaneBoundaryMarkingRef = hd_lane_markings_pb2.MarkingReference(marking_id = common_attributes_pb2.Reference(id=rrLaneBoundaryMarking.id), flip_laterally=True)
                    #rrLaneBoundary.parametric_attributes.add()
            
                    rrLaneBoundaryParamAttrib.marking_reference.marking_id.id = rrLaneBoundaryMarking.id
                    rrMap.lane_markings.append(rrLaneBoundaryMarking)
                rrLaneBoundary.parametric_attributes.append(rrLaneBoundaryParamAttrib)
                rrMap.lane_boundaries.append(rrLaneBoundary)

            all_lanes = road.get_all_lanes()
            for lane in all_lanes:
                rrLane = hd_lanes_pb2.Lane(id=lane.get_id())
                roadrunnerConverter.processMultiLineSegmentList(lane.get_center_line(), rrLane.geometry.values)
                rrLane.lane_type = roadrunnerConverter.processLaneType(lane.get_type(), rrLane.lane_type)
                rrLane.travel_dir = roadrunnerConverter.processTravelDir(lane.get_travel_dir(), rrLane.travel_dir)

            

                if (lane.get_successor()):
                    rrLane.successors.append(common_attributes_pb2.AlignedReference(reference=common_attributes_pb2.Reference(id=lane.get_successor().get_id()), alignment=common_attributes_pb2.Alignment.ALIGNMENT_FORWARD))
                if (lane.get_predecessor()):
                    rrLane.predecessors.append(common_attributes_pb2.AlignedReference(reference=common_attributes_pb2.Reference(id=lane.get_predecessor().get_id()), alignment=common_attributes_pb2.Alignment.ALIGNMENT_FORWARD))

            

                for i in range (len(rrMap.lane_boundaries)):
                    if lane.rightBoundaryObject.id == rrMap.lane_boundaries[i].id:
                        rrLane.right_lane_boundary.alignment = common_attributes_pb2.Alignment.ALIGNMENT_FORWARD
                        rrLane.right_lane_boundary.reference.id = rrMap.lane_boundaries[i].id
                    if lane.leftBoundaryObject.id == rrMap.lane_boundaries[i].id:
                        rrLane.left_lane_boundary.alignment = common_attributes_pb2.Alignment.ALIGNMENT_FORWARD
                        rrLane.left_lane_boundary.reference.id = rrMap.lane_boundaries[i].id
        
            #for i in range (len(all_lanes)):
                #lane = all_lanes[i]
                #lane.right_lane_boundary.alignment = common_attributes_pb2.Alignment.ALIGNMENT_FORWARD
                #lane.right_lane_boundary.reference.id = road.get_lane_boundaries[i].id
                #lane.left_lane_boundary.alignment = common_attributes_pb2.Alignment.ALIGNMENT_FORWARD
                #lane.left_lane_boundary.reference.id = road.get_lane_boundaries[i+1].id

                rrMap.lanes.append(rrLane)

        
        headerMessage = hd_map_header_pb2.Header()
        headerMessage.projection.projection = 'PROJCS["WGS 84 / Transverse Mercator",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",0],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
        
        filepath = output_folder_path  + "/road_network.rrhd"
        self.writeRRHD(filepath, headerMessage, rrMap)

        return filepath