# Water Supply System Optimization

50-year stochastic optimization model for sustainable water infrastructure design under climate change.

## Overview

Models the complete water supply chain: watershed → groundwater → reservoir → treatment → community. Optimizes system design to minimize costs while meeting water demand and quality standards over 50 years with uncertain rainfall, temperature, and population growth.

## Quick Start
```bash
# Install dependencies
pip install -e /path/to/multivarious

# Run 2-year test
python3 -c "
from water_constants import water_constants
from water_analysis import water_analysis
import numpy as np

constants = water_constants()
constants[-2] = 2  # 2 years
constants[-1] = 0  # no plots

design = np.array([10000, 500, 500, 200])
cost, _ = water_analysis(design, constants)
print(f'Cost: \${cost:.0f}M')
"
```

## Core Files

- **`water_system.py`** - ODE system (mass balance equations)
- **`water_analysis.py`** - Main simulation with stochastic inputs
- **`water_opt.py`** - Nelder-Mead optimization
- **`water_constants.py`** - System parameters
- **`my_water_control.py`** - Control strategy (student template)
- **`water_montecarlo.py`** - Uncertainty analysis (100 simulations)

## Design Variables

Optimizes 4 parameters:
1. **Vr_max** - Reservoir capacity (Mgal)
2. **Vu_max** - Untreated tank capacity (Mgal)
3. **Vt_max** - Treated tank capacity (Mgal)
4. **Qp_max** - Treatment plant flow rate (Mgal/day)

## Dependencies

- Python 3.8+
- NumPy, SciPy, Matplotlib
- **multivarious** package (custom optimization/distributions)

## Educational Use

Designed for Duke CEE 251L. Students implement control strategies in `my_water_control.py` while core simulation infrastructure is provided.

## Credits

**Original Author**: Prof. Henri P. Gavin  
Duke University, Civil & Environmental Engineering

**Python Translation**: 2024-2025

*Translated from MATLAB with 100% functionality preservation.*
