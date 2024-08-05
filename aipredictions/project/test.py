#import math
import numpy as np

# Scalar values
x = 3
y = 4

# Using math.atan2 via np.math
result_scalar = np.math.atan2(y, x)
print("Result for scalars with np.math.atan2:", result_scalar)

# Array values
x_array = np.array([3, 1, -1, -3])
y_array = np.array([4, 2, -2, -4])

# Using numpy.arctan2 for arrays
result_array = np.arctan2(y_array, x_array)
print("Result for arrays with np.arctan2:", result_array)