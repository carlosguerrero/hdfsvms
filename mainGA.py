    #!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 08:04:42 2017

@author: carlos
"""

import matplotlib
matplotlib.use('Agg')
import GA as ga
import random as random
import SYSTEMMODEL as systemmodel
import numpy as np
import pickle
from datetime import datetime
import os
import matplotlib.pyplot as plt 
import math as math
import pickle
import os
import copy




executionId= datetime.now().strftime('%Y%m%d%H%M%S')
file_path = "./"+executionId


if not os.path.exists(file_path):
    os.makedirs(file_path)

#res = results.RESULTS()


vmScaleLevel = [2.0]
pmScaleLevel = [100]
fileNumberScaleLevel = [50]


#vmScaleLevel = [0.5,1.0,2.0,4.0]
#pmScaleLevel = [50,100,200,500]
#fileNumberScaleLevel = [25,50,100,200]

experimentList = []
# 0 - BOTH or VM or BLOCK
# 1 - NSGA2 or AIA
# 2 - lowScale, midScale or highScale
# 3 - mutation probability 0-1.0
# 4 - population size
# 5 - seed for random values for generation of the initial population
# 6 - seed for random values for evolution of populations
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100,400,500])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'midScale', 0.25,100])
#experimentList.append(['BOTH','NSGA2', 'highScale', 0.25,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100,400,500])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'midScale', 0.25,100])
#experimentList.append(['VM','NSGA2', 'highScale', 0.25,100])
experimentList.append(['BLOCK','NSGA2', 'lowScale', 0.4,100,400,500])
#experimentList.append(['BLOCK','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BLOCK','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BLOCK','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BLOCK','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BLOCK','NSGA2', 'midScale', 0.25,100])
#experimentList.append(['BLOCK','NSGA2', 'highScale', 0.25,100])
experimentList.append(['BOTH','AIA', 'lowScale', 0.95,100,400,500])
#experimentList.append(['BOTH','AIA', 'lowScale', 0.95,100])
#experimentList.append(['BOTH','AIA', 'lowScale', 0.95,100])
#experimentList.append(['BOTH','AIA', 'lowScale', 0.95,100])
#experimentList.append(['BOTH','AIA', 'lowScale', 0.95,100])
#experimentList.append(['BLOCK','AIA', 'midScale', 0.95,100])
#experimentList.append(['BLOCK','AIA', 'highScale', 0.95,100])


#TODO
########

## PENSAR SI SERIA NECESARIO TENER EN CUENTA LOS CROSSOVER UNICAMENTE SOBRE MULTIPLOS DE REPLICATION FACTOR

## pensar si hay que mejorar el selectsolution para evitar picos comparando con la solucion anterior

########



numberofGenerations = 5

csvoutputSPA = open(file_path+'/agregatedResultsSPA.csv', 'w')
csvoutputUK = open(file_path+'/agregatedResultsUK.csv', 'w')

for vmSL in vmScaleLevel:
    for pmSL in pmScaleLevel:
        for fnSL in fileNumberScaleLevel:
            

            for i,v in enumerate(experimentList):
                
                
                
                experimentName = str(v[:3])+"-vm"+str(vmSL)+"-pm"+str(pmSL)+"-fs"+str(fnSL)
                experimentName = experimentName.replace(",","-").replace(".","p").replace(" ","").replace("'","").replace("[","").replace("]","")
                experimentName = str(i)+"-"+experimentName
                print("*********************************") 
                print "*" + experimentName + " :::: "+ str(datetime.now())
                print("*********************************")
                system = systemmodel.SYSTEMMODEL()
            
            
                if v[2]=='lowScale': system.lowScale(v[5],vmSL,pmSL,fnSL)
                
                g = ga.GA(system,v[5],v[6])
                g.experimentScenario = v[0] # BOTH VM or BLOCK
                g.optimizationAlgorithm = v[1]
                g.mutationProbability = v[3]
                g.populationSize = v[4]
                
                g.generatePopulation(g.populationPt)
                
                print "*** INITIAL POPULATION GENERATED ***"
                
                time=datetime.now()
                selectedSolution = []

                
                energy_weight= 1.0/3.0
                resourcewaste_weight= 1.0/3.0
                unavailability_weight= 1.0/3.0
                
                indexSelectedSolution = g.selectSolution(g.populationPt,energy_weight,resourcewaste_weight,unavailability_weight)   
                selectedSolution.append({"population": copy.deepcopy(g.populationPt.population[indexSelectedSolution]) ,"fitness": copy.deepcopy(g.populationPt.fitness[indexSelectedSolution]) ,"fitnessNormalized": copy.deepcopy(g.populationPt.fitnessNormalized[indexSelectedSolution]) ,"pmsUsages": copy.deepcopy(g.populationPt.pmsUsages[indexSelectedSolution]) ,"vmsUsages":  copy.deepcopy(g.populationPt.vmsUsages[indexSelectedSolution])  })
                
                
                for i in range(0,numberofGenerations):
                    if g.optimizationAlgorithm == 'NSGA2':
                        g.evolveNSGA2()
                    if g.optimizationAlgorithm == 'AIA':
                        g.evolveAIA()
                    indexSelectedSolution = g.selectSolution(g.populationPt,energy_weight,resourcewaste_weight,unavailability_weight)   
                    selectedSolution.append({"population": copy.deepcopy(g.populationPt.population[indexSelectedSolution]) ,"fitness": copy.deepcopy(g.populationPt.fitness[indexSelectedSolution]) ,"fitnessNormalized": copy.deepcopy(g.populationPt.fitnessNormalized[indexSelectedSolution]) ,"pmsUsages": copy.deepcopy(g.populationPt.pmsUsages[indexSelectedSolution]) ,"vmsUsages":  copy.deepcopy(g.populationPt.vmsUsages[indexSelectedSolution])  })
                    timeold = time
                    time=datetime.now()
                    print "[Generation number "+str(i)+"] "+ str(time-timeold)
                    
                    
                resultValues = str(i)+";"+str(v[0])+";"+str(v[1])+";"+str(v[2])+";"+str(vmSL)+";"+str(pmSL)+";"+str(fnSL)+";"+str(selectedSolution[-1]['fitness']['energy'])+";"+str(selectedSolution[-1]['fitness']['resourcewaste'])+";"+str(selectedSolution[-1]['fitness']['unavailability'])+";"+str(selectedSolution[-1]['fitnessNormalized']['energy'])+";"+str(selectedSolution[-1]['fitnessNormalized']['resourcewaste'])+";"+str(selectedSolution[-1]['fitnessNormalized']['unavailability'])
                csvoutputUK.write(resultValues+'\n')
                csvoutputUK.flush()
                csvoutputSPA.write(resultValues.replace(".",",")+'\n')
                csvoutputSPA.flush()                
                
                
            
                output = open(file_path+'/'+experimentName+'-lastGeneration.pkl', 'wb')
                pickle.dump(g.populationPt, output)
                output.close()
                
                output = open(file_path+'/'+experimentName+'-selectedSolution.pkl', 'wb')
                pickle.dump(selectedSolution, output)
                output.close()    
            
csvoutputUK.close()
csvoutputSPA.close()


#g.removeEmptyVms(g.populationPt.population[1])

#off = []
#print g.populationPt.population[0]
#print g.populationPt.population[1]
#
#g.crossover(g.populationPt.population[0],g.populationPt.population[1],off)

#tmp1 = off[1]
#tmp0 = off[0]
#off = []
#
#print tmp0
#print tmp1
#
#g.crossover(tmp0,tmp1,off)
#print off

