# Python program to illustrate ElGamal encryption
import sys

import random
from math import pow

a = random.randint(2, 10)


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b;
    else:
        return gcd(b, a % b)

    # Generating large random numbers



def sprawdz_zlozonosc_miller_rabin(a, d, n, r):
    if power(a, d, n) == 1:
        return False
    for j in range(r):
        if power(a, 2**j * d, n) == n-1:
            return False
    return True


def czy_pierwsza_miller_rabin(n, k=64):  # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    if n != int(n):
        return False
    n = int(n)
    if n == 0 or n == 1:
        return False
    if n == 2 or n == 3:
        return True
    r = 0
    d = n - 1
    while d%2 == 0:
        d = d // 2
        r += 1
    assert(2**r * d == n - 1)
    d = int(d)
    r = int(r)
    for i in range (k):
        a = random.randint(2, n - 2)
        if sprawdz_zlozonosc_miller_rabin(a, d, n, r):
            return False
    return True


def gen_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)

    return key


# Modular exponentiation
def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)

    return x % c


def find_primitive_root( p ):
    if p == 2:
        return 1
        #the prime divisors of p-1 are 2 and (p-1)/2 because
        #p = 2x + 1 where x is a prime
    p1 = 2
    p2 = (p-1) // p1

    #test random g's until one is found that is a primitive root mod p
    while( 1 ):
        g = random.randint( 2, p-1 )
        #g is a primitive root if for all prime factors of p-1, p[i]
        #g^((p-1)/p[i]) (mod p) is not congruent to 1
        print("jd")
        if not (power( g, (p-1)//p1, p ) == 1):
            if not power( g, (p-1)//p2, p ) == 1:
                return g

# Asymmetric encryption
def encrypt(msg, q, h, g):
    en_msg = []

    #k = gen_key(q)  # Private key for sender
    k = random.randrange(0, sys.maxsize)
    s = power(h, k, q)
    p = power(g, k, q)

    for i in range(0, len(msg)):
        en_msg.append(msg[i])

    print("uzywamy g^k = ", p)
    print("uzywamy g^ak = ", s)
    for i in range(0, len(en_msg)):
        en_msg[i] = s * ord(en_msg[i])

    return en_msg, p


def decrypt(en_msg, p, key, q):
    dr_msg = []
    h = power(p, key, q)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i] / h)))

    return dr_msg

# Mneu code
def menu():
    print("Witamy w pogramie szyfrujacym za pomoca algorymtu ElGamal\n")
    choice = "a"
    while choice != "P" and choice != "k":
        choice = input("Chcesz zaszyfrowac wiadomosc z pliku czy z konsoli? [P,k] \n")
        if choice != "P" and choice != "k":
            print("prosze podać P lub k")
    message = ""
    if choice == "k":
        while message == "":
            message = input("podaj wybrana wiadomosc \n")
            if message == "":
                print("nie udalo sie odczytac wiadomosci lub wiadomosc "
                      "jest pusta, prosze wprowadzic wiadomosc przez konsole")
    elif choice == "P":
        message = ""
        file = input("podaj nazwe pliku \n")
        if file.endswith('.txt'):
            message = read_file_message(file)
        else:
            file += ".txt"
            message = read_file_message(file)
        while message == -1:
            print("nie udalo sie odczytac wiadomosci lub wiadomosc "
                  "jest pusta, prosze wprowadzic wiadomosc przez konsole")
            message = input("podaj wybrana wiadomosc \n")

    return message

def read_file_message(message):
    try:
        message_plik = open(message, "r+")
    except IOError:
        print("Nie udalo sie otworzyc pliku wiadomosci")
        return -1
    message = message_plik.read()
    message_plik.close()
    return message

def write_to_file_private_key(x):
    try:
        private_key_plik = open("El_Gamal_private_key.txt", "w+")
    except IOError:
        print("Nie udalo sie otworzyc pliku klucza prywatnego odbiorcy")
        return -1
    private_key_plik.write((str(x)))
    private_key_plik.close()
    print("zapisano klucz prywatny odbiorcy w pliku El_Gamal_private_key.txt")

def write_to_file_en_msg(x):
    try:
        private_key_plik = open("El_Gamal_en_msg.txt", "w+")
    except IOError:
        print("Nie udalo sie otworzyc pliku z zaszyfrowana wiadomoscia")
        return -1
    private_key_plik.write((str(x)))
    private_key_plik.close()
    print("zapisano zaszyfrowana wiadomosc w pliku El_Gamal_en_msg.txt")


def gen_prime_bits(bits = 160):
    x = random.randrange(2 ** (bits - 1), 2 ** bits)
    if bits < 1:
        return False
    while not czy_pierwsza_miller_rabin(x, 64):
        x = random.randrange(2 ** (bits - 1), 2 ** bits)
    return x


def gen_prime_L_bit(L = 512 + 64):
    # Choose the modulus length N such that  N<L and N <=|H|
    p = 1
    if L > 1024 or L < 512 or L % 64 != 0:
        return False
   # q = gen_prime_bits(160)
    while not (czy_pierwsza_miller_rabin(p) and p.bit_length() == L):
        x = random.randrange(2 ** (L - 160 - 1), 2 ** (L - 160))
        # Choose an N-bit prime q
        # Choose an L-bit prime p such that p − 1 is a multiple of q.
       # p = x * q + 1
    return p


# Driver code
def main():
    msg = menu()
    print("Wybrana wiadomosc do zaszyfrowania :\n",msg)

    #q = random.randint(pow(10, 20), pow(10, 50))
    q = gen_prime_L_bit()
    key = find_primitive_root(q)
    g = random.randint(2, q)
    print( czy_pierwsza_miller_rabin(3))
   # key = gen_key(q)  # Private key for receiver
    write_to_file_private_key(key)
    h = power(g, key, q)
    print("uzywamy g = ", g)
    print("uzywamy g^a = ", h)

    en_msg, p = encrypt(msg, q, h, g)
    write_to_file_en_msg(en_msg)
    dr_msg = decrypt(en_msg, p, key, q)
    dmsg = ''.join(dr_msg)
    print("Odszyfrowana wiadomosc :\n", dmsg);


if __name__ == '__main__':
    main()
