
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

# Geometry
l = 10000                 # [mm] span
b = 300                   # [mm] width
#=====================================
# Material properties
mu_fm = 26.6              # [MPa] mean material resistance
cov_fm = 0.15             # coeff. of variation
std_fm = mu_fm*cov_fm     # [MPa] standard deviation

mu_R = mu_fm*b/6
std_R = std_fm*b/6
#======================================
# Load
mu_q = 24.1               # [N/mm] mean load
cov_q = 0.3               # coeff. of variation
std_q = mu_q*cov_q        # [MPa] standard deviation

mu_S = (l**2/8)*mu_q
std_S = (l**2/8)*std_q

#=======================================
# Cost model
c_gl = 4000*1E-9          # [NOK/mm^3] Cost Glulam 
C0 = 50000                # [NOK] Fixed cost of construction
H = C0*20                 # Direct cost of failure
C1 = l*b*c_gl             # [NOK/mm] Variable cost
i = 0.03                  # interest rate
T = 25                    # Service life
C_tau = 1/((1+i)**T)      # discount factor

#=====================================
# Reliability index as a function of the decision variable
BETA = lambda h,mu_S,std_S: (mu_R*h**2-mu_S)/(((std_R*h**2)**2+(std_S)**2)**0.5)
h1 = np.linspace(500,1500, num=10000)
beta = BETA(h1,mu_S,std_S)
PF = sp.stats.norm.cdf(-beta)

# Plot
plt.figure()

plt.subplot(121)
plt.plot(h1,beta, color='black',lw=2)
plt.xlabel('$h$ [m]',fontsize=fontsizes)
plt.ylabel(r'$\beta$',fontsize=fontsizes)
plt.xlim(500,1500)
plt.ylim(0,6)
plt.subplot(122)
plt.plot(h1,PF, color='black',lw=2)
plt.yscale('log')
plt.xlabel('$h$ [m]',fontsize=fontsizes)
plt.ylabel('$P_f$',fontsize=fontsizes)
plt.xlim(500,1500)
plt.ylim(1e-10,1e0)
plt.tight_layout()
plt.show()