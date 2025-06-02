class State:
    def __init__(self,id,lon,lat):
            self.identifier = id
            self.longitude = lon
            self.latitude = lat

    def __eq__(self, other):
        return isinstance(other, State) and self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def __repr__(self):
        return (f"State({self.identifier} | "
                f"latitude: {self.latitude}, longitude: {self.longitude})")

    def __str__(self):
        return ('The state corresponds to intersection ' + str(self.identifier) +
                ', located at latitude: ' + str(self.latitude) +
                ', and longitude: ' + str(self.longitude))