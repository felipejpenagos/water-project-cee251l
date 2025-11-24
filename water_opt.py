# water_opt.py -- optimize the water treatment system for
# [ Vr_max,  Vu_max,  Vt_max,  Qd_max ]

import numpy as np
from water_constants import water_constants
from water_analysis import water_analysis
from multivarious.opt import nms  # Nelder-Mead Simplex
from multivarious.utils import plot_cvg_hst


# assign numerical values to all the constants in this system
analysis_constants = water_constants()

Years = 50     # duration of the analysis
Plots = 0      # 1: draw plots, 0: don't draw plots

analysis_constants[-2] = Years

#              Vr,max  Vu,max  Vt,max  Qp,max
#              Mg      Mg      Mg      Mg/day
design_vars_init = np.array([10000, 500, 500, 200])   ## <<< put initial guess here


# evaluate the initial guess   -----------------------------------------
analysis_constants[-1] = 1  # plots on
f_init = water_analysis(design_vars_init, analysis_constants)

response = input('   OK to continue? [y]/n : ')
if response == 'n':
    exit()

# optimize the design ---------------------------------------------------
# design_vars_lb  = np.array([    ,     ,      ,     ])  ## <<< put lower bound values here
# design_vars_ub  = np.array([    ,     ,      ,     ])  ## <<< put upper bound values here

design_vars_ub = 0.5 * design_vars_init
design_vars_lb = 1.5 * design_vars_init

# algorithmic constants ...

#           display  tolX  tolF   tolG  MaxEvals  Penalty  Exponent  nMax errJ
options = {
    'display': 2,
    'tolX': 0.10,
    'tolF': 1.00,
    'tolG': 1.0,
    'MaxEvals': 500,
    'Penalty': 1000,
    'Exponent': 2.0,
    'nMax': 9,
    'errJ': 0.1
}

analysis_constants[-1] = Plots  # plots on/off
design_vars_opt, f_opt, g_opt, cvg_hst = nms(
    water_analysis, design_vars_init, design_vars_lb, design_vars_ub, 
    options, analysis_constants
)
# Or use ORS:
# from multivarious.opt import ors
# design_vars_opt, f_opt, g_opt, cvg_hst = ors(
#     water_analysis, design_vars_init, design_vars_lb, design_vars_ub, 
#     options, analysis_constants
# )

plot_cvg_hst(cvg_hst, design_vars_opt, 20)

# assess the one example of the optimized design  ---------------------------
# ... consider assessing the optimized design a few times
analysis_constants[-1] = 1  # plots on
f_opt = water_analysis(design_vars_opt, analysis_constants)

# water_opt ----------------------------------------------------------------
# 2022-04-11   2025-11-24