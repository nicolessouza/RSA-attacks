import math

def egcd(a, b):
    """Algoritmo extendido de Euclides para encontrar o inverso modular."""
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    """Encontra o inverso modular de 'a' modulo 'm'."""
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('Inverso modular não existe para os números fornecidos.')
    else:
        return x % m

def ler_arquivo_eml_e_converter_para_lista(nome_arquivo):
    """
    Lê um arquivo .eml e converte o corpo e assunto para uma lista de inteiros
    """

    email = ler_arquivo_eml(nome_arquivo)

    corpo = email["corpo"]
    assunto = email["assunto"]

    # Tirando espaços, quebras de linhas e '=' do corpo do e-mail
    corpo = corpo.replace(' ', '')
    corpo = corpo.replace('\n', '')
    corpo = corpo.replace('=', '')

    corpo, chave = corpo.split("---")
    # a chave esta no formato (N, e)
    N = int(chave.split(',')[0][1:])
    e = int(chave.split(',')[1][:-1])

    blocos_corpo = [int(numero) for numero in corpo.split('_')]
    blocos_assunto = [int(numero) for numero in assunto.split('_')]

    return {"N": N, "e": e, "corpo": blocos_corpo, "assunto": blocos_assunto}

import email
from email import policy
from email.parser import BytesParser

def ler_arquivo_eml(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as arquivo:
        # Use BytesParser para analisar o arquivo .eml
        msg = BytesParser(policy=policy.default).parse(arquivo)
        
        # Exibindo informações do e-mail
        assunto = msg.get('Subject')
        corpo = obter_corpo_email(msg)

    return {'assunto': assunto, 'corpo': corpo}
        

def obter_corpo_email(msg):
    # Se o e-mail tiver várias partes, como texto e HTML, você pode personalizar essa função para obter o corpo desejado
    if msg.is_multipart():
        for parte in msg.iter_parts():
            if parte.get_content_type() == 'text/plain':
                return parte.get_payload()
    else:
        return msg.get_payload()

# Função que fatora em números primos
def fatorar_em_primos(numero):
    fatores = []
    while numero % 2 == 0:
        fatores.append(2)
        numero = numero // 2
    for i in range(3, int(math.sqrt(numero)) + 1, 2):
        while numero % i == 0:
            fatores.append(int(i))
            numero = numero // i
    if numero > 2:
        fatores.append(int(numero))
    return list(set(fatores))

# Descriptografando sabendo p e q
def decrypt_pq(c, p, q, e):
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    return pow(c, d, p * q)
