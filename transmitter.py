import numpy as np
import config
from qam import qam_modulate
from ofdm import apply_hermitian, ifft

def generate_bits(num_bits):
    """
    Generates an array of random binary bits.
    """
    return np.random.randint(0, 2, num_bits)

def add_dc_bias(x, kappa):
    """
    Adds a DC bias scaling proportional to the standard deviation of the signal.
    """
    sigma_x = np.std(x)
    dc_bias = kappa * sigma_x
    return x + dc_bias, dc_bias

def clip_negative(x_biased):
    """
    Clips negative time-domain samples to model unipolar LED/laser diode intensity.
    """
    return np.maximum(0.0, x_biased)

def generate_tx_signal(N, M_qam, kappa):
    """
    Full transmitter pipeline for a single DCO-OFDM frame.
    
    Returns:
        tuple: (tx_bits, tx_symbols, x_clipped, X)
    """
    num_active = N // 2 - 1
    bits_per_sym = 2 if M_qam == 4 else 4
    num_bits = num_active * bits_per_sym
    
    tx_bits = generate_bits(num_bits)
    tx_symbols = qam_modulate(tx_bits, M_qam)
    X = apply_hermitian(tx_symbols, N)
    x = ifft(X)
    x_biased, dc_val = add_dc_bias(x, kappa)
    x_clipped = clip_negative(x_biased)
    
    return tx_bits, tx_symbols, x_clipped, X
