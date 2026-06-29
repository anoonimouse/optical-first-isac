import numpy as np

def qam_modulate(bits, M):
    """
    Modulate input bits into QAM symbols.
    
    Parameters:
        bits (ndarray): Binary array of bits.
        M (int): QAM modulation order (4 or 16).
        
    Returns:
        ndarray: Complex QAM symbols normalized to unit average power.
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
            symbols[i] = (real + 1j*imag) / np.sqrt(2.0)
        return symbols
    elif M == 16:
        bits_per_sym = 4
        symbols = np.zeros(num_bits // bits_per_sym, dtype=complex)
        # Gray mapping for 16-QAM
        mapping = {
            (0,0,0,0): -3-3j, (0,0,0,1): -3-1j, (0,0,1,1): -3+1j, (0,0,1,0): -3+3j,
            (0,1,0,0): -1-3j, (0,1,0,1): -1-1j, (0,1,1,1): -1+1j, (0,1,1,0): -1+3j,
            (1,1,0,0): 1-3j,  (1,1,0,1): 1-1j,  (1,1,1,1): 1+1j,  (1,1,1,0): 1+3j,
            (1,0,0,0): 3-3j,  (1,0,0,1): 3-1j,  (1,0,1,1): 3+1j,  (1,0,1,0): 3+3j
        }
        for i in range(len(symbols)):
            b = tuple(bits[i*4:(i+1)*4])
            symbols[i] = mapping[b] / np.sqrt(10.0)
        return symbols
    else:
        raise ValueError("Only 4-QAM and 16-QAM are supported.")

def qam_demodulate(symbols, M):
    """
    Demodulate QAM symbols back to bits.
    
    Parameters:
        symbols (ndarray): Complex received QAM symbols.
        M (int): QAM modulation order (4 or 16).
        
    Returns:
        ndarray: Decoded binary bits.
    """
    num_syms = len(symbols)
    if M == 4:
        bits = np.zeros(num_syms * 2, dtype=int)
        for i in range(num_syms):
            real_val = np.real(symbols[i])
            imag_val = np.imag(symbols[i])
            bits[i*2] = 0 if real_val > 0 else 1
            bits[i*2+1] = 0 if imag_val > 0 else 1
        return bits
    elif M == 16:
        bits = np.zeros(num_syms * 4, dtype=int)
        constellation = np.array([-3, -1, 1, 3]) / np.sqrt(10.0)
        for i in range(num_syms):
            real_val = np.real(symbols[i])
            imag_val = np.imag(symbols[i])
            
            r_idx = np.argmin(np.abs(constellation - real_val))
            i_idx = np.argmin(np.abs(constellation - imag_val))
            
            r_bits = {0: (0,0), 1: (0,1), 2: (1,1), 3: (1,0)}[r_idx]
            i_bits = {0: (0,0), 1: (0,1), 2: (1,1), 3: (1,0)}[i_idx]
            
            bits[i*4 : i*4+2] = r_bits
            bits[i*4+2 : i*4+4] = i_bits
        return bits
    else:
        raise ValueError("Only 4-QAM and 16-QAM are supported.")
