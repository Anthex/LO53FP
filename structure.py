from operator import itemgetter as ig
from math import floor

class RSSVector():
    distances = []
    def __init__(self, n1, n2, n3, n4):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4

class Location():
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

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

    def getPositionInArray(self, arraySize=3):
        temp = Location(self.x, self.y)
        temp /= 2
        temp -= Location(1,1)
        return floor((temp.x * arraySize + temp.y)/2)

    @staticmethod
    def fromID(id, arraySize=3):
        id -= 1
        y=id % 3
        x=floor((id - y) / 3)
        returnValue = Location(x, y)
        returnValue *= 2
        returnValue += Location(1,1)
        returnValue *= 2
        return returnValue

class Cell():
    def __init__(self, v_, loc):
        self.v = v_
        self.location = loc

class MarkovValue():
    def __init__(self, nb=0, percentage=0.0):
        self.nb = nb
        self.percentage = percentage # Probability of Markov model (100% <=> 1.0)

class MarkovModel():
    def __init__(self,cells):
        self.MarkovValues = [] #table of the coefficients of the Markov Model
        self.cells = cells
        self.previousCell = 0
        for i in range (0, 11):
            self.MarkovValues.append([])
            for _ in range (0, 10):
                self.MarkovValues[i].append(MarkovValue())
        self.MarkovValues[10][0].nb = 1 #initial position sigma increment  

    def moveToCellID(self, nextCell):
        self.MarkovValues[nextCell][self.previousCell].nb += 1     
        self.MarkovValues[10][nextCell].nb += 1
        self.refreshPercentage(self.previousCell)
        self.previousCell = nextCell
        
    def moveToCell(self, nextCell):
        self.moveToCellID(nextCell.location.getPositionInArray()+1)

    def refreshPercentage(self, col):
        if  self.MarkovValues[10][col].nb:
            for k in range(0,10):
                    self.MarkovValues[k][col].percentage = self.MarkovValues[k][col].nb / self.MarkovValues[10][col].nb
            
    def printValues(self):
        print("\t? \t1 \t2 \t3\t4 \t5 \t6 \t7 \t8 \t9")
        print("---------------------------------------------------------------------------------", end='')
        
        for i in range (0, 11):
            print("\r\n", end='')
            if i == 10 or i == 1:
                print("---------------------------------------------------------------------------------\r\n",end='')
            
            print(i, end='\t')
            for k in range (0,10):
                print(self.MarkovValues[i][k].nb, end='\t')
        print("")

    def printPercentages(self):
        print("\t? \t1 \t2 \t3\t4 \t5 \t6 \t7 \t8 \t9")
        print("---------------------------------------------------------------------------------", end='')
    
        for i in range (1, 10):
            print("\r\n", end='')
            
            print(i, end='\t')
            for k in range (0,10):
                if not self.MarkovValues[i][k].percentage:
                    print("\033[0;31;40m", end='')
                else:
                    print("\033[1;36;40m", end='')
                print(str(floor(self.MarkovValues[i][k].percentage * 100)), end='%\t')
                print("\033[1;37;40m", end='')
        print("")

    def getMostLikely(self):
        return self.getMostLikelyFromCell(self.previousCell)

    def getMostLikelyFromCell(self, currentCell):
        max=0
        max_id=0
        for k in range(1,10):
            if self.MarkovValues[k][currentCell].nb > max:
                max = self.MarkovValues[k][currentCell].nb
                max_id = k
        return max_id 

    def path(self, locationIDs):
        for loc in locationIDs:
            self.moveToCellID(loc)
    

def newCell(n1, n2, n3, n4, l1, l2):
    return Cell(RSSVector(n1,n2,n3,n4), Location(l1,l2))
    
def KNeighbors(fingerprints, sample):  
    '''
    Returns the 4 closest cells to the given sample and fills sample distance data
    :param Cell[3][3] fingerprints: 2D array of all the cells
    :param RSSVector sample: Mobile terminal sample
    :return Cell[4]: the 4 nearest cells
    '''
    distances, neighbours = [], []
    for row in fingerprints:
        for currentItem in row:
            dist = abs(currentItem.v.n1 - sample.n1) \
                 + abs(currentItem.v.n2 - sample.n2) \
                 + abs(currentItem.v.n3 - sample.n3) \
                 + abs(currentItem.v.n4 - sample.n4) 
            distances.append((dist, currentItem))
    distances = sorted(distances, key=ig(0))
    for k in range (0,4):
        neighbours.append(distances[k][1])
        sample.distances.append(distances[k][0])
    return neighbours



def resolve_barycenter(nC, d):
    '''
    Returns the weighted barycenter of the 4 neighbouring cells
    :param Cell[4] nC: (neighborCells) Array containing the 4 closest cells
    :param distance[4] d: distances of the sample of the mobile terminal
    :return Location: Estimated location of the mobile terminal (return None if error)
    '''
    return None if len(nC) != 4 or len(d) != 4 else  \
          1 / (1+d[0]/d[1]+d[0]/d[2]+d[0]/d[3])*nC[0].location \
        + 1 / (1+d[1]/d[0]+d[1]/d[2]+d[1]/d[3])*nC[1].location \
        + 1 / (1+d[2]/d[1]+d[2]/d[0]+d[2]/d[3])*nC[2].location \
        + 1 / (1+d[3]/d[1]+d[3]/d[2]+d[3]/d[0])*nC[3].location 
     