import numpy as np
from scipy import stats
from Distribution import Distribution  #wrapper for stats distribution, samples bulkwise
import itertools
import networkx as nx
import network2tikz
import matplotlib.pyplot as plt
import datetime
import os
import tikzplotlib as plt2tikz

class HyperbolicGraphSimulation:

    def __init__(self):
        #bulkwise sampler is quicker then sampling one by one
        self.uniformSampler = Distribution(stats.uniform()) 
        self.dir = ""

    def setOutputFolder(self, dir):
        assert os.path.isdir(dir), "checking if valid folder"
        self.dir = dir 

    def generateGraph(self, n, average_degrees, negative_curvature):
        self.v = average_degrees
        self.a = negative_curvature
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
    def draw(self, fp="", style="", show = False):
        #get default filepath
        if fp == "":
            fp = datetime.datetime.now().strftime("%Hh%Mm%Ss %d-%m-%Y") +".tikz"
        
        #get the positions of all nodes in euclidian coordinates
        layout = {k : self.convertPolarToEuclidian(self.pointsPositions[k]) for k in self.pointsPositions.keys()}
        #convert the network to tikz
        network2tikz.plot(self.G, self.dir+fp.replace('.tikz', '.tex'), layout=layout, canvas=(10,10))
        self.addStyleString(fp, style)

        #display the matplotlib view of the graph
        if show:
            nx.draw(self.G, pos=layout)
            plt.grid(True)
            plt.show()

    '''
    add the given style options to the output.tex at appropriate place
    '''
    def addStyleString(self, fp, style):

        #read in the output file and interlace the styling options
        allLines = []
        shouldSave = False #filter to only save the tikz picture
        with open(self.dir+fp.replace('.tikz', '.tex'), "r") as f:
            for line in f:
                if not shouldSave:
                    if "begin{tikzpicture}" in line: #start of tikzpicutre
                        for style_line in style:
                            allLines.append(style_line)
                        shouldSave = True
                if shouldSave:
                    allLines.append(line)
                    if "end{tikzpicture}" in line: #end of tikzpicutre
                        shouldSave = False

        #output the file again
        with open(self.dir+fp.replace('.tex', '.tikz'), "w") as f:
            for line in allLines:
                f.write(line)

        #remove original .tex file
        os.remove(self.dir+fp.replace('.tikz', '.tex'))   
    
    '''
    saves the degree distribution of the currently generated graph

    parameters: 
    fp: filepath to save file to
    show: whether to display the plot on screen
    '''
    def saveDegreeDistribution(self, fp, show=False):
        print("Saving: " + fp)
        assert ".tikz" in fp, "filepath does not end in .tikz"

        degrees = [self.G.degree(n) for n in self.G.nodes()]
        degrees.sort()
        total = sum(degrees)
        cumulative = [sum(degrees[n::])/total for n in range(len(degrees))]
        prev = degrees[0]
        index = [prev]
        freq = [cumulative[0]]
        for i in range(1, len(degrees)):
            if not (degrees[i] == prev):
                prev = degrees[i]
                index.append(degrees[i])
                freq.append(cumulative[i])
                
        plt.loglog(index, freq)

        if dump:
            plt2tikz.save(self.dir+fp) #output

        if show:
            plt.show()
        
        plt.clf() #clear plot
