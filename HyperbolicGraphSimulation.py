import math

class HyperBolicGraphSimulation:

    def __init__(self, average_degrees, number_of_points, negative_curvature):
        self.v = average_degrees
        self.n = number_of_points
        self.a = negative_curvature
        self.R = 2*math.log(self.n/self.v)



    def generateGraph(self):

    '''
    returns given size of random random points
    '''
    def samplePoints(self, size):
        return True
    '''
    returns random radius
    '''
    def sampleRadius(self):
        return True

    '''
    returns random angle
    '''
    def sampleAngle(self):
        return True

    '''
    returns hyperbolic distance between two points
    '''
    def calculateDistance(self, p1, p2):
        #p1= (r, angle), p2 = (r', angle')
        return 10


if __name__ == "__main__":
    simulator = HyperBolicGraphSimulation(1, 30, 1)
