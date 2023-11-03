rrMap = roadrunnerHDMap;
roadCenters = [0 0;0 50;0 100];
roadWidth = 6;
rrMap.LaneBoundaries(1) = roadrunner.hdmap.LaneBoundary(ID="Left",Geometry=roadCenters-[roadWidth/2 0]);
rrMap.LaneBoundaries(2) = roadrunner.hdmap.LaneBoundary(ID="Right",Geometry=roadCenters+[roadWidth/2 0]);
rLane = roadrunner.hdmap.Lane(ID="Lane",Geometry=roadCenters,TravelDirection="Forward",LaneType="Driving");
leftBoundary(rLane,"Left",Alignment="Forward");
rightBoundary(rLane,"Right",Alignment="Forward");
rrMap.Lanes = rLane;
solidWhiteAsset = roadrunner.hdmap.RelativeAssetPath(AssetPath="Assets\Markings\SolidSingleWhite.rrlms.rrmeta");
rrMap.LaneMarkings = roadrunner.hdmap.LaneMarking(ID="SolidWhite",AssetPath=solidWhiteAsset);
markingRefSW = roadrunner.hdmap.MarkingReference(MarkingID=roadrunner.hdmap.Reference(ID="SolidWhite"));
markingSpan = [0 1];
markingAttribSW = roadrunner.hdmap.ParametricAttribution(MarkingReference=markingRefSW,Span=markingSpan);
rrMap.LaneBoundaries(1).ParametricAttributes = markingAttribSW;
rrMap.LaneBoundaries(2).ParametricAttributes = markingAttribSW;
write(rrMap,"C:\Users\balia\Desktop\Szakdolgozat\process\import_to_RoadRunner\simpleRoad.rrhd");
