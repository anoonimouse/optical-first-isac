import numpy as np

def apply_hermitian(tx_symbols, N):
    """
    Arranges complex symbols to satisfy Hermitian symmetry.
    X[0] = 0 (DC component)
    X[1:N/2] = symbols
    X[N/2] = 0 (Nyquist component)
    X[N/2+1:] = conj(symbols[::-1])
    """
    X = np.zeros(N, dtype=complex)
    X[1:N//2] = tx_symbols
    X[N//2+1:] = np.conj(tx_symbols[::-1])
    return X

def ifft(X):
    """
    Computes standard IFFT and extracts the real part.
    """
    x = np.fft.ifft(X, norm='ortho')
    return np.real(x)

def fft(x):
    """
    Computes standard FFT.
    """
    return np.fft.fft(x, norm='ortho')
