import json
from textwrap import wrap

class PlayFair:
    def __init__(self, password):
        self.__pass = password
        self.square = {}

    def generate_square(self):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        seen = set()

        row, col = 0, 0
        for char in self.__pass + alphabet:
            if char not in seen:
                seen.add(char)
                self.square[char] = (row, col)
                col += 1
                if col == 5:
                    col = 0
                    row += 1

    def find_position(self, char):
        if char in self.square:
            return self.square[char]
        raise ValueError(f"Character {char} not found in square")

    def preproccess(self, text):    
        # J and I are the same
        processed_text = text.upper().replace('J', 'I')
        processed_text = ''.join(filter(str.isalpha, processed_text)) # keep only letters
        i = 0 
        while i < len(processed_text)-1: #-1 because we need to check all chars including last
            if processed_text[i] == processed_text[i+1]:
                processed_text = processed_text[:i + 1] + 'X' + processed_text[i + 1:] # append X in the middle of all duplicates
            i += 2
    
        # append X if length is odd
        if len(processed_text) % 2 != 0:
            processed_text += "X"
        
        # array of 2 character strings
        arr = wrap(processed_text, 2)
        print(arr)
        return arr
    
    
    def swap_pair(self, pair, mode):
        multi = 1 
        if mode == "decrypt":
            multi = -1
            
        r1, c1 = self.find_position(pair[0])
        r2, c2 = self.find_position(pair[1])

        if r1 == r2:  # Same row
            return self.get_char(r1, (c1 + (1 * multi)) % 5) + self.get_char(r2, (c2 + (1 * multi)) % 5)
        elif c1 == c2:  # Same column
            return self.get_char((r1 + (1 * multi)) % 5, c1) + self.get_char((r2 + (1 * multi)) % 5, c2)
        else:  # Rectangle
            return self.get_char(r1, c2) + self.get_char(r2, c1)

    def get_char(self, row, col):
        for char, pos in self.square.items():
            if pos == (row, col):
                return char

    def encrypt(self, text):
        self.generate_square()
        text = self.preproccess(text)
        encrypted_text = ''.join([self.swap_pair(pair, "encrypt") for pair in text])
        return bytearray(encrypted_text, 'utf-8')

    def decrypt(self, byte_array):
        self.generate_square()
        text = str(byte_array, 'utf-8')
        decrypted_text = ''.join([self.swap_pair(pair, "decrypt") for pair in wrap(text, 2)])
        return decrypted_text
    
    def encode_keys(self):
        return json.dumps({"password": self.__pass})
