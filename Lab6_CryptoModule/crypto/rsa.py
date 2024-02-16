import pickle
import random
from math import gcd

class RSA:
    def __init__(self, keys=None):
        self._n = None
        self._e = None
        self._d = None
        
    def encrypt(self, message, keys = None):
        self._set_keys(keys)
        encrypted_msg = [pow(ord(char), self._e, self._n) for char in message] #(character keycode^e)mod(n) for each character in the message
        return pickle.dumps(encrypted_msg)

    def decrypt(self, encrypted_message, keys = None):
        self._set_keys(keys)
        encrypted_msg = pickle.loads(encrypted_message)
        decrypted_msg = ''.join(chr(pow(char, self._d, self._n)) for char in encrypted_msg) #(character keycode^d)mod(n) for each character in the message
        return decrypted_msg

    def _generate_keys(self, keysize=1024):
        p = self._generate_prime(keysize)
        q = self._generate_prime(keysize)
        if p == q:  # In the rare case that p == q, regenerate q
            while p == q:
                q = self._generate_prime(keysize)
        self._n = p * q
        phi = (p - 1) * (q - 1)
        self._e = self._choose_e(phi)
        self._d = self._extended_euclids_GCD(self._e, phi)

    def _generate_prime(self, keysize = 1024):
        def __rabinMiller(num):
            # inventwithpython.com (BSD License)

            # Returns True if num is a prime number.
            s = num - 1
            t = 1
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
                
        while True:
            num = random.getrandbits(keysize)
            if num % 2 == 0:
                num += 1  # Ensure num is odd
            if __rabinMiller(num):
                return num
        
        
    
    def _choose_e(self, phi):
        e = 65537
        while gcd(e, phi) != 1:
            e += 2
        return e


    def _extended_euclids_GCD(self, a, m):
        m0, x0, x1 = m, 0, 1
        if m == 1: return 0  # no inverse if m is 1
        
        while a > 1:
            # q is quotient
            q = a // m
            t = m

            # m is remainder now, same as euclid's gcd
            m = a % m
            a = t
            t = x0

            # update x0 and x1
            x0 = x1 - q * x0
            x1 = t

        # make d positive if negative 
        if x1 < 0:
            x1 += m0

        return x1

    # normal euclids GCD
    def _egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self._egcd(b % a, a)
            return (g, x - (b // a) * y, y)
        
    def _set_keys(self, keys):
        if keys is None:
            self._generate_keys()
        else:
            self._n = keys.get('public', (None, None))[1]
            self._e = keys.get('public', (None, None))[0]
            self._d = keys.get('private', None)

    def encode_keys(self):
        return {'public': (self._e, self._n), 'private': self._d}
    
