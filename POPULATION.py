#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:56:02 2017

@author: carlos
"""
import copy

class POPULATION:
    
    def populationUnion(self,a,b):
        
        r=POPULATION(1)
        
        r.population = copy.deepcopy(a.population) + copy.deepcopy(b.population)
        r.vmsUsages = copy.deepcopy(a.vmsUsages) + copy.deepcopy(b.vmsUsages)
        r.pmsUsages = copy.deepcopy(a.pmsUsages) + copy.deepcopy(b.pmsUsages)
        r.fitness = copy.deepcopy(a.fitness) + copy.deepcopy(b.fitness)
        r.fitnessNormalized = copy.deepcopy(a.fitnessNormalized) + copy.deepcopy(b.fitnessNormalized)
        for i,v in enumerate(r.fitness):
            r.fitness[i]["index"]=i
        r.dominatesTo = copy.deepcopy(a.dominatesTo) + copy.deepcopy(b.dominatesTo)
        r.dominatedBy = copy.deepcopy(a.dominatedBy) + copy.deepcopy(b.dominatedBy)
        r.fronts = copy.deepcopy(a.fronts) + copy.deepcopy(b.fronts)
        r.crowdingDistances = copy.deepcopy(a.crowdingDistances) + copy.deepcopy(b.crowdingDistances)
        
        return r
        
    def paretoExport(self):
        
        paretoPop = self.__class__(len(self.population))
        
        paretoPop.fronts[0] = copy.deepcopy(self.fronts[0])
        
        
        for i in paretoPop.fronts[0]:
            paretoPop.population[i] = copy.deepcopy(self.population[i])
            paretoPop.fitness[i] = copy.deepcopy(self.fitness[i])
            paretoPop.fitnessNormalized[i] = copy.deepcopy(self.fitnessNormalized[i])
            paretoPop.vmsUsages[i] = copy.deepcopy(self.vmsUsages[i])
            paretoPop.pmsUsages[i] = copy.deepcopy(self.pmsUsages[i])
            
        return paretoPop
        
    


    def __init__(self,size):
        
        self.population = [{}]*size
        self.fitness = [{}]*size
        self.fitnessNormalized = [{}]*size
        self.dominatesTo = [set()]*size
        self.dominatedBy = [set()]*size
        self.fronts = [set()]*size
        self.crowdingDistances = [float(0)]*size
        self.vmsUsages = [list()]*size
        self.pmsUsages = [list()]*size
    
   
