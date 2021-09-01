#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 14:09:45 2020

@author: jorgemen
"""


import numpy as np
import scipy as sp
from tktstat import distparam,x2u,xdiffu,form,distinv

class opt_form(object):
    
    def __init__(self,X,L,Cost):
        self.X = X
        self.L = L
        self.Cost = Cost

    def inputpostproc(self):
        """Add new entries to input dictionary"""    
        for key in self.X:
            dist = self.X[key]['dist']
            mu = self.X[key]['mu']
            sigma = self.X[key]['sigma']
            par1,par2 = distparam(dist)(mu,sigma)
            
            self.X[key]['param'] = {}
            self.X[key]['param'][0],self.X[key]['param'][1] = par1,par2
            self.X[key]['x2u'] = {}
            self.X[key]['x2u'] = x2u(dist,[par1,par2])
            self.X[key]['xdiffu'] = xdiffu(dist,[par1,par2])
        return
    
    def gX(self,x,phi,h):
        lsf = (np.pi/4*10*5) * phi**2 * x[0] * x[3] \
        + (np.pi*10*0.4) * phi * x[1] * self.L * x[2] \
        + (np.pi*5*0.4) *  phi * x[1] * (h-self.L) * x[3] \
        - (np.pi*25/4)* h * phi**2 - x[4] - x[5]
        return lsf
    
    def gU(self,u,phi,h):
        lsf = self.gX([self.X['X1']['x2u'](u[0]),self.X['X2']['x2u'](u[1]),self.X['X3']['x2u'](u[2]),self.X['X4']['x2u'](u[3]),self.X['X5']['x2u'](u[4]),self.X['X6']['x2u'](u[5])],phi,h)
        return lsf

    def alphanext(self,phi,h):
        # Gradient of lsf
        gdiff = []
        gdiff.append(lambda u: 25/2*np.pi*phi**2*self.X['X1']['xdiffu'](u[0])*self.X['X4']['x2u'](u[3]))
        gdiff.append(lambda u: 4 * np.pi * phi * self.X['X2']['xdiffu'](u[1]) * self.L * self.X['X3']['x2u'](u[2]) +  2*np.pi*phi*self.X['X2']['xdiffu'](u[1])*(h-self.L)*self.X['X4']['x2u'](u[3]))
        gdiff.append(lambda u: 4*np.pi*phi*self.X['X2']['x2u'](u[1])*self.L* self.X['X3']['xdiffu'](u[2]))
        gdiff.append(lambda u: (25/2*np.pi*phi**2*self.X['X1']['x2u'](u[0])+2*np.pi*phi*self.X['X2']['x2u'](u[1])*(h-self.L))*self.X['X4']['xdiffu'](u[3]))
        gdiff.append(lambda u: -self.X['X5']['xdiffu'](u[4]))
        gdiff.append(lambda u: -self.X['X6']['xdiffu'](u[5]))
           
        k = lambda u: np.sqrt(gdiff[0](u)**2+gdiff[1](u)**2+gdiff[2](u)**2+gdiff[3](u)**2+gdiff[4](u)**2+gdiff[5](u)**2)
    
        anext = []
        anext.append(lambda u: -gdiff[0](u)/k(u))
        anext.append(lambda u: -gdiff[1](u)/k(u))
        anext.append(lambda u: -gdiff[2](u)/k(u))
        anext.append(lambda u: -gdiff[3](u)/k(u))
        anext.append(lambda u: -gdiff[4](u)/k(u))
        anext.append(lambda u: -gdiff[5](u)/k(u))
        # anext = np.zeros_like(gdiff)
        # for ii in np.arange(0, len(gdiff)):
        #     anext[ii] = lambda u: -gdiff[ii](u)/k(u)
            # anext.append(lambda u: -gdiff[ii](u)/k(u))
        return anext


    def f1(self,phi,h):
        
        self.inputpostproc()
    
        gab = lambda a,b: self.gU(a*b,phi,h)                        # lsf as a funciton of alpha and beta
        anext = self.alphanext(phi,h)
    
        alpha0 = 1/np.sqrt(6) * np.array([-1,-1,-1,-1,1,1])     # Initial alpha-vector
    
        beta,alpha = form(gab,anext,alpha0)
        
        Pf = sp.stats.norm.cdf(-beta)
        
        CI = phi**2 * np.pi * 0.25 * self.Cost['c_pile'] 
        C_constr = self.Cost['C0'] + CI * h;
        EC_obs = (C_constr + self.Cost['D']) * 1/self.Cost['T']/self.Cost['gamma']
        ECf = (C_constr+self.Cost['H']) * Pf/self.Cost['gamma']
        if phi<=0 or h<5:
            ECtot = 10e30
        else:
            ECtot = C_constr + EC_obs + ECf

        return beta, Pf, alpha, C_constr, EC_obs, ECf, ECtot
    
    def f1_MCS(self,phi,h):
        self.inputpostproc()
        n_sim = int(1e6)
        # U = np.random.randn(6,n_sim)
        # i = -1
        for key in self.X:
            U = np.random.uniform(size=n_sim)
            self.X[key]['rndnum'] = distinv(self.X[key]['dist'])(U,self.X[key]['param'])
        
        g = self.gX([self.X['X1']['rndnum'],self.X['X2']['rndnum'],self.X['X3']['rndnum'],self.X['X4']['rndnum'],self.X['X5']['rndnum'],self.X['X6']['rndnum']],phi,h)
        fails = np.zeros(n_sim)
        fails[np.nonzero(g<=0)[0]] = 1
        Pf = np.sum(fails)/n_sim
        beta = -sp.stats.norm.ppf(Pf)
        return beta, Pf

