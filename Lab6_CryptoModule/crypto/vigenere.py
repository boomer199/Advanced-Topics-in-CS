import json

class Vigenere:
    def __init__(self, password):  
        self.__pass = password
        
    def is_printable(self, char):
        return 32 <= ord(char) <= 126

    def vigenere_transform(self, char, key_char, mode):
        char_code = ord(char)
        key_code = ord(key_char)
        operation = 1 if mode == "encrypt" else -1
        transformed_char_code = ((char_code - 32 + operation * (key_code - 32)) % 95) + 32
        return chr(transformed_char_code)

    def process(self, message, mode):
        encrypted_text = ""
        for i, char in enumerate(message):
            if not self.is_printable(char): 
                raise ValueError(f"INVALID CHARACTER: {ord(char)}")
            key_char = self.__pass[i % len(self.__pass)]
            shifted_char = self.vigenere_transform(char, key_char, mode)  
            encrypted_text += shifted_char
        return encrypted_text

    def encrypt(self, message):
        return bytearray(self.process(message, "encrypt"), 'utf-8')

    def decrypt(self, message):
        text = bytes(message).decode('utf-8')
        return self.process(text, "decrypt")
    
    def encode_keys(self):
        return json.dumps({"__pass": self.__pass})
