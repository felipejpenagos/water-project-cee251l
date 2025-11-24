# water_montecarlo.py
# Monte-Carlo analysis for cost and sensitivity of a water supply design system
# to be run after running truss_opt.m
# CEE 201, Duke University, HP Gavin, 2019, 2022

import numpy as np
import matplotlib.pyplot as plt
from time import time
from datetime import datetime, timedelta
from water_constants import water_constants
from water_analysis import water_analysis
from multivarious.rvs import lognormal
from multivarious.utils import plotCDFci


# on line 9 of water_constants.py . . . Plots = 0;

#  v[0]  Vr_max  volume of the resevoir                       Mgal
#  v[1]  Vu_max  volume of the untreated water tank           Mgal
#  v[2]  Vt_max  volume of the treated water tank             Mgal
#  v[3]  Qp_max  max. flow through the water treatment plant  Mgal/day
#   . . . etc . . . if you have other design variables to include . . . 

#              Vr,max Vu,max Vt,max Qp,max
# opt_v = np.array([??  , ??   , ??   , ??   ])  #  * PUT YOUR BEST PARAMETERS HERE *

analysis_constants = water_constants()  # assign numerical values to system constants
analysis_constants[-2] = 50             # 50 year simulation
analysis_constants[-1] = 1              # show plots

cost, constraints = water_analysis(opt_v, analysis_constants)
response = input('   OK to continue? [y]/n : ')
if response == 'n':
    exit()

NP  = len(opt_v)                 # number of design variables 
NS  = 100                        # total number of simulations             *
NR  = 4                          # number of random variables in the MCS

# --- probability models for uncertain quantities

# a sample of NS observations of NR uncorrelated log normal random variables
rv = lognormal.rnd(
    medX = np.array([CCTS, Tc, P2, Cc]), 
    covX = np.array([0.3, 0.2, 0.1, 0.3]), 
    N = NS, 
    R = np.eye(NR)
)

cost84   = np.zeros(NS)  # 84th percentile cost
cost_avg = np.zeros(NS)  # average cost
avg_cost = 0             # average cost 
ssq_cost = 0

plt.figure(10)
plt.clf()
plt.hold(True)
hdl_a, = plt.plot(0, 500, 'ob')
hdl_b, = plt.plot(0, 500, 'or')
hdl_c, = plt.plot(0, 500, 'og')
plt.grid(True)
plt.axis([1, NS, 500, 1200])
plt.xlabel('simulation number')
plt.ylabel('costs')
plt.legend(['sample', 'avg+std.dev', 'average'])

start_time = time()

analysis_constants[-1] = 0  # no plots
cost = np.zeros(NS)
for sim in range(NS):            # Monte Carlo simulation  (MCS)

    analysis_constants[22] = rv[0, sim]    # CCTS
    analysis_constants[27] = rv[1, sim]    #  Tc
    analysis_constants[29] = rv[2, sim]    #  P2
    analysis_constants[13] = rv[3, sim]    #  Cc

    cost[sim], _ = water_analysis(opt_v, analysis_constants)

    delta_cost = cost[sim] - avg_cost
    avg_cost = avg_cost + delta_cost / (sim + 1)
    ssq_cost = ssq_cost + delta_cost * (cost[sim] - avg_cost)
    if sim > 0:
        cost84[sim] = avg_cost + np.sqrt(ssq_cost / sim)
    cost_avg[sim] = avg_cost

    hdl_a.set_xdata(np.arange(1, sim + 2))
    hdl_b.set_xdata(np.arange(1, sim + 2))
    hdl_c.set_xdata(np.arange(1, sim + 2))
    hdl_a.set_ydata(cost[:sim + 1])
    hdl_b.set_ydata(cost84[:sim + 1])
    hdl_c.set_ydata(cost_avg[:sim + 1])
    plt.draw()
    plt.pause(0.001)

    # how much longer??
    secs = time() - start_time
    secs_left = (NS - sim - 1) * secs / (sim + 1)
    eta = datetime.now() + timedelta(seconds=secs_left)
    print(f'sim: {sim+1:3d} ({100*(sim+1)/NS:5.1f}%); {secs/(sim+1):5.2f} secs/sim; eta: {eta.strftime("%H:%M:%S")} ({secs_left:5.0f} s) cost: {cost[sim]:5.0f} {cost84[sim]:5.0f} M$')

    if not (cost[sim] > 0):
        print('uh oh - non-positive cost!')
        break

# emperical cumulative distribution function ...

eCDF = (np.arange(1, NS + 1) - 0.5) / NS

cost_sort = np.sort(cost)

# Plots ----

plt.figure(4)
plt.hist(cost, bins=20)
plt.xlabel('lifetime cost')
plt.ylabel('histogram count')

x_avg, x_med, x_sd, x_cov = plotCDFci(cost, 95, 5)
plt.xlabel('lifetime cost')
plt.ylabel('non-exceedance probability')
plt.grid(True)

# correlation plots ...

crrl = np.zeros(NR)
for i in range(NR):
    crl = np.corrcoef(rv[i, :], cost)
    crrl[i] = crl[0, 1]

plt.figure(6)
plt.clf()
plt.plot(rv[0, :], cost, 'o')
plt.xlabel('CCTS, y, climate change time scale')
plt.ylabel('lifetime cost, M$')
plt.title(f'correlation = {crrl[0]:5.2f}')

plt.figure(7)
plt.clf()
plt.plot(rv[1, :], cost, 'o')
plt.xlabel('dT_c, deg F, climate change temperature rise')
plt.ylabel('lifetime cost, M$')
plt.title(f'correlation = {crrl[1]:5.2f}')

plt.figure(8)
plt.clf()
plt.plot(rv[2, :], cost, 'o')
plt.xlabel('P_2, quadratic coefficient for population growth')
plt.ylabel('lifetime cost, M$')
plt.title(f'correlation = {crrl[2]:5.2f}')

plt.figure(9)
plt.clf()
plt.plot(rv[3, :], cost, 'o')
plt.xlabel('C_c, drought water reduction percentage')
plt.ylabel('lifetime cost, M$')
plt.title(f'correlation = {crrl[3]:5.2f}')

# water_montecarlo  ------------------------------------------- 21 Mar 2022