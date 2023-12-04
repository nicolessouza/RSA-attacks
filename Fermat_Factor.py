from math import ceil, sqrt
def Fermat_Factor(N):
    a = ceil(sqrt(N))
    while True:
        b2 = a*a - N
        b = sqrt(b2)
        if b.is_integer():
            break
        a += 1
    return int(a-b), int(a+b)