```python
"""
Fetches SDO/HMI data for helioseismic analysis.
"""
from sunpy.net import Fido, attrs as a
from datetime import datetime, timedelta
import sunpy.timeseries as ts
def fetch_hmi_series(start_time, end_time, series_type='hmi.V_45s'):
    """
    Fetches HMI time series data for a given time range.
    """
    query = Fido.search(a.Time(start_time, end_time),
                       a.Instrument('HMI'),
                       a.Physobs(series_type))
    try:
        downloaded_files = Fido.fetch(query)
        hmi_ts = ts.TimeSeries(downloaded_files)
        return hmi_ts
    except Exception as e:
        print(f"Error fetching SDO data: {e}")
        return None
```
