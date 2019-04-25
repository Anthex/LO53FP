from structure import RSSVector, Location, Cell, newCell, KNeighbors, resolve_barycenter, MarkovModel
from random import random
from math import floor

Tf = [] #cells table

testSample = RSSVector(-26, -42, -13, -46)

#known fingerprints
Tf = [[newCell(-38,-27,-54,-13,2,2),newCell(-74,-62,-48,-33,2,6),newCell(-13,-28,-12,-40,2,10) ],\
      [newCell(-34,-27,-38,-41,6,2), newCell(-64,-48,-72,-35,6,6), newCell(-45,-37,-20,-15,6,10)], \
      [newCell(-17,-50,-44,-33,10,2), newCell(-27,-28,-32,-45,10,6), newCell(-30,-20,-60,-40,10,10)]]

def main():
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

        # small set fixed definition
        MM.path([8,7,8,7,8,7,8,5,8,2,9,8,1,9,8,9,5,4,3,2,3,2,4,5,4,5,6,6,7,6,9,5,9,3,2,4,3,5,3,4,3,3,5,6,7,6,7,6,5,4,3,4,3,4])

        # larger set random generation
        for k in range(0,100):
                MM.moveToCellID(floor(random()*9+1))

        print("\r\n")
        MM.printValues()
        print("\r\nPERCENTAGES : \r\n")
        MM.printPercentages()

        print("\r\ncurrent cell is \033[1;32;40m#" + str(MM.previousCell) + "\033[1;37;40m , most likely next cell is \033[1;32;40m#" + str(MM.getMostLikely()) + "\033[1;37;40m which is located at \033[1;32;40m" + str(Location.fromID(MM.getMostLikely()).toString()) + "\033[1;37;40m")
        
        while(1):
                print("Input next location ID (between 1 and 9)\r\n>>", end='')
                in_char = int(input())
                print(chr(27)+'[2j')
                print('\033c')
                print('\x1bc')
                if in_char > 0 and in_char < 10:
                        MM.moveToCellID(in_char)
                        MM.printValues()
                        print("\r\nPERCENTAGES : \r\n")
                        MM.printPercentages()
                        print("\r\ncurrent cell is \033[0;32;40m#" + str(MM.previousCell) + "\033[1;37;40m , most likely next cell is \033[1;32;40m#" + str(MM.getMostLikely()) + "\033[1;37;40m which is located at \033[1;32;40m" + str(Location.fromID(MM.getMostLikely()).toString()) + "\033[1;37;40m")
                else:
                        print("invalid ID")
                        break

if __name__ == '__main__':
        main()
