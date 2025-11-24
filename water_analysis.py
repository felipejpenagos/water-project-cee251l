import numpy as np
import matplotlib.pyplot as plt
from multivarious.rvs import gamma, lognormal
from water_system import water_system
from multivarious.utils import ode4u


def water_analysis(v, constants):
    """
    cost = water_analysis( v , constants )
    simulate the behavior of the drinking water supply system as described in
    the provided m-function: water_supply.m
    and controlled by the controller as described in the m-function:
    my_water_control.m
    
     INPUTS  VARIABLE DESCRIPTION
     v[0]    Vr_max  volume of the resevoir                       Mgal
     v[1]    Vu_max  volume of the untreated water tank           Mgal
     v[2]    Vt_max  volume of the treated water tank             Mgal
     v[3]    Qp_max  max. flow through the water treatment plant  Mgal/day
     constants a set of many constants involved in this system
    
     OUTPUTS   DESCRIPTION
     cost      cost of operating water supply system for fifty years
    """

    # --------- READ, BUT DO NOT CHANGE ANYTHING IN THIS FILE -------------

    #  ---- the design variables  ... 

    # volume capacity of the  reservoir, Mgal    
    Vr_max = v[0]

    # volume capacity of the  untreated water storage tank, Mgal
    Vu_max = v[1]

    # volume capacity of the    treated water storage tank, Mgal
    Vt_max = v[2]

    # treatment capacity of the  water treatment plant, Mgal/day
    # should be less than Vu_max and less than Vt_max
    Qp_max = v[3]

    # non-design paraemters ...  see water_constants.py for definitions 

    avg_rpd  = constants[6]     # average rainfall per day, inches
    T_r      = constants[7]     # rainfall return period
    watershed_area = constants[8]     # watershed area

    Cs_base  = constants[9]     # baseline concentrations
    cp       = constants[10]    # sensitivity of concentrations to population
    cs       = constants[11]    # sensitivity of concentrations to stream flow
    
    Cc       = constants[13]    # percentage of water conserved during droughts
    Vg_max   = constants[14]    # groundwater storage capacity

    Ct_allow = constants[17]    # allowable treated water contaminant concentrations
    Pc       = constants[18]    # penalty cost for providing contaminated water
    Pv       = constants[19]    # penalty cost for running out of water
    Pf       = constants[20]    # penalty cost for flooding downstream

    CCTS     = constants[22]    # climate change time scale
    T_avg    = constants[23]    # 
    T1       = constants[24]    # 
    Td       = constants[26]    # 
    T7       = constants[26]    # 
    Tc       = constants[27]    # climate change temperature rise
    P1       = constants[28]    # population model linear    coefficient
    P2       = constants[29]    # population model quadratic coefficient
    Cr       = constants[30]    # 
    Cu       = constants[31]    # 
    Ct       = constants[32]    # 

    Years    = constants[-2]    # duration of the analysis, years
    Plots    = constants[-1]    # 1: draw plots, 0: don't draw plots

    #  pre-determine time series sequences for:
    #  precipitation, temperature, population, and consumption 
    #  Des-ti-ny!  Des-ti-ny!    No escaping!  That's for me!  - Gene Wilder
    #  It is your DEStiney!   - Darth Vader

    days = 365 * Years      # planned days of operation for the plant
    t = np.arange(1, days + 1)   # the days of the water plant operation

    # precipitation sequence  ...
    Tr = T_r * (1 + (t / (CCTS * 365)))  # linearly increasing rain return period 
    ipr = avg_rpd * Tr                   # average number of inches per rainfall
    #     will it rain on any given day?   If so, how much?
    RainFall = (np.random.rand(days) <= 1.0 / Tr) * gamma.rnd(m=ipr, c=1.47, R=1, C=days) # <-------------- revise this line !!!

    # rainfall_area is assumed to be un-correlated with rainfall amount 
    rainfall_area = lognormal.rnd(medX=0.6 * watershed_area, covX=0.90, N=days)            # <-------------- revise this line !!!
    rainfall_area = np.minimum(rainfall_area, watershed_area)  # only catch in watershed
    precipitation = rainfall_area * RainFall   # daily rainfall input, Mgal/day

    # temperature sequence ...
    temperature = T_avg - T1 * np.cos(2*np.pi*(t-15)/365) + T7*np.sin(2*np.pi*t/7/365) + Tc*t/(CCTS*365)
    # dT = dlsym(0.5,Td,1.0,0.0,np.random.randn(days),d)  # random day-to-day temp variation
    # T = T + dT   # add random day-to-day temperature variation

    # population sequence ...
    population = 100e3 + P1*(t/365) + P2*(t/365)**2 + 1500*np.random.randn(days)

    # water demand sequence ...
    gpppd = 100 + 0.4*(temperature - T_avg) + 5.0 * np.random.randn(days)
    water_demand = population * gpppd / 1e6    # water demand, Mgal/day

    # all environmental time series sequences ...
    w = np.vstack([population, temperature, precipitation, water_demand])


    # initial volumes of water in various "containers"

    Vg = 0.9 * Vg_max       # start with almost full ground water
    Vr = 0.8 * Vr_max       # start with almost full reservoir 
    Vu = 0.5 * Vu_max       # start with half full untreated water tank
    Vt = 0.5 * Vt_max       # start with half full   treated water tank

    Z  = 1 + 0.01*Vr_max + 0.5*Vu_max + 0.5*Vt_max + 0.1*Qp_max  # initial cost M$

    x0 = np.array([Vg, Vr, Vu, Vt, *(Cr*Vr), *(Cu*Vu), *(Ct*Vt), Z])  # initial system state

    ode_constants = [v, *constants]
    t, x, dxdt, Q = ode4u(water_system, t, x0, u=w, c=ode_constants)

    cost = x[13, days - 1]

    # plant may not process more water than it can hold. 
    constraint = np.array([1.2*Qp_max / Vu_max - 1,
                           1.2*Qp_max / Vt_max - 1])


    if Plots:  # ----------------------------------------------------------------
        # display plots to show how your plant design and control plan worked out

        x[x < 10*np.finfo(float).eps] = np.nan
        Q[Q < 10*np.finfo(float).eps] = np.nan

        Qt = Q[0, :]                    # transpiration,              Mgal / day
        Qs = Q[1, :]                    # stream flow (runoff),       Mgal / day
        Qg = Q[2, :]                    # ground water flow,          Mgal / day
        Qe = Q[3, :]                    # evaporation from reservoir, Mgal / day
        Qr = Q[4, :]                    # river flow,                 Mgal / day

        Cs = Cs_base + cp*population + cs*Qs    # streamflow contaminant concentrations
        Cs[Cs < 1e-3] = 1e-2

        # compute the one-year precipitation index 
        SPI = np.full(days, np.nan)
        n = int(1.0 * 365)  # one year of data
        for d in range(n, days):
            SPI[d] = np.sum(RainFall[d:d-n:-1]) - avg_rpd * n

        year = t / 365 + 2025

        """
        plt.figure(9)
        plt.clf()
        plt.subplot(311)
        plt.plot(year, RainFall)
        plt.ylabel('rainfall, in.')
        plt.subplot(312)
        plt.plot(year, np.cumsum(RainFall), year, avg_rpd*t)
        plt.ylabel('cumulative rainfall, in.')
        plt.subplot(313)
        rainfall_area[rainfall_area == 0] = 1
        plt.plot(rainfall_area / watershed_area, RainFall, 'o')
        plt.xlabel('rainfall area / watershed area')
        plt.ylabel('rainfall, in.')
        """

        plt.figure(1)
        plt.clf()
        plt.subplot(311)
        plt.plot(year, ipr)
        plt.plot(year, 1.0 / Tr)
        plt.ylabel('statistical averages')
        plt.legend(['avg. inch per rainfall', '1/rain return period'], loc='northwest')
        plt.axis([2025, 2025 + Years, 0, 1.0])
        plt.title(f'CCTS = {CCTS:.0f}y, Tc={Tc:4.1f} deg.F, P_2={P2:4.1f}, C_c={Cc*100:4.2f}%, cost={cost:.0f} M$')
        plt.subplot(312)
        plt.plot(year, np.cumsum(precipitation / rainfall_area))
        plt.plot(year, np.cumsum(Qt / watershed_area))
        plt.ylabel('cumulative Tgal')
        plt.legend(['cumulative precipitation', 'cumulative transpiration'], loc='northwest')
        plt.subplot(313)
        plt.plot(year, np.zeros(days), '-k')
        plt.plot(year, SPI)
        plt.xlabel('year')
        plt.ylabel('1-yr precipitation index, in')
        # plt.savefig('Fig1.pdf', bbox_inches='tight')

        colors = np.array([[240, 170, 0], [0, 10, 200], [5, 210, 5], [0, 148, 228]]) / 256

        plt.figure(2)
        plt.clf()
        plt.subplot(311)
        plt.plot(year, Qg)
        plt.plot(year, Qe)
        plt.legend(['groundwater flow', 'evaporation'], loc='southwest', frameon=False)
        plt.ylabel('Mgal / day')
        plt.title(f'V_r = {Vr_max:5.0f} Mg, V_u={Vu_max:5.0f} Mg, V_t={Vt_max:5.0f} Mg, Q_p={Qp_max:4.0f} Mg/d, cost={cost:.0f} M$')
        plt.subplot(312)
        plt.plot(year, x[0, :] / Vg_max, '-', color=colors[0])
        plt.plot(year, x[1, :] / Vr_max, '-', color=colors[1])
        plt.plot(year, x[2, :] / Vu_max, '-', color=colors[2])
        plt.plot(year, x[3, :] / Vt_max, '-', color=colors[3])
        plt.ylabel('volumes / capacities')
        plt.legend(['ground water', 'reservoir', 'untreated', 'treated'], loc='southwest', frameon=False)
        plt.axis([year[0], year[days - 1], 0, 1.2])
        plt.subplot(313)
        plt.semilogy(year, Qr)
        plt.semilogy(year, Qs)
        plt.legend(['river flow', 'stream flow'], loc='southwest', frameon=False)
        plt.ylabel('Mgal / day')
        # plt.savefig('Fig2.pdf', bbox_inches='tight')

        plt.figure(3)
        plt.clf()
        plt.subplot(311)
        plt.plot(year, population / 1000)
        plt.ylabel('population/1000')
        plt.title(f'CCTS = {CCTS:.0f}y, Tc={Tc:4.1f} deg.F, P_2={P2:4.1f}, C_c={Cc*100:4.2f}%, cost={cost:.0f} M$')
        plt.subplot(312)
        plt.plot(year, water_demand / population * 1e6)  # gal per person, water demand
        plt.ylabel('consumption, gpppd')
        plt.subplot(313)
        plt.plot(year, x[13, :])
        plt.ylabel('cost, M$')
        # plt.savefig('Fig3.pdf', bbox_inches='tight')

        plt.figure(4)
        plt.clf()
        y = np.array([year[0], year[days - 1]])
        o = np.array([1, 1])
        plt.subplot(311)
        plt.semilogy(year, Cs[0, :] / Ct_allow[0], '-', color=colors[0])
        plt.semilogy(year, x[4, :] / x[1, :], '-', color=colors[1])
        plt.semilogy(year, x[7, :] / x[2, :], '-', color=colors[2])
        plt.semilogy(year, x[10, :] / x[3, :], '-', color=colors[3])
        plt.semilogy(y, o * Ct_allow[0], '--k')
        plt.ylabel('micro-organisms')
        plt.text(year[1*365], Cs[0, 1*365], 'C_s', fontweight='bold')
        plt.text(year[2*365], x[4, 2*365] / x[1, 2*365] / Ct_allow[0], 'C_r', fontweight='bold')
        plt.text(year[3*365], x[7, 3*365] / x[2, 3*365] / Ct_allow[0], 'C_u', fontweight='bold')
        plt.text(year[4*365], x[10, 4*365] / x[3, 4*365] / Ct_allow[0], 'C_t', fontweight='bold')
        plt.axis([year[0], year[days - 1], 1e-3, 1e3])
        plt.subplot(312)
        plt.semilogy(year, Cs[1, :] / Ct_allow[1], '-', color=colors[0])
        plt.semilogy(year, x[5, :] / x[1, :], '-', color=colors[1])
        plt.semilogy(year, x[8, :] / x[2, :], '-', color=colors[2])
        plt.semilogy(year, x[11, :] / x[3, :], '-', color=colors[3])
        plt.semilogy(y, o * Ct_allow[1], '--k')
        plt.ylabel('suspended solids')
        plt.text(year[1*365], Cs[1, 1*365], 'C_s', fontweight='bold')
        plt.text(year[2*365], x[5, 2*365] / x[1, 2*365] / Ct_allow[1], 'C_r', fontweight='bold')
        plt.text(year[3*365], x[8, 3*365] / x[2, 3*365] / Ct_allow[1], 'C_u', fontweight='bold')
        plt.text(year[4*365], x[11, 4*365] / x[3, 4*365] / Ct_allow[1], 'C_t', fontweight='bold')
        plt.axis([year[0], year[days - 1], 1e-3, 1e3])
        plt.subplot(313)
        plt.semilogy(year, Cs[2, :] / Ct_allow[2], '-', color=colors[0])
        plt.semilogy(year, x[6, :] / x[1, :], '-', color=colors[1])
        plt.semilogy(year, x[9, :] / x[2, :], '-', color=colors[2])
        plt.semilogy(year, x[12, :] / x[3, :], '-', color=colors[3])
        plt.semilogy(y, o * Ct_allow[2], '--k')
        plt.ylabel('petro-chemical')
        plt.text(year[1*365], Cs[2, 1*365], 'C_s', fontweight='bold')
        plt.text(year[2*365], x[6, 2*365] / x[1, 2*365] / Ct_allow[2], 'C_r', fontweight='bold')
        plt.text(year[3*365], x[9, 3*365] / x[2, 3*365] / Ct_allow[2], 'C_u', fontweight='bold')
        plt.text(year[4*365], x[12, 4*365] / x[3, 4*365] / Ct_allow[2], 'C_t', fontweight='bold')
        plt.axis([year[0], year[days - 1], 1e-3, 1e3])
        # plt.savefig('Fig4.pdf', bbox_inches='tight')

        plt.draw()
        plt.pause(0.001)

        dirty_water_days = np.where(np.sum(x[10:13, :] / (np.ones((3, 1)) * x[3, :]) > Ct_allow.reshape(-1, 1), axis=0))[0]
        out_of_water_days = np.where(x[3, :] < 0.11 * Vt_max)[0]
        flooded_river_days = np.where(Qr > 5e3)[0]
        # treated_tank_volumes = x[3, out_of_water_days]
        # flood_flow = Qr[flooded_river_days]

        """
        print('dirty water on years ... ')
        for i in range(len(dirty_water_days)):
            print(f'{2025 + dirty_water_days[i] / 365:7.2f}')
        print('out of water on years ... ')
        for i in range(len(out_of_water_days)):
            print(f'{2025 + out_of_water_days[i] / 365:7.2f}')
        print('flooded river on years ... ')
        for i in range(len(flooded_river_days)):
            print(f'{2025 + flooded_river_days[i] / 365:7.2f}')
        print()
        """

    # ------------------------------------------ Plots

    return cost, constraint

# water_analysis ============================================================
# updated 2012-04-22  2016-03-25   2022-03-22   2025-11-24
# H.P. Gavin, Dept. Civil & Environ. Eng'g, Duke Univ.