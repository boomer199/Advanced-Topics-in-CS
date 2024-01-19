
import json
from textwrap import wrap

class PlayFair:
    def __init__(self, password):
        self.__pass = password.upper().replace('J', 'I')  # Convert password to uppercase and replace J with I
        self.square = self.generate_square()

    def generate_square(self):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        seen = set()
        square = {}

        # Generate the square
        for char in self.__pass + alphabet:
            if char not in seen and char != 'J':  # Skip 'J'
                seen.add(char)
                square[char] = divmod(len(seen) - 1, 5)  # Calculate row and column

        return square

    def find_position(self, char):
        if char in self.square:
            return self.square[char]
        else:
            raise ValueError(f"Character {char} not found in square")

    def preproccess(self, text):    
        processed_text = text.upper().replace('J', 'I')
        processed_text = ''.join(filter(str.isalpha, processed_text))  # Keep only letters

        # Insert 'X' between duplicate letters and at the end if needed
        i = 0 
        while i < len(processed_text) - 1:
            if processed_text[i] == processed_text[i + 1]:
                processed_text = processed_text[:i + 1] + 'X' + processed_text[i + 1:]
                i += 1
            i += 1

        if len(processed_text) % 2 != 0:
            processed_text += "X"

        return [processed_text[i:i + 2] for i in range(0, len(processed_text), 2)]

    def swap_pair(self, pair, mode):
        r1, c1 = self.find_position(pair[0])
        r2, c2 = self.find_position(pair[1])

        if r1 == r2:  # Same row
            return self.get_char(r1, (c1 + 1) % 5 if mode == "encrypt" else (c1 - 1) % 5) + \
                   self.get_char(r2, (c2 + 1) % 5 if mode == "encrypt" else (c2 - 1) % 5)
        elif c1 == c2:  # Same column
            return self.get_char((r1 + 1) % 5 if mode == "encrypt" else (r1 - 1) % 5, c1) + \
                   self.get_char((r2 + 1) % 5 if mode == "encrypt" else (r2 - 1) % 5, c2)
        else:  # Rectangle
            return self.get_char(r1, c2) + self.get_char(r2, c1)

    def get_char(self, row, col):
        for char, (r, c) in self.square.items():
            if r == row and c == col:
                return char

    def encrypt(self, text):
        text = self.preproccess(text)
        encrypted_text = ''.join(self.swap_pair(pair, "encrypt") for pair in text)
        return bytearray(encrypted_text, 'utf-8')

    def decrypt(self, byte_array):
        text = bytes(byte_array).decode('utf-8')
        return ''.join(self.swap_pair(pair, "decrypt") for pair in wrap(text, 2))

    def encode_keys(self):
        return json.dumps({"password": self.__pass})

