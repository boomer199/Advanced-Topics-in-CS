from .caesar import Caesar
from .vigenere import Vigenere
from .playfair import PlayFair
from .rsa import RSA

import random

ciphers = {
    "caesar": Caesar,
    "vigenere": Vigenere,
    "playfair": PlayFair,
    "rsa": RSA
}


def gen_password(len=50):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choice(letters) for i in range(len))

password = gen_password()


def encrypt(cipher_type, plaintext, password=password):
    if cipher_type == "caesar":
        password = sum(ord(char) for char in password) 
        cipher_instance = ciphers[cipher_type](password)
    else:
        cipher_instance = ciphers[cipher_type](password)
    return cipher_instance.encrypt(plaintext)

def decrypt(cipher_type, encrypted_bytearray, password=password):
    if cipher_type == "caesar":
        password = sum(ord(char) for char in password) 
        cipher_instance = ciphers[cipher_type](password)
    else:
        cipher_instance = ciphers[cipher_type](password)  
    return cipher_instance.decrypt(encrypted_bytearray)
