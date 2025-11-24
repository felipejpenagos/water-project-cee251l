# Water Supply System Optimization - Python Implementation

A 50-year stochastic optimization model for designing and operating sustainable water supply systems under climate change and population growth constraints.

## Overview

This project models the complete water supply chain from watershed to community:
- **Watershed hydrology** with stochastic rainfall (gamma distribution)
- **Groundwater storage** and natural flows (transpiration, stream flow)
- **Reservoir management** with evaporation and overflow control
- **Treatment plant operations** for three pollutant types
- **Storage tanks** (untreated and treated water)
- **Water quality monitoring** and regulatory compliance
- **Cost optimization** including capital, operating, and penalty costs

The system uses **Monte Carlo uncertainty analysis** (100 simulations) to evaluate design robustness under varying climate and demographic scenarios.

## Project Structure

### Core Modules

- **`water_system.py`** - ODE system implementing mass balance equations for all water compartments
- **`water_analysis.py`** - Main simulation driver with 50-year stochastic scenario generation
- **`water_opt.py`** - Optimization wrapper using Nelder-Mead Simplex algorithm
- **`water_constants.py`** - System parameters including climate, costs, and treatment effectiveness
- **`my_water_control.py`** - **Student template** for implementing control strategies
- **`water_montecarlo.py`** - Uncertainty quantification via 100 Monte Carlo simulations
- **`ode4u.py`** - 4th-order Runge-Kutta solver for ODE integration

### Supporting Files

- **Documentation** - Setup instructions, technical notes, compatibility guides
- **Answer key** - `my_water_control_ANSWER_KEY.py` (instructor use only)

## Dependencies

This project requires the **multivarious** package for optimization and probability distributions:
```bash
# Clone and install multivarious
git clone https://github.com/YOUR_ORG/multivarious.git
cd multivarious
pip install -e .
```

Additional requirements:
- Python 3.8+
- NumPy
- SciPy
- Matplotlib

## Installation
```bash
# Clone this repository
git clone https://github.com/YOUR_ORG/water-optimization-project.git
cd water-optimization-project

# Verify multivarious is installed
python3 -c "from multivarious.rvs import lognormal; print('✓ Ready')"
```

## Quick Start

### Run a simple 2-year test simulation:
```python
from water_constants import water_constants
from water_analysis import water_analysis
import numpy as np

# Setup
constants = water_constants()
constants[-2] = 2  # 2 years
constants[-1] = 0  # no plots

# Design variables: [Vr_max, Vu_max, Vt_max, Qp_max]
design = np.array([10000, 500, 500, 200])

# Run simulation
cost, metrics = water_analysis(design, constants)
print(f'Total Cost: ${cost:.0f}M')
```

### Run optimization:
```python
from water_opt import water_opt

# Optimize design over 50-year period
optimal_design, optimal_cost = water_opt()
```

### Run Monte Carlo uncertainty analysis:
```python
from water_montecarlo import water_montecarlo

# Evaluate design robustness (100 scenarios)
results = water_montecarlo(design)
```

## Design Variables

The optimization determines four key design parameters:

1. **Vr_max** - Reservoir capacity (million gallons)
2. **Vu_max** - Untreated water tank capacity (million gallons)
3. **Vt_max** - Treated water tank capacity (million gallons)
4. **Qp_max** - Treatment plant maximum flow rate (million gallons/day)

## Control Strategy

Students implement real-time operational control in `my_water_control.py`:

- **Qu** - Flow from reservoir to untreated tank
- **Qp** - Flow through treatment plant
- **q[1:3]** - Decontaminant application rates for three pollutants

Control decisions are based on measured system state (tank levels, water quality).

## Performance Metrics

The objective function minimizes the **84th percentile lifetime cost**:

- **Capital costs** - Infrastructure construction (one-time)
- **Operating costs** - Daily treatment and pumping
- **Penalty costs** - Water shortages, contamination violations, downstream flooding

Cost = mean(cost) + std(cost) over 100 Monte Carlo simulations

## Key Features

### Stochastic Modeling
- Gamma-distributed rainfall with climate change trends
- Temperature variations affecting evaporation
- Population growth with uncertainty

### Physical Constraints
- Mass balance for all water compartments
- Water quality tracking (3 pollutant types)
- Treatment effectiveness matrix (3×3 processes)
- Regulatory limits on treated water quality

### Climate Change Integration
- 50-year climate change timescale (CCTS)
- Temperature coefficient trends
- Evolving precipitation patterns

## Example Results

Typical optimized designs achieve:
- **84th percentile cost**: ~$1,200M over 50 years
- **Reservoir size**: 8,000-12,000 million gallons
- **Treatment capacity**: 150-250 million gallons/day
- **Water quality compliance**: >99% of time

## Educational Use

This project is designed for engineering coursework in:
- Systems optimization
- Water resources management
- Stochastic simulation
- Control systems design

**Students complete the control strategy implementation** while the core simulation infrastructure is provided.

## Translation Notes

This Python implementation was translated from the original MATLAB version with:
- ✅ 100% functionality preservation
- ✅ All comments and structure maintained
- ✅ Compatible with custom `ode4u` RK4 solver
- ✅ Integration with `multivarious` optimization package
- ✅ Full stochastic capability (gamma, lognormal distributions)

### Key Differences from MATLAB
- Array indexing: 0-based (Python) vs 1-based (MATLAB)
- Matrix operations: `@` operator for matrix multiply
- Import system: Explicit module imports required
- Random number generation: Uses NumPy/SciPy distributions

## Credits

**Original Author**: Professor Henri P. Gavin  
Department of Civil and Environmental Engineering  
Duke University

**Python Translation**: 2024-2025  
Translated for CEE 251L course deployment

## License

Educational use only. Please contact Prof. Henri P. Gavin for permissions regarding other uses.

## Contact

For questions about this implementation:
- Course website: [Duke CEE 251L]
- Original MATLAB version: Prof. Henri P. Gavin

---

*This project demonstrates the application of optimization theory to real-world civil engineering challenges in sustainable water infrastructure design.*
