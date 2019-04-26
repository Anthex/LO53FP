from operator import itemgetter as ig
from math import floor, sqrt, ceil, exp
from numpy import arange
class RSSVector():
    distances = []
    def __init__(self, n1, n2, n3, n4):
        '''
        :param n1: AP1 RSSI
        :param n2: AP2 RSSI
        :param n3: AP3 RSSI
        :param n4: AP4 RSSI
        '''
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
    
    def __eq__(self, v2):
        return True if v2.n1 == self.n1 and  v2.n2 == self.n2 \
        and  v2.n3 == self.n3 and  v2.n4 == self.n4 else False
        
class Location():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, loc2):
        return bool(self.x == loc2.x and self.y == loc2.y and self.z == loc2.z)
        
    def __mul__(self, multiplier):
        returnValue = Location(self.x, self.y, self.z)
        returnValue.x *= multiplier
        returnValue.y *= multiplier
        returnValue.z *= multiplier
        return returnValue

    def __rmul__(self, multiplier):
        return self * multiplier

    def __add__(self, added):
        returnValue = Location(self.x, self.y, self.z)
        returnValue.x += added.x
        returnValue.y += added.y
        returnValue.z += added.z
        return returnValue

    def __isub__(self, value):
        return self + -1 * value

    def __itruediv__(self, divider):
        returnValue = Location(self.x, self.y, self.z)
        returnValue.x /= divider
        returnValue.y /= divider
        returnValue.z /= divider
        return returnValue

    def toString(self):
        return "(" + str(self.x) + " ; " + str(self.y) + " ; " + str(self.z) + ")"

    def distanceTo(self, loc):
        return sqrt(pow(self.x - loc.x, 2) + pow(self.y - loc.y, 2) + pow(self.z - loc.z,2))

    def getPositionInArray(self, arraySize=3):
        '''
        Returns the unique ID of a fingerprint given its location
        :param arraySize: (Optional) dimension of the array
        '''
        temp = Location(self.x, self.y)
        temp /= 2
        temp -= Location(1,1)
        return floor((temp.x * arraySize + temp.y)/2)

    @staticmethod
    def fromID(origin_id, arraySize=3):
        '''
        Returns the Location of a fingerprint of known ID
        :param: ID to resolve
        :param arraySize: (Optional) dimension of the array
        '''
        origin_id -= 1
        y=origin_id % 3
        x=floor((origin_id - y) / 3)
        returnValue = Location(x, y)
        returnValue *= 2
        returnValue += Location(1,1)
        returnValue *= 2
        return returnValue

class Cell():
    def __init__(self, v_, loc):
        '''
        :param v_: RSSI vector of the fingerprint
        :param loc: Location of the fingerprint
        '''
        self.v = v_
        self.location = loc

class MarkovValue():
    def __init__(self, nb=0, percentage=0.0):
        '''
        :param nb: Counter of incoming/outgoing movements
        :param percentage: probability of being the next movement [0.0 , 1.0]
        '''
        self.nb = nb
        self.percentage = percentage # Probability of Markov model (100% <=> 1.0)

class MarkovModel():
    def __init__(self,cells):
        '''
        :param cells: an array containing all the cells of the model
        '''
        self.MarkovValues = [] #table of the coefficients of the Markov Model
        self.cells = cells
        self.previousCell = 0
        for i in range (0, 11):
            self.MarkovValues.append([])
            for _ in range (0, 10):
                self.MarkovValues[i].append(MarkovValue())
        self.MarkovValues[10][0].nb = 1 #initial position sigma increment

    def moveToCellID(self, nextCell):
        '''
        Registers a movement from the current cell to a specified location by its ID
        :param nextCell: The ID of the new location
        '''
        self.MarkovValues[nextCell][self.previousCell].nb += 1
        self.MarkovValues[10][nextCell].nb += 1
        self.refreshPercentage(self.previousCell)
        self.previousCell = nextCell
        
    def moveToCell(self, nextCell):
        '''
        Registers a movement from the current cell to another based on the Location of its fingerprint
        :param nextCell: The location of the new cell
        '''
        self.moveToCellID(nextCell.location.getPositionInArray()+1)

    def refreshPercentage(self, col):
        '''
        Refreshes the probabilities of a column after a counter is changed
        Needed after every change to the nb field
        :param col: the # of the column to refresh
        '''
        if  self.MarkovValues[10][col].nb:
            for k in range(0,10):
                    self.MarkovValues[k][col].percentage = self.MarkovValues[k][col].nb / self.MarkovValues[10][col].nb
            
    def printValues(self):
        '''
        Prints the counters of the Markov Model in a human-readable table form
        '''
        print("\t? \t1 \t2 \t3\t4 \t5 \t6 \t7 \t8 \t9")
        print("---------------------------------------------------------------------------------", end='')
        
        for i in range (0, 11):
            print("\r\n", end='')
            if i == 10 or i == 1:
                print("---------------------------------------------------------------------------------\r\n",end='')
            
            print(i, end='\t')
            for k in range (0,10):
                if not self.MarkovValues[i][k].nb:
                    print("\033[0;31;40m", end='')
                else:
                    print("\033[0;32;40m", end='')
                print(self.MarkovValues[i][k].nb, end='\t')
                print("\033[1;37;40m", end='')
        print("")

    def printPercentages(self):
        '''
        Prints the percentages of the Markov Model in a human-readable table form
        '''
        print("\t? \t1 \t2 \t3\t4 \t5 \t6 \t7 \t8 \t9")
        print("---------------------------------------------------------------------------------", end='')
    
        for i in range (1, 10):
            print("\r\n", i, end='\t')
            for k in range (0,10):
                if not self.MarkovValues[i][k].percentage:
                    print("\033[0;31;40m", end='')
                elif k != self.previousCell or self.getMostLikely() != i:
                    print("\033[0;32;40m", end='')
                else:
                    print("\033[4;30;47m", end='')
                print(str(floor(self.MarkovValues[i][k].percentage * 100)), end='%')
                print("\033[1;37;40m\t", end='')
        print("")

    def getMostLikely(self):
        '''
        Returns the ID of the most likely next location
        Convert to coordinates using the Location.fromID() function
        :return: ID of the most likely next location
        '''
        return self.getMostLikelyFromCell(self.previousCell)

    def getMostLikelyFromCell(self, currentCell):
        '''
        Returns the ID of the most likely next location with a given previous cell ID
        Typically called by getMostLikely() function
        Convert to coordinates using the Location.fromID() function
        :param currentCell: ID of the last cell
        :return: ID of the most likely next location
        '''
        max_value=0
        max_id=0
        for k in range(1,10):
            if self.MarkovValues[k][currentCell].nb > max_value:
                max_value = self.MarkovValues[k][currentCell].nb
                max_id = k
        return max_id

    def path(self, locationIDs):
        '''
        shorthand for defining multiple movements betweens cells
        :param LocationIDs: Array containing the different cell IDs in order of movement
        '''
        for loc in locationIDs:
            self.moveToCellID(loc)
    

def newCell(n1, n2, n3, n4, l1, l2):
    '''
    Shorthand for Cell creation
    :param n1: AP1 RSSI
    :param n2: AP2 RSSI
    :param n3: AP3 RSSI
    :param n4: AP4 RSSI
    :param L1: x coordinate of the fingerprinting location
    :param L2: y coordinate of the fingerprinting location
    :return: Cell with given characteristics
    '''
    return Cell(RSSVector(n1,n2,n3,n4), Location(l1,l2))

def KNeighbors(fingerprints, sample):
    '''
    Returns the 4 closest cells to the given sample and fills sample distance data
    :param fingerprints: 2D array of all the cells
    :param sample: Mobile terminal sample
    :return: the 4 nearest cells
    '''
    distances = []
    for row in fingerprints:
        for currentItem in row:
            dist = abs(currentItem.v.n1 - sample.n1) \
                 + abs(currentItem.v.n2 - sample.n2) \
                 + abs(currentItem.v.n3 - sample.n3) \
                 + abs(currentItem.v.n4 - sample.n4)
            distances.append((dist, currentItem))
    distances = sorted(distances, key=ig(0))
    sample.distances = [x[0] for x in distances][:4]
    return [x[1] for x in distances][:4]



def resolve_barycenter(nC, d):
    '''
    Returns the weighted barycenter of the 4 neighbouring cells
    :param nC: (neighborCells) Array containing the 4 closest cells
    :param d: distances of the sample of the mobile terminal
    :return: Estimated location of the mobile terminal (return None if error)
    '''
    return None if len(nC) != 4 or len(d) != 4 else  \
          1 / (1+d[0]/d[1]+d[0]/d[2]+d[0]/d[3])*nC[0].location \
        + 1 / (1+d[1]/d[0]+d[1]/d[2]+d[1]/d[3])*nC[1].location \
        + 1 / (1+d[2]/d[1]+d[2]/d[0]+d[2]/d[3])*nC[2].location \
        + 1 / (1+d[3]/d[1]+d[3]/d[2]+d[3]/d[0])*nC[3].location


def NLateration(data, step=.1, xSize=0.0, ySize=0.0, zSize=0.0):
    '''
    Returns a tuple containing (Computed Location, Total distance)
    :param data: Array of tuples containing (Location, distance) of known emitters
    :param step: Increment of grid search (lower step => better precision => slower computation)
    :param xSize: The X dimension of the cuboid containing all the emitters (automatically computed if not specified)
    :param ySize: The Y dimension of the cuboid containing all the emitters (automatically computed if not specified)
    :param zSize: The Z dimension of the cuboid containing all the emitters (automatically computed if not specified)
    :return: args 4 and 5 are the x/y dimensions of the cuboid, imageArray contains and image of the distances for graphic representation
    '''
    minLoc = Location()
    minDist = 0.0
    #gifArray = []
    for k in data:
        minDist += abs(k[0].distanceTo(Location()) - k[1])
        xSize = k[0].x if k[0].x > xSize  else xSize
        ySize = k[0].y if k[0].y > ySize  else ySize
        zSize = k[0].z if k[0].z > zSize  else zSize
    imageArray=[[] for i in range(0,floor(zSize*10))]
    for k in arange(0,xSize,step):
        for l in arange(0,ySize,step):
            for m in arange(0,zSize,step):
                d = .0
                for n in data:
                    d += abs(n[0].distanceTo(Location(k,l,m)) - n[1])
                if d < minDist:
                    minDist = d
                    minLoc = Location(round(k,2),round(l,2),round(m,2))
                imageArray[floor(l*10)].append(d*10+255-min(10+exp(d*2),255))
    return (minLoc, minDist, imageArray[0], floor(ySize/step), floor(xSize/step), imageArray)
