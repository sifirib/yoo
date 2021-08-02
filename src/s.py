def multiple(a, b, r=0):
    r += (1 - ((b<=0) * 2)) * a
    b -= 1 - ((b<=0) * 2)
    if b == 0:
        return r
    return multiple(a, b, r)

print(multiple(-5, 10))