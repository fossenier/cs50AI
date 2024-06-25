a = set((1, 2, 3))
b = set((1, 2, 3))

print(a.issubset(b))
print(a.difference(b) == set())
print(a == b)
