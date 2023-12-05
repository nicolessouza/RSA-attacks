import gmpy2
gmpy2.get_context().precision = 4096

from binascii import unhexlify
from functools import reduce
from gmpy2 import root, invert
from common_module_functions import PAndQFoundException
from utils import fatorar_em_primos
from math import gcd

EXPONENT = 3

def chinese_remainder_theorem(items):
    # Determine N, the product of all n_i
    N = 1
    for a, n in items:
        N *= n

    # Find the solution (mod N)
    result = 0
    for a, n in items:
        m = N // n
        r, s, d = extended_gcd(n, m)
        
        # If the gcd is not 1, try to factorize n
        if d != 1:
            p = gcd(n, m)
            q = n // p
            raise PAndQFoundException(p, q)

        result += a * s * m

    # Make sure we return the canonical solution.
    return result % N


def extended_gcd(a, b):
    x, y = 0, 1
    lastx, lasty = 1, 0

    while b:
        a, (q, b) = b, divmod(a, b)
        x, lastx = lastx - q * x, x
        y, lasty = lasty - q * y, y

    return (lastx, lasty, a)


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def hastads_broadcast_attack(ciphertexts, modulus):
    # modulus = [N1, N2, N3]
    # ciphertexts = [C1, C2, C3]

    C = chinese_remainder_theorem([(c, n) for c, n in zip(ciphertexts, modulus)])
    M = int(root(C, 3))
    return M