<div align="center">

# Water Supply System Optimization

### Fifty-year stochastic design of a drinking-water system under climate uncertainty

[![Duke](https://img.shields.io/badge/Duke-CEE%20251L-00539B?style=flat-square)](#about)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](#setup)
[![Multivarious](https://img.shields.io/badge/built%20on-Multivarious-555555?style=flat-square)](https://github.com/hpgavin/multivarious)
[![Assignment](https://img.shields.io/badge/Assignment-PDF-B31B1B?style=flat-square&logo=adobeacrobatreader&logoColor=white)](water-project.pdf)

</div>

---

A community draws water through a chain of watershed, groundwater, reservoir, treatment plant, and storage tanks. Rainfall, temperature, and population growth are uncertain for the next fifty years. The task is to size the system so it meets demand and water-quality standards at the lowest cost, and to show the design still works when the future does not match the forecast.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f770dbdb-2467-411a-997a-5d37b7581638" alt="Water supply system flow diagram" width="680"/>
  <br><sub>System model: watershed → groundwater → reservoir → treatment → community</sub>
</p>

## Approach

- **Dynamics.** Mass balances for water volume and contaminant mass form an ODE system, integrated over fifty years.
- **Uncertainty.** Rain arrives on random days with gamma-distributed depths over a lognormal catchment area; temperature follows a seasonal cycle with a warming trend; per-capita demand carries random noise. Every simulation sees a different climate.
- **Optimization.** Four design variables are tuned with Nelder-Mead against a cost that adds penalties for delivering contaminated water, running out of water, and flooding downstream.
- **Robustness.** The optimized design is re-run under 100 simulated climates to estimate the full distribution of fifty-year cost.

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/dce689e4-b259-4cd0-b204-c114036f41b1" alt="Optimization results" width="420"/>
      <br><sub>Fifty-year optimization results</sub>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/4d1b2351-57b6-43a9-84e3-d309679c2fa5" alt="Probabilistic modeling" width="420"/>
      <br><sub>Probabilistic inputs</sub>
    </td>
  </tr>
</table>

## Design variables

| Variable | Meaning | Units |
|---|---|---|
| `Vr_max` | Reservoir capacity | Mgal |
| `Vu_max` | Untreated-water tank capacity | Mgal |
| `Vt_max` | Treated-water tank capacity | Mgal |
| `Qp_max` | Treatment-plant flow rate | Mgal/day |

## Files

| File | Purpose |
|---|---|
| `water_system.py` | ODE system: mass-balance equations |
| `water_analysis.py` | Fifty-year simulation with stochastic inputs |
| `water_opt.py` | Nelder-Mead optimization |
| `water_montecarlo.py` | Uncertainty analysis over 100 simulated climates |
| `water_constants.py` | System parameters |
| `my_water_control.py` | Control strategy (the part students write) |
| `notes_for_students.txt` | Setup and workflow instructions |

## Setup

```bash
pip install numpy scipy matplotlib
pip install -e /path/to/multivarious
python water_opt.py
python water_montecarlo.py
```

## About

Project 3 for CEE 251L, Uncertainty, Design, and Optimization, at Duke University. The original MATLAB project is by Prof. Henri P. Gavin; I translated it to Python as a teaching assistant for the course in 2025.
