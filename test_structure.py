from structure import KNeighbors, resolve_barycenter, Location, newCell, MarkovModel, RSSVector, NLateration
from io import StringIO
import sys

testEmitters = [(Location(.5,.5,.5), 3.0), (Location(4.0,.0,.0), 2.0), (Location(4.0,5.0,5.0), 4.2), (Location(3.0,3.0,3.0), 2.5)]

Tf = [[newCell(-38,-27,-54,-13,2,2),newCell(-74,-62,-48,-33,2,6),newCell(-13,-28,-12,-40,2,10) ],\
      [newCell(-34,-27,-38,-41,6,2), newCell(-64,-48,-72,-35,6,6), newCell(-45,-37,-20,-15,6,10)], \
      [newCell(-17,-50,-44,-33,10,2), newCell(-27,-28,-32,-45,10,6), newCell(-30,-20,-60,-40,10,10)]]

testSample = RSSVector(-26, -42, -13, -46)
testCells = [Tf[0][2], Tf[2][1], Tf[1][0], Tf[2][0]]
testDistances = [34, 35, 53, 61]



def test_KNeighbors():
    assert KNeighbors(Tf, testSample)[0].location.toString() == "(2 ; 10 ; 0)"
    assert KNeighbors(Tf, testSample)[1].location.toString() == "(10 ; 6 ; 0)"
    assert KNeighbors(Tf, testSample)[2].location.toString() == "(6 ; 2 ; 0)"
    assert KNeighbors(Tf, testSample)[3].location.toString() == "(10 ; 2 ; 0)"

def test_resolve_barycenter():

    result = resolve_barycenter(testCells, testDistances)
    print(testSample.distances)
    assert round(result.x, 2) == 6.67
    assert round(result.y, 2) == 5.75

def test_Location():
    loc1 = Location(1,2)
    loc2 = Location(3, 4)
    assert loc1 + loc2 == Location(4,6)
    assert loc1 * 2 == Location(2,4)
    loc2 -= Location(1,1)
    assert loc2 == Location(2,3)
    loc1 *= 3
    assert loc1 == Location(3,6)

def test_MarkovModel():
    test_MM = MarkovModel(Tf)
    assert test_MM.previousCell == 0
    test_MM.moveToCellID(3)
    assert test_MM.previousCell == 3
    test_MM.moveToCell(Tf[0][1])
    assert test_MM.previousCell  == 2

def test_newCell():
      testCell = newCell(-38,-27,-54,-13,2,2)
      assert testCell.location == Location(2,2)
      assert testCell.v == RSSVector(-38,-27,-54,-13)

def test_Path():
      test_MM = MarkovModel(Tf)
      assert test_MM.previousCell == 0
      test_MM.path([1,2,3,4])
      assert test_MM.previousCell == 4
      test_MM.path([8,4,4])
      assert test_MM.previousCell == 4

def test_getPositionInArray():
      test_loc = Location(2,2)
      assert test_loc.getPositionInArray() == 0
      test_loc = Location(2,6)
      assert test_loc.getPositionInArray() == 1
      test_loc = Location(10,10)
      assert test_loc.getPositionInArray() == 8
      
def test_fromID():
      test_loc = Location.fromID(3)
      assert test_loc == Location(2,10)
      test_loc = Location.fromID(9)
      assert test_loc == Location(10,10)

def test_getModeLikely():
      test_MM = MarkovModel(Tf)
      test_MM.path([1,2,3,4,3,4,3,5,4,5,6,4,3])
      assert test_MM.getMostLikely() == 4
      test_MM.path([5,6,7,6,7,6,7,5,6])
      assert test_MM.getMostLikely() == 7
      test_MM.path([4,4,4,4,4,4,4])
      assert test_MM.getMostLikely() == 4

def test_printValues():
      test_MM = MarkovModel(Tf)
      test_MM.path([1,2,3,2,3,4,3,4])

      with OutputBuffer() as output:
            test_MM.printValues()
      assert len(output.out) > 2500
      print(len(output.out))

def test_printPercentage():
      test_MM = MarkovModel(Tf)
      test_MM.path([1,2,3,2,3,4,3,4])

      with OutputBuffer() as output:
            test_MM.printPercentages()
      assert len(output.out) > 2000
      print(len(output.out))

def test_NLateration():
      test_result = NLateration(testEmitters)
      assert test_result[0] == Location(3.3, 1.5, 1.1)
      assert round(test_result[1],2) == 1.19
class OutputBuffer(object):

    def __init__(self):
        self.stdout = StringIO()
        self.stderr = StringIO()

    def __enter__(self):
        self.original_stdout, self.original_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self.stdout, self.stderr
        return self

    def __exit__(self, exception_type, exception, traceback):
        sys.stdout, sys.stderr = self.original_stdout, self.original_stderr

    @property
    def out(self):
        return self.stdout.getvalue()
