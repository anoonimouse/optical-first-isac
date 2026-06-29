import numpy as np
from ofdm import fft
from qam import qam_demodulate

def photodiode(r_optical, responsivity):
    """
    Converts optical power to photocurrent.
    """
    return r_optical * responsivity

def remove_dc(r):
    """
    Removes the DC bias component from the received electrical signal.
    """
    return r - np.mean(r)

def equalizer(R_comm, h_channel):
    """
    Performs one-tap frequency-domain equalization.
    """
    return R_comm / h_channel

def demodulate(symbols, M):
    """
    Demodulates received symbols back into bits.
    """
    return qam_demodulate(symbols, M)

def calculate_BER(tx_bits, rx_bits):
    """
    Computes the Bit Error Rate (BER).
    """
    return np.sum(tx_bits != rx_bits) / len(tx_bits)

def decode_dco_ofdm_comm(r_comm_noisy, N, M_qam, atten_db, responsivity):
    """
    Full communication receiver pipeline.
    """
    # 1. Photodiode conversion
    r_elec = photodiode(r_comm_noisy, responsivity)
    
    # 2. FFT
    R_comm = fft(r_elec)
    
    # 3. Equalizer (channel gain = responsivity * path loss factor)
    h_gain = responsivity * (10**(-atten_db / 20.0))
    R_eq = equalizer(R_comm, h_gain)
    
    # 4. Extract active subcarriers and demodulate
    rx_symbols = R_eq[1:N//2]
    rx_bits = demodulate(rx_symbols, M_qam)
    
    return rx_bits
