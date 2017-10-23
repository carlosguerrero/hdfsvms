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


class PLOTS:
    

    def __init__(self,folder):
        
        

        self.totalplots = []
        self.totalplots.append({"decisionvariables": 'BOTH' ,"optimization": 'NSGA2' ,"configuration": 'lowScale', "color": 'yellow', "marker": '*'})
        #self.totalplots.append({"decisionvariables": 'VM' ,"optimization": 'NSGA2' ,"configuration": 'lowScale', "color": 'green', "marker": 'o'})
        #self.totalplots.append({"decisionvariables": 'BLOCK' ,"optimization": 'NSGA2' ,"configuration": 'lowScale', "color": 'red', "marker": '^'})
        self.totalplots.append({"decisionvariables": 'BLOCK' ,"optimization": 'AIA' ,"configuration": 'lowScale', "color": 'blue', "marker": 's'})


        self.folderpath=folder
        
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

            
            pkl_file = open(self.folderpath+'/'+str(i)+'-'+v['decisionvariables']+'-'+v['optimization']+'-'+v['configuration']+'-selectedSolution.pkl', 'rb')
            variable = pickle.load(pkl_file)
            pkl_file.close()

            i_resultvalues={"name": '' ,"energy": [] ,"resourcewaste": [] ,"unavailability":  [], "vm" : []  }

            i_resultvalues['name']= i
            
            for j in variable:
                i_resultvalues['energy'].append(j['fitness']['energy'])
                i_resultvalues['resourcewaste'].append(j['fitness']['resourcewaste'])
                i_resultvalues['unavailability'].append(j['fitness']['unavailability'])
                i_resultvalues['vm'].append(len(j['population']['vm']))
            self.resultvalues.append(i_resultvalues)
            
            
     
            

    def plotfitEvoluation(self):
        
        font = {'size'   : 18}

        matplotlib.rc('font', **font)
        
                
        for dimensionToPlot in ['energy','unavailability','resourcewaste','vm']:
            
            
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
#            plt.legend(loc="upper center", ncol=3, fontsize=14) 
        #upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
            #plt.legend()
       #    plt.show()
       
#            plt.ylim(ymin=minYaxes[plotId])
       
       
            plt.grid()
            fig.savefig(self.folderpath+'/'+dimensionToPlot+'.pdf')
            plt.close(fig)

 