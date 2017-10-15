#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:56:02 2017

@author: carlos
"""
import copy
import random as random
import math as math

class SYSTEMMODEL:
    
    def __init__(self):
        
        
        self.vmNumber = 0 #numero inicial/medio/fijo de virtual machines
        self.pmNumber = 0 #numero inicial/medio/fijo de pyshical machines
        self.blockNumber = 0 #numero inicial/medio/fijo de bloques
        self.replicationFactor = 0 #numero de replicas de cada bloque
        
        self.replicaNumber=0
        
        self.blockSize = 0
        
        self.resourceCPUUsageMultiplier = 0.0
        self.resourceIOUsageMultiplier = 0.0
        self.resourceNETUsageMultiplier = 0.0
        
    def lowScale(self):
        self.vmNumber=500 #initial number of vms in the system
        self.pmNumber=100
        
        self.replicationFactor=3
        
        self.epsilomResourceWaste = 0.15
        
        
        self.replicaNumber=self.blockNumber * self.replicationFactor
        
        
        fileSizes = [1600, 1623, 1646, 1671, 1696, 1723, 1750, 1779, 1809, 1839, 1872, 1905, 1941, 1977, 2016, 2056, 2099, 2143, 2190, 2239, 2292, 2347, 2406, 2468, 2535, 2606, 2681, 2763, 2851, 2946, 3049, 3161, 3283, 3418, 3567, 3733, 3918, 4128, 4367, 4643, 4965, 5347, 5810, 6382, 7113, 8087, 9462, 11586, 15412, 25101]
        fileAccess =[125 ,77 ,57 ,47 ,40 ,35 ,31 ,29 ,26 ,24 ,23 ,21 ,20 ,19 ,18 ,17 ,17 ,16 ,15 ,15, 14 ,14 ,13 ,13 ,13 ,12 ,12 ,12 ,11 ,11, 11 ,10 ,10 ,10 ,10 ,10 ,9 ,9 ,9 ,9, 9 ,9 ,8 ,8 ,8 ,8 ,8 ,8 ,8 ,7]        

        #transformamos los accesos a %
        
        totalAccess = float(sum(fileAccess))
        for i in range(len(fileAccess)):
            fileAccess[i] = float(fileAccess[i])/totalAccess
            
        #siempre ha de ser menor que los recursos de cpu disponibles
        self.resourceCPUUsageMultiplier = 0.1
        self.resourceIOUsageMultiplier =0.064
        self.resourceNETUsageMultiplier = 0.064

        

        self.blockSize = 64        
        #transformamos el tamaño de los ficheros a bloques
        for i in range(len(fileSizes)):
            fileSizes[i]=fileSizes[i]/self.blockSize
        
        
        
        self.blockLoad = [] 
        for i,v in enumerate(fileSizes):
            bcpu = fileAccess[i] * self.resourceCPUUsageMultiplier
            bio = fileAccess[i] * self.resourceIOUsageMultiplier
            bnet = fileAccess[i] * self.resourceNETUsageMultiplier
            for j in range(0,v):
                for k in range(0,self.replicationFactor):
                    self.blockLoad.append({"cpu" : bcpu, "io" : bio, "net" : bnet})
            
        self.blockNumber=sum(fileSizes)
        self.replicaNumber=len(self.blockLoad)

#******************************************************************************************
#   Variables modelo de energía de las máquinas
#******************************************************************************************
        
        self.pmTemplate = []
        self.pmTemplate.append({"name": "m0x", "cpu" : 24.0, "io" : 17800.0, "net" : 76800.0, "minfailrate": 0.0015, "maxfailrate": 0.0019, "energyLambda": 0.12, "energyAlpha": 5.29, "energyBeta": 0.68, "eneryGamma": 0.05, "eneryDelta": 0.1, "eneryIdle": 501.0, "energyMax": 804.0})
        self.pmTemplate.append({"name": "0x", "cpu" : 12.0, "io" : 15000.0, "net" : 38400.0, "minfailrate": 0.003, "maxfailrate": 0.004, "energyLambda": 0.12, "energyAlpha": 4.33, "energyBeta": 0.47, "eneryGamma": 0.05, "eneryDelta": 0.1, "eneryIdle": 164.0, "energyMax": 382.0})
           

        self.pmDefinition = []
        for i in range(0,self.pmNumber):
            self.pmDefinition.append(copy.deepcopy(self.pmTemplate[i%len(self.pmTemplate)]))

        self.vmTemplate = []
        self.vmTemplate.append({"name": "c3xlarge", "cpu" : 4.0, "io" : 2500.0, "net" : 750.0, "minfailrate": 0.002, "maxfailrate": 0.025, })
        self.vmTemplate.append({"name": "c32xlarge", "cpu" : 8.0, "io" : 5000.0, "net" : 1500.0, "minfailrate": 0.004, "maxfailrate": 0.05,})
        self.vmTemplate.append({"name": "c34xlarge", "cpu" : 16.0, "io" : 10000.0, "net" : 3000.0, "minfailrate": 0.002, "maxfailrate": 0.025, })
        self.vmTemplate.append({"name": "m3xlarge", "cpu" : 4.0, "io" : 5000.0, "net" : 1500.0, "minfailrate": 0.004, "maxfailrate": 0.05,})
        self.vmTemplate.append({"name": "m32xlarge", "cpu" : 8.0, "io" : 10000.0, "net" : 3000.0, "minfailrate": 0.002, "maxfailrate": 0.025, })
                

        self.vmDefinition = []
        for i in range(0,self.vmNumber):
            self.vmDefinition.append(copy.deepcopy(self.vmTemplate[i%len(self.vmTemplate)]))

      
       


    def lowScaleold(self):
        self.vmNumber=500 #initial number of vms in the system
        self.pmNumber=100
        
        self.replicationFactor=3
        
        self.epsilomResourceWaste = 0.15
        
        
        self.replicaNumber=self.blockNumber * self.replicationFactor
        
        
        fileSizes = [1600, 1623, 1646, 1671, 1696, 1723, 1750, 1779, 1809, 1839, 1872, 1905, 1941, 1977, 2016, 2056, 2099, 2143, 2190, 2239, 2292, 2347, 2406, 2468, 2535, 2606, 2681, 2763, 2851, 2946, 3049, 3161, 3283, 3418, 3567, 3733, 3918, 4128, 4367, 4643, 4965, 5347, 5810, 6382, 7113, 8087, 9462, 11586, 15412, 25101]
        fileAccess =[125 ,77 ,57 ,47 ,40 ,35 ,31 ,29 ,26 ,24 ,23 ,21 ,20 ,19 ,18 ,17 ,17 ,16 ,15 ,15, 14 ,14 ,13 ,13 ,13 ,12 ,12 ,12 ,11 ,11, 11 ,10 ,10 ,10 ,10 ,10 ,9 ,9 ,9 ,9, 9 ,9 ,8 ,8 ,8 ,8 ,8 ,8 ,8 ,7]        

        #transformamos los accesos a %
        
        totalAccess = float(sum(fileAccess))
        for i in range(len(fileAccess)):
            fileAccess[i] = float(fileAccess[i])/totalAccess
            
        #siempre ha de ser menor que los recursos de cpu disponibles
        self.resourceCPUUsageMultiplier = 0.1
        self.resourceIOUsageMultiplier =0.064
        self.resourceNETUsageMultiplier = 0.064

        

        self.blockSize = 64        
        #transformamos el tamaño de los ficheros a bloques
        for i in range(len(fileSizes)):
            fileSizes[i]=fileSizes[i]/self.blockSize
        
        
        
        self.blockLoad = [] 
        for i,v in enumerate(fileSizes):
            bcpu = fileAccess[i] * self.resourceCPUUsageMultiplier
            bio = fileAccess[i] * self.resourceIOUsageMultiplier
            bnet = fileAccess[i] * self.resourceNETUsageMultiplier
            for j in range(0,v):
                for k in range(0,self.replicationFactor):
                    self.blockLoad.append({"cpu" : bcpu, "io" : bio, "net" : bnet})
            
        self.blockNumber=sum(fileSizes)
        self.replicaNumber=len(self.blockLoad)

#******************************************************************************************
#   Variables modelo de energía de las máquinas
#******************************************************************************************
        
        self.pmTemplate = []
        self.pmTemplate.append({"name": "m0x", "cpu" : 320.0, "io" : 10000.0, "net" : 50000.0, "minfailrate": 0.01, "maxfailrate": 0.01, "energyLambda": 0.12, "energyAlpha": 5.29, "energyBeta": 0.68, "eneryGamma": 0.05, "eneryDelta": 0.1, "eneryIdle": 501.0, "energyMax": 804.0})
        self.pmTemplate.append({"name": "0x", "cpu" : 400.0, "io" : 20000.0, "net" : 50000.0, "minfailrate": 0.02, "maxfailrate": 0.01, "energyLambda": 0.12, "energyAlpha": 4.33, "energyBeta": 0.47, "eneryGamma": 0.05, "eneryDelta": 0.1, "eneryIdle": 164.0, "energyMax": 382.0})
        

        self.pmDefinition = []
        for i in range(0,self.pmNumber):
            self.pmDefinition.append(copy.deepcopy(self.pmTemplate[i%len(self.pmTemplate)]))

        self.vmTemplate = []
        self.vmTemplate.append({"name": "m0x", "cpu" : 10.0, "io" : 1000.0, "net" : 1000.0, "minfailrate": 0.03, "maxfailrate": 0.01, })
        self.vmTemplate.append({"name": "0x", "cpu" : 10.0, "io" : 2000.0, "net" : 1000.0, "minfailrate": 0.04, "maxfailrate": 0.01,})
        self.vmTemplate.append({"name": "m0x", "cpu" : 10.0, "io" : 1000.0, "net" : 1000.0, "minfailrate": 0.05, "maxfailrate": 0.01, })
        self.vmTemplate.append({"name": "0x", "cpu" : 10.0, "io" : 2000.0, "net" : 1000.0, "minfailrate": 0.06, "maxfailrate": 0.01,})
        self.vmTemplate.append({"name": "m0x", "cpu" : 10.0, "io" : 1000.0, "net" : 1000.0, "minfailrate": 0.07, "maxfailrate": 0.01, })
        self.vmTemplate.append({"name": "0x", "cpu" : 10.0, "io" : 2000.0, "net" : 1000.0, "minfailrate": 0.08, "maxfailrate": 0.01,})
        self.vmTemplate.append({"name": "m0x", "cpu" : 10.0, "io" : 1000.0, "net" : 1000.0, "minfailrate": 0.09, "maxfailrate": 0.01, })
        self.vmTemplate.append({"name": "0x", "cpu" : 10.0, "io" : 2000.0, "net" : 1000.0, "minfailrate": 0.1, "maxfailrate": 0.01,})
        

        self.vmDefinition = []
        for i in range(0,self.vmNumber):
            self.vmDefinition.append(copy.deepcopy(self.vmTemplate[i%len(self.vmTemplate)]))

      
 
            

    def newCofiguration(self):

        self.vmNumber=10 #initial number of vms in the system
        self.pmNumber=4
        self.blockNumber=2
        self.replicationFactor=3
        
        self.epsilomResourceWaste = 0.15
        
        
        self.replicaNumber=self.blockNumber * self.replicationFactor
        
        
        self.blockLoad = []
        for i in range(0,self.replicaNumber):
            self.blockLoad.append({"cpu" : 1.0, "io" : 1.0, "net" : 1.0})
        
#        self.blockLoad = {}
#        self.blockLoad['cpu']=range(0,self.replicaNumber)
#        self.blockLoad['io']=range(10,self.replicaNumber+10)
#        self.blockLoad['net']=range(20,self.replicaNumber+20)

        
#******************************************************************************************
#   Variables modelo de energía de las máquinas
#******************************************************************************************
        
        self.pmTemplate = []
        self.pmTemplate.append({"name": "m0x", "cpu" : 32.0, "io" : 1000.0, "net" : 5000.0, "failrate": 0.01, "energyLambda": 0.12, "energyAlpha": 5.29, "energyBeta": 0.68, "eneryGamma": 0.05, "eneryDelta": 0.1, "eneryIdle": 501.0, "energyMax": 804.0})
        self.pmTemplate.append({"name": "0x", "cpu" : 40.0, "io" : 2000.0, "net" : 5000.0, "failrate": 0.02, "energyLambda": 0.12, "energyAlpha": 4.33, "energyBeta": 0.47, "eneryGamma": 0.05, "eneryDelta": 0.1, "eneryIdle": 164.0, "energyMax": 382.0})
        

        self.pmDefinition = []
        for i in range(0,self.pmNumber):
            self.pmDefinition.append(copy.deepcopy(self.pmTemplate[i%len(self.pmTemplate)]))

        self.vmTemplate = []
        self.vmTemplate.append({"name": "m0x", "cpu" : 1.0, "io" : 100.0, "net" : 100.0, "failrate": 0.03 })
        self.vmTemplate.append({"name": "0x", "cpu" : 1.0, "io" : 200.0, "net" : 100.0, "failrate": 0.04})
        self.vmTemplate.append({"name": "m0x", "cpu" : 1.0, "io" : 100.0, "net" : 100.0, "failrate": 0.05 })
        self.vmTemplate.append({"name": "0x", "cpu" : 1.0, "io" : 200.0, "net" : 100.0, "failrate": 0.06})
        self.vmTemplate.append({"name": "m0x", "cpu" : 1.0, "io" : 100.0, "net" : 100.0, "failrate": 0.07 })
        self.vmTemplate.append({"name": "0x", "cpu" : 1.0, "io" : 200.0, "net" : 100.0, "failrate": 0.08})
        self.vmTemplate.append({"name": "m0x", "cpu" : 1.0, "io" : 100.0, "net" : 100.0, "failrate": 0.09 })
        self.vmTemplate.append({"name": "0x", "cpu" : 1.0, "io" : 200.0, "net" : 100.0, "failrate": 0.1})
        

        self.vmDefinition = []
        for i in range(0,self.vmNumber):
            self.vmDefinition.append(copy.deepcopy(self.vmTemplate[i%len(self.vmTemplate)]))

      
        
        
        
    def normalizeConfiguration(self):
        for i,v in enumerate(self.serviceTupla):
            self.serviceTupla[i]['scaleLevel']= int(math.ceil((self.serviceTupla[i]['computationalResources']*self.serviceTupla[i]['requestNumber']*self.requestPerApp[self.serviceTupla[i]['application']])/self.serviceTupla[i]['threshold']))
            self.serviceTupla[i]['containerUsage']= self.serviceTupla[i]['computationalResources']/self.serviceTupla[i]['scaleLevel'] 


    def configurationNew(self, costmultiplier, capacitymultiplier, latencymultiplier):

        self.ScaleLevel = 1
        self.StorageLevel = 1
        self.vmNumber = 4


        self.repairTimes = {}
        self.repairTimes[0] = 1.0  #time to run a stored container
        self.repairTimes[-1] = 50.0  # time to download and run a container        

        self.serviceTupla= []

        self.serviceTupla.append({"application" : 0, "requestNumber" :  3.2 , "computationalResources":   0.1 , "storageResources":   0.01 , "threshold":   1.0 , "failrate": 0.04   , "consumeServices": []})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  1.8 , "computationalResources":  11.7 , "storageResources":   1.17 , "threshold":  25.0 , "failrate": 0.02   , "consumeServices": [12]})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  3.2 , "computationalResources":  20.0 , "storageResources":   2.0  , "threshold": 200.0 , "failrate": 0.02   , "consumeServices": [1,3]})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  1.4 , "computationalResources":   0.1 , "storageResources":   0.01 , "threshold":  10.0 , "failrate": 0.0002 , "consumeServices": []})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  2.3 , "computationalResources":  27.1 , "storageResources":   2.71 , "threshold":  80.0 , "failrate": 0.02   , "consumeServices": [2,3,9,10,11]})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  0.8 , "computationalResources":   2.8 , "storageResources":   0.28 , "threshold":  30.0 , "failrate": 0.0001 , "consumeServices": []})
        self.serviceTupla.append({"application" : 0, "requestNumber" : 15.1 , "computationalResources":   3.8 , "storageResources":   0.38 , "threshold":  50.0 , "failrate": 0.003  , "consumeServices": [4,5,8]})
        self.serviceTupla.append({"application" : 0, "requestNumber" : 15.1 , "computationalResources":   0.5 , "storageResources":   0.05 , "threshold":  10.0 , "failrate": 0.0001 , "consumeServices": [6]})
        self.serviceTupla.append({"application" : 0, "requestNumber" : 12.0 , "computationalResources":   0.2 , "storageResources":   0.02 , "threshold":   3.0 , "failrate": 0.0006 , "consumeServices": []})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  3.2 , "computationalResources":  41.3 , "storageResources":   4.13 , "threshold": 100.0 , "failrate": 0.02   , "consumeServices": [11]})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  0.1 , "computationalResources":  45.1 , "storageResources":   4.51 , "threshold": 100.0 , "failrate": 0.003  , "consumeServices": [11]})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  3.2 , "computationalResources":  26.3 , "storageResources":   2.63 , "threshold":  80.0 , "failrate": 0.04   , "consumeServices": []})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  3.2 , "computationalResources":   4.0 , "storageResources":   0.4  , "threshold":  40.0 , "failrate": 0.0006 , "consumeServices": [0,2]})
        self.serviceTupla.append({"application" : 0, "requestNumber" :  3.2 , "computationalResources":  13.2 , "storageResources":   1.32 , "threshold": 100.0 , "failrate": 0.0003 , "consumeServices": []})

        self.numberMicroServices = len(self.serviceTupla)

        self.numberProviders = 3
        
#        #definimos las "plantillas" de máquinas
#        self.vminstancesTypes = []
#        self.vminstancesTypes.append({"provider": 0, "name": "tinny", "capacity" : 100.0 * capacitymultiplier, "failrate": 0.025, "cost": {"running": 3.0 * costmultiplier, "usage": 0.0 * costmultiplier, "storage": 0.0 * costmultiplier}})
#        self.vminstancesTypes.append({"provider": 0, "name": "small", "capacity" : 200.0 * capacitymultiplier, "failrate": 0.025, "cost": {"running": 8.0 * costmultiplier, "usage": 0.0 * costmultiplier, "storage": 0.0 * costmultiplier}})
#        self.vminstancesTypes.append({"provider": 1, "name": "medium", "capacity" : 400.0  * capacitymultiplier, "failrate": 0.025, "cost": {"running": 0.0 * costmultiplier, "usage": 10.0 * costmultiplier, "storage": 1.0 * costmultiplier}})
#        self.vminstancesTypes.append({"provider": 2, "name": "big", "capacity" : 800.0 * capacitymultiplier, "failrate": 0.025, "cost": {"running": 0.0 * costmultiplier, "usage": 10.0 * costmultiplier, "storage": 0.0 * costmultiplier}})

        self.vminstancesTypes = []
        self.vminstancesTypes.append({"provider": 0, "name": "tinny", "capacity" : 100.0 * capacitymultiplier, "failrate": 0.025, "cost": {"running": 100.0 * costmultiplier, "usage": 0.0 * costmultiplier, "storage": 0.0 * costmultiplier}})
        self.vminstancesTypes.append({"provider": 0, "name": "small", "capacity" : 200.0 * capacitymultiplier, "failrate": 0.025, "cost": {"running": 150.0 * costmultiplier, "usage": 0.0 * costmultiplier, "storage": 0.0 * costmultiplier}})
        self.vminstancesTypes.append({"provider": 1, "name": "medium", "capacity" : 400.0  * capacitymultiplier, "failrate": 0.025, "cost": {"running": 250.0 * costmultiplier, "usage": 0.0 * costmultiplier, "storage": 0.0 * costmultiplier}})
        self.vminstancesTypes.append({"provider": 2, "name": "big", "capacity" : 800.0 * capacitymultiplier, "failrate": 0.025, "cost": {"running": 1000.0 * costmultiplier, "usage": 0.0 * costmultiplier, "storage": 0.0 * costmultiplier}})


        
        #asignamos un tipo/plantilla de máquina a cada uno de los nodos del sistema
        #igual número de máquinas de cada tipo
        self.nodeFeatures = []
        for n in range(self.nodenumber):
            self.nodeFeatures.append(self.plantillasMaquinas[n % len(self.plantillasMaquinas)])
            #self.nodeFeatures.append(self.plantillasMaquinas[self.rnd.randint(0,len(self.plantillasMaquinas)-1)])

            
        self.providersLatency = {}

        for i in range(0,self.numberProviders):
            for j in range(0,self.numberProviders):
                if i == j:
                    self.providersLatency[(i,j)]= 1.0 * latencymultiplier
                else:
                    self.providersLatency[(i,j)]= 10 * latencymultiplier

        
        
        
        
    def configurationA(self,nodes, apps, req):

        self.nodenumber = nodes
        self.requestPerApp = []
        self.serviceTupla= []
        for i in range(apps):
            self.requestPerApp.append(4.0*float(req))

            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [0]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [1,0]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [2]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [2,0]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [2,3,4]})

        self.numberMicroServices = len(self.serviceTupla)

        #definimos las "plantillas" de máquinas
        self.plantillasMaquinas = []
        self.plantillasMaquinas.append({"name": "tinny", "capacity" : 10.0, "failrate": 0.01})
        self.plantillasMaquinas.append({"name": "small", "capacity" : 20.0, "failrate": 0.01})
        self.plantillasMaquinas.append({"name": "medium", "capacity" : 40.0, "failrate": 0.01})
        self.plantillasMaquinas.append({"name": "big", "capacity" : 80.0, "failrate": 0.01})
        
        #asignamos un tipo/plantilla de máquina a cada uno de los nodos del sistema
        #igual número de máquinas de cada tipo
        self.nodeFeatures = []
        for n in range(self.nodenumber):
            self.nodeFeatures.append(self.plantillasMaquinas[n % len(self.plantillasMaquinas)])
            #self.nodeFeatures.append(self.plantillasMaquinas[self.rnd.randint(0,len(self.plantillasMaquinas)-1)])
            
       

        #******************************************************************************************
        #   Definición de la red del CPD
        #******************************************************************************************



        self.cpdNetwork = [[0 for x in range(self.nodenumber)] for y in range(self.nodenumber)]
        
        #las máquinas se distribuyen en dos racks.
                            
        for r in range(0,self.nodenumber/2):
            for s in range(0,self.nodenumber/2):
                self.cpdNetwork[r][s]=1.0
                self.cpdNetwork[s][r]=1.0            
        for r in range(0,self.nodenumber/2):
            for s in range(self.nodenumber/2,self.nodenumber):
                self.cpdNetwork[r][s]=4.0
                self.cpdNetwork[s][r]=4.0     
        for r in range(self.nodenumber/2,self.nodenumber):
            for s in range(0,self.nodenumber/2):
                self.cpdNetwork[r][s]=4.0
                self.cpdNetwork[s][r]=4.0     
        for r in range(self.nodenumber/2,self.nodenumber):
            for s in range(self.nodenumber/2,self.nodenumber):
                self.cpdNetwork[r][s]=1.0
                self.cpdNetwork[s][r]=1.0   
        #******************************************************************************************
        #   END Definición de la red del CPD
        #******************************************************************************************
        
        #******************************************************************************************
        #   BEGIN cálculo del escalado ajustado a threshold
        #******************************************************************************************



        self.normalizeConfiguration()        
                                        
        #******************************************************************************************
        #   END cálculo del escalado ajustado a threshold
        #******************************************************************************************
 


           
            
    def configurationB(self,nodes, apps, req):

        self.nodenumber = nodes
        self.requestPerApp = []
        self.serviceTupla= []
        for i in range(apps):
            self.requestPerApp.append(4.0*float(req))

            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":   0.1 , "threshold":   1.0 , "failrate": 0.04   , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" :  1.8 , "computationalResources":  11.7 , "threshold":  25.0 , "failrate": 0.02   , "consumeServices": [12]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":  20.0 , "threshold": 200.0 , "failrate": 0.02   , "consumeServices": [1,3]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  1.4 , "computationalResources":   0.1 , "threshold":  10.0 , "failrate": 0.0002 , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" :  2.3 , "computationalResources":  27.1 , "threshold":  80.0 , "failrate": 0.02   , "consumeServices": [2,3,9,10,11]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  0.8 , "computationalResources":   2.8 , "threshold":  30.0 , "failrate": 0.0001 , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" : 15.1 , "computationalResources":   3.8 , "threshold":  50.0 , "failrate": 0.003  , "consumeServices": [4,5,8]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 15.1 , "computationalResources":   0.5 , "threshold":  10.0 , "failrate": 0.0001 , "consumeServices": [6]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 12.0 , "computationalResources":   0.2 , "threshold":   3.0 , "failrate": 0.0006 , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":  41.3 , "threshold": 100.0 , "failrate": 0.02   , "consumeServices": [11]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  0.1 , "computationalResources":  45.1 , "threshold": 100.0 , "failrate": 0.003  , "consumeServices": [11]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":  26.3 , "threshold":  80.0 , "failrate": 0.04   , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":   4.0 , "threshold":  40.0 , "failrate": 0.0006 , "consumeServices": [0,2]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":  13.2 , "threshold": 100.0 , "failrate": 0.0003 , "consumeServices": []})

        self.numberMicroServices = len(self.serviceTupla)

        #definimos las "plantillas" de máquinas
        self.plantillasMaquinas = []
        self.plantillasMaquinas.append({"name": "tinny", "capacity" : 100.0, "failrate": 0.025})
        self.plantillasMaquinas.append({"name": "small", "capacity" : 200.0, "failrate": 0.025})
        self.plantillasMaquinas.append({"name": "medium", "capacity" : 400.0, "failrate": 0.025})
        self.plantillasMaquinas.append({"name": "big", "capacity" : 800.0, "failrate": 0.025})
        
        #asignamos un tipo/plantilla de máquina a cada uno de los nodos del sistema
        #igual número de máquinas de cada tipo
        self.nodeFeatures = []
        for n in range(self.nodenumber):
            self.nodeFeatures.append(self.plantillasMaquinas[n % len(self.plantillasMaquinas)])
            #self.nodeFeatures.append(self.plantillasMaquinas[self.rnd.randint(0,len(self.plantillasMaquinas)-1)])

            
            
        #******************************************************************************************
        #   Definición de la red del CPD
        #******************************************************************************************
        


        self.cpdNetwork = [[0 for x in range(self.nodenumber)] for y in range(self.nodenumber)]
        
        #las máquinas se distribuyen en dos racks.
                            
        for r in range(0,self.nodenumber/2):
            for s in range(0,self.nodenumber/2):
                self.cpdNetwork[r][s]=1.0
                self.cpdNetwork[s][r]=1.0            
        for r in range(0,self.nodenumber/2):
            for s in range(self.nodenumber/2,self.nodenumber):
                self.cpdNetwork[r][s]=4.0
                self.cpdNetwork[s][r]=4.0     
        for r in range(self.nodenumber/2,self.nodenumber):
            for s in range(0,self.nodenumber/2):
                self.cpdNetwork[r][s]=4.0
                self.cpdNetwork[s][r]=4.0     
        for r in range(self.nodenumber/2,self.nodenumber):
            for s in range(self.nodenumber/2,self.nodenumber):
                self.cpdNetwork[r][s]=1.0
                self.cpdNetwork[s][r]=1.0        
        #******************************************************************************************
        #   END Definición de la red del CPD
        #******************************************************************************************
        
        #******************************************************************************************
        #   BEGIN cálculo del escalado ajustado a threshold
        #******************************************************************************************
        


        self.normalizeConfiguration()   
                            

        #******************************************************************************************
        #   END cálculo del escalado ajustado a threshold
        #******************************************************************************************
        

   
