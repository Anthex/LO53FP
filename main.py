from structure import RSSVector, Location, Cell, newCell, KNeighbors, resolve_barycenter, MarkovModel, MarkovValue
import sys 

Tf = [] #cells table

testSample = RSSVector(-26, -42, -13, -46)

#cells Table initialization
for i in range (0, 3):
    Tf.append([])
    for _ in range (0,3):
        Tf[i].append([])

#known fingerprints
Tf[0][0] = newCell(-38,-27,-54,-13,2,2)
Tf[0][1] = newCell(-74,-62,-48,-33,2,6)
Tf[0][2] = newCell(-13,-28,-12,-40,2,10)
Tf[1][0] = newCell(-34,-27,-38,-41,6,2)
Tf[1][1] = newCell(-64,-48,-72,-35,6,6)
Tf[1][2] = newCell(-45,-37,-20,-15,6,10)
Tf[2][0] = newCell(-17,-50,-44,-33,10,2)
Tf[2][1] = newCell(-27,-28,-32,-45,10,6)
Tf[2][2] = newCell(-30,-20,-60,-40,10,10)

def main(args):
        #### K neighbours ####
        print("\nk neighbors of test sample : ")
        neighborsCells = KNeighbors(Tf, testSample)
        for k in neighborsCells:
                print("(", k.location.x, ";", k.location.y, ")")

        #### Distances ####
        print ("\ndistances : " + str(testSample.distances))

        #### Barycenter ####
        a = resolve_barycenter(neighborsCells, testSample.distances)
        print(a.toString())

        #### Markov ####
        MM = MarkovModel(Tf)    
        MM.path([8,7,8,7,8,7,8,5,8,2,9,8,1,9,8,9,5,4,3,2,3,2,4,5,4,5,6,6,7,6,9,5,9,3,2,4,3,5,3,4,3,3,5,6,7,6,7,6,5,4,3,4,3,4])
        
        MM.printValues()
        print("\r\nPERCENTAGES : \r\n")
        MM.printPercentages()

        print("\r\ncurrent cell is #" + str(MM.previousCell) + " , most likely next cell is #" + str(MM.getMostLikely()) + " which is located at " + str(Location.fromID(MM.getMostLikely()).toString()))
        
main(sys.argv)