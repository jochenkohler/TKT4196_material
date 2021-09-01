#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 16:53:20 2020

@author: jorgemen
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.stats
import warnings
import pandas as pd
import seaborn as sns

fontsizes=18
plt.rcParams.update({'font.size': fontsizes})
plt.rcParams.update({"font.family": "serif"})
plt.rcParams.update({"mathtext.fontset" : "cm"})
plt.rcParams.update({'font.serif': 'Times New Roman'})
plt.close('all')


# =============================================================================
# INPUT
n_sim = int(1E7)                 # Number of simulations (> 1e4 due to plotting)


l = 10000                        # [mm] beam length
h = 200                          # [mm] cross-section height and width
kmod = 1

A = h**2                         # Area
I = h**4/12                      # Moment of inertia
W = h**3/6                       # Cross-section modulus

# Create dictonary to organize random variables
def dicentry(key,mu,sigma,dtype,order):
    """create dictionary entry"""    
    X[key] = {}
    X[key]['theta'] = [mu,sigma]
    X[key]['dist'] = dtype  
    X[key]['ordering'] = order
    return X

X = {}
X = dicentry('Fm',20.,5.,'lognormal',int(0))           # [MPa] material strength
X = dicentry('Fc',15.,3.75,'lognormal',int(1))         # [MPa] material strength
X = dicentry('E',11000.,1430.,'lognormal',int(2))      # [MPa] Elasticity modulus
X = dicentry('G',10.15e3,1.03e3,'normal',int(3))       # [N] Elasticity modulus
X = dicentry('Q',28.23e3,0.4*28.23e3,'gumbel',int(4))  # [N] Elasticity modulus
X = dicentry('xi',0.,3.,'normal',int(5))               # [mm] mean initial bow

C = np.array([[1, 0.8, 0.8, 0,0,0],
              [0.8, 1, 0.6, 0,0,0],
              [0.8, 0.6, 1, 0,0,0],
              [0,   0,   0, 1,0,0],
              [0,   0,   0, 0,1,0],
              [0,   0,   0, 0,0,1]])

# =============================================================================
# Find parameters of distribitions associated with specified mean and std
def distparam(dist):
        # Compute the distribution parameters of distribution specified in dist
        # given mean and standard deviation
        def logn2param(theta):
            # Created by Jorge Mendoza February, 2020
            # Takes the parameters of the log-normal distribution and transforms them
            # to the parameters of the associated normal distribution
            if theta[0]>0:
                par1 = np.log( (theta[0]**2) / np.sqrt(theta[1]**2 + theta[0]**2) )
                par2 = np.sqrt( np.log( theta[1]**2/theta[0]**2 + 1) )
            else:
                raise Exception('Lognormal par1 needs be larger than 0')
            return [par1,par2]
        def norm2param(theta):
            return [theta[0],theta[1]]
        def gumb2norm(theta):
            # Created by Jorge Mendoza September, 2018
            # Takes the expected value m and standard devatiation s of a Gumbel 
            # distribution and finds the scale and shape parameters (a and b)
            # F = exp( -exp( -a*(x-b) ) )
            a = np.pi/( np.sqrt(6)*theta[1] )
            b = theta[0] - 0.5772156649/a
            return [a,b]
        switcher={
                'normal':norm2param,
                'lognormal':logn2param,
                'gumbel':gumb2norm
                }
        return switcher.get(dist,"Distribution out of scope")
    
def distinv(dist):
        def norminv(u,param):
            sp.stats.norm.ppf
            x  = sp.stats.norm.ppf(u,param[0],param[1])
            return x
        def gumbinv(u,param):
            x = param[1] - 1/param[0] * np.log( -np.log( u ) )
            return x
        def logninv(u,param):
            x  = sp.stats.lognorm(param[1],scale=np.exp(param[0])).ppf(u)
            return x
        switcher={
                'normal': norminv,
                'lognormal': logninv,
                'gumbel': gumbinv,
                }
        return switcher.get(dist,"Distribution out of scope")
    
def distMCS(dist):
        def gumbrnd(param,n_sim):
            x = distinv('gumbel')(np.random.uniform(size=n_sim),param[0],param[1])
            return x
        switcher={
                'normal': np.random.normal,
                'lognormal': np.random.lognormal,
                'gumbel': gumbrnd,
                }
        return switcher.get(dist,"Distribution out of scope")

# Step 1 - Draw uncorrelated samples from standard normal distribution
X1 = np.random.randn(len(C),n_sim)

# Step 2 - Compute Cholesky transformation of the covariance matrix
R = np.linalg.cholesky(C)
# Step 3 - Draw correlated normal distributed samples
Y = np.dot(R,X1)
# Step 4 - Transform to correlated uniform distributed samples by U = PHI(Y)
U = sp.stats.norm.cdf(Y)
# Step 5 - Transform to variable distribution by x = F^-1(U)
n_simplot = int(1e4)
Z = np.zeros((U.shape[0],n_simplot))
idx = 0
for key in X:
    X[key]['param'] = distparam(X[key]['dist'])(X[key]['theta'])
    X[key]['rndnum'] = distinv(X[key]['dist'])(U[X[key]['ordering']],X[key]['param'])
    Z[idx] = X[key]['rndnum'][0:n_simplot]
    idx += 1
    
x_cor = pd.DataFrame(Z.T)                   # Transpose

sns.pairplot(x_cor)    

# Verify correlation of samples
if 0.8 != round(np.corrcoef(X['Fm']['rndnum'],X['Fc']['rndnum'])[0][1],1):
    warnings.warn('Wrong correlation between Fm-Fc')

if 0.8 != round(np.corrcoef(X['Fm']['rndnum'],X['E']['rndnum'])[0][1],1):
    warnings.warn('Wrong correlation between Fm-E')

if 0.6 != round(np.corrcoef(X['Fc']['rndnum'],X['E']['rndnum'])[0][1],1):
    warnings.warn('Wrong correlation between Fc-E')


# =============================================================================
# Solution of structural reliability problem
n = X['G']['rndnum'] + X['Q']['rndnum']
nr = kmod * X['Fc']['rndnum']  * A
mr = kmod * X['Fm']['rndnum'] *  W
ncrit = np.pi**2 * X['E']['rndnum'] * I / l**2
alpha = 1 / (1 - n/ncrit)

g1 = 1 - (n/nr)**2 - n*np.abs(X['xi']['rndnum']*alpha)/mr # LSF1
g2 = 1 - n/nr                                             # LSF2
g3 = 1 - n/ncrit                                          # LSF3

# % Count the number of failures
fails = np.zeros(n_sim);
fails[np.nonzero(np.logical_or(g1<=0, g2<=0, g3<=0))[0]] = 1;
Pf = np.sum(fails)/n_sim

# Check convergence
m = int(n_sim/500)
t = 0
plt_range = np.arange(m-1,n_sim,m)
nn = np.zeros(len(plt_range))
Pf_plt = np.zeros(len(plt_range))
beta_plt = np.zeros(len(plt_range))
cov = np.zeros(len(plt_range))
for j in plt_range:
    nn[t] = j;
    Pf_plt[t] = np.mean(fails[0:j])
    beta_plt[t] = -sp.stats.norm.ppf(Pf_plt[t])
    cov[t] = 1 / Pf_plt[t] * np.sqrt((Pf_plt[t] - Pf_plt[t]**2)/j)
    t = t+1

plt.figure()
plt.subplot(121)
plt.plot(nn, beta_plt,'k')
plt.plot(np.array([0,n_sim]),np.array([beta_plt[t-1],beta_plt[t-1]]),'--k')
plt.ylabel(r'$\beta$')
plt.xlabel(r'$\#$ simulations')
plt.xlim(0,n_sim)
plt.ylim(0,5)
plt.tight_layout()
plt.show()
plt.subplot(122)
plt.plot(nn, cov,'k')
plt.ylabel('Coeff. of variation')
plt.xlabel(r'$\#$ simulations')
plt.xlim(0,n_sim)
plt.ylim(0)
plt.tight_layout()
plt.show()


print("Probability of failure = {pf:.2e}\n".format(pf=float(Pf)))
print("beta = {b:.2f}\n".format(b=float(beta_plt[t-1])))

