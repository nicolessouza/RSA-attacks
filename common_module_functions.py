import rsa
from math import gcd
from utils import fatorar_em_primos, modinv

def str_to_int(s):
    """Converte uma string para um número inteiro."""
    return int.from_bytes(s.encode(), 'big')

def int_to_str(i):
    """Converte um número inteiro para uma string."""
    return i.to_bytes((i.bit_length() + 7) // 8, 'big').decode()


def encrypt(msg, e, n):
    """Realiza a operação de encriptação usando o algoritmo RSA."""
    return pow(msg, e, n)

# definindo exceção para quando p e q são descobertos, ela retorna p e q
class PAndQFoundException(Exception):
    def __init__(self, p, q):
        self.p = p
        self.q = q

def attack(c1, c2, e1, e2, N):
    """Função de ataque ao RSA."""
    # print("Iniciando o ataque...")
    
    # Verifica se os expoentes são coprimos
    if gcd(e1, e2) != 1:
        raise ValueError("Expoentes e1 e e2 precisam ser coprimos.")
    
    # Calcula o inverso modular de e1 modulo e2
    x = modinv(e1, e2)
    
    # Calcula o coeficiente y usando o algoritmo extendido de Euclides
    y = (gcd(e1, e2) - e1 * x) // e2

    # Calcula o inverso modular de c2 modulo N
    try:
        temp = modinv(c2, N)
    except:
        print(f"Não foi possível encontrar o inverso modular de {c2} modulo {N}, logo, eles possuem um fator em comum.")
        
        # Fatorando o c2
        fatores = fatorar_em_primos(c2)
        for fator in fatores:
            if N % fator == 0:
                p = fator
        q = N // p
        
        # levanta um erro especial, indicando que p e q foram descobertos
        raise PAndQFoundException(p, q)

    # Calcula os termos do produto que resulta na mensagem original
    m1 = pow(c1, x, N)
    m2 = pow(temp, -y, N)
    
    # Retorna a mensagem descriptografada
    return (m1 * m2) % N

def generate_keys(size):
    # Gera as chaves n, e1, e2 para teste
    pub, priv = rsa.newkeys(size)
    return pub.n, pub.e