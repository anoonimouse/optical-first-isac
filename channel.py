import numpy as np

def apply_path_loss(x, atten_db):
    """
    Applies geometric and propagation path loss in dB.
    """
    h_atten = 10**(-atten_db / 20.0)
    return x * h_atten

def apply_gamma_gamma(x, alpha=2.29, beta=1.30):
    """
    Applies Gamma-Gamma scintillation to simulate moderate atmospheric turbulence.
    Mean of the channel intensity fluctuation is E[I] = 1.0.
    """
    alpha = max(alpha, 1e-3)
    beta = max(beta, 1e-3)
    
    # Generate Gamma-Gamma random variable
    Ix = np.random.gamma(alpha, 1.0/alpha, x.shape)
    Iy = np.random.gamma(beta, 1.0/beta, x.shape)
    I = Ix * Iy
    return x * I

def add_awgn(x, noise_var):
    """
    Adds Additive White Gaussian Noise (AWGN) to the signal.
    """
    noise = np.random.normal(0, np.sqrt(noise_var), x.shape)
    return x + noise

def add_shot_noise(x, responsivity, bandwidth, dark_current=1e-9):
    """
    Adds signal-dependent shot noise: sigma_shot^2 = 2 * q * (I_signal + I_dark) * B.
    """
    q = 1.602e-19
    I_sig = responsivity * x
    I_sig = np.maximum(0.0, I_sig)  # Ensure non-negative current
    var_shot = 2.0 * q * (I_sig + dark_current) * bandwidth
    noise = np.random.normal(0, np.sqrt(var_shot), x.shape)
    return x + noise

def add_thermal_noise(x, bandwidth, temperature=290.0, load_resistance=50.0):
    """
    Adds thermal noise: sigma_thermal^2 = 4 * k_B * T * B / R_L.
    """
    k_B = 1.38e-23
    var_thermal = (4.0 * k_B * temperature * bandwidth) / load_resistance
    noise = np.random.normal(0, np.sqrt(var_thermal), x.shape)
    return x + noise

def apply_fso_channel_snr(x_clipped, snr_db, atten_db, N, is_comm=True, delay_tau=0.0, fs=1e9, use_turbulence=False):
    """
    Utility wrapper to simulate FSO propagation with path loss, optional turbulence, 
    and AWGN scaled to a target SNR for easy Monte Carlo sweeps.
    """
    h_atten_factor = 10**(-atten_db / 20.0)
    
    if is_comm:
        # Path loss
        r = apply_path_loss(x_clipped, atten_db)
        # Optional Gamma-Gamma turbulence
        if use_turbulence:
            r = apply_gamma_gamma(r)
            
        # Scaling AWGN to target electrical SNR
        p_ac = np.var(r)
        noise_var = p_ac / (10**(snr_db / 10.0))
        r_noisy = add_awgn(r, noise_var)
        return r_noisy
    else:
        # Sensing path (delayed and attenuated echo)
        X_clipped = np.fft.fft(x_clipped, norm='ortho')
        T = 1.0 / fs
        freqs = np.fft.fftfreq(N, d=T)
        phase_shift = np.exp(-1j * 2 * np.pi * freqs * delay_tau)
        Y_sens_clean = h_atten_factor * X_clipped * phase_shift
        
        # Scintillation flat scaling factor per frame
        if use_turbulence:
            Ix = np.random.gamma(2.29, 1.0/2.29)
            Iy = np.random.gamma(1.30, 1.0/1.30)
            I = Ix * Iy
            Y_sens_clean = Y_sens_clean * I
            
        p_sens_rx = np.mean(np.abs(Y_sens_clean)**2)
        noise_var_sens = p_sens_rx / (10**(snr_db / 10.0))
        noise_sens = (np.random.normal(0, np.sqrt(noise_var_sens/2.0), N) + 
                      1j * np.random.normal(0, np.sqrt(noise_var_sens/2.0), N))
        return Y_sens_clean + noise_sens
