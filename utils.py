import csv
import json
import os

def export_results_csv(snr_range, ber_results, rmse_results, results_dir="results"):
    """
    Exports simulation BER and RMSE results to CSV files.
    """
    os.makedirs(results_dir, exist_ok=True)
    
    # 1. Export BER CSV
    ber_path = os.path.join(results_dir, "ber.csv")
    with open(ber_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        header = ["SNR_dB"] + [f"Bias_{bias}_sigma" for bias in ber_results.keys()]
        writer.writerow(header)
        for i, snr in enumerate(snr_range):
            row = [snr] + [ber_results[bias][i] for bias in ber_results.keys()]
            writer.writerow(row)
            
    # 2. Export RMSE CSV
    rmse_path = os.path.join(results_dir, "rmse.csv")
    with open(rmse_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        header = ["SNR_dB"] + [f"Bias_{bias}_sigma" for bias in rmse_results.keys()]
        writer.writerow(header)
        for i, snr in enumerate(snr_range):
            row = [snr] + [rmse_results[bias][i] for bias in rmse_results.keys()]
            writer.writerow(row)

def export_results_json(snr_range, results, file_path="results/simulation_results.json"):
    """
    Exports full simulation results to a structured JSON file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Convert numpy types to native Python types for JSON compatibility
    json_data = {
        "snr_range": [int(snr) for snr in snr_range],
        "results": {
            str(bias): {
                "ber": [float(val) for val in data["ber"]],
                "rmse": [float(val) for val in data["rmse"]]
            } for bias, data in results.items()
        }
    }
    
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)
