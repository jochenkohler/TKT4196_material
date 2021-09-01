#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:17:03 2020

@author: jorgemen
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import inputfile
from opt_form import opt_form
from mpl_toolkits.mplot3d import Axes3D

X, L, Cost = inputfile.inputgen()
obj = opt_form(X,L,Cost)

# Evaluate reliability index for phi = 0.6 and h = 10
phi = 0.6
h = 10
beta_MCS,Pf_MCS = obj.f1_MCS(phi,h)
beta, Pf, alpha, C_constr, EC_obs, ECf, ECtot = obj.f1(phi,h)

print("MCS Reliability index for phi={phi:.1f} and h={h:.0f} is {b:.3f}\n".format(phi=phi,h = h,b = beta_MCS))
print("FORM Reliability index for phi={phi:.1f} and h={h:.0f} is {b:.3f}\n".format(phi=phi,h = h,b = beta))

# Plot of costs
PHI = 10**(np.linspace(np.log10(0.2),np.log10(1),15))
H = 10**(np.linspace(np.log10(5),np.log10(20),15))

pp,hh = np.meshgrid(PHI,H)

BETA = np.zeros_like(pp)
PF = np.zeros_like(pp)
C_constr = np.zeros_like(pp)
EC_obs = np.zeros_like(pp)
ECf = np.zeros_like(pp)
ECtot = np.zeros_like(pp)

for idx_p in range(len(PHI)):
    for idx_h in range(len(H)):
        res = obj.f1(pp[idx_p,idx_h],hh[idx_p,idx_h])
        BETA[idx_p,idx_h] = res[0]
        PF[idx_p,idx_h]  = res[1]
        C_constr[idx_p,idx_h]  = res[3]
        EC_obs[idx_p,idx_h] = res[4]
        ECf[idx_p,idx_h] = res[5]
        ECtot[idx_p,idx_h] = res[6]


fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
surf = ax1.plot_surface(pp, hh, BETA,cmap=plt.cm.coolwarm)
ax1.set_xlabel('$\phi$')
ax1.set_xlim(PHI[0],PHI[-1])
ax1.set_ylabel('$h$')
ax1.set_ylim(H[0],H[-1])
ax1.set_zlabel(r'$\beta$')
plt.tight_layout()
plt.show()


fig = plt.figure()
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot_surface(pp,hh,ECf,cmap=plt.cm.coolwarm)
ax1.set_xlabel('$\phi$ [m]')
ax1.set_ylabel('$h$ [m]')
ax1.set_zlabel('$C_{obs}}$')
ax1.set_zlabel('$E[C_{tot}]$')


ax2 = fig.add_subplot(222, projection='3d')
ax2.plot_surface(pp,hh,C_constr,cmap=plt.cm.coolwarm)
ax2.set_xlabel('$\phi$ [m]')
ax2.set_ylabel('$h$ [m]')
ax2.set_zlabel('$C_{constr}$')


ax3 = fig.add_subplot(223, projection='3d')
ax3.plot_surface(pp,hh,EC_obs,cmap=plt.cm.coolwarm)
ax3.set_xlabel('$\phi$ [m]')
ax3.set_ylabel('$h$ [m]')
ax3.set_zlabel('$C_{obs}}$')

ax4 = fig.add_subplot(224, projection='3d')
ax4.plot_surface(pp,hh,ECf,cmap=plt.cm.coolwarm)
ax4.set_xlabel('$\phi$ [m]')
ax4.set_ylabel('$h$ [m]')
ax4.set_zlabel('$C_{obs}}$')
ax4.set_zlabel('$E[C_{f,ULS}]$')
plt.tight_layout()
plt.show()


# Optimal height for phi = 0.7
phi_opt = 0.7
f2 = lambda h: obj.f1(phi_opt,h)[-1]
res = sp.optimize.minimize(f2,5.5)
h_opt  = res.x[0]
beta_opt = obj.f1(phi_opt,h_opt)[0]
print("h_opt = {h:.3f}, with beta_opt = {b:.3f}\n".format(h = h_opt,b = beta_opt))




