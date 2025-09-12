```python
"""
Fetches the SOHO/LASCO CME catalog.
"""
from sunpy.net import Fido, attrs as a
import pandas as pd
def fetch_cme_catalog(start_date, end_date):
    """
    Retrieves CME catalog data from SOHO/LASCO.
    Returns a pandas DataFrame.
    """
    result = Fido.search(a.Time(start_date, end_date),
                        a.Provider('SOHO'),
                        a.Instrument('LASCO'))
    cme_table = result['soho']['lasco'].to_pandas()
    return cme_table
```
