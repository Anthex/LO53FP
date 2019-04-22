

## CLASSES

 1. Cell  
 2.  Location 
 3.   MarkovModel 
 4.   MarkovValue  
 5.  RSSVector

    class Cell
     |  Methods defined here:
     |
     |  __init__(self, v_, loc)
     |      :param v_: RSSI vector of the fingerprint
     |      :param loc: Location of the fingerprint
     |
     
    class Location
     |  Methods defined here:
     |
     |  __add__(self, added)
     |
     |  __init__(self, x, y, z=0)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  __isub__(self, value)
     |
     |  __itruediv__(self, divider)
     |
     |  __mul__(self, multiplier)
     |
     |  __rmul__(self, multiplier)
     |
     |  getPositionInArray(self, arraySize=3)
     |      Returns the unique ID of a fingerprint given its location
     |      :param arraySize: (Optional) dimension of the array
     |
     |  toString(self)
     |
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |
     |  fromID(id, arraySize=3)
     |      Returns the Location of a fingerprint of known ID
     |      :param: ID to resolve
     |      :param arraySize: (Optional) dimension of the array
     
    class MarkovModel
     |  Methods defined here:
     |
     |  __init__(self, cells)
     |      :param cells: an array containing all the cells of the model
     |
     |  getMostLikely(self)
     |      Returns the ID of the most likely next location
     |      Convert to coordinates using the Location.fromID() function
     |      :return: ID of the most likely next location
     |
     |  getMostLikelyFromCell(self, currentCell)
     |      Returns the ID of the most likely next location with a given previous cell ID
     |      Typically called by getMostLikely() function
     |      Convert to coordinates using the Location.fromID() function
     |      :param currentCell: ID of the last cell
     |      :return: ID of the most likely next location
     |
     |  moveToCell(self, nextCell)
     |      Registers a movement from the current cell to another based on the Location of its fingerprint
     |      :param nextCell: The location of the new cell
     |
     |  moveToCellID(self, nextCell)
     |      Registers a movement from the current cell to a specified location by its ID
     |      :param nextCell: The ID of the new location
     |
     |  path(self, locationIDs)
     |      shorthand for defining multiple movements betweens cells
     |      :param LocationIDs: Array containing the different cell IDs in order of movement
     |
     |  printPercentages(self)
     |      Prints the percentages of the Markov Model in a human-readable table form
     |
     |  printValues(self)
     |      Prints the counters of the Markov Model in a human-readable table form
     |
     |  refreshPercentage(self, col)
     |      Refreshes the probabilities of a column after a counter is changed
     |      Needed after every change to the nb field
     |      :param col: the # of the column to refresh

    class MarkovValue
     |  Methods defined here:
     |
     |  __init__(self, nb=0, percentage=0.0)
     |      :param nb: Counter of incoming/outgoing movements
     |      :param percentage: probability of being the next movement [0.0 , 1.0]

    class RSSVector
     |  Methods defined here:
     |
     |  __init__(self, n1, n2, n3, n4)
     |      :param n1: AP1 RSSI
     |      :param n2: AP2 RSSI
     |      :param n3: AP3 RSSI
     |      :param n4: AP4 RSSI
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  distances = []

## FUNCTIONS

    KNeighbors(fingerprints, sample)
        Returns the 4 closest cells to the given sample and fills sample distance data
        :param fingerprints: 2D array of all the cells
        :param sample: Mobile terminal sample
        :return: the 4 nearest cells

    newCell(n1, n2, n3, n4, l1, l2)
        Shorthand for Cell creation
        :param n1: AP1 RSSI
        :param n2: AP2 RSSI
        :param n3: AP3 RSSI
        :param n4: AP4 RSSI
        :param L1: x coordinate of the fingerprinting location
        :param L2: y coordinate of the fingerprinting location
        :return: Cell with given characteristics

    resolve_barycenter(nC, d)
        Returns the weighted barycenter of the 4 neighbouring cells
        :param nC: (neighborCells) Array containing the 4 closest cells
        :param d: distances of the sample of the mobile terminal
        :return: Estimated location of the mobile terminal (return None if error)
