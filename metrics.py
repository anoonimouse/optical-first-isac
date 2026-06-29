import numpy as np

def calculate_BER(tx_bits, rx_bits):
    """
    Computes the Bit Error Rate (BER).
    """
    if len(tx_bits) == 0:
        return 1.0
    return np.sum(tx_bits != rx_bits) / len(tx_bits)

def rmse(errors):
    """
    Computes the Root Mean Square Error (RMSE).
    """
    if len(errors) == 0:
        return 100.0  # Fallback for outlier/no samples
    return np.sqrt(np.mean(np.array(errors)**2))
