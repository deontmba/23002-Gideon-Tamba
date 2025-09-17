def generate_vigenere_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def vigenere_encrypt(plaintext, key):
    ciphertext = []
    extended_key = generate_vigenere_key(plaintext, key)
    for i in range(len(plaintext)):
        p_val = ord(plaintext[i].upper()) - ord('A')
        k_val = ord(extended_key[i].upper()) - ord('A')
        c_val = (p_val + k_val) % 26
        
        ciphertext.append(chr(c_val + ord('A')))
        
    return "".join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    plaintext = []
    extended_key = generate_vigenere_key(ciphertext, key)
    for i in range(len(ciphertext)):
        c_val = ord(ciphertext[i].upper()) - ord('A')
        k_val = ord(extended_key[i].upper()) - ord('A')
        p_val = (c_val - k_val + 26) % 26
        
        plaintext.append(chr(p_val + ord('A')))
        
    return "".join(plaintext)

if __name__ == "__main__":
    plaintext = "ASPRAKGANTENG"
    key = "DEON"
    
    encrypted_text = vigenere_encrypt(plaintext, key)
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Hasil Enkripsi Vigenere: {encrypted_text}")
    
    print("-" * 20)
    
    decrypted_text = vigenere_decrypt(encrypted_text, key)
    print(f"Ciphertext: {encrypted_text}")
    print(f"Key: {key}")
    print(f"Hasil Dekripsi Vigenere: {decrypted_text}")
