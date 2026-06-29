# config.py

# OFDM parameters
FFT_SIZE = 256
ACTIVE_SUBCARRIERS = 127  # Hermitian symmetry active subcarriers (1 to N/2-1)
BANDWIDTH = 1.0e9         # 1 GHz bandwidth
SUBCARRIER_SPACING = 3.9e6 # 3.9 MHz subcarrier spacing
FRAME_SYMBOLS = 32        # symbols per frame

# Waveform parameters
QAM_ORDER = 4             # 4 for QPSK, 16 for 16-QAM
BIAS = 2.0                # DC bias scaling factor (kappa)

# Ranging/Sensing target parameters
TARGET_RANGE = 200.0      # Target distance in meters
SPEED_OF_LIGHT = 3.0e8    # Speed of light in m/s

# Photodiode parameters
RESPONSIVITY = 0.6        # PD responsivity in A/W

# Path loss parameters (in dB)
COMM_PATH_LOSS = -2.2     # -2.2 dB attenuation for communication path
SENSING_PATH_LOSS = -23.2 # -23.2 dB attenuation for sensing path (round-trip)

# Monte Carlo parameters
MONTE_CARLO = 200         # Number of Monte Carlo trials (frames)
