# Water Supply System Optimization

50-year stochastic optimization model for sustainable water infrastructure design under climate change.

## Overview

Models the complete water supply chain: **watershed → groundwater → reservoir → treatment → community**. Optimizes system design to minimize costs while meeting water demand and quality standards over 50 years with uncertain rainfall, temperature, and population growth.

## System Visualizations

<p align="center">
  <img src="https://github.com/user-attachments/assets/f770dbdb-2467-411a-997a-5d37b7581638" alt="Water System Flow Diagram" width="700"/>
  <br>
  <em>Complete water supply chain model</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/dce689e4-b259-4cd0-b204-c114036f41b1" alt="Optimization Results" width="500"/>
  <br>
  <em>50-year stochastic optimization results</em>
</p>

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/4d1b2351-57b6-43a9-84e3-d309679c2fa5" alt="System Performance" width="450"/>
      <br>
      <em>Probabilistic Modeling</em>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/7ffd879f-58a3-4977-a1d7-1f34109d5855" alt="Uncertainty Analysis" width="380"/>
      <br>
      <em>Uncertainty Analysis from Real Data</em>
    </td>
  </tr>
</table>

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

**Python Translation**: Felipe Jaramillo (TA - CEE251 2025)  
*Translated from MATLAB with 100% functionality preservation* | 2024-2025
