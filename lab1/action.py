class Action:
    def __init__(self, origin, destination, distance, speed):
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.speed = speed
        self.cost = distance / (speed/3.6)

    def __repr__(self):
        return (f"Action({self.origin} to {self.destination} | "
                f"distance: {self.distance}, speed: {self.speed}, cost: {self.cost})")

    def __str__(self):
        return ('The intersection starts on ' + str(self.origin) +
                ' and finishes at ' + str(self.destination) +
                ', with a distance of ' + str(self.distance) +
                ', speed: ' + str(self.speed) +
                ', time cost: ' + f"{self.cost:.2f}")