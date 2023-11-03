"""@author: EvangeliaSamara, Sept 21/2023"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime
import decimal
from decimal import Decimal


def calculate_dtw_cost(real_stand, model_stand):
	'''
    	Computes DTW scores and eventually the SSF Skill Score for the evaluation of time series.
	Lists must be same size and have matching indicies.

            Parameters:
                    pred (type: list): list of your predicted time series
                    obs (type: list): list of your observed time series

            Returns:
                    DTW score
    '''
	cost = np.zeros((len(real_stand), len(model_stand))) 
	DTW = np.ones((len(real_stand)+1, len(model_stand)+1))
	DTW = DTW*np.infty 

	w = np.max([300, abs(len(real_stand)-len(model_stand))])
 
	DTW[0,0] = cost[0,0] 
        
	########## calculate all the other elements #############
	for i in range(1, len(real_stand)+1):
    		for j in range(np.max([1, i-w]), np.min([len(model_stand)+1, i+w])):   #### applying also a small punishment to the non-diagonal elements
        		cost[i-1,j-1] = abs(model_stand[j-1]-real_stand[i-1])
        		DTW[i,j] = min(DTW[i-1, j-1], DTW[i-1, j], DTW[i, j-1]) + cost[i-1,j-1] 
        
	DTW = DTW[1:,1:]
	DTW_score=DTW[len(real_stand)-1, len(model_stand)-1]     
	
	return DTW_score


def calculate_dtw_cost_ref(real_stand, model_stand):
        '''
        Computes DTW score between obs and the reference-case scenario
        Lists must be same size and have matching indicies.

            Parameters:
                    pred (type: list): list of your predicted time series
                    obs (type: list): list of your observed time series

            Returns:
                    DTW score between obs and the reference-case scenario 
    '''
        cost = np.zeros((len(real_stand), len(model_stand)))
        DTW = np.ones((len(real_stand)+1, len(model_stand)+1))
        DTW = DTW*np.infty

        w = np.max([300, abs(len(real_stand)-len(model_stand))])

        DTW[0,0] = cost[0,0]

        ########## calculate all the other elements #############
        for i in range(1, len(real_stand)+1):
                for j in range(np.max([1, i-w]), np.min([len(model_stand)+1, i+w])):   #### applying also a small punishment to the non-diagonal elements
                        cost[i-1,j-1] = abs(model_stand[j-1]-real_stand[i-1])
                        DTW[i,j] = min(DTW[i-1, j-1], DTW[i-1, j], DTW[i, j-1]) + cost[i-1,j-1]

        DTW = DTW[1:,1:]
        DTW_score_ref=DTW[len(real_stand)-1, len(model_stand)-1]

        return DTW_score_ref




def SSF_SkillScore(DTW_score1, DTW_score2):
	
	SSF = DTW_score1/DTW_score2

	return SSF




# This is the first function to plot
def path_DTW(model_stand, real_stand):
    
	cost = np.zeros((len(real_stand), len(model_stand)))
	DTW = np.ones((len(real_stand)+1, len(model_stand)+1))
	DTW = DTW*np.infty

	w = np.max([300, abs(len(real_stand)-len(model_stand))])
	DTW[0,0] = cost[0,0]

	########## calculate all the other elements #############
	for i in range(1, len(real_stand)+1):
		for j in range(np.max([1, i-w]), np.min([len(model_stand)+1, i+w])):   #### applying also a small punishment to the non-diagonal elements
			cost[i-1,j-1] = abs(model_stand[j-1]-real_stand[i-1])
			DTW[i,j] = min(DTW[i-1, j-1], DTW[i-1, j], DTW[i, j-1]) + cost[i-1,j-1]

	DTW = DTW[1:,1:]
	DTW_score=DTW[len(real_stand)-1, len(model_stand)-1]

	path = [[len(model_stand)-1, len(real_stand)-1]]
	DTW_new = 0
	i = len(real_stand)-1
	j = len(model_stand)-1
	while i>0 or j>0:
		if i==0:
			j = j - 1
		elif j==0:
			i = i - 1
		else:
			if DTW[i-1, j] == min(DTW[i-1, j-1], DTW[i-1, j], DTW[i, j-1]):
				i = i - 1
			elif DTW[i, j-1] == min(DTW[i-1, j-1], DTW[i-1, j], DTW[i, j-1]):
				j = j-1
			else:
				i = i - 1
				j= j- 1
		path.append([j, i])
	for [real_stand, model_stand] in path:
		DTW_new = DTW_new +cost[model_stand, real_stand]
	return path, DTW_new


def plot_dtw(real_stand, model_stand, ref):
	plt.figure(figsize=(15,5))
	plt.plot(real_stand, 'b-', label = 'Wind', linewidth=7)
	plt.plot(model_stand, 'r-' ,label='EUHFORIA', linewidth=3)
	DTW_score_ref = calculate_dtw_cost_ref(real_stand, ref)
	DTW_score = calculate_dtw_cost(real_stand, model_stand)
	plt.text(0.55, 0.9, r'DTW$_{{\rm score}}$$(O,M) = {}$'.format(round(DTW_score, 2)), fontsize=25, color='k', transform=plt.gca().transAxes)

	SSF=DTW_score/DTW_score_ref
	plt.text(0.55, 0.8, r'SSF = {} '.format(round(SSF, 2)), fontsize=25, color='k', transform=plt.gca().transAxes)

	plt.legend(fontsize=20, ncol=1, bbox_to_anchor=[-0.01, 1.5],loc='upper left');paths = path_DTW(model_stand, real_stand)[0]
	paths = path_DTW(model_stand, real_stand)[0]
	for [map_x, map_y] in paths:
    		plt.plot([map_x, map_y], [model_stand[map_x], real_stand[map_y]], 'g', linewidth=0.1)

	import datetime
	plt.xlim(0,len(model_stand))
	plt.ylim(250,750)
	plt.xticks(fontsize=25)
	plt.yticks(fontsize=25)
	plt.ylabel(r'V$_{b}$ (km/s)', fontsize=28)
	plt.xlabel('Time elements', fontsize=32)
