def add(a, b):
    a += b
    return a


a = 1
b = 2
c = add(a, b)
print(c)  # 3
print(a, b)  # 1, 2

a = [1, 2]
b = [3, 4]
c = add(a, b)
print(c)  # [1, 2, 3, 4]
print(a, b)  # [1, 2, 3, 4], [3, 4]

a = (1, 2)
b = (3, 4)
c = add(a, b)
print(c)  # (1, 2, 3, 4)
print(a, b)  # (1, 2), (3, 4)
