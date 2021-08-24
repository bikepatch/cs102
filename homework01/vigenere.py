def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i, symbol in enumerate(plaintext):
        cipher = symbol
        length = len(keyword)
        shift = ord(keyword[i % length]) % 32 - 1
        if ("A" <= symbol <= "Z") or ("a" <= symbol <= "z"):
            if 0 <= ord(symbol) - ord("A") <= 25:
                tmp = (ord(symbol) - ord("A") + shift) % 26
                cipher = chr(tmp + ord("A"))
            else:
                tmp = (ord(symbol) - ord("a") + shift) % 26
                cipher = chr(tmp + ord("a"))
        ciphertext += cipher
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i, cipher in enumerate(ciphertext):
        s = cipher
        length = len(keyword)
        shift = ord(keyword[i % length]) % 32 - 1
        if ("A" <= cipher <= "Z") or ("a" <= cipher <= "z"):
            if 0 <= ord(cipher) - ord("A") <= 25:
                tmp = (ord(cipher) - ord("A") - shift) % 26
                s = chr(tmp + ord("A"))
            else:
                tmp = (ord(cipher) - ord("a") - shift) % 26
                s = chr(tmp + ord("a"))
        plaintext += s
    return plaintext
