import numpy as np


def my_water_control(msmnts, design_vars):
    """
    my_water_control - determine water system control actions
    based on measurements
    
    YOUR NAME, Civil Eng'g, Duke Univ, THE DATE
    """

    # Resevoir capacity, Mgal
    Vr_max = design_vars[0]

    # volume capacity for the untreated water storage tank, Mgal
    Vu_max = design_vars[1]

    # volume capacity for the   treated water storage tank, Mgal
    Vt_max = design_vars[2]

    # water flow capacity for the water treatment plant, Mgal/day
    Qp_max = design_vars[3]

    Vr = msmnts[0]     # resevoir volume
    Vu = msmnts[1]     # untreated volume
    Vt = msmnts[2]     #   treated volume
    Cu = msmnts[3:6]   # untreated concentrations
    Ct = msmnts[6:9]   #   treated concentrations

    # use the measurements of volumes and concentrations
    # (current values and allowable limits)
    # to determine flows through the treatment plant

    # flow from reservoir into untreated tank
    Qu = Qp_max * (1 - (Vt / Vt_max)**2)        # ??? (this is *technically* the answer key, replace line with: Qu = ???) !!!

    # flow processed through the treatment plant
    Qp = Qp_max * (1 - (Vt / Vt_max)**2)        # ??? (this is *technically* the answer key, replace line with: Qp = ???) !!!

    # flows for each of the three decontaminants
    q = np.array([7e-7, 9e-5, 2e-4]) * Cu * Qp  # ??? (this is *technically* the answer key, replace line with: q = np.array([???, ???, ???]) !!!


    u = np.array([Qu, Qp, *q])

    return u

# my_water_control ------------------------------------------------ 24 Nov 2025