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
import RESULTS as results
import pickle
import os
import copy




executionId= datetime.now().strftime('%Y%m%d%H%M%S')
file_path = "./"+executionId


if not os.path.exists(file_path):
    os.makedirs(file_path)

#res = results.RESULTS()

experimentList = []
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['BOTH','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['BOTH','NSGA2', 'midScale', 0.25,100])
#experimentList.append(['BOTH','NSGA2', 'highScale', 0.25,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
experimentList.append(['VM','NSGA2', 'lowScale', 0.4,100])
#experimentList.append(['VM','NSGA2', 'midScale', 0.25,100])
#experimentList.append(['VM','NSGA2', 'highScale', 0.25,100])
#experimentList.append(['BLOCK','NSGA2', 'lowScale', 0.25,100])
#experimentList.append(['BLOCK','NSGA2', 'midScale', 0.25,100])
#experimentList.append(['BLOCK','NSGA2', 'highScale', 0.25,100])
#experimentList.append(['BLOCK','AIA', 'lowScale', 0.95,100])
#experimentList.append(['BLOCK','AIA', 'midScale', 0.95,100])
#experimentList.append(['BLOCK','AIA', 'highScale', 0.95,100])



numberofGenerations = 400

for i,v in enumerate(experimentList):
    
    experimentName = str(v[:3]).replace(",","-").replace(" ","").replace("'","").replace("[","").replace("]","")
    experimentName = str(i)+"-"+experimentName
    print("*********************************") 
    print "*" + experimentName + " :::: "+ str(datetime.now())
    print("*********************************")
    system = systemmodel.SYSTEMMODEL()
    if v[2]=='lowScale': system.lowScale()
    
    g = ga.GA(system)
    g.experimentScenario = v[0] # BOTH VM or BLOCK
    g.optimizationAlgorithm = v[1]
    g.mutationProbability = v[3]
    g.populationSize = v[4]
    
    g.generatePopulation(g.populationPt)
    
    print "*** INITIAL POPULATION GENERATED ***"
    
    time=datetime.now()
    selectedSolution = []
    
    
    
    indexSelectedSolution = g.selectSolution(g.populationPt)   
    selectedSolution.append({"population": copy.deepcopy(g.populationPt.population[indexSelectedSolution]) ,"fitness": copy.deepcopy(g.populationPt.fitness[indexSelectedSolution]) ,"pmsUsages": copy.deepcopy(g.populationPt.pmsUsages[indexSelectedSolution]) ,"vmsUsages":  copy.deepcopy(g.populationPt.vmsUsages[indexSelectedSolution])  })
    
    
    for i in range(0,numberofGenerations):
        if g.optimizationAlgorithm == 'NSGA2':
            g.evolveNSGA2()
        if g.optimizationAlgorithm == 'AIA':
            g.evolveAIA()
        indexSelectedSolution = g.selectSolution(g.populationPt)   
        selectedSolution.append({"population": copy.deepcopy(g.populationPt.population[indexSelectedSolution]) ,"fitness": copy.deepcopy(g.populationPt.fitness[indexSelectedSolution]) ,"pmsUsages": copy.deepcopy(g.populationPt.pmsUsages[indexSelectedSolution]) ,"vmsUsages":  copy.deepcopy(g.populationPt.vmsUsages[indexSelectedSolution])  })
        timeold = time
        time=datetime.now()
        print "[Generation number "+str(i)+"] "+ str(time-timeold)

    output = open(file_path+'/'+experimentName+'-lastGeneration.pkl', 'wb')
    pickle.dump(g.populationPt, output)
    output.close()
    
    output = open(file_path+'/'+experimentName+'-selectedSolution.pkl', 'wb')
    pickle.dump(selectedSolution, output)
    output.close()    




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

