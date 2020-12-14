import numpy as np
from scipy import stats
from Distribution import Distribution  #wrapper for stats distribution, samples bulkwise
import itertools
import networkx as nx
import network2tikz
import matplotlib.pyplot as plt

class HyperBolicGraphSimulation:

    def __init__(self, average_degrees, number_of_points, negative_curvature):
        self.v = average_degrees
        self.a = negative_curvature
        self.uniformSampler = Distribution(stats.uniform())
        #self.uniformSampler = stats.uniform()

    def generateGraph(self, n):
        self.R = 2*np.log(n/self.v)
        self.samplePoints(n)

        self.G = nx.Graph()
        # add all nodes
        for i in self.pointsPositions.keys():
            self.G.add_node(i)
        # add all edges between nodes if distance is smaller then radius
        for pair in itertools.combinations(self.pointsPositions.keys(), r=2):
            p1 = self.pointsPositions[pair[0]]
            p2 = self.pointsPositions[pair[1]]
            if self.calculateDistance(p1, p2) <= self.R:
                self.G.add_edge(pair[0], pair[1])
        # 
        self.drawGraph()

    '''
    returns given size of random random points
    '''
    def samplePoints(self, size):
        self.pointsPositions = {}
        for i in range(size):
            self.pointsPositions[i] = (self.sampleRadius(), self.sampleAngle())

    '''
    returns random radius
    '''
    def sampleRadius(self):

        '''the inverse of the density function'''         
        def invDensityRadius(y):
             return np.arcsinh((y*(np.cosh(self.a*self.R)-1))/self.a) / self.a

        return invDensityRadius(self.uniformSampler.rvs())

    '''
    returns random angle
    '''
    def sampleAngle(self):
        return self.uniformSampler.rvs() * 2* np.pi

    '''
    returns hyperbolic distance between two points
    '''
    def calculateDistance(self, p1, p2):
        #p1= (r, angle), p2 = (r', angle')
        dist_ang = np.pi - abs(np.pi - abs(p1[1]-p2[1]))
        return np.arccosh(np.cosh(p1[0])*np.cosh(p2[0]) - np.sinh(p1[0])*np.sinh(p2[0])* np.cos(dist_ang))

    '''
    convert polar coordinates to euclidian coordinates
    '''
    def convertPolarToEuclidian(self, p):
        #p= (r, angle)
        x = p[0]*np.cos(p[1])
        y = p[0]*np.sin(p[1])
        return (x, y)

    '''
    output to tex and display graph
    '''
    def drawGraph(self, fp="output.tex"):
        layout = {k : self.convertPolarToEuclidian(self.pointsPositions[k]) for k in self.pointsPositions.keys()}
        nx.draw(self.G, pos=layout)
        network2tikz.plot(self.G, fp, layout=layout)
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    simulator = HyperBolicGraphSimulation(1, 30, 1)
    simulator.generateGraph(1000)
