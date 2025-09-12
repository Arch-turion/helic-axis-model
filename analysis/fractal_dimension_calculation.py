```python
"""
Calculates fractal dimension of sunspot regions.
"""
import numpy as np
from skimage import measure
def calculate_fractal_dimension(magnetogram_data, thresholds=[50, 100, 150]):
    """
    Calculates fractal dimension of magnetic structures
    using box-counting method at multiple thresholds.
    """
    dimensions = []
    for threshold in thresholds:
        # Create binary image
        binary_image = np.abs(magnetogram_data) > threshold
        # Calculate fractal dimension
        dim = measure.box_count(binary_image)
        dimensions.append(dim)
    return np.mean(dimensions)
```
