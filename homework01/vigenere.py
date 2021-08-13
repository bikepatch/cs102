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
        if "A" <= symbol <= "z":
            length = len(keyword)
            shift = ord(keyword[i % length])
            if "a" <= symbol <= "z":
                shift -= ord("a")
            else:
                shift -= ord("A")
            enc = ord(symbol) + shift
            if ("a" <= symbol <= "z" and enc > ord("z")) or (
                "A" <= symbol <= "Z" and enc > ord("Z")
            ):
                enc -= 26
            cipher = chr(enc)
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
        if "A" <= cipher <= "z":
            shift = ord(keyword[i % len(keyword)])
            if "a" <= cipher <= "z":
                shift -= ord("a")
            else:
                shift -= ord("A")
            enc = ord(cipher) - shift
            if ("a" <= cipher <= "z" and enc < ord("a")) or (
                "A" <= cipher <= "Z" and enc < ord("A")
            ):
                enc += 26
            s = chr(enc)
        plaintext += s
    return plaintext
