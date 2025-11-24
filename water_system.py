import numpy as np
from my_water_control import my_water_control


def water_system(t, x, w, ode_constants):
    """
    [dxdt,Q] = water_system(t,x,w,ode_constants)
    determine the state derivitive of the water supply system based on: 
    the state of the system x, 
    the controls of the system u, and
    the environmental conditions w

    H.P. Gavin, Civil & Environ. Eng'g, Duke Univ.  2022-03-13

    x, u, and w must be column vectors
    """

    # dynamic states of the water plant ...
    Vg  = x[0]       # water volume in surface ground water        Mgal
    Vr  = x[1]       # water volume in reservoir                   Mgal
    Vu  = x[2]       # water volume in untreated water tank        Mgal
    Vt  = x[3]       # water volume in   treated water tank        Mgal

    mr  = x[4:7]     # mass of pollutants in reservoir             gal
    mu  = x[7:10]    # mass of pollutants in untreated tank        gal
    mt  = x[10:13]   # mass of pollutants in   treated tank        gal 

    Z   = x[13]      # total cost of operating the plant, up to today $

    # definition of the environmental conditions ...
    P   = w[0]       # population                             ?
    T   = w[1]       # temperature                           deg F
    Qi  = w[2]       # input precipitation                   Mgal/day
    Qd  = w[3]       # daily water demand from treated tank  Mgal/day

    # design variables ...
    design_vars = ode_constants[0]
    Vr_max = design_vars[0]    # resevoir capacity, Mgal    
    Vu_max = design_vars[1]    # plant untreated water storage capacity, Mgal
    Vt_max = design_vars[2]    # plant untreated water storage capacity, Mgal
    Qp_max = design_vars[3]    # plant treatment capacity,  Mgal/day


    # analysis_constants = { alpha_t , beta_t , alpha_s , alpha_g , alpha_e , beta_e , avg_rpd, T_r, watershed_area, Cs_base , cp , cs , cr , Cc , Vg_max , Qr_min , R , Ct_allow , Pc , Pv , Pf , operating_cost , CCTS , T_avg, T1, Td, T7, Tc , P1 , P2 , Cr , Cu , Ct , Years , Plots};


    # non-design paraemters ...  see water_constants.py for definitions 
    alpha_t  = ode_constants[1]
    beta_t   = ode_constants[2]
    alpha_s  = ode_constants[3]
    alpha_g  = ode_constants[4]
    alpha_e  = ode_constants[5]
    beta_e   = ode_constants[6]

    Cs_base  = ode_constants[10]  # baseline concentrations
    cp       = ode_constants[11]  # sensitivity of concentrations to population
    cs       = ode_constants[12]  # sensitivity of concentrations to stream flow
    cr       = ode_constants[13]  # std. dev. of concentration fluxuation
    
    Cc       = ode_constants[14]
    Vg_max   = ode_constants[15]  # groundwater storage capacity
    Qr_min   = ode_constants[16]  # minimum allowable river flow

    R        = ode_constants[17]  # pollution treatment effectiveness (dimensionless)
    Ct_allow = ode_constants[18]  # allowable treated water contaminant concentrations
    Pc       = ode_constants[19]  # penalty cost for providing contaminated water
    Pv       = ode_constants[20]  # penalty cost for running out of water
    Pf       = ode_constants[21]  # penalty cost for flooding downstream
    operating_cost = ode_constants[22]
    
    Cr = mr / Vr               # concentrations in reservoir
    Cu = mu / Vu               # concentrations in untreated tank
    Ct = mt / Vt               # concentrations in   treated tank

    # # standard deviation of measurement errors
    # 
    # msmnt_errr = [ 0.01*Vr_max  ; 0.01*Vu_max; 0.01*Vt_max ; ...
    #                 0.1*Ct_allow ; 0.1*Ct_allow ];

    # available measurements of the water supply and treatment system 
    msmnts = np.array([Vg, Vu, Vt, *(mu/Vu), *(mt/Vt)])

    # _your_ function to control the treatment plant ...
    controls = my_water_control(msmnts, design_vars)

    Qu  = controls[0]      # flow into untreated tank              Mgal/day
    Qp  = controls[1]      # water flow through treatments         Mgal/day
    q   = controls[2:5]    # decontaminant flows into treatments   Mgal/day

    # enforce limits on Qp and q
    Qp  = min(Qp, Qp_max)       # limit max flow  through the treatment processes
    Qp  = max(Qp, 0.1)          # limit min flow  through the treatment processes
    q   = np.maximum(q, 1e-3)   # limit min decon through the treatment processes

    # environmental flows

    Qt = (alpha_t + beta_t*T) * Vg/Vg_max    # transpiration of ground water
    Qs = (alpha_s) * Vg/Vg_max               # stream flow
    Qg = (alpha_g) * Vg/Vg_max               # ground water flow
    Qe = (alpha_e + beta_e*T) * Vr/Vr_max    # evaporation from reservoir 
    if Vr < 0.05*Vr_max:      # can NOT drain reservoir
        Qu = 0
        Qr = 1
    elif Vr > 0.8*Vr_max:     # keep reservoir about 70% full, to prevent floods
        Qr = Qr_min + (Vr - 0.8*Vr_max)/3
    else:
        Qr = Qr_min           # minimum river flow from reservoir
    
    if Vu < 0.20*Vu_max: 
        Qp = 0.01*Qp_max      # should NOT drain untreated tank
    if Vu < 0.05*Vu_max: 
        Qp = 0.0              # can    NOT drain untreated tank
    if Vt < 0.05*Vt_max: 
        Qd = 0.0              # can    NOT drain   treated tank

    if Vr/Vr_max < 0.5:       # don't water your lawn mower, it won't cut any mower
        Qd = Qd * (1.0 - Cc)  # enforce water conservation

    #

    # check for over-flow conditions , increase over-flows accordingly

    if Vg > Vg_max:
        Qs = Qs + (Vg - Vg_max)/4         # overflow groundwater goes to streamflow
    
    Qro = 0                               # overflow from reservoir
    if Vr > Vr_max:
        Qro = (Vr - Vr_max)/9             # overflow reservoir water goes to river
    
    Quo = 0                               # overflow from untreated water tank
    if Vu > Vu_max:
        Quo = (Vu - Vu_max)               # untreated overflow goes to river
    
    Qto = 0                               # overflow from treated water tank
    if Vt > Vt_max:
        Qto = (Vt - Vt_max)               # treated overflow goes to river

    Qu = min(Qu, 0.9*(Vr - Qe - Qr))  # can not take out more than what's in reservoir

    Cs = Cs_base + cp*P + cs*Qs            # streamflow contaminant concentrations
    Cs[Cs < 1e-3] = 1e-2

    Cp = Cu * np.exp(-R@q/(Qp + np.finfo(float).eps))  # post-treatment concentrations  # !!! check this line !!! matmult @ appropriate??

    # the time rate of change of water volumes and contaminant mass
    # ... mass conservation ...

    dVg_dt = Qi - Qs - Qt - Qg              # groundwater volume 
    dVr_dt = Qs + Qg - Qe - Qu - Qr - Qro   # reservoir volume
    dVu_dt = Qu - Qp - Quo                  # untreated water volume
    dVt_dt = Qp - Qd - Qto                  # treated water volume

    dmr_dt = Cs*Qs - Cr*Qu - Cr*Qr - Cr*Qro # contaminant flow into reservoir
    dmu_dt = Cr*Qu - Cu*Qp - Cu*Quo         # contaminant flow into untreated tank
    ### print(f"Cp shape: {np.shape(Cp)}, Ct shape: {np.shape(Ct)}, Qp: {Qp}, Qd: {Qd}, Qto: {Qto}") #**temprary debug print************
    dmt_dt = Cp*Qp - Ct*Qd - Ct*Qto         # contaminant flow into   treated tank

    Qr = Qr + Qro + Quo + Qto               # overflows go to the river

    # update the rate of cost increase of operating the water treatment system

    dZ_dt = np.sum(operating_cost * q)      # daily operating costs

    if np.any(Ct > Ct_allow):               # treated water is too contaminated
        dZ_dt = dZ_dt + Pc*Qd               # ... add a contamination penalty
    
    if Vt < 0.11*Vt_max:                    # treated water supply is depleted
        dZ_dt = dZ_dt + Pv*Qd               # ... add a supply penalty
    
    if Qr > 5e3:                            # river floods
        dZ_dt = dZ_dt + Pf                  # ... add a flooding penalty

    # the state derivitive

    ### print(f"Shapes: dVg={np.shape(dVg_dt)}, dmr={np.shape(dmr_dt)}, dmu={np.shape(dmu_dt)}, dmt={np.shape(dmt_dt)}, dZ={np.shape(dZ_dt)}") #**temprary debug print************
    dxdt = np.concatenate([
        np.atleast_1d(dVg_dt),
        np.atleast_1d(dVr_dt),
        np.atleast_1d(dVu_dt),
        np.atleast_1d(dVt_dt),
        np.ravel(dmr_dt),
        np.ravel(dmu_dt),
        np.ravel(dmt_dt),
        np.atleast_1d(dZ_dt)
        ])

    Q = np.array([Qt, Qs, Qg, Qe, Qr])  # flows within the system

    return dxdt, Q

# water_system -------------------------------------------------- 2025-11-24