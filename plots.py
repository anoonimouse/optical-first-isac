import matplotlib.pyplot as plt
import os

def plot_ber_vs_snr(snr_range, ber_results, output_path="figures/figure4a.png"):
    """
    Plots Communication BER vs. Electrical SNR for different DC bias levels.
    """
    plt.figure(figsize=(7, 5))
    colors = {1.0: "r", 2.0: "g", 3.0: "b"}
    markers = {1.0: "o", 2.0: "s", 3.0: "^"}
    
    for bias, ber in ber_results.items():
        plt.semilogy(snr_range, ber, color=colors.get(bias, "k"), 
                     marker=markers.get(bias, "x"), label=f"Bias = {bias} $\sigma$")
        
    plt.xlabel("Electrical SNR (dB)")
    plt.ylabel("Bit Error Rate (BER)")
    plt.grid(True, which="both", ls="--")
    plt.ylim([1e-5, 1.0])
    plt.legend()
    plt.title("Communication BER vs. SNR")
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_rmse_vs_snr(snr_range, rmse_results, output_path="figures/figure4b.png"):
    """
    Plots Sensing Range RMSE vs. Electrical SNR for different DC bias levels.
    """
    plt.figure(figsize=(7, 5))
    colors = {1.0: "r", 2.0: "g", 3.0: "b"}
    markers = {1.0: "o", 2.0: "s", 3.0: "^"}
    
    for bias, rmse_val in rmse_results.items():
        plt.plot(snr_range, rmse_val, color=colors.get(bias, "k"), 
                 marker=markers.get(bias, "x"), label=f"Bias = {bias} $\sigma$")
        
    plt.xlabel("Electrical SNR (dB)")
    plt.ylabel("Range RMSE (m)")
    plt.grid(True, which="both", ls="--")
    plt.ylim([0.0, 0.5])
    plt.legend()
    plt.title("Ranging RMSE vs. SNR")
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
