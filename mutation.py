class Mutation():
    def __init__(self, type, id):
        self.type = type
        self.id = id
    
    def apply(self, roadNetwork):
        pass


class LaneMarkingReplacer(Mutation):
    def __init__(self, type, id, newLaneType):
        super().__init__(type=type, id=id)
        self.newLaneType = newLaneType
    
    def apply(self, roadNetwork):
        lane_marking = roadNetwork.get_item_by_id(self.id)
        if lane_marking is not None:
            print("newLaneType: ", self.newLaneType)
            lane_marking.replace(self.newLaneType)
            print("Sikeres lane_type csere")


        else:
            print("Specified element cannot be found")

        return roadNetwork
    
class SpeedLimitPlacer(Mutation):
    def __init__(self, type, id, speedLimitValue, side, offset):
        super().__init__(type, id)
        self.speedLimitValue = speedLimitValue
        self.side = side
        self.offset = offset
    
    def apply(self, roadNetwork):
        road = roadNetwork.get_item_by_id(self.id)
        if road is not None:
            road.add_speed_limit(offset=self.offset, value=self.speedLimitValue, side=self.side)
        else:
            print("Specified element cannot be found")

        return roadNetwork
