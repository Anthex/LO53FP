
from structure import *
import sys 

Tf = [] #cells table
testSample = RSSVector(-26, -42, -13, -46)


#cells Table initialization
for i in range (0, 3):
    Tf.append([])
    for k in range (0,3):
        Tf[i].append([])

Tf[0][0] = Cell(RSSVector(-38,-27,-54,-13), Location(2,2))
Tf[0][1] = Cell(RSSVector(-74,-62,-48,-33), Location(2,6))
Tf[0][2] = Cell(RSSVector(-13,-28,-12,-40), Location(2,10))
Tf[1][0] = Cell(RSSVector(-34,-27,-38,-41), Location(6,2))
Tf[1][1] = Cell(RSSVector(-64,-48,-72,-35), Location(6,6))
Tf[1][2] = Cell(RSSVector(-45,-37,-20,-15), Location(6,10))
Tf[2][0] = Cell(RSSVector(-17,-50,-44,-33), Location(10,2))
Tf[2][1] = Cell(RSSVector(-27,-28,-32,-45), Location(10,6))
Tf[2][2] = Cell(RSSVector(-30,-20,-60,-40), Location(10,10))

def main(args):

        print(Tf[1][1].v.n2)


        print("\nk neighbors of test sample : ")
        neighborsCells = KNeighbors(Tf, testSample)
        for k in neighborsCells:
                print("(", k.location.x, ";", k.location.y, ")")

        print ("\ndistances : " + str(testSample.distances))

        testLoc = Location(3,4,5)
        loc2 = Location(1,2,3)
        print((testLoc+loc2).toString())

        a = resolve_barycenter(neighborsCells, testSample)
        print(a.toString)
        return 0;


main(sys.argv)