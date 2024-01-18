import json
from textwrap import wrap

class PlayFair:
    """
    The PlayFair class implements the Playfair cipher, a technique of symmetric encryption 
    which uses a 5x5 matrix of letters constructed from a keyword.

    Attributes:
        __pass (str): The keyword used to generate the cipher's 5x5 matrix.
        square (dict): The dictionary representing the 5x5 matrix with characters as keys and their positions as values.
    """
    
    def __init__(self, password):
        """
        Constructs a PlayFair object with a given password.

        Args:
            password (str): The password used to generate the cipher matrix.
        """
        self.__pass = password
        self.square = {}

    def generate_square(self):
        """
        Generates the 5x5 matrix used for the Playfair cipher using the password.
        It omits 'J' and fills the matrix with the remaining unique letters of the alphabet.
        """
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
        """
        Finds the position of a character in the cipher matrix.

        Args:
            char (str): The character to find in the matrix.

        Returns:
            tuple: A tuple (row, col) representing the position of the character.
        """
        if char in self.square:
            return self.square[char]

    def preproccess(self, text):    
        """
        Preprocesses the text for encryption or decryption.
        Converts 'J' to 'I', removes non-alpha characters, adds 'X' between duplicate letters, 
        and ensures even length by padding with 'X' if necessary.

        Args:
            text (str): The text to preprocess.

        Returns:
            list: A list of 2-character strings after preprocessing.
        """
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
    
    
    def swap_pair(self, pair, mode):  # works for encrypt and dcrypt :)
        """
        Swaps a pair of characters based on their position in the cipher matrix.

        Args:
            pair (str): A string of two characters to swap.
            mode (str): 'encrypt' or 'decrypt' to determine the direction of the swap.

        Returns:
            str: The resulting 2-character string after swapping.
        """
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
        """
        Retrieves a character based on its position in the cipher matrix.

        Args:
            row (int): The row of the character.
            col (int): The column of the character.

        Returns:
            str: The character found at the given position in the matrix.
        """
        for char, pos in self.square.items():
            if pos == (row, col):
                return char

    def encrypt(self, text):
        """
        Encrypts a given text using the Playfair cipher.

        Args:
            text (str): The text to encrypt.

        Returns:
            bytearray: The encrypted text represented as a byte array.
        """
        self.generate_square()
        text = self.preproccess(text)
        encrypted_text = ''.join([self.swap_pair(pair, "encrypt") for pair in text])
        return bytearray(encrypted_text, 'utf-8')

    def decrypt(self, byte_array):
        """
        Decrypts a given byte array using the Playfair cipher.

        Args:
            byte_array (bytearray): The byte array to decrypt.

        Returns:
            str: The decrypted text.
        """
        self.generate_square()
        text = str(byte_array, 'utf-8')
        decrypted_text = ''.join([self.swap_pair(pair, "decrypt") for pair in wrap(text, 2)])
        return decrypted_text
    
    def encode_keys(self):
        """
        Encodes the password of the cipher into a JSON format.

        Returns:
            str: The JSON string containing the encoded password.
        """
        return json.dumps({"password": self.__pass})
