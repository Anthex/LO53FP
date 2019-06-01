from structure import output, printf, RSSVector, Location, newCell, KNeighbors, resolve_barycenter, MarkovModel, NLateration
from random import random
from math import floor


Tf = [] #cells table

#dataset : list of tuples representing emitters (Location, distance)
dataset = [(Location(.5,.5,.5), 3.0), (Location(4.0,.0,.0), 2.0), (Location(4.0,5.0,5.0), 4.2), (Location(3.0,3.0,3.0), 2.5)]

testSample = RSSVector(-26, -42, -13, -46)

#known fingerprints
Tf = [[newCell(-38,-27,-54,-13,2,2),newCell(-74,-62,-48,-33,2,6),newCell(-13,-28,-12,-40,2,10) ],\
      [newCell(-34,-27,-38,-41,6,2), newCell(-64,-48,-72,-35,6,6), newCell(-45,-37,-20,-15,6,10)], \
      [newCell(-17,-50,-44,-33,10,2), newCell(-27,-28,-32,-45,10,6), newCell(-30,-20,-60,-40,10,10)]]


def main():
        #### N-Lateration ####
        NLat_result = NLateration(dataset, step=1)
        printf("\r\nN-Lateration :\nComputed location : " + NLat_result[0].toString())
        printf("With distance = " + str(round(NLat_result[1], 2)) + " m")

        #### K neighbours ####
        printf("\nK-neighbors of test sample : ")
        neighborsCells = KNeighbors(Tf, testSample)
        for k in neighborsCells:
                printf("(", k.location.x, ";", k.location.y, ")")

        #### Distances ####
        print ("\nDistances : " + str(testSample.distances))

        #### Barycenter ####
        printf("\r\nWeighted barycenter :")
        a = resolve_barycenter(neighborsCells, testSample.distances)
        printf(a.toString())

        #### Markov ####
        MM = MarkovModel(Tf)

        # small set fixed definition
        MM.path([8,7,8,7,8,7,8,5,8,2,9,8,1,9,8,9,5,4,3,2,3,2,4,5,4,5,6,6,7,6,9,5,9,3,2,4,3,5,3,4,3,3,5,6,7,6,7,6,5,4,3,4,3,4])

        # larger set random generation
        for k in range(0,100):
                MM.moveToCellID(floor(random()*9+1))

        printf("\r\n")
        MM.printValues()
        printf("\r\nPERCENTAGES : \r\n")
        MM.printPercentages()

        printf("\r\ncurrent cell is {output.GREEN}" + str(MM.previousCell) + "{output.NORMAL} , most likely next cell is {output.GREEN}" + str(MM.getMostLikely()) + "{output.NORMAL} which is located at {output.GREEN}" + str(Location.fromID(MM.getMostLikely()).toString()) + "{output.NORMAL}")

        while(1):
                printf("Input next location ID (between 1 and 9)\r\n>>", end='')
                in_char = int(input())
                printf(output.CLEAR)
                if in_char > 0 and in_char < 10:
                        MM.moveToCellID(in_char)
                        MM.printValues()
                        printf("\r\nPERCENTAGES : \r\n")
                        MM.printPercentages()
                        printf("\r\ncurrent cell is {output.GREEN}#" + str(MM.previousCell) + "{output.NORMAL} , most likely next cell is {output.GREEN}" + str(MM.getMostLikely()) + "{output.NORMAL} which is located at {output.GREEN}" + str(Location.fromID(MM.getMostLikely()).toString()) + "{output.NORMAL}")
                else:
                        printf("invalid ID")
                        break

if __name__ == '__main__':
        main()
