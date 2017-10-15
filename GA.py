# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""
import matplotlib
matplotlib.use('Agg')
import numpy as np
import random as random
import sys
import matplotlib.pyplot as plt 
import matplotlib.cm as cm 
import POPULATION as pop
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt3d
import SYSTEMMODEL as systemmodel
import copy
import numpy as np



class GA:
    
    
    
    def __init__(self, system):
        
        
        
        self.system = system
        
        self.populationSize = 100
        self.populationPt = pop.POPULATION(self.populationSize)
        self.mutationProbability = 0.25
        
        self.rndPOP = random.Random()
        self.rndEVOL = random.Random()
        
        
        self.optimizationAlgorithm = 'NSGA2' # NSGA2 or AIA
        
        #indicates the decision variables of the optimization: only blocks, only vms or boths.
        self.experimentScenario = 'BOTH' # BOTH VM or BLOCK
        
#        self.initialGeneration = 'ADJUSTED' # or RANDOM
#        
#        
#        
#        
#
#        self.scaleLevel='SINGLE' # or OLD
#        self.reliabilityAwarness = False
#        
#        self.networkDistanceCalculation = 'MEAN' #or TOTAL
#        self.thersholdCalculation = 'SINGLE' # or ACCUMULATED






    def selectSolution(self, population):
        
        energy = []
        resourcewaste = []
        unavailability = []
        for i in range(0,len(population.fitness)):
            energy.append(population.fitness[i]['energy'])
            resourcewaste.append(population.fitness[i]['resourcewaste'])
            unavailability.append(population.fitness[i]['unavailability'])
            
        minenergy = min(energy)
        minresourcewaste = min(resourcewaste)
        minunavailability = min(unavailability)
        
        diffenergy = max(energy) - minenergy
        diffresourcewaste = max(resourcewaste) - minresourcewaste
        diffunavailability = max(unavailability) - minunavailability
        
        myWeight = 3.0
        
        fitness = []
        
        for i,v in enumerate(energy):
        
            if (diffenergy) > 0:
                energyValue = (1.0/myWeight) * ((energy[i]-minenergy)/diffenergy)
            else:
                energyValue = 1.0*(1.0/myWeight)
            
            if (diffresourcewaste) > 0:
                resourcewasteValue = (1.0/myWeight) * ((resourcewaste[i]-minresourcewaste)/diffresourcewaste)
            else:
                resourcewasteValue = 1.0*(1.0/myWeight)

            if (diffunavailability) > 0:
                unavailabilityValue = (1.0/myWeight) * ((unavailability[i]-minunavailability)/diffunavailability)
            else:
                unavailabilityValue = 1.0*(1.0/myWeight)
        
            fitness.append(energyValue+resourcewasteValue+unavailabilityValue)
            
            
        minfitness = min(fitness)
        
        return fitness.index(minfitness)
                
            



#******************************************************************************************
#   MUTATIONS
#******************************************************************************************




    def VmGrowth(self,child):
        
        child['vm'].append(self.rndEVOL.randint(0,self.system.pmNumber-1))
        child['vmtype'].append(self.rndEVOL.randint(0,len(self.system.vmTemplate)-1))
        child['block'][self.rndEVOL.randint(0,len(child['block'])-1)] = len(child['vm'])-1        

        self.removeEmptyVms(child)

        
    def VmShrink(self,child):
        vm_i = self.rndEVOL.randint(0,len(child['vm'])-1)
        del child['vm'][vm_i]
        del child['vmtype'][vm_i]
        
        for i,v in enumerate(child['block']):
            if v == vm_i:
                child['block'][i] = self.rndEVOL.randint(0,len(child['vm'])-1)  
            elif v>vm_i:
                child['block'][i] -= 1
          
        
    def VmSwap(self,child):
        
        vm_is = self.rndEVOL.sample(xrange(0,len(child['vm'])),2)  
        child['vm'][vm_is[0]], child['vm'][vm_is[1]] = child['vm'][vm_is[1]], child['vm'][vm_is[0]] 
        
        
    def VmReplace(self,child):
        
        vm_i = self.rndEVOL.randint(0,len(child['vm'])-1)
        child['vm'][vm_i] = self.rndEVOL.randint(0,self.system.pmNumber-1)

    def BlockSwap2(self,child):

        block_is = self.rndEVOL.sample(xrange(0,len(child['block'])/self.system.replicationFactor),2)
        for i in range(0,self.system.replicationFactor):
            child['block'][block_is[0]+i], child['block'][block_is[1]+i] = child['block'][block_is[1]+i], child['block'][block_is[0]+i] 

        
        
    def BlockReplace2(self,child):


        block_i = self.rndEVOL.randint(0,(len(child['block'])/self.system.replicationFactor)-1) 
        vm_is = self.rndEVOL.sample(xrange(0,len(child['vm'])),self.system.replicationFactor)
        
        for i in range(0,self.system.replicationFactor):
            child['block'][block_i+i] = vm_is[i]        

        self.removeEmptyVms(child)

        
        
    def BlockSwap(self,child):

        block_is = self.rndEVOL.sample(xrange(0,len(child['block'])),2)  
        child['block'][block_is[0]], child['block'][block_is[1]] = child['block'][block_is[1]], child['block'][block_is[0]] 

        
        
    def BlockReplace(self,child):


        block_i = self.rndEVOL.randint(0,len(child['block'])-1)
        child['block'][block_i] = self.rndEVOL.randint(0,len(child['vm'])-1)        

        self.removeEmptyVms(child)
                
    def mutate(self,child):
        #print "[Offsrping generation]: Mutation in process**********************"


        if self.experimentScenario=='BOTH':
            mutationOperators = [] 
            mutationOperators.append(self.VmGrowth)
            mutationOperators.append(self.VmShrink)
            mutationOperators.append(self.VmSwap)
            mutationOperators.append(self.VmReplace)
            mutationOperators.append(self.BlockSwap2)
            mutationOperators.append(self.BlockReplace2)

        if self.experimentScenario=='VM':
            mutationOperators = [] 
            mutationOperators.append(self.VmGrowth)
            mutationOperators.append(self.VmShrink)
            mutationOperators.append(self.VmSwap)
            mutationOperators.append(self.VmReplace)

        if self.experimentScenario=='BLOCK':
            mutationOperators = [] 
            mutationOperators.append(self.BlockSwap2)
            mutationOperators.append(self.BlockReplace2)


      
        mutationOperators[self.rndEVOL.randint(0,len(mutationOperators)-1)](child)
    

#******************************************************************************************
#   END MUTATIONS
#******************************************************************************************


#******************************************************************************************
#   CROSSOVER
#******************************************************************************************



    def normalizeBlockAllocatedToNonExistingVMs(self,blockCh,limit):
        for i,v in enumerate(blockCh):
            if v>=limit:
                blockCh[i] = v % limit


    def crossoverBOTH2(self,f1,f2,offs):

        
        c1 = copy.deepcopy(f1)
        c2 = copy.deepcopy(f2)
        
        cuttingPoint = self.rndEVOL.randint(1,len(c1['block'])-1)
        
        #apply one-point cutting point to the block-chromosome

        newblockCh1 = c1['block'][:cuttingPoint] + c2['block'][cuttingPoint:]
        newblockCh2 = c2['block'][:cuttingPoint] + c1['block'][cuttingPoint:]
        
        cuttingPoint = self.rndEVOL.randint(1,min(len(c1['vm']),len(c2['vm']))-1)
        
        newvmCh1 = c1['vm'][:cuttingPoint] + c2['vm'][cuttingPoint:]
        newvmCh2 = c2['vm'][:cuttingPoint] + c1['vm'][cuttingPoint:]

        newvmtypeCh1 = c1['vmtype'][:cuttingPoint] + c2['vmtype'][cuttingPoint:]
        newvmtypeCh2 = c2['vmtype'][:cuttingPoint] + c1['vmtype'][cuttingPoint:]
        
        
        self.normalizeBlockAllocatedToNonExistingVMs(newblockCh1,len(newvmCh1))
        self.normalizeBlockAllocatedToNonExistingVMs(newblockCh2,len(newvmCh2))


        c1['vm'] = newvmCh1      
        c2['vm'] = newvmCh2      

        c1['vmtype'] = newvmtypeCh1      
        c2['vmtype'] = newvmtypeCh2      


        c1['block'] = newblockCh1      
        c2['block'] = newblockCh2      
            
        
        self.removeEmptyVms(c1)
        self.removeEmptyVms(c2)


        offs.append(c1)
        #print "[Offsrping generation]: Children 1 added **********************"
        offs.append(c2)
        #print "[Offsrping generation]: Children 2 added **********************"




    def crossoverBOTH(self,f1,f2,offs):

        
        c1 = copy.deepcopy(f1)
        c2 = copy.deepcopy(f2)
        
        cuttingPoint = self.rndEVOL.randint(1,len(c1['block'])-1)
        
        shiftVm4c2 = len(c1['vm'])
        
        #rename all the vms of the second father/child
        for i in range(0,len(c2['block'])):
            c2['block'][i] += shiftVm4c2
            
        #create the vm-chromosomes from the joining of both complete vm-chromosomes of the fathers
        
        newvmCh1 = c1['vm'] + c2['vm']
        newvmCh2 = c1['vm'] + c2['vm']
        
        newvmtypeCh1 = c1['vmtype'] + c2['vmtype']
        newvmtypeCh2 = c1['vmtype'] + c2['vmtype']
        
        #apply one-point cutting point to the block-chromosome

        newblockCh1 = c1['block'][:cuttingPoint] + c2['block'][cuttingPoint:]
        newblockCh2 = c2['block'][:cuttingPoint] + c1['block'][cuttingPoint:]
        

        c1['vm'] = newvmCh1      
        c2['vm'] = newvmCh2      

        c1['vmtype'] = newvmtypeCh1      
        c2['vmtype'] = newvmtypeCh2      


        c1['block'] = newblockCh1      
        c2['block'] = newblockCh2      
            
        
        self.removeEmptyVms(c1)
        self.removeEmptyVms(c2)


        offs.append(c1)
        #print "[Offsrping generation]: Children 1 added **********************"
        offs.append(c2)
        #print "[Offsrping generation]: Children 2 added **********************"


    def crossoverVM(self,f1,f2,offs):

        c1 = copy.deepcopy(f1)
        c2 = copy.deepcopy(f2)
        
        cuttingPoint = self.rndEVOL.randint(1,min(len(c1['vm']),len(c2['vm']))-1)
        
        newvmCh1 = c1['vm'][:cuttingPoint] + c2['vm'][cuttingPoint:]
        newvmCh2 = c2['vm'][:cuttingPoint] + c1['vm'][cuttingPoint:]
        

        c1['vm'] = newvmCh1      
        c2['vm'] = newvmCh2      

        newvmtypeCh1 = c1['vmtype'][:cuttingPoint] + c2['vmtype'][cuttingPoint:]
        newvmtypeCh2 = c2['vmtype'][:cuttingPoint] + c1['vmtype'][cuttingPoint:]
        

        c1['vmtype'] = newvmtypeCh1      
        c2['vmtype'] = newvmtypeCh2
        
        
        #we distribute the blocks in the vms in a roundrobin strategy
        c1['block'] = self.generateRoundRobin1D(self.system.replicaNumber,len(c1['vm']))
        c2['block'] = self.generateRoundRobin1D(self.system.replicaNumber,len(c2['vm']))
        
        

        offs.append(c1)
        #print "[Offsrping generation]: Children 1 added **********************"
        offs.append(c2)
        #print "[Offsrping generation]: Children 2 added **********************"

        
        
    def crossoverBLOCK(self,f1,f2,offs):

        c1 = copy.deepcopy(f1)
        c2 = copy.deepcopy(f2)
        
        cuttingPoint = self.rndEVOL.randint(1,len(c1['block'])-1)
        
        
        #apply one-point cutting point to the block-chromosome

        newblockCh1 = c1['block'][:cuttingPoint] + c2['block'][cuttingPoint:]
        newblockCh2 = c2['block'][:cuttingPoint] + c1['block'][cuttingPoint:]
        

        c1['block'] = newblockCh1      
        c2['block'] = newblockCh2      
            

        offs.append(c1)
        #print "[Offsrping generation]: Children 1 added **********************"
        offs.append(c2)
        #print "[Offsrping generation]: Children 2 added **********************"

        
        
        
    def crossover(self,f1,f2,offs):
        
        if self.experimentScenario=='BOTH':
            #self.crossoverBOTH(f1,f2,offs)
            self.crossoverBOTH2(f1,f2,offs)

        if self.experimentScenario=='VM':
            self.crossoverVM(f1,f2,offs)

        if self.experimentScenario=='BLOCK':
            self.crossoverBLOCK(f1,f2,offs)




#******************************************************************************************
#   END CROSSOVER
#******************************************************************************************




#******************************************************************************************
#   Node Workload calculation
#******************************************************************************************

    def calculateVmsWorkload(self, solution):
        
        
        vmsLoad = {}
        vmsLoad['cpu']=[]
        vmsLoad['io']=[]
        vmsLoad['net']=[]
        
        
        for vm_i in range(0,len(solution['vm'])):
            vmsLoad['cpu'].append(0.0)
            vmsLoad['io'].append(0.0)
            vmsLoad['net'].append(0.0)
            
        for block_i in range(0,len(solution['block'])):
            vmsLoad['cpu'][solution['block'][block_i]] += self.system.blockLoad[block_i]['cpu']
            vmsLoad['io'][solution['block'][block_i]] += self.system.blockLoad[block_i]['io']
            vmsLoad['net'][solution['block'][block_i]] += self.system.blockLoad[block_i]['net']

        return vmsLoad
        
    def calculatePmsWorkload(self, solution, vmsLoad):
        
        pmsLoad = {}
        pmsLoad['cpu']=[]
        pmsLoad['io']=[]
        pmsLoad['net']=[]
        
        
        for pm_i in range(0,self.system.pmNumber):
            pmsLoad['cpu'].append(0.0)
            pmsLoad['io'].append(0.0)
            pmsLoad['net'].append(0.0)
            

        for vm_i in range(0,len(solution['vm'])):
            pmsLoad['cpu'][solution['vm'][vm_i]] += vmsLoad['cpu'][vm_i]
            pmsLoad['io'][solution['vm'][vm_i]] += vmsLoad['io'][vm_i]
            pmsLoad['net'][solution['vm'][vm_i]] += vmsLoad['net'][vm_i]
            
        return pmsLoad
        
        
        
    def calculateSolutionsWorkload(self,pop):
        
        for i,citizen in enumerate(pop.population):
            pop.vmsUsages[i]=self.calculateVmsWorkload(citizen)
            pop.pmsUsages[i]=self.calculatePmsWorkload(citizen,pop.vmsUsages[i])
        

#******************************************************************************************
#   END Node Workload calculation
#******************************************************************************************


#******************************************************************************************
#   Model constraints
#******************************************************************************************

    
    def resourceUsages(self,pop,index):

#checking pm has less resources usages than their templates

        for pm_i in range(0,self.system.pmNumber):
            
            pmtemplate = self.system.pmDefinition[pm_i]
            
            if pmtemplate['cpu']<pop.pmsUsages[index]['cpu'][pm_i]:
#                print "CPU usage constraint not satified for solution "+str(index)+ " and PM "+str(pm_i)
#                print "template value "+str(pmtemplate['cpu']) + " and usage value "+str(pop.pmsUsages[index]['cpu'][pm_i])
                return False

            if pmtemplate['net']<pop.pmsUsages[index]['net'][pm_i]:
#                print "NET usage constraint not satified for solution "+str(index)+ " and PM "+str(pm_i)
#                print "template value "+str(pmtemplate['net']) + " and usage value "+str(pop.pmsUsages[index]['net'][pm_i])
                return False

            if pmtemplate['io']<pop.pmsUsages[index]['io'][pm_i]:
#                print "IO usage constraint not satified for solution "+str(index)+ " and PM "+str(pm_i)
#                print "template value "+str(pmtemplate['io']) + " and usage value "+str(pop.pmsUsages[index]['io'][pm_i])
                return False



        
        
#checking vm has less resource usages than their templates        

        for vm_i in range(0,len(pop.population[index]['vmtype'])):
            
            vmtemplate = self.system.vmTemplate[pop.population[index]['vmtype'][vm_i]]
            
            if vmtemplate['cpu']<pop.vmsUsages[index]['cpu'][vm_i]:
#                print "CPU usage constraint not satified for solution "+str(index)+ " and VM "+str(vm_i)
#                print "template value "+str(vmtemplate['cpu']) + " and usage value "+str(pop.vmsUsages[index]['cpu'][vm_i])
                return False

            if vmtemplate['net']<pop.vmsUsages[index]['net'][vm_i]:
#                print "NET usage constraint not satified for solution "+str(index)+ " and VM "+str(vm_i)
#                print "template value "+str(vmtemplate['net']) + " and usage value "+str(pop.vmsUsages[index]['net'][vm_i])
                return False
                return False

            if vmtemplate['io']<pop.vmsUsages[index]['io'][vm_i]:
#                print "IO usage constraint not satified for solution "+str(index)+ " and VM "+str(vm_i)
#                print "template value "+str(vmtemplate['io']) + " and usage value "+str(pop.vmsUsages[index]['io'][vm_i])
                return False

        return True

#TODO por si se quiere cmabiar a que en lugar de al menos un container, haya un cierto grado de escalaraidad
#simplemente sería sumar los que hay en cada uno, en lugar de comprobar si al menos hay un vm con un container        
    def duplicatedReplicaInVM(self, blockChromosome,solnumber):

        i=0
        limit = len(blockChromosome)
        while i < limit:
            
            replicas = set(blockChromosome[i:i+self.system.replicationFactor])
            if len(replicas)<self.system.replicationFactor:
#                print "Duplicated block in solution "+str(solnumber)+ " and piece "+str(i)
#                print blockChromosome[i:i+self.system.replicationFactor]
#                print blockChromosome
                return True
            i+=self.system.replicationFactor
        return False
        
        
    def checkConstraints(self,pop, index):
             
        if self.duplicatedReplicaInVM(pop.population[index]['block'],index):
#            print("duplicatedReplica")
            return False
        if not self.resourceUsages(pop,index):
            print("resourceUsages")
            return False
        return True

#******************************************************************************************
#   END Model constraints
#******************************************************************************************

#******************************************************************************************
#   Unavailability calculation
#******************************************************************************************
    def vmFailureCurve(self,minvalue,maxvalue,usage):
        
        return minvalue + usage * (maxvalue - minvalue)
    
    def pmFailureCurve(self,minvalue,maxvalue,usage):
        
        if usage > 0.3:
            return maxvalue - (usage/0.3) * (maxvalue-minvalue)
        else:
            return minvalue + (usage-0.3/0.7) * (maxvalue - minvalue) 

    def calculateUnavailability2(self,chromosome,pmsusages,vmsusages):
        
#        print "solution"
#        print chromosome

        
        blockChromosome = chromosome['block']
        
        failureTotal = 0.0

        i=0
        limit = len(blockChromosome)
        while i < limit:
            
            #calculation of the unavailability of each set of replicas of the same block
            
            blockVmReplicas = blockChromosome[i:i+self.system.replicationFactor]
            
#            print "vms"
#            print blockVmReplicas
            
            blockPmReplicas = []
            
            #two list, one for the vms where the replicas are stored 
            #and another one for the pms where the replicas are stored
            
            for k in range(0,len(blockVmReplicas)):
                blockPmReplicas.append(chromosome['vm'][blockVmReplicas[k]])
                
            setPmReplicas = set(blockPmReplicas)

#            print "pms"
#            print blockPmReplicas
            
            failureBlock = 1.0
            
            for pm_i in setPmReplicas:
                
                
                #######YO CREO QUE DE LO SIGUIENTE EL VALOR ES X y no Y
                #elements=[y for y,x in enumerate(blockPmReplicas) if x==pm_i]
                elements=[y for y,x in enumerate(blockPmReplicas) if x==pm_i]
 #               print "iguales"
 #               print elements
                
                # i need to calculate failure(pm)+ PRODCT [failure(vms)] for each
                #machiner where a block is stored. I calculate the set of vms in
                # the same pm.
                minfail = self.system.pmDefinition[blockPmReplicas[elements[0]]]['minfailrate']
                maxfail = self.system.pmDefinition[blockPmReplicas[elements[0]]]['maxfailrate']
                pmU = pmsusages['cpu'][blockPmReplicas[elements[0]]]
                
                failurePm = self.pmFailureCurve(minfail,maxfail,pmU)
                
                failureVm = 1.0
                
                for i_e,v_e in enumerate(elements):
                    minfail = self.system.vmTemplate[chromosome['vmtype'][blockVmReplicas[v_e]]]['minfailrate']
                    maxfail = self.system.vmTemplate[chromosome['vmtype'][blockVmReplicas[v_e]]]['maxfailrate']
                    vmU = vmsusages['cpu'][blockVmReplicas[v_e]]
                    failureVm *= self.vmFailureCurve(minfail,maxfail,vmU)
                
                failureBlock *= (failurePm + failureVm)
                
            failureTotal += failureBlock
            i+=self.system.replicationFactor
         
        #To calculate the mean value
        failureTotal = failureTotal / (len(blockChromosome)/self.system.replicationFactor)

        return failureTotal

    def calculateUnavailability(self,chromosome):
        
#        print "solution"
#        print chromosome
        
        blockChromosome = chromosome['block']
        
        failureTotal = 0.0

        i=0
        limit = len(blockChromosome)
        while i < limit:
            
            #calculation of the unavailability of each set of replicas of the same block
            
            blockVmReplicas = blockChromosome[i:i+self.system.replicationFactor]
            
#            print "vms"
#            print blockVmReplicas
            
            blockPmReplicas = []
            
            #two list, one for the vms where the replicas are stored 
            #and another one for the pms where the replicas are stored
            
            for k in range(0,len(blockVmReplicas)):
                blockPmReplicas.append(chromosome['vm'][blockVmReplicas[k]])
                
            setPmReplicas = set(blockPmReplicas)

#            print "pms"
#            print blockPmReplicas
            
            failureBlock = 1.0
            
            for pm_i in setPmReplicas:
                
                elements=[y for y,x in enumerate(blockPmReplicas) if x==pm_i]
 #               print "iguales"
 #               print elements
                
                # i need to calculate failure(pm)+ PRODCT [failure(vms)] for each
                #machiner where a block is stored. I calculate the set of vms in
                # the same pm.
                
                failurePm = self.system.pmDefinition[blockPmReplicas[elements[0]]]['failrate']
                
                failureVm = 1.0
                
                for i_e,v_e in enumerate(elements):
                    failureVm *= self.system.vmTemplate[chromosome['vmtype'][blockVmReplicas[v_e]]]['failrate']
                
                failureBlock *= (failurePm + failureVm)
                
            failureTotal += failureBlock
            i+=self.system.replicationFactor
         
        #To calculate the mean value
        failureTotal = failureTotal / (len(blockChromosome)/self.system.replicationFactor)

        return failureTotal
        
        


#******************************************************************************************
#   END Unavailability calculation
#******************************************************************************************


#******************************************************************************************
#   ResourceWaste calculation
#******************************************************************************************

    def calculateResourceWaste(self, solutionPmsUsages):

        resourceWaste = 0.0        
        for i in range(0,self.system.pmNumber):
            cpuUsage = solutionPmsUsages['cpu'][i] / self.system.pmDefinition[i]['cpu']
            netUsage = solutionPmsUsages['net'][i] / self.system.pmDefinition[i]['net']
            ioUsage = solutionPmsUsages['io'][i] / self.system.pmDefinition[i]['io']
            
            datos = [cpuUsage, netUsage, ioUsage]           
            sumUsage = np.sum(datos)
            stdUsage = np.std(datos)
            
            if sumUsage > 0.0:
                resourceWaste += (stdUsage + self.system.epsilomResourceWaste) / sumUsage
            
        return resourceWaste

#******************************************************************************************
#   END ResourceWaste calculation
#******************************************************************************************


#******************************************************************************************
#   Energy calculation
#******************************************************************************************

    def calculateEnergy(self, solutionPmsUsages):

        energyConsumption = 0.0        
        for i in range(0,self.system.pmNumber):
            
            Prh = self.system.pmDefinition[i]['energyMax'] - self.system.pmDefinition[i]['eneryIdle']
            
            cpuUsage = solutionPmsUsages['cpu'][i] / self.system.pmDefinition[i]['cpu']
            netUsage = solutionPmsUsages['net'][i] / self.system.pmDefinition[i]['net']
            ioUsage = solutionPmsUsages['io'][i] / self.system.pmDefinition[i]['io']
            
            if cpuUsage <= self.system.pmDefinition[i]['energyLambda']:
                energyCPU = self.system.pmDefinition[i]['energyAlpha'] * Prh * cpuUsage
            else:
                energyCPU = self.system.pmDefinition[i]['energyBeta'] * Prh + (1 - self.system.pmDefinition[i]['energyBeta']) * Prh * cpuUsage

            energyNET = self.system.pmDefinition[i]['eneryGamma'] * Prh * netUsage
            energyIO = self.system.pmDefinition[i]['eneryDelta'] * Prh * ioUsage

#            print energyCPU            
#            print energyNET
#            print energyIO
#            print "======="

            
            energyConsumption += energyCPU + energyNET + energyIO
            
        return energyConsumption

#******************************************************************************************
#   END Energy calculation
#******************************************************************************************






#******************************************************************************************
#   Objectives and fitness calculation
#******************************************************************************************


    def calculateFitnessObjectives(self, pop, index):
        chr_fitness = {}
        chr_fitness["index"] = index
        
        chromosome=pop.population[index]
        pmsUsages=pop.pmsUsages[index]
        vmsUsages=pop.vmsUsages[index]
        
        if self.checkConstraints(pop,index):
            chr_fitness["energy"] = self.calculateEnergy(pmsUsages)
            chr_fitness["unavailability"] = self.calculateUnavailability2(chromosome,pmsUsages,vmsUsages)
            chr_fitness["resourcewaste"] = self.calculateResourceWaste(pmsUsages)
        else:
#            print ("not constraints")
            chr_fitness["energy"] = float('inf')
            chr_fitness["unavailability"] = float('inf')
            chr_fitness["resourcewaste"] = float('inf')
            
        return chr_fitness
        
    def calculatePopulationFitnessObjectives(self,pop):   
        for index,citizen in enumerate(pop.population):
            cit_fitness = self.calculateFitnessObjectives(pop,index)
            pop.fitness[index] = cit_fitness
            
        #print "[Fitness calculation]: Calculated **********************"       
        
         
    
#******************************************************************************************
#   END Objectives and fitness calculation
#******************************************************************************************


    def removeEmptyVms(self,chromosome):
        
#        print chromosome
        
        usedVms =  [ 0 for i in range(0,len(chromosome['vm']))]
        
        for i,v in enumerate(chromosome['block']):
            usedVms[v]=1
    
#        print usedVms
        
        vmShiftPosition = []
        shiftValue = 0
        quantityRemoved = 0
        for i,v in enumerate(usedVms):
            vmShiftPosition.append(shiftValue)
            if v==0:
                shiftValue += 1
                chromosome['vm'].pop(i-quantityRemoved)
                chromosome['vmtype'].pop(i-quantityRemoved)
                quantityRemoved +=1
        
#        print vmShiftPosition
        
        for i in range(0,len(chromosome['block'])):
            chromosome['block'][i] = chromosome['block'][i] - vmShiftPosition[chromosome['block'][i]]
            
        
#        print chromosome
        
        
            




#******************************************************************************************
#   NSGA-II Algorithm
#******************************************************************************************

            
    def dominates(self,a,b):
        #checks if solution a dominates solution b, i.e. all the objectives are better in A than in B
        Adominates = True
        #### OJOOOOOO Hay un atributo en los dictionarios que no hay que tener en cuenta, el index!!!
        for key in a:
            if key!="index":  #por ese motivo está este if.
                if b[key]<=a[key]:
                    Adominates = False
                    break
        return Adominates        

        
    def crowdingDistancesAssigments(self,popT,front):
        
        for i in front:
            popT.crowdingDistances[i] = float(0)
            
        frontFitness = [popT.fitness[i] for i in front]
        #OJOOOOOO hay un atributo en el listado que es index, que no se tiene que tener en cuenta.
        for key in popT.fitness[0]:
            if key!="index":   #por ese motivo está este if.
                orderedList = sorted(frontFitness, key=lambda k: k[key])
                
                popT.crowdingDistances[orderedList[0]["index"]] = float('inf')
                minObj = orderedList[0][key]
                popT.crowdingDistances[orderedList[len(orderedList)-1]["index"]] = float('inf')
                maxObj = orderedList[len(orderedList)-1][key]
                
                normalizedDenominator = float(maxObj-minObj)
                if normalizedDenominator==0.0:
                    normalizedDenominator = float('inf')
        
                for i in range(1, len(orderedList)-1):
                    popT.crowdingDistances[orderedList[i]["index"]] += (orderedList[i+1][key] - orderedList[i-1][key])/normalizedDenominator

    def calculateCrowdingDistances(self,popT):
        
        i=0
        while len(popT.fronts[i])!=0:
            self.crowdingDistancesAssigments(popT,popT.fronts[i])
            i+=1


    def calculateDominants(self,popT):
        
        for i in range(len(popT.population)):
            popT.dominatedBy[i] = set()
            popT.dominatesTo[i] = set()
            popT.fronts[i] = set()

        for p in range(len(popT.population)):
            for q in range(p+1,len(popT.population)):
                if self.dominates(popT.fitness[p],popT.fitness[q]):
                    popT.dominatesTo[p].add(q)
                    popT.dominatedBy[q].add(p)
                if self.dominates(popT.fitness[q],popT.fitness[p]):
                    popT.dominatedBy[p].add(q)
                    popT.dominatesTo[q].add(p)        

    def calculateFronts(self,popT):

        addedToFronts = set()
        
        i=0
        while len(addedToFronts)<len(popT.population):
            popT.fronts[i] = set([index for index,item in enumerate(popT.dominatedBy) if item==set()])
            addedToFronts = addedToFronts | popT.fronts[i]
            
            for index,item in enumerate(popT.dominatedBy):
                if index in popT.fronts[i]:
                    popT.dominatedBy[index].add(-1)
                else:
                    popT.dominatedBy[index] = popT.dominatedBy[index] - popT.fronts[i]
            i+=1        
            
    def fastNonDominatedSort(self,popT):
        
        self.calculateDominants(popT)
        self.calculateFronts(popT)
             
    def plotFronts(self,popT):  
      
        f = 0
        #fig = plt.figure()
        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
        while len(popT.fronts[f])!=0:
            thisfront = [popT.fitness[i] for i in popT.fronts[f]]

            a = [thisfront[i]["thresholdDistance"] for i,v in enumerate(thisfront)]
            b = [thisfront[i]["reliability"] for i,v in enumerate(thisfront)]

            #ax1 = fig.add_subplot(111)
            
            plt.scatter(a, b, s=10, color=next(colors), marker="o")
            #ax1.annotate('a',(a,b))
            f +=1
        
        plt.show()    
        
    def plot3DFronts(self,popT):  
          
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        f = 0

        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        #### quitarlo para que no sea solo el frente pareto 
        while len(popT.fronts[f])!=0:
            thisfront = [popT.fitness[i] for i in popT.fronts[f]]

            a = [thisfront[i]["mttr"] for i,v in enumerate(thisfront)]
            b = [thisfront[i]["latency"] for i,v in enumerate(thisfront)]
            c = [thisfront[i]["cost"] for i,v in enumerate(thisfront)]


            ax.scatter(a, b, c, color=next(colors), marker="o")
            f +=1
    
        ax.set_xlabel('mttr')
        ax.set_ylabel('latency')
        ax.set_zlabel('cost')
    
        plt3d.show()  
                
#******************************************************************************************
#   END NSGA-II Algorithm
#******************************************************************************************


#******************************************************************************************
#   Evolution based on NSGA-II 
#******************************************************************************************

    def generateRoundRobin1D(self, mylistsize, mylistrange):
        
        mylist = []
        rangelist = range(0,mylistrange)
        while len(mylist)<mylistsize:
            mylist += rangelist
        mylist=mylist[0:mylistsize]
        return mylist


    def generateRoundRobin2Dshuffle(self, mylistsize, piecesize, mylistrange):
        
        mylist = self.generateRoundRobin1D(mylistsize,mylistrange)


        i=0
        mylist2=[]
        while i<len(mylist):
            tmppiece=mylist[i:i+piecesize]
            self.rndPOP.shuffle(tmppiece)
            mylist2.append(tmppiece)
            i+=piecesize
        self.rndPOP.shuffle(mylist2)
        return mylist2

    def serialize2D(self, mylist2):
        
        finallist=[]
        for i in mylist2:
            for j in i:
                finallist.append(j)
        return finallist
    
    


    def generatePopulation(self,popT):
        
        for individual in range(self.populationSize):
            chromosome = {}
        
        
            if self.experimentScenario=='BOTH': 
                #vmNumber = self.system.vmNumber 
                vmNumber = max(self.rndPOP.randint(1,self.system.vmNumber),self.system.pmNumber)
                #TODO habria que pensar si fijamos el numero minimo de VM de otra forma
                #vmNumber = min(self.rnd.randint(1,vmNumber),self.system.pmNumber)


            if self.experimentScenario=='VM':
                vmNumber = max(self.rndPOP.randint(1,self.system.vmNumber),self.system.pmNumber)


            #if the optimization is done only by managing the blocks, the number of vms
            #is equal to the number of pms and there is a 1:1 mapping between pms and vms

            if self.experimentScenario=='BLOCK':
                vmNumber = self.system.pmNumber

            block = []

            if self.experimentScenario=='VM':
                block = self.generateRoundRobin1D(self.system.replicaNumber,vmNumber)
            
            if self.experimentScenario=='BLOCK' or self.experimentScenario=='BOTH':   
                block = self.generateRoundRobin2Dshuffle(self.system.replicaNumber,self.system.replicationFactor,vmNumber)
                block = self.serialize2D(block)
            
            #Si en lugar de round robin queremos aleatorio, descomentar la siguiente linea
            #block = [random.randint(0,vmNumber-1) for i in range(0,self.system.replicaNumber) ]
            
            vm = []
            vm = self.generateRoundRobin1D(vmNumber,self.system.pmNumber)
            
            
            
            vmtype = []
            vmtype = self.generateRoundRobin1D(vmNumber,len(self.system.vmTemplate))


            if self.experimentScenario=='BOTH':
                self.rndPOP.shuffle(vm)
                self.rndPOP.shuffle(vmtype)
                
               
            if self.experimentScenario=='VM':
                self.rndPOP.shuffle(vmtype)            
                self.rndPOP.shuffle(vm)            
            
            chromosome['block']=block
            chromosome['vm']=vm
            chromosome['vmtype']=vmtype
            
            self.removeEmptyVms(chromosome)
            
            popT.population[individual]=chromosome
            popT.dominatedBy[individual]=set()
            popT.dominatesTo[individual]=set()
            popT.fronts[individual]=set()
            popT.crowdingDistances[individual]=float(0)
            
        self.calculateSolutionsWorkload(popT)
        self.calculatePopulationFitnessObjectives(popT)
#        self.fastNonDominatedSort(popT)
#        self.calculateCrowdingDistances(popT)

    def tournamentSelection(self,k,popSize):
        selected = sys.maxint 
        for i in range(k):
            selected = min(selected,self.rndEVOL.randint(0,popSize-1))
        return selected
           
    def fatherSelection(self, orderedFathers): #TODO
        i = self.tournamentSelection(2,len(orderedFathers))
        return  orderedFathers[i]["index"]
        




    def evolveToOffspring(self):
        
        offspring = pop.POPULATION(self.populationSize)
        offspring.population = []

        orderedFathers = self.crowdedComparisonOrder(self.populationPt)
        

        #offspring generation

        while len(offspring.population)<self.populationSize:
            father1 = self.fatherSelection(orderedFathers)
            father2 = father1
            while father1 == father2:
                father2 = self.fatherSelection(orderedFathers)
            #print "[Father selection]: Father1: %i **********************" % father1
            #print "[Father selection]: Father1: %i **********************" % father2
            
            self.crossover(self.populationPt.population[father1],self.populationPt.population[father2],offspring.population)
        
        #offspring mutation
        
        for index,children in enumerate(offspring.population):
            if self.rndEVOL.uniform(0,1) < self.mutationProbability:
                self.mutate(children)
                #print "[Offsrping generation]: Children %i MUTATED **********************" % index
            
        #print "[Offsrping generation]: Population GENERATED **********************"  
        
        return offspring

        
    def crowdedComparisonOrder(self,popT):
        valuesToOrder=[]
        for i,v in enumerate(popT.crowdingDistances):
            citizen = {}
            citizen["index"] = i
            citizen["distance"] = v
            citizen["rank"] = 0
            valuesToOrder.append(citizen)
        
        f=0    
        while len(popT.fronts[f])!=0:
            for i,v in enumerate(popT.fronts[f]):
                valuesToOrder[v]["rank"]=f
            f+=1
             
        return sorted(valuesToOrder, key=lambda k: (k["rank"],-k["distance"]))



        
    def evolveAIA(self):
        
        offspring = pop.POPULATION(self.populationSize)
        offspring.population = []

        orderedFathers = self.crowdedComparisonOrder(self.populationPt)
        

        #offspring generation

        while len(offspring.population)<self.populationSize:
            father1 = self.fatherSelection(orderedFathers)
            children = copy.deepcopy(self.populationPt.population[father1])
            if self.rndEVOL.uniform(0,1) < self.mutationProbability:
                self.mutate(children)
            offspring.population.append(children)
            
        self.populationPt = offspring
       
        self.calculateSolutionsWorkload(self.populationPt)
        self.calculatePopulationFitnessObjectives(self.populationPt)
        self.fastNonDominatedSort(self.populationPt)
        self.calculateCrowdingDistances(self.populationPt)        
                 
            
        #print "[Offsrping generation]: Population GENERATED **********************"  
        
        return offspring


        
       
    def evolveNSGA2(self):
        
        offspring = pop.POPULATION(self.populationSize)
        offspring.population = []

        offspring = self.evolveToOffspring()
        
        self.calculateSolutionsWorkload(offspring)
        self.calculatePopulationFitnessObjectives(offspring)
        
        populationRt = offspring.populationUnion(self.populationPt,offspring)
        
        self.fastNonDominatedSort(populationRt)
        self.calculateCrowdingDistances(populationRt)
        
        orderedElements = self.crowdedComparisonOrder(populationRt)
        
        finalPopulation = pop.POPULATION(self.populationSize)
        
        for i in range(self.populationSize):
            finalPopulation.population[i] = populationRt.population[orderedElements[i]["index"]]
            finalPopulation.fitness[i] = populationRt.fitness[orderedElements[i]["index"]]
            finalPopulation.vmsUsages[i] = populationRt.vmsUsages[orderedElements[i]["index"]]

        for i,v in enumerate(finalPopulation.fitness):
            finalPopulation.fitness[i]["index"]=i        
        
        #self.populationPt = offspring
        self.populationPt = finalPopulation
        
        
        self.fastNonDominatedSort(self.populationPt)
        self.calculateCrowdingDistances(self.populationPt)
        

#        self.plot3DFronts(self.populationPt)
        #self.plotFronts(self.populationPt)
        
        

 
        
       
        

#******************************************************************************************
#  END Evolution based on NSGA-II 
#******************************************************************************************





#blocksPerFilePerMapReduceJobs1 = np.array([[2,3,1],[5,5,0],[3,4,1],[8,3,1]])
#blocksPerFilePerMapReduceJobs = np.array([2,3,1])
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([5,5,0])))
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([3,4,1])))
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([8,3,1])))

#definition of the files for each MapReduce job. 1:1 jobs:files

#nodenumber = 50
#populationSize = 10
#population = []
#
#for i in range(populationSize):
#    chromosome = {}
#    fileId = 0
#    blockId = 0
#    
#    for (MRjobID,MRjobFileID), value in np.ndenumerate(blocksPerFilePerMapReduceJobs):
#        for blockId in range(value): #iteration of the three files of each mapreducejob
#            replicationFactor = int(round(np.random.normal(3.0, 0.4))) # mean and standard deviation
#            if replicationFactor>nodenumber: #when the block replica is bigger than total node number, is set to the maximum
#                replicationFactor=nodenumber        
#            try:
#                allocation=self.rnd.sample(range(1, nodenumber), replicationFactor) #random selection of the node to place the blocks
#                #selection of the nodes to be read by the tasks of the mapreduce job            
#                readallocation=[]
#                readnode = self.rnd.choice(allocation)
#                allocation.remove(readnode)
#                readallocation.append(readnode)
#            except ValueError:
#                print('Sample size exceeded population size.')
#            chromosome[fileId,blockId] = {"filetype": MRjobFileID % 3 , "wnode":allocation,"rnode":readallocation}
#            blockId+=1
#        fileId+=1
#    population.append(chromosome)
#    
#
#chromosome


#
#for fileId,totalBlock in enumerate(blocksPerFile):
#    for blockId in range(totalBlock):
#        chromosome[fileId,b] = {"wnode":[1,2,3],"rnode":[]}

