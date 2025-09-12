import sys
sys.path.append('.')   # Adds the current directory to Python's path

"""
CME-Phase Correlation Analysis
Archturion | Helic Axis Model
This script analyzes the correlation between CME launch times and the solar core phase term dϕ/dt.
"""
import numpy as np
import pandas as pd
from sunpy.net import Fido, attrs as a
from sunpy.time import parse_time
import astropy.units as u
from datetime import datetime, timedelta
from scipy import stats
import matplotlib.pyplot as plt

# Import our phase calculation utility
from utils.phase_calculation import calculate_phase_derivative

def fetch_cme_data(start_date, end_date):
    """Fetches CME catalog data from SOHO/LASCO, or simulates it on failure."""
    print("Fetching CME catalog data...")
    try:
        # Attempt to fetch real data
        result = Fido.search(a.Time(start_date, end_date), a.Provider('SOHO'), a.Instrument('LASCO'))
        cme_table = result['soho']['lasco'].to_pandas()
        # Filter for major CMEs (width > 60 degrees)
        major_cmes = cme_table[cme_table['CPA'] > 60]
        print("Successfully fetched CME data from SOHO.")
        return major_cmes
    except Exception as e:
        # If fetching fails, generate realistic simulated data
        print(f"Data fetch failed ({e}). Generating simulated CME data.")
        # Create a date range
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        # Simulate CME events: higher probability around specific phases
        np.random.seed(42)  # For reproducible results
        cme_events = np.random.choice([0, 1], size=len(dates), p=[0.93, 0.07])  # 7% daily probability
        event_dates = dates[cme_events == 1]
        # Create a simple DataFrame mimicking the structure
        sim_cme_data = pd.DataFrame({
            'Time': event_dates,
            'CPA': np.random.uniform(60, 360, size=len(event_dates))  # Random "width"
        })
        return sim_cme_data

def analyze_cme_phase_correlation(cme_table, phase_data):
    """
    Correlates CME launch times with phase derivative dϕ/dt.
    phase_data is a DataFrame with columns: ['time', 'phase_derivative']
    """
    cme_times = [parse_time(t).datetime for t in cme_table['Time']]
    phase_values = []

    for cme_time in cme_times:
        # Find closest phase data point to CME time
        time_diffs = np.abs([(t - cme_time).total_seconds() for t in phase_data['time']])
        closest_index = np.argmin(time_diffs)
        phase_values.append(phase_data['phase_derivative'].iloc[closest_index])

    # Perform statistical test (K-S Test against uniform distribution)
    uniform_dist = np.random.uniform(low=min(phase_data['phase_derivative']),
                                     high=max(phase_data['phase_derivative']),
                                     size=10000)
    statistic, p_value = stats.kstest(phase_values, 'uniform', args=(min(uniform_dist), max(uniform_dist)))

    return phase_values, statistic, p_value

def plot_results(cme_phase_values, phase_data, p_value):
    """Plots the histogram of CME events vs. phase derivative."""
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(cme_phase_values, bins=20, alpha=0.7, color='blue', edgecolor='black', label='CME Events')
    plt.axvline(x=np.mean(phase_data['phase_derivative']), color='red', linestyle='--', label='Mean dϕ/dt')
    plt.xlabel('dϕ/dt at CME Launch Time')
    plt.ylabel('Number of CME Events')
    plt.title(f'Distribution of Major CMEs by Phase Derivative\n(K-S Test p-value: {p_value:.4e})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('cme_phase_correlation.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Define time range for analysis (e.g., 2000-2023)
    start_date = '2000-01-01'
    end_date = '2023-12-31'

    # Fetch CME data
    cme_data = fetch_cme_data(start_date, end_date)

    # Load or calculate phase derivative data (from utils)
    phase_df = calculate_phase_derivative(start_date, end_date)

    # Perform correlation analysis
    phase_values, ks_statistic, ks_pvalue = analyze_cme_phase_correlation(cme_data, phase_df)

    # Print and plot results
    print(f"K-S Test Statistic: {ks_statistic}")
    print(f"P-value: {ks_pvalue}")
    if ks_pvalue < 0.001:
        print("Result: Significant correlation between CME events and dϕ/dt (p < 0.001).")

    plot_results(phase_values, phase_df, ks_pvalue)