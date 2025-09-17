def power(base, exp, mod):
    res = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res

def modInverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def elgamal_encrypt(plaintext, p, g, y, k):
    c1 = power(g, k, p)
    
    yk_mod_p = power(y, k, p)
    
    ciphertext_pairs = []
    for char in plaintext:
        m = ord(char.upper()) - ord('A')
        
        c2 = (m * yk_mod_p) % p
        ciphertext_pairs.append(c2)
        
    return (c1, ciphertext_pairs)

def elgamal_decrypt(c1, c2_list, p, x):
    c1x_mod_p = power(c1, x, p)
    c1x_inverse = modInverse(c1x_mod_p, p)
    
    plaintext = []
    for c2 in c2_list:
        m = (c2 * c1x_inverse) % p
        
        plaintext.append(chr(m + ord('A')))
        
    return "".join(plaintext)

if __name__ == "__main__":
    p = 37
    g = 3
    x = 2  
    k = 15 
    plaintext = "EZKRIPTOGRAFI"

    # 1. Pembangkitan Kunci Publik
    y = power(g, x, p) # y = 3^2 mod 37 = 9
    print(f"Kunci Publik (p, g, y): ({p}, {g}, {y})")
    print(f"Kunci Privat (x): {x}")
    print("-" * 30)

    # 2. Enkripsi
    c1, c2_list = elgamal_encrypt(plaintext, p, g, y, k)
    print(f"Plaintext: {plaintext}")
    print("Hasil Enkripsi ElGamal:")
    print(f"C1 = {c1}")
    print(f"C2 = {c2_list}")
    print("-" * 30)

    # 3. Dekripsi
    decrypted_text = elgamal_decrypt(c1, c2_list, p, x)
    print(f"Ciphertext (C1, C2_list): ({c1}, {c2_list})")
    print(f"Hasil Dekripsi ElGamal: {decrypted_text}")