import pickle
import random
from math import gcd

class RSA:
    def __init__(self, keys=None):
        self._n = None
        self._e = None
        self._d = None
        if keys is None:
            self._generate_keys()
        else:
            self._n = keys.get('public', (None, None))[1]
            self._e = keys.get('public', (None, None))[0]
            self._d = keys.get('private', None)

    def encrypt(self, message):
        encrypted_msg = [pow(ord(char), self._e, self._n) for char in message]
        return pickle.dumps(encrypted_msg)

    def decrypt(self, encrypted_message):
        encrypted_msg = pickle.loads(encrypted_message)
        decrypted_msg = ''.join(chr(pow(char, self._d, self._n)) for char in encrypted_msg)
        return decrypted_msg

    def _generate_prime(self, keysize=1024):
        random_number = random.getrandbits(keysize)
        if(self.__rabinMiller(random_number)):
            return random_number
        else:
            return self._generate_prime()


    def __rabinMiller(num):
        # inventwithpython.com (BSD License)

        # Returns True if num is a prime number.

        s = num - 1
        t = 0
        while s % 2 == 0:
            # keep halving s while it is even (and use t
            # to count how many times we halve s)
            s = s // 2
            t += 1

        # Increase the trials to improve probability
        # Anything over 40 is mathematically not worth the computation
        for trials in range(5): # try to falsify num's primality 5 times
            a = random.randrange(2, num - 1)
            v = pow(a, s, num)
            if v != 1: # this test does not apply if v is 1.
                i = 0
                while v != (num - 1):
                    if i == t - 1:
                        return False
                    else:
                        i = i + 1
                        v = (v ** 2) % num
        return True

    def _choose_e(self, phi):
        pass

    #extended euclids :O
    def _egcd(self, a, b):
        #base case :)
        if a == b:
            return b,0,1
        
        gcd, x1, y1 = self._egcd(b%a,a)
        x = y1 - (b//a) * x1 
        y = x1 
     
        return gcd,x,y 
    
    
    def encode_keys(self):
        return {'public': (self.__e, self.__n), 'private': self.__d}