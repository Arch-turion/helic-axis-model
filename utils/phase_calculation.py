"""
Phase Calculation Utility
Calculates the solar core phase term ϕ(t) and its derivative dϕ/dt from helioseismology data.
"""

import numpy as np
import pandas as pd
from sunpy.net import Fido, attrs as a
from datetime import datetime, timedelta

def fetch_helioseismology_data(time_range):
    """Placeholder function to fetch core rotation rate data."""
    # In practice, this would fetch real data from SDO/HMI or MDI
    # For now, we simulate a data stream with a ~27-day periodicity (solar rotation)
    dates = pd.date_range(start=time_range[0], end=time_range[1], freq='D')
    base_period = 27.0  # days
    noise = np.random.normal(0, 0.1, len(dates))
    omega_c = (2*np.pi / base_period) + 0.1 * np.sin(2*np.pi * dates.dayofyear / 365.25) + noise
    return dates, omega_c

def calculate_phase_derivative(start_date, end_date):
    """Calculates dϕ/dt from the core rotation rate ω_c(t)."""
    dates, omega_c = fetch_helioseismology_data((start_date, end_date))
    
    # Calculate phase ϕ(t) = ∫ ω_c(t) dt
    phase = np.cumsum(omega_c) * (1.0)  # Integral approximation
    # Calculate derivative dϕ/dt ≈ ω_c(t)
    phase_derivative = omega_c
    
    return pd.DataFrame({'time': dates, 'phase_derivative': phase_derivative, 'phase': phase})