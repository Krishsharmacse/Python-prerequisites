def average(numbers=[1, 2, 3, 4, 5]):
    return sum(numbers) / len(numbers)

# Example usage:
print(average())  # Output: 3.0 (average of the default list)
print(average([10, 20, 30]))  # Output: 20.0 (average of the provided list)