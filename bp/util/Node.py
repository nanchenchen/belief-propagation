'''
This is a class that implements a node in a Bayesian network. 

The distribution field is a dictionary containing the conditional probability distribution of the node given its parents.
The keys to the dictionary are tuples containing the names of the possible states of the node and the evidence of the parents
for each line in the CPD table. If a node has no parents, the distribution will store the marginal distribution.

This is my implementation for a node. Feel free to alter it based on your own design for what a node should look like.
If you change the node constructor parameters, however, remember to change the BIF parse script so that the number of variables
received by the constructor is the same as the number of variables given to the constructor. 

'''

__author__ = "Antoine Bosselut"
__version__ = "1.0.1"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"

class Node:
    def __init__(self, theName, theType, numberStates, theStates, theProperty):
        self.name =  theName
        self.myType = theType
        self.numStates = numberStates
        self.states = theStates
        self.parents = []
        self.children = []
        self.dist = None
        self.myProperty = theProperty
        self.marginal = None
    
    #Add children when building the BN
    def addChildren(self, theChildren):
        for a in theChildren:
            self.children.append(a)
    
    #Add parents to a state when building the BN
    def addParent(self, theParents):
        for a in theParents:
            self.parents.append(a)
    
    #Check whether this is a root state with no parents
    def isRoot(self):
        return self.numParents()==0
        
    #Check whether this is a leaf state with no parents    
    def isLeaf(self):
        return self.numChildren()==0
    
    #Get the name of the node
    def getName(self):
        return self.name
    
    #Return the number of children of this node
    def numChildren(self):
        return len(self.children)
    
    #Return the possible states of the node
    def getStates(self):
        return self.states
    
    #Return the number of parents of this node
    def numParents(self):
        return len(self.parents)
    
    #Set the Probability Distribution of this node
    def setDist(self, distribution):
        self.dist = distribution
    
    #Return the probability distribution of thise node
    def getDist(self):
        return self.dist

    #Update the marginal based on new information
    def updateMarginal(self, information):
        #TODO: come up with a function for updating the marginal based on the information
        print ""

    #Return marginal distribution of node variable in node 
    def getMarginal(self):
        return self.marginal