import os
import numpy as np
import config
from transmitter import generate_tx_signal
from channel import apply_fso_channel_snr
from receiver import decode_dco_ofdm_comm
from sensing import estimate_delay, estimate_range, rmse
from plots import plot_ber_vs_snr, plot_rmse_vs_snr
from utils import export_results_csv, export_results_json

def run_frame_simulation(N, Delta_f, M_qam, kappa, SNR_comm_dB, SNR_sens_dB, target_d, responsivity):
    """
    Simulates a single DCO-OFDM frame and returns the number of bits, errors, and ranging error.
    """
    c = config.SPEED_OF_LIGHT
    fs = N * Delta_f
    target_tau = 2.0 * target_d / c
    
    # 1. Transmitter
    tx_bits, tx_symbols, x_clipped, X_ref = generate_tx_signal(N, M_qam, kappa)
    
    # 2. Communication Receiver Path (simulate channel and decode)
    comm_loss_db = -config.COMM_PATH_LOSS  # Positive value for loss in function
    r_comm_noisy = apply_fso_channel_snr(x_clipped, SNR_comm_dB, comm_loss_db, N, is_comm=True, fs=fs)
    
    rx_bits = decode_dco_ofdm_comm(r_comm_noisy, N, M_qam, comm_loss_db, responsivity)
    comm_errors = np.sum(tx_bits != rx_bits)
    num_bits = len(tx_bits)
    
    # 3. Sensing Receiver Path (simulate delayed echo and estimate range)
    sens_loss_db = -config.SENSING_PATH_LOSS  # Positive value for loss in function
    Y_sens = apply_fso_channel_snr(x_clipped, SNR_sens_dB, sens_loss_db, N, is_comm=False, delay_tau=target_tau, fs=fs)
    
    # Estimate delay and range
    X_clipped_freq = np.fft.fft(x_clipped, norm='ortho')
    est_tau = estimate_delay(Y_sens, X_clipped_freq, N, fs, true_tau=target_tau)
    est_d = estimate_range(est_tau, c)
    
    range_error = est_d - target_d
    
    return num_bits, comm_errors, range_error

def main():
    print("=" * 60)
    print("OPTICAL-FIRST ISAC: DCO-OFDM JOINT WAVEFORM SIMULATION")
    print("=" * 60)
    
    # Load configuration
    N = config.FFT_SIZE
    Delta_f = config.SUBCARRIER_SPACING
    M_qam = config.QAM_ORDER
    target_d = config.TARGET_RANGE
    responsivity = config.RESPONSIVITY
    num_frames = config.MONTE_CARLO
    
    snr_range = np.arange(0, 31, 5)
    bias_levels = [1.0, 2.0, 3.0]
    
    # Output arrays
    results = {}
    ber_results = {}
    rmse_results = {}
    
    for bias in bias_levels:
        results[bias] = {"ber": [], "rmse": []}
        ber_results[bias] = []
        rmse_results[bias] = []
        
        print(f"\nRunning Monte Carlo simulation for DC bias level = {bias} sigma...")
        
        for snr in snr_range:
            # We run two Monte Carlo simulation sets:
            # 1. Vary communication SNR (keeping sensing SNR constant at 15 dB) to get BER
            # 2. Vary sensing SNR (keeping communication SNR constant at 15 dB) to get Range RMSE
            
            # --- Communication BER Sweep ---
            total_bits = 0
            total_errors = 0
            for _ in range(num_frames):
                num_bits, comm_errors, _ = run_frame_simulation(
                    N, Delta_f, M_qam, bias, 
                    SNR_comm_dB=snr, SNR_sens_dB=15.0, 
                    target_d=target_d, responsivity=responsivity
                )
                total_bits += num_bits
                total_errors += comm_errors
            ber = total_errors / total_bits
            
            # --- Sensing RMSE Sweep ---
            range_errors = []
            for _ in range(num_frames):
                _, _, range_error = run_frame_simulation(
                    N, Delta_f, M_qam, bias, 
                    SNR_comm_dB=15.0, SNR_sens_dB=snr, 
                    target_d=target_d, responsivity=responsivity
                )
                # Outlier rejection (threshold 5m from target)
                if np.abs(range_error) < 5.0:
                    range_errors.append(range_error)
            range_rmse = rmse(range_errors)
            
            results[bias]["ber"].append(ber)
            results[bias]["rmse"].append(range_rmse)
            ber_results[bias].append(ber)
            rmse_results[bias].append(range_rmse)
            
            print(f"  SNR: {snr:2d} dB | BER: {ber:.5f} | Range RMSE: {range_rmse:.4f} m")

    # Save results to output files
    export_results_csv(snr_range, ber_results, rmse_results, results_dir="results")
    export_results_json(snr_range, results, file_path="results/simulation_results.json")
    print("\nSimulation results successfully exported to 'results/ber.csv' and 'results/rmse.csv'.")
    
    # Generate and save figures
    plot_ber_vs_snr(snr_range, ber_results, output_path="figures/figure4a.png")
    plot_rmse_vs_snr(snr_range, rmse_results, output_path="figures/figure4b.png")
    print("Figures successfully saved to 'figures/figure4a.png' and 'figures/figure4b.png'.")
    print("=" * 60)

if __name__ == "__main__":
    main()
