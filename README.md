# Water Supply System Optimization
<img width="637" height="237" alt="Screenshot 2025-12-26 at 11 30 45 PM" src="https://github.com/user-attachments/assets/f770dbdb-2467-411a-997a-5d37b7581638" />
<img width="435" height="682" alt="Screenshot 2025-12-26 at 11 31 08 PM" src="https://github.com/user-attachments/assets/dce689e4-b259-4cd0-b204-c114036f41b1" />
<img width="484" height="353" alt="Screenshot 2025-12-26 at 11 31 15 PM" src="https://github.com/user-attachments/assets/4d1b2351-57b6-43a9-84e3-d309679c2fa5" />
<img width="382" height="314" alt="Screenshot 2025-12-26 at 11 31 21 PM" src="https://github.com/user-attachments/assets/7ffd879f-58a3-4977-a1d7-1f34109d5855" />



50-year stochastic optimization model for sustainable water infrastructure design under climate change.

## Overview

Models the complete water supply chain: watershed → groundwater → reservoir → treatment → community. Optimizes system design to minimize costs while meeting water demand and quality standards over 50 years with uncertain rainfall, temperature, and population growth.

## Quick Start
```bash
# Install dependencies
pip install -e /path/to/multivarious

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

Translated to Python by: Felipe Jaramillo (TA - CEE251 2025)

**Python Translation**: 2024-2025

*Translated from MATLAB with 100% functionality preservation.*
