import numpy as np
from matplotlib import pyplot
import random


#set age of first reproduction
ageOfMaturity=4
#set some population parameters
CarryCapacity = 200 #int(raw_input("Carrying Capacity?\n"))
#define initial population size
InitialPopSize = 200 #int(raw_input("Initial Population Size?\n"))
#value to simulate role of a fluctuating environment in population dynamics
environmentalVariation=100
#Create an empty list called Population
Population=[]
#Create variable to measure number of annual offspring
NumOffspring = 0
#Create list used to track model results
Popsizes=[]
geneticDiversity=[]
Nevalues=[]
NeNratio=[]


#make a population model
class Nudibranch:
    #set initial conditions for my nudibranchs
    def __init__(self):
        #all nudes start with an age of 0
        self.age=0
        #all nudes start with 0 offspring
        self.offspring=0
        #assign sex, randomly 0 or 1
        self.sex = np.random.randint(2)
        #locus list
        self.locus = self.randomGenotype()

    #method that models reproduction by changing number of offspring they can create
    def reproduce(self):
        self.offspring=5
    #method that allows individuals ages to increase incrementally
    def growOld(self):
        self.age+=1

    def randomGenotype(self):
        randomGenotypes = np.random.randint(2, size = 2)

        randomGt = []
        randomGt.append(randomGenotypes[0])
        randomGt.append(randomGenotypes[1])

        return randomGt

    #method that takes allele from father and mother and sets to new instance of Nudibranch
    def setGenotype(self, motherAllele, fatherAllele):
        self.locus[0] = motherAllele
        self.locus[1] = fatherAllele

def freqAllele(population, alleleIdentifier):
    alleleCount = 0
    for nudibranch in population:
        # check first allele for identifier 
        if nudibranch.locus[0] == alleleIdentifier:
            alleleCount += 1
        # check second allele for identifier 
        if nudibranch.locus[1] == alleleIdentifier:
            alleleCount += 1

    return alleleCount

# need to fix
def getRandomParentAllele(population, sex):
    rightSex = False
    
    while rightSex == False:
        randomParent = random.choice(population)
        if randomParent.sex == sex:
            allele = randomParent.locus[sex]
            rightSex = True
        else:
            continue

    return allele


#Initalize and propograte my popoulation with nudes -- these are all the babies to start with.
for i in range(InitialPopSize):
    #ADD CODE FOR PART 2A
    baby = Nudibranch()

    Population.append(baby)

    #USE FUNCTION FROM PART 3 TO CALCULATE FREQUENCIES FOR ALLELES 0 AND 1

p_init = freqAllele(Population, 0)
q_init = freqAllele(Population, 1)

#Run a population model for 1000 time steps
for j in range(200):
    #create list to track figure out who live and dies, males in population and females in population
    died=[]
    males=[]
    females=[]
    #loop through population and evaluate the probability of each individual surviving.
    for i in range(len(Population)):
        #determine mortality/survival probability threshold based on age
        #using Lorenzen model of mortality: m(i)=0.4298/i^0.488 where
        #i is age
        if(Population[i].age>0):
            ProbSurv=1-(0.4298/float(Population[i].age)**0.488)
        else:
            ProbSurv=0.4
        #Use this probability threshold and randomness to see
        #whether an individual's index gets added to the death
        #list
        if(ProbSurv < np.random.random()):
            died.append(i)

    #a little programming trickery; reverse the indices to start with largest and end with smallest
    died.reverse()
    #take each index value from died and use it to remove a specific member from Population
    for i in died:
        Population.remove(Population[i])
    #variable to hold populationsize
    N=len(Population)
    #if no individuals in population, end loop
    if N==0:
        break
    #ADD CODE FOR PART 4

    #print("Total died:" + str(len(died)))

    #USE THIS VARIABLE TO HOLD CALCULATED HETEROZYGOSITY
    for nudibranch in Population:
        heterozygotes = 0
        if (nudibranch.locus[0] == 1 and nudibranch.locus[1] == 0) or (nudibranch.locus[0] == 0 and nudibranch.locus[1] == 1):
            heterozygotes += 1

    heterozygosity = heterozygotes / N

    geneticDiversity.append(heterozygosity)

    #USE FUNCTION FROM PART 3 TO CALCULATE FREQUENCIES FOR ALLELES 0 AND 1
    p_freq = freqAllele(Population, 0)
    q_freq = freqAllele(Population, 1)
    #Calculate effective population size
    var_p = (p_init*q_init)/(2*N)
    Ne=(p_freq*q_freq)/(2*var_p)

    Nevalues.append(Ne)

    NeN = Ne/N
    NeNratio.append(NeN)

    #hold onto current population allele frequencies for next loop to calculate Ne
    p_freq = p_init
    q_freq = q_init
    #ADD CODE FOR PART 5

    #use loop to age all individuals in a population
    for i in range(len(Population)):
        # each individual's age in population increased by 1
        Population[i].growOld()
        #split sexes into respective lists
        if(Population[i].sex==0):
            females.append(Population[i])
        else:
            males.append(Population[i])
    #if no males or females, reproduction can't happen so loop stops
    if (len(females)==0 or len(males)==0):
        break
    #use carrying capacity to limit reproduction; make carrying capacity
    #a normally distributed random value to model environmental variation
    #and its effects on population dynamics
    if(len(Population)<np.random.normal(CarryCapacity,environmentalVariation)):
        #use a for loop to allow each individual population to reproduce
        for i in range(len(females)):
            #make reproduction dependent on age
            if(females[i].age>=ageOfMaturity):
                females[i].reproduce()
    #use a for loop to count all the offspring in the population
    for i in range(len(females)):
        NumOffspring+=females[i].offspring
    #print("Population Size: %d; Number of Offspring: %d" % (len(Population), NumOffspring))
    Popsizes.append(len(Population))
    #add new offspring to the population
    for i in range(NumOffspring):

        #ADD/COMPLETE CODE FOR PART 2B
        #female = 
        #male =
        allele1 = getRandomParentAllele(Population, 0)
        allele2 = getRandomParentAllele(Population, 1)
        #print("Parent 1 Allele:" + str(allele1) + " Parent 2 Allele: " + str(allele2))

        # make sure to set genotype here
        baby = Nudibranch()
        baby.setGenotype(allele1, allele2)

        Population.append(baby)
    #Reset some variable
    NumOffspring=0

    for i in range(len(Population)):
        Population[i].offspring=0



#Plot results of Population dynamics
pyplot.figure(1)
pyplot.subplot(221)
pyplot.title("He")
pyplot.plot(geneticDiversity)
pyplot.grid(True)
pyplot.subplot(222)
pyplot.title("Ne/N")
pyplot.plot(NeNratio)
pyplot.grid(True)
pyplot.subplot(223)
pyplot.title("Ne")
pyplot.plot(Nevalues)
pyplot.grid(True)
pyplot.subplot(224)
pyplot.title("N")
pyplot.plot(Popsizes)
pyplot.grid(True)
pyplot.show()
