from operator import itemgetter as ig

class RSSVector():
    distances = []
    def __init__(self, n1, n2, n3, n4):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4

class Location():
    def __init(self):
        self.x = self.y = self.z = 0

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

    def toString(self):
        return "(" + str(self.x) + " ; " + str(self.y) + " ; " + str(self.z) + ")"


class Cell():
    def __init__(self, v_, loc):
        self.v = v_
        self.location = loc
        self.Likeliness = .0 # Probability of Markov model
        self.pastCount = 1

def KNeighbors(fingerprints, sample):  
    '''
    Returns the 4 closest cells to the given sample and fills sample distance data
    :param Cell[3][3] fingerprints: 2D array of all the cells
    :param RSSIVector sample: Mobile terminal sample
    :return Cell[4]: the 4 nearest cells
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
    neighbours = []
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
    return None if len(nC) != 4  else  \
          1 / (1+d[0]/d[1]+d[0]/d[2]+d[0]/d[3])*nC[0].location \
        + 1 / (1+d[1]/d[0]+d[1]/d[2]+d[1]/d[3])*nC[1].location \
        + 1 / (1+d[2]/d[1]+d[2]/d[0]+d[2]/d[3])*nC[2].location \
        + 1 / (1+d[3]/d[1]+d[3]/d[2]+d[3]/d[0])*nC[3].location 
     