from .caesar import Caesar
from .vigenere import Vigenere
from .playfair import PlayFair
from .rsa import RSA

ciphers = {
    "caesar": Caesar,
    "vigenere": Vigenere,
    "playfair": PlayFair,
    "rsa": RSA
}
