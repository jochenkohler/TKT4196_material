#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 14:30:15 2020

@author: jorgemen
"""

import numpy as np
import scipy as sp
import scipy.stats as sp_s
import matplotlib.pyplot as plt
import sympy as sy
import sympy.stats as sy_s

def inputgen():
    # Deterministic parameters
    L = 5                            # [m] Thickness of the clay layer
    
    # Random variables
    X = {}
               
    # X[]['dist'] = {}             # Distribution type, e.g. 'normal','lognormal','gumbel'
    # X[]['mu'] = {}               # Mean value
    # X[]['sigma'] = {}            # Standard deviation
    # X[]['param'] = {}             # Parameter 1 from distribution
    
    # deltat: toe bearing resistance model uncertainty
    X['X1'] = {}
    X['X1']['dist'] = 'normal'             
    X['X1']['mu'] = 1.12
    X['X1']['sigma'] = 0.32*X['X1']['mu']         
    
    # deltaf: shaft resistance model uncertainty
    X['X2'] = {}   
    X['X2']['dist'] = 'normal'             
    X['X2']['mu'] = 1.1
    X['X2']['sigma'] = 0.2*X['X2']['mu']  
    
    # N1: CPT test in first layer
    X['X3'] = {}    
    X['X3']['dist'] = 'lognormal'             
    X['X3']['mu'] = 40
    X['X3']['sigma'] = 0.3*X['X3']['mu']
    
    # N2: CPT test in second layer
    X['X4'] = {}  
    X['X4']['dist'] = 'lognormal'             
    X['X4']['mu'] = 60
    X['X4']['sigma'] = 0.2*X['X4']['mu']
    
    # G: selfweight [kN]
    X['X5'] = {}  
    X['X5']['dist'] = 'gumbel'             
    X['X5']['mu'] = 400
    X['X5']['sigma'] = 0.1*X['X5']['mu']
    
    # Q: variable load [kN]
    X['X6'] = {}  
    X['X6']['dist'] = 'gumbel'             
    X['X6']['mu'] = 500
    X['X6']['sigma'] = 0.35*X['X6']['mu']
    
    # Cost model 
    Cost = {}
    Cost['C0'] = 50000                       # [NOK] Fixed construction cost
    Cost['c_pile'] = 10000                    # [NOK/m^3] Cost of pile per cubic meter
    Cost['Nf'] = 5                           # Expected number of fatalities given failure
    Cost['gamma'] = 0.03                     # Interest rate
    Cost['gamma_s'] = 0.025                  # Societal interest rate
    Cost['T'] = 50                           # Structural design life
    Cost['SWTP'] = 32100000                  # [NOK] Societal willingness to pay for saving a statistical life 
    Cost['H'] = 20*Cost['C0']                # [NOK] Cost of failure 
    Cost['D'] = 2*Cost['C0']                 # [NOK] Demolition costs

    return X, L, Cost