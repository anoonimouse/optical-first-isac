import numpy as np

def qam_modulate(bits, M):
    """
    Modulate bits into QAM symbols.
    M can be 4 (QPSK) or 16.
    """
    num_bits = len(bits)
    if M == 4:
        bits_per_sym = 2
        symbols = np.zeros(num_bits // bits_per_sym, dtype=complex)
        for i in range(len(symbols)):
            b = bits[i*2:(i+1)*2]
            # Gray mapping for QPSK
            real = 1 - 2*b[0]
            imag = 1 - 2*b[1]
            symbols[i] = (real + 1j*imag) / np.sqrt(2)
        return symbols
    elif M == 16:
        bits_per_sym = 4
        symbols = np.zeros(num_bits // bits_per_sym, dtype=complex)
        # 16-QAM mapping
        mapping = {
            (0,0,0,0): -3-3j, (0,0,0,1): -3-1j, (0,0,1,1): -3+1j, (0,0,1,0): -3+3j,
            (0,1,0,0): -1-3j, (0,1,0,1): -1-1j, (0,1,1,1): -1+1j, (0,1,1,0): -1+3j,
            (1,1,0,0): 1-3j,  (1,1,0,1): 1-1j,  (1,1,1,1): 1+1j,  (1,1,1,0): 1+3j,
            (1,0,0,0): 3-3j,  (1,0,0,1): 3-1j,  (1,0,1,1): 3+1j,  (1,0,1,0): 3+3j
        }
        for i in range(len(symbols)):
            b = tuple(bits[i*4:(i+1)*4])
            symbols[i] = mapping[b] / np.sqrt(10)
        return symbols
    else:
        raise ValueError("Only 4-QAM and 16-QAM are supported.")

def generate_dco_ofdm_waveform(tx_symbols, N, kappa):
    """
    Generate DCO-OFDM real-valued signal with Hermitian symmetry and DC bias clipping.
    
    Parameters:
        tx_symbols (ndarray): Modulated QAM symbols.
        N (int): Number of subcarriers.
        kappa (float): DC bias scaling factor (b = kappa * std(x)).
        
    Returns:
        tuple: (x_clipped, X) where x_clipped is the time-domain clipped signal,
               and X is the full Hermitian symmetric frequency-domain signal.
    """
    X = np.zeros(N, dtype=complex)
    X[1:N//2] = tx_symbols
    X[N//2+1:] = np.conj(tx_symbols[::-1])
    
    # IFFT to obtain real-valued time domain signal
    x = np.fft.ifft(X, norm='ortho')
    x = np.real(x)
    
    # DC bias scaling and clipping
    sigma_x = np.std(x)
    DC_bias = kappa * sigma_x
    x_biased = x + DC_bias
    x_clipped = np.maximum(0, x_biased)
    return x_clipped, X
