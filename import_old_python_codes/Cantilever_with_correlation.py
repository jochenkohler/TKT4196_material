#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:43:53 2020

@author: jorgemen
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.stats

fontsizes=18
plt.rcParams.update({'font.size': fontsizes})
plt.rcParams.update({"font.family": "serif"})
plt.rcParams.update({"mathtext.fontset" : "cm"})
plt.rcParams.update({'font.serif': 'Times New Roman'})
plt.close('all')


#==============================================================================
# INPUT
#==============================================================================
# Geometry 
l = 4e3                                 # [mm] 
W = 1.5e6                               # [mm^3] 

# Material resistance
mu_Fm = 167                             # [N/mm^2]      
sigma_Fm = 20                           # [N/mm^2]    

# Loads
mu_P1 = 10e3                            # [N]    
sigma_P1 = 3e3                          # [N]  

mu_P2 = 10e3                            # [N]    
sigma_P2 = 3e3                          # [N]  

#==============================================================================
# Correlated variables
E = np.array([mu_Fm, mu_P1, mu_P2])
a = np.array([W, -l, -2*l])
at = np.transpose(a)

rhoV = np.arange(-1, 1, 0.1)
rhoV[np.abs(rhoV.real) < 1e-15] = 0.0
betalist = []
for rho in rhoV:
    Cx = np.array([[sigma_Fm**2, 0, 0],
                   [0, sigma_P1**2, sigma_P1*sigma_P2*rho],
                   [0, sigma_P1*sigma_P2*rho, sigma_P2**2]])
    betalist.append(np.dot(at,E)/np.sqrt(np.dot(np.dot(at,Cx),a)))

# Uncorrelated case
beta_rho0 =  np.array(betalist)[np.nonzero(rhoV==0.)[0]]                # Reliability index

print("Reliability index beta for uncorrelated variables {b:.2f}\n".format(b=float(beta_rho0)))

# Plot
fig, ax = plt.subplots()
ax.plot(rhoV,betalist,'k')
ax.plot(0,beta_rho0,'or')
ax.text(0,beta_rho0,'({r:.0f},{b:.2f})\n'.format(r=0,b=float(beta_rho0)))
ax.set_xlabel(r'$\rho$')
ax.set_ylabel(r'$\beta$')
ax.set_xlim(-1,1)
plt.tight_layout()
plt.show()

