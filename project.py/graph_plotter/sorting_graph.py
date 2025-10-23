import time
import matplotlib.pyplot as plt
import random

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

input_sizes = list(range(1000, 10001, 1000))  # From 1,000 to 10,000
times = []

for size in input_sizes:
    data = list(range(size))
    target = -1  # Ensure worst-case (not found)
    
    start_time = time.time()
    linear_search(data, target)
    end_time = time.time()
    
    times.append((end_time - start_time) * 1000)  # Convert to ms

# Plotting
plt.plot(input_sizes, times, marker='o')
plt.title('Linear Search Time Complexity')
plt.xlabel('Input Size (n)')
plt.ylabel('Time (ms)')
plt.grid(True)
plt.show()
