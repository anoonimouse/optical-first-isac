# Optical-First Integrated Sensing and Communications (O-ISAC) DCO-OFDM Simulation

This repository contains the complete, modular Python simulation code to reproduce the numerical results for the joint **DCO-OFDM Optical Integrated Sensing and Communications (O-ISAC)** waveform analysis, as detailed in the review paper: *"Optical-First Integrated Sensing and Communications (O-ISAC): A Comprehensive Review, System Architecture, and Future Roadmap"*.

## Repository Structure

```
optical-first-isac/
│
├── README.md
├── requirements.txt
├── simulate.py       # Simulation orchestrator (Monte Carlo loop)
├── config.py         # Simulation parameters (aligns with Table V)
├── transmitter.py    # DCO-OFDM transmitter pipeline functions
├── receiver.py       # DCO-OFDM receiver pipeline functions
├── channel.py        # FSO propagation, Gamma-Gamma turbulence, AWGN, shot/thermal noise
├── sensing.py        # Sensing receiver phase & sub-sample delay/range estimators
├── qam.py            # QAM Gray mapping (QPSK / 16-QAM) modulation/demodulation
├── ofdm.py           # Core OFDM operations (Hermitian symmetry, FFT/IFFT)
├── metrics.py        # Performance metrics (Bit Error Rate and range RMSE)
├── plots.py          # Script to generate Figures 4(a) and 4(b)
├── utils.py          # Data export utilities (CSV and JSON)
├── results/          # Generated output files (ber.csv, rmse.csv, logs)
└── figures/          # Generated plots (figure4a.png, figure4b.png)
```

## Setup Instructions

### Python Version
The codebase is written and tested for **Python 3.8+**.

### Installation
Clone this repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

The key dependencies are:
- `numpy`
- `scipy`
- `matplotlib`
- `pandas`

## Parameter Values (Table V matching)
The parameters defined in `config.py` correspond exactly to Table V of the paper:

| Parameter | Symbol / Value | Description |
| :--- | :--- | :--- |
| **Number of Subcarriers** | `FFT_SIZE = 256` | FFT/IFFT length |
| **Active Subcarriers** | `ACTIVE_SUBCARRIERS = 127` | Subcarrier count for data |
| **Total Bandwidth** | `BANDWIDTH = 1e9` | 1 GHz bandwidth |
| **Subcarrier Spacing** | `SUBCARRIER_SPACING = 3.9e6` | 3.9 MHz spacing |
| **OFDM Frame Symbols** | `FRAME_SYMBOLS = 32` | Symbols per frame |
| **Constellation Order** | `QAM_ORDER = 4` | 4-QAM (QPSK) mapping |
| **DC Bias Scaling** | `BIAS = 2` | DC offset scaling factor ($\kappa$) |
| **Target Physical Distance** | `TARGET_RANGE = 200` | Physical range (200 m) |
| **PD Responsivity** | `RESPONSIVITY = 0.6` | Responsivity in A/W |
| **Comm Path Loss** | `COMM_PATH_LOSS = -2.2` | Attenuation in dB |
| **Sensing Path Loss** | `SENSING_PATH_LOSS = -23.2` | Attenuation in dB |
| **Monte Carlo Frames** | `MONTE_CARLO = 200` | Simulation trials |

## How to Run the Simulation & Reproduce the Figures

To run the Monte Carlo simulation engine and regenerate the paper figures:

```bash
python simulate.py
```

### Outputs Generated
Upon execution, the script automatically performs the simulation and exports all outputs:
1. **Performance Plots:**
   - `figures/figure4a.png` (Communication BER vs. SNR)
   - `figures/figure4b.png` (Sensing Ranging RMSE vs. SNR)
2. **Raw Data CSVs:**
   - `results/ber.csv`
   - `results/rmse.csv`
3. **Structured Logs:**
   - `results/simulation_results.json`
