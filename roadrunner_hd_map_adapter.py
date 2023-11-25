import mathworks.scenario.scene.hd.hd_map_pb2 as hd_map_pb2
import mathworks.scenario.scene.hd.hd_map_header_pb2 as hd_map_header_pb2
import mathworks.scenario.scene.hd.hd_lanes_pb2 as hd_lanes_pb2
import mathworks.scenario.scene.hd.common_attributes_pb2 as common_attributes_pb2
import mathworks.scenario.scene.hd.hd_lane_markings_pb2 as hd_lane_markings_pb2
import mathworks.scenario.common.geometry_pb2 as geometry_pb2
import google.protobuf.internal.encoder as encoder
import google.protobuf.internal.decoder as decoder

from adapter import Adapter
import shapely

class RoadRunnerHDMapAdapter(Adapter):

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


def WriteToRRHD(filepath, headerMessage, HDMap):
    # Open the file as output binary
    fileStream = open(filepath, 'wb')

    # Serialize the header message to a byte array
    headerBytes = headerMessage.SerializeToString()

    # Write the length of the header message as a varint
    headerLengthVarint = encoder._VarintBytes(len(headerBytes))
    fileStream.write(headerLengthVarint)
    fileStream.write(headerBytes)

    # Serialize the HDMap message to a byte array
    HDMapBytes = HDMap.SerializeToString()

    # Write the length of the HDMap message as a varint
    HDMapLengthVarint = encoder._VarintBytes(len(HDMapBytes))
    #fileStream.write(HDMapLengthVarint)
    fileStream.write(HDMapBytes)

    fileStream.close()

def generate_roadrunner_hd_map(road_network, output_folder_path):

    roadrunnerConverter = RoadRunnerHDMapAdapter()
    rrMap = hd_map_pb2.HDMap()

    for road in road_network.get_roads():
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
    
    filepath = output_folder_path  + "/rrMap.rrhd"
    WriteToRRHD(filepath, headerMessage, rrMap)

    print("------HD_map------")
    print("------lanes--------")
    for lane in rrMap.lanes:
        print("\n\nid: ", lane.id)
        print("geo: ", lane.geometry)
        print("travel_dir: ", lane.travel_dir)
        print("type: ", lane.lane_type)
        print("right_boundary: ", lane.right_lane_boundary)
        print("left_boundary: ", lane.left_lane_boundary)
        for i in range(len(lane.successors)):
            print("suc: ", lane.successors[i])
        for i in range(len(lane.predecessors)):
            print("pred: ", lane.predecessors[i])
    
    print("------lane_boundaries--------")
    for laneBoundary in rrMap.lane_boundaries:
        print("\n\nid: ", laneBoundary.id)
        print("geo: ", laneBoundary.geometry)
        print("param_attributes: ", laneBoundary.parametric_attributes)

    
    print("------lane_markings--------")
    for laneMarking in rrMap.lane_markings:
        print("\n\nid: ", laneMarking.id)


    
        

