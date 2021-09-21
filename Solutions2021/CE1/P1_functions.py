#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 15:51:02 2020

@author: jorgemen
"""

def plots_task3(diameters,beta_left,pf_left,beta_right,pf_right):
    import matplotlib.pyplot as plt
    
    fig1, ax1 = plt.subplots(1, 2)
    ax1[0].plot(diameters,beta_left, color='black',lw=2)
    ax1[0].set_xlabel('$d_{o}$ [m]')
    ax1[0].set_ylabel(r'$\beta_{P1}$')
    ax1[0].set_xlim(diameters[0],diameters[-1])
    
    ax1[1].plot(diameters,pf_left, color='black',lw=2)
    ax1[1].set_yscale('log')
    ax1[1].set_xlabel('$d_{0}$ [m]')
    ax1[1].set_ylabel('$P_{f,P1}$')
    ax1[1].set_xlim(diameters[0],diameters[-1])
    plt.tight_layout()
    plt.show()
    
    
    
    fig2, ax2 = plt.subplots(1, 2)
    ax2[0].plot(diameters,beta_right, color='black',lw=2)
    ax2[0].set_xlabel('$d_{o}$ [m]')
    ax2[0].set_ylabel(r'$\beta_{P3}$')
    ax2[1].set_xlim(diameters[0],diameters[-1])
    
    ax2[1].plot(diameters,pf_right, color='black',lw=2)
    ax2[1].set_yscale('log')
    ax2[1].set_xlabel('$d_{0}$ [m]')
    ax2[1].set_ylabel('$P_{f,P3}$')
    ax2[1].set_xlim(diameters[0],diameters[-1])
    plt.tight_layout()
    plt.show()
    
    Pf = pf_left+pf_right
    fig3, ax3 = plt.subplots()
    ax3.plot(diameters,Pf, color='black',lw=2)
    ax3.set_yscale('log')
    ax3.set_xlabel('$d_{0}$ [m]')
    ax3.set_ylabel('$P_f$')
    ax3.set_xlim(diameters[0],diameters[-1])
    plt.tight_layout()
    plt.show()

def optdesign(ECtot,Pf_fun):
    import scipy as sp
    
    res = sp.optimize.minimize(ECtot,6,method='nelder-mead',options={'xatol': 1e-8, 'disp': True})
    p_opt = res.x[0]
    ECtot_min = res.fun
    pf_opt = Pf_fun(p_opt)
    beta_opt = -sp.stats.norm.ppf(pf_opt)
    
    return p_opt,pf_opt,beta_opt,ECtot_min

def plots_task4(diameters,ECtot,EC_f,C_c):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1,1)
    ax.plot(diameters,ECtot(diameters),'k',label='E$[C_{tot}]$')
    ax.plot(diameters,EC_f(diameters),'m',label='E$[C_{F}]$')
    ax.plot(diameters,C_c(diameters),'c',label='E$[C_{C}]$')
    ax.set_xlim(diameters[0],diameters[-1])
    ax.set_xlabel('$d_{o}$ [m]')
    ax.set_ylabel('E$[C_{tot}]$')
    plt.tight_layout()
    return ax
