#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:56:02 2017

@author: carlos
"""

from datetime import datetime
import os
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt3d
import pickle
from scipy.stats.mstats import gmean


class PLOTS2:
    

    def __init__(self,folder):
        
        

        self.totalplots = []
        self.totalplots.append({"decisionvariables": 'BOTH' ,"optimization": 'NSGA2' ,"configuration": 'lowScale', "color": 'yellow', "marker": '*'})
        self.totalplots.append({"decisionvariables": 'VM' ,"optimization": 'NSGA2' ,"configuration": 'lowScale', "color": 'green', "marker": 'o'})
        self.totalplots.append({"decisionvariables": 'BLOCK' ,"optimization": 'NSGA2' ,"configuration": 'lowScale', "color": 'red', "marker": '^'})
        self.totalplots.append({"decisionvariables": 'BOTH' ,"optimization": 'AIA' ,"configuration": 'lowScale', "color": 'blue', "marker": 's'})


        self.folderpath=folder
        
        self.numberofdatafile = len(os.listdir(self.folderpath))
        
        self.valuesToPlot = 'ABSOLUTE' #ABSOLUTE or FITNESS
        #self.numberofdatafile = 6
#        self.filesnamesEvol = []
#        self.filesnamesFinal = []
#        
#        
#        
#        self.filesnamesFinal.append('0-BOTH-NSGA2-lowScale-lastGeneration.pkl')
#        self.filesnamesEvol.append('0-BOTH-NSGA2-lowScale-selectedSolution.pkl')
#        self.filesnamesFinal.append('1-VM-NSGA2-lowScale-lastGeneration.pkl')
#        self.filesnamesEvol.append('1-VM-NSGA2-lowScale-selectedSolution.pkl')
#        self.filesnamesFinal.append('2-BLOCK-NSGA2-lowScale-lastGeneration.pkl')
#        self.filesnamesEvol.append('2-BLOCK-NSGA2-lowScale-selectedSolution.pkl')
#        self.filesnamesFinal.append('3-BLOCK-AIA-lowScale-lastGeneration.pkl')
#        self.filesnamesEvol.append('3-BLOCK-AIA-lowScale-selectedSolution.pkl')
#        
        

        self.resultvalues = []
        
        
        for i,v in enumerate(self.totalplots):
            
            i_resultvalues={"name": '' ,"energy": [] ,"resourcewaste": [] ,"unavailability":  [], "vm" : [], "fitness" : []   }
            
            for j in range(0,self.numberofdatafile):
                myfilename=self.folderpath+'/'+str(j)+'-'+v['decisionvariables']+'-'+v['optimization']+'-'+v['configuration']+'-selectedSolution.pkl'
                isthefirst = True
                if os.path.exists(myfilename):
                    print "Loadind file "+myfilename+"..."
                    energy_j = []
                    resourcewaste_j = []
                    unavailability_j = []
                    vm_j = []
                    fitness_j=[]
                    pkl_file = open(myfilename, 'rb')
                    variable = pickle.load(pkl_file)
                    pkl_file.close()
        
                    
                    for j in variable:
                        if self.valuesToPlot == 'ABSOLUTE':
                            energy_j.append(j['fitness']['energy'])
                            resourcewaste_j.append(j['fitness']['resourcewaste'])
                            unavailability_j.append(j['fitness']['unavailability'])
                            vm_j.append(len(j['population']['vm']))
                        if self.valuesToPlot == 'FITNESS':
                            energy_j.append(j['fitnessNormalized']['energy'])
                            resourcewaste_j.append(j['fitnessNormalized']['resourcewaste'])
                            unavailability_j.append(j['fitnessNormalized']['unavailability'])
                            vm_j.append(len(j['population']['vm'])) 
                            fitness_j.append(j['fitnessNormalized']['fitness'])
                    if isthefirst:
                        isthefirst=False
                        energy = np.array([energy_j])
                        resourcewaste = np.array([resourcewaste_j])
                        unavailability = np.array([unavailability_j])
                        vm = np.array([vm_j])
                        fitness = np.array([fitness_j])
                    else:
                        energy = np.append(energy,[energy_j],axis=0)
                        resourcewaste = np.append(resourcewaste,[resourcewaste_j],axis=0)
                        unavailability = np.append(unavailability,[unavailability_j],axis=0)
                        vm = np.append(vm,[vm_j],axis=0)  
            i_resultvalues['energy']=np.mean(energy,axis=0) 
            i_resultvalues['resourcewaste']=np.mean(resourcewaste,axis=0)
            i_resultvalues['unavailability']=np.mean(unavailability,axis=0)
            i_resultvalues['vm']=np.mean(vm,axis=0)
            if self.valuesToPlot == 'FITNESS':
                i_resultvalues['fitness']=np.mean(fitness,axis=0)
#            i_resultvalues['energy']=np.median(np.sort(energy,axis=0),axis=0) 
#            i_resultvalues['resourcewaste']=np.median(np.sort(resourcewaste,axis=0) ,axis=0)
#            i_resultvalues['unavailability']=np.median(np.sort(unavailability,axis=0) ,axis=0)
#            i_resultvalues['vm']=np.median(np.sort(vm,axis=0) ,axis=0)
            
#            i_resultvalues['energy']=gmean(energy,axis=0)
#            i_resultvalues['resourcewaste']=gmean(resourcewaste,axis=0)
#            i_resultvalues['unavailability']=gmean(unavailability,axis=0)
#            i_resultvalues['vm']=gmean(vm,axis=0)
            
            
            #i_resultvalues['name']=v['decisionvariables']+'-'+v['optimization']+'-'+v['configuration']
            i_resultvalues['name']=i
            self.resultvalues.append(i_resultvalues)
            
            
     
            

    def plotfitEvolution(self):
        
        font = {'size'   : 18}

        matplotlib.rc('font', **font)
        
                
        for dimensionToPlot in ['energy','unavailability','resourcewaste','vm','fitness']:
            
            
            figtitleStr = dimensionToPlot
        #ejemplo sacado de http://matplotlib.org/users/text_intro.html    
            fig = plt.figure()
       #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
            fig.suptitle(figtitleStr, fontsize=18)
            ax = fig.add_subplot(111)
            fig.subplots_adjust(bottom=0.15)
       #    ax.set_title('axes title')
            ax.set_xlabel('Generations', fontsize=18)
            ax.set_ylabel(dimensionToPlot, fontsize=18)
            plt.gcf().subplots_adjust(left=0.18)
            plt.gcf().subplots_adjust(right=0.95)
            
            
            for v in self.resultvalues:
                ax.plot(v[dimensionToPlot], label=self.totalplots[v['name']]['decisionvariables']+'-'+self.totalplots[v['name']]['optimization']+'-'+self.totalplots[v['name']]['configuration'], linewidth=2.5,color=self.totalplots[v['name']]['color'],marker=self.totalplots[v['name']]['marker'],markersize=10,markevery=30)
            
            
#            if 'max' in seriesToPlot:
#                ax.plot(mydataSerie['max'], label='max', linewidth=2.5,color='yellow',marker='*',markersize=10,markevery=30)
#            if 'mean' in seriesToPlot:    
#                ax.plot(mydataSerie['mean'], label='mean', linewidth=2.5,color='green',marker='o',markersize=10,markevery=30)
#            if 'min' in seriesToPlot:
#                ax.plot(mydataSerie['min'], label='min', linewidth=2.5,color='red',marker='^',markersize=10,markevery=30)
#            if 'single' in seriesToPlot:
#                ax.plot(mydataSerie['sfit'], label='weighted', linewidth=2.5,color='blue',marker='s',markersize=10,markevery=30)    
            plt.legend(loc="upper center", ncol=2, fontsize=14) 
        #upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
            #plt.legend()
       #    plt.show()
       
#            plt.ylim(ymin=minYaxes[plotId])
       
       
            plt.grid()
            fig.savefig(self.folderpath+'/'+dimensionToPlot+'.pdf')
            plt.close(fig)

 