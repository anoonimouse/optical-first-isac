import matplotlib.pyplot as plt
import numpy as np
import os

def plot_ber_vs_snr(snr_range, ber_results, ber_se, output_path="figures/figure4a.png"):
    """
    Plots Communication BER vs. Electrical SNR for different DC bias levels with 95% confidence intervals.
    """
    plt.figure(figsize=(7, 5))
    colors = {1.0: "r", 2.0: "g", 3.0: "b"}
    markers = {1.0: "o", 2.0: "s", 3.0: "^"}
    
    for bias, ber in ber_results.items():
        ber_arr = np.array(ber)
        se_arr = np.array(ber_se[bias])
        plt.semilogy(snr_range, ber_arr, color=colors.get(bias, "k"), 
                     marker=markers.get(bias, "x"), label=f"Bias = {bias} $\sigma$")
        
        # 95% Confidence Interval: mean +/- 1.96 * SE
        lower = np.maximum(1e-6, ber_arr - 1.96 * se_arr)
        upper = ber_arr + 1.96 * se_arr
        plt.fill_between(snr_range, lower, upper, color=colors.get(bias, "k"), alpha=0.1)
        
    plt.xlabel("Electrical SNR (dB)")
    plt.ylabel("Bit Error Rate (BER)")
    plt.grid(True, which="both", ls="--")
    plt.ylim([1e-5, 1.0])
    plt.legend()
    plt.title("Communication BER vs. SNR (with 95% CI)")
    
    # On-plot parameter annotations
    param_text = "Simulation Settings:\n- Waveform: DCO-OFDM\n- FFT Size: 256\n- Subcarriers: 127 active\n- Monte Carlo: 200 trials\n- Seed: 42"
    plt.text(0.05, 0.05, param_text, transform=plt.gca().transAxes, fontsize=9,
             verticalalignment='bottom', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.85))
             
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_rmse_vs_snr(snr_range, rmse_results, rmse_se, output_path="figures/figure4b.png"):
    """
    Plots Sensing Range RMSE vs. Electrical SNR for different DC bias levels with 95% confidence intervals.
    """
    plt.figure(figsize=(7, 5))
    colors = {1.0: "r", 2.0: "g", 3.0: "b"}
    markers = {1.0: "o", 2.0: "s", 3.0: "^"}
    
    for bias, rmse_val in rmse_results.items():
        rmse_arr = np.array(rmse_val)
        se_arr = np.array(rmse_se[bias])
        plt.plot(snr_range, rmse_arr, color=colors.get(bias, "k"), 
                 marker=markers.get(bias, "x"), label=f"Bias = {bias} $\sigma$")
        
        # 95% Confidence Interval: mean +/- 1.96 * SE
        lower = np.maximum(0.0, rmse_arr - 1.96 * se_arr)
        upper = rmse_arr + 1.96 * se_arr
        plt.fill_between(snr_range, lower, upper, color=colors.get(bias, "k"), alpha=0.1)
        
    plt.xlabel("Electrical SNR (dB)")
    plt.ylabel("Range RMSE (m)")
    plt.grid(True, which="both", ls="--")
    plt.ylim([0.0, 0.5])
    plt.legend()
    plt.title("Ranging RMSE vs. SNR (with 95% CI)")
    
    # On-plot parameter annotations
    param_text = "Simulation Settings:\n- Target Range: 200 m\n- Channel: FSO\n- Monte Carlo: 200 trials\n- Seed: 42"
    plt.text(0.55, 0.55, param_text, transform=plt.gca().transAxes, fontsize=9,
             verticalalignment='bottom', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.85))
             
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
