import json

class Caesar:
    def __init__(self, password=1):  # very secure
        self.__pass = password

    @staticmethod
    def is_printable(char):
        return 32 <= ord(char) <= 126

    def encrypt(self, message): 
        result = ""
        for char in message:
            if not Caesar.is_printable(char):
                raise ValueError(f"INVALID CHARACTER: {ord(char)}")
            shifted_char = chr(((ord(char) - 32 + self.__pass) % 95) + 32)  
            result += shifted_char
        return bytearray(result, 'utf-8')

    def decrypt(self, message):  
        text = bytes(message).decode('utf-8')
        result = ""
        for char in text:  
            if not Caesar.is_printable(char):
                raise ValueError(f"INVALID CHARACTER: {ord(char)}")
            shifted_char = chr(((ord(char) - 32 - self.__pass) % 95) + 32)  
            result += shifted_char
        return result

    def encode_keys(self):
        return json.dumps({"password": self.__pass})
    