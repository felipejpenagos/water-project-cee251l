# water_constants.py
# CEE 201, Spring 2024
# constants used in the water supply and treatment project
# do not change any values in this file

import numpy as np


def water_constants():
    """
    Returns a list of constants used in the water supply and treatment project.
    
    Returns:
        analysis_constants: list containing all system constants
    """
    
    # climate change time scale modeling

    Years =  50            # total number of years in the simulation
    Plots =   1            # 1: draw plots, 0: don't draw plots

    CCTS =   50            # expected climate change time scale, years

    # temperature modeling coefficients

    T_avg = 65             # average yearly temperature, deg.F
    T1 = 30                # yearly temperature variation, deg.F
    Td = 5                 # daily temperature variation, deg.F
    T7 = 8                 # seven-year temperature cycle, deg.F
    Tc = 4                 # temperature trend, deg.F

    # population modelling coefficients

    P1 = 1298              # linear population growth coefficient
    P2 = 54                # quadratic population growth coefficient

    # water conservation effectiveness modeling

    Cc = 0.15              # expected water conservation percentage during droughts

    # rainfall modelling coefficients

    avg_rpd = 0.094                    # average yearly rainfall / 365
    T_r = 3.28                         # return period for rain events, days
    watershed_area =  200              # watershed area, square miles
    watershed_area = watershed_area * (5280*12)**2/231/1e6  # area, Mgal/in

    alpha_t =   10.0       # transpiration saturation  coefficient, Mgal/day
    beta_t  =    7.0       # transpiration temperature coefficient, Mgal/day / deg.F
    alpha_s =    5         # streamflow saturation coefficient, Mgal/day
    alpha_g =   50         # groundwater flow saturation coefficient, Mgal/day
    alpha_e =    1         # evaporation saturation coefficient, Mgal/day  
    beta_e  =    0.20      # evaporation temperature coefficient, Mgal/day / deg.F

    Vg_max =  10*watershed_area        # ground water capacity, Mgal
    Qr_min = 20                        # minimum allowable flow into the river, Mgal/d


    # water pollution modeling for each day in the simulation
    # pollution types: 1= micro-organisms, 2= suspended-solids, 3= petro-chemical
    # treatment types: 1= chlorine       , 2= filters         , 3= activated carbon 

    # initial pollution concentrations

    Cs_base = np.array([10, 5.0, 1.0])      # baseline streamflow concentrations
    cp = np.array([5e-4, 1e-3, 1e-4])       # sensitivity of concentrations to population
    cs = np.array([-0.10, 0.5, 0.20])       # sensitivity of concentrations to stream flow
    cr = 0.1

    Cr = np.array([10, 5, 2])               # initial reservoir concentrations, ppm
    Cu = np.array([0.1, 0.1, 0.1])          # initial untreated concentrations, ppm
    Ct = np.array([0.1, 0.1, 0.1])          # initial   treated concentrations, ppm

    Ct_allow = np.array([2, 2, 1])          # allowable water pollution concentrations, ppm

    # pollution treatment effectiveness (dimensionless)
    # R(i,j) shows the effectiveness of treatment "j" for pollutant "i"
    # Note: treatment "i" is most effective for pollutant "i"
    #     chlorine     filters      activated carbon          
    R = np.array([
        [ 1000,        1000,         250  ],      # micro-organisms
        [   50,        2500,          50  ],      # suspended solids
        [  100,         100,        1000  ]       # petro-chemical
    ])


    # operating costs for three treatment types, $/gal of treatment
    #                  chlorine  filters activated carbon
    operating_cost = np.array([0.03, 0.01, 0.05])    # $ per gallon used

    Pc =  0.10              # penalty for contaminated water,  $/gal
    Pf =  5.00              # penalty for contaminated water, M$
    Pv =  0.05              # penalty for not enough water,    $/gal

    analysis_constants = [
        alpha_t, beta_t, alpha_s, alpha_g, alpha_e, beta_e, avg_rpd, T_r, 
        watershed_area, Cs_base, cp, cs, cr, Cc, Vg_max, Qr_min, R, Ct_allow, 
        Pc, Pv, Pf, operating_cost, CCTS, T_avg, T1, Td, T7, Tc, P1, P2, 
        Cr, Cu, Ct, Years, Plots
    ]

    return analysis_constants