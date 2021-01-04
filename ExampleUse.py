from HyperbolicGraphSimulation import HyperbolicGraphSimulation
import os

#define vertex style
style = ["\SetVertexStyle[MinSize=0.3\DefaultUnit, LineWidth=0pt, FillColor=mycolor1]\n", "\SetEdgeStyle[LineWidth=0.25pt]\n"]

#set up simulator
simulator = HyperbolicGraphSimulation()
simulator.setOutputFolder(os.getcwd()+ "//output_batch_2//" )

#parameters combinates
nrOfPoints = 250
avg_degrees = 4
neg_curvature = [(2.5-1)/2, (3.5-1)/2]

for curv in neg_curvature:
    #generate filepath
    filepath = "n{}_v{}_a{}.tikz".format(nrOfPoints, str(avg_degrees).replace(".", ","), str(curv).replace(".", ","))
    print(filepath)

    #generate graph
    simulator.generateGraph(nrOfPoints, avg_degrees, curv)
    #output relevant pictures
    simulator.draw(style=style, fp=filepath) #main graph
    simulator.saveDegreeDistribution(filepath.replace(".tikz", "_degreedistr.tikz"), show=True)   #degree distribution