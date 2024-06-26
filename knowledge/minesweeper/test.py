a = [1, 2, 3]
b = [2, 3, 4]
c = [5, 6, 7]

abc = [a, b, c]

for letter in abc:
    if 2 in letter:
        for letter in abc:
            if 2 in letter:
                letter.remove(2)
    print(letter)
