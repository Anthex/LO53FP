from structure import *

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