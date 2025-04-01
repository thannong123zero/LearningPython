import numpy as np

# Creating a numpy array
my_numpy_array = np.array([1, 2, 3, 4, 5])

# Accessing elements
print(my_numpy_array[0])  # Output: 1

# Modifying elements
my_numpy_array[1] = 10
print(my_numpy_array)  # Output: [ 1 10  3  4  5]

# Adding elements (numpy arrays are immutable, so you need to create a new array)
my_numpy_array = np.append(my_numpy_array, 6)
print(my_numpy_array)  # Output: [ 1 10  3  4  5  6]

# Removing elements (numpy arrays are immutable, so you need to create a new array)
my_numpy_array = np.delete(my_numpy_array, 1)
print(my_numpy_array)  # Output: [1 3 4 5 6]