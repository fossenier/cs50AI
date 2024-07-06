data = {"a": [1, 2, 3], "b": [], "c": [2]}

numbers = set()
for value in data.values():
    for item in value:
        numbers.add(item)

print(numbers)
