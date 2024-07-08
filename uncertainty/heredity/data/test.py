"""
Simulating probability because I'm confused.
"""

N = 100000

from random import random

# Two magical dice
die1 = False  # always gives False
die2 = True  # always gives True

# Counters for the results
true_false_count = 0

# Simulate the rolls
for i in range(N):
    result1 = die1
    result2 = die2

    # 1% chance to flip the result of die1
    if random() < 0.01:
        result1 = not result1

    # 1% chance to flip the result of die2
    if random() < 0.01:
        result2 = not result2

    # Check if one die gives True and the other gives False
    if result1 != result2:
        true_false_count += 1

# Calculate the percentage
percentage = (true_false_count / N) * 100

print(
    f"Percentage of the time that one die is true and the other is false: {percentage:.2f}%"
)
