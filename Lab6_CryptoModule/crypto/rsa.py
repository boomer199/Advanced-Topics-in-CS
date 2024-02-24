import pickle
import json
import random
from math import gcd

class RSA:
    def __init__(self, keys=None):
        self._n = None
        self._e = None
        self._d = None
        
    def encrypt(self, message, keys = None):
        self._set_keys(keys)
        encrypted_msg = [pow(ord(str(char)), self._e, self._n) for char in message] #(character keycode^e)mod(n) for each character in the message
        print(encrypted_msg)
        return pickle.dumps(encrypted_msg)

    def decrypt(self, encrypted_message, keys = None):
        self._set_keys(keys)
        encrypted_msg = pickle.loads(encrypted_message)
        decrypted_msg = ''.join(chr(pow(char, self._d, self._n)) for char in encrypted_msg) #(character keycode^d)mod(n) for each character in the message
        return decrypted_msg

    def _generate_keys(self, keysize=1024):
        p = self._generate_prime(keysize)
        q = self._generate_prime(keysize)
        if p == q:  # case that p == q, regenerate q
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
                # to count how many times we halve  s)
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

keys = {"public": (65537, 497679112866164075884610870123939261420051439851932632211358307463530694682151277585439619691307080042382053465282605705800913120250276795666456725087596594714580400593080570872176422605982837375378129653207723722834794666135800914068527269021434942050062830740351895723352465810799669687956185490546288342555410869845296682644628741854301094533946320077832461075867313723812998050899306845288467091784864636085136777279500126613821381334080735545472302283591743727934735122056917860957524109619545105461745918186099625234470670120139867032388273537651902723835965137559058298999565221213537400085583056294715249349), "private":81656827450903494331251364670990720937025087091686094788726000277024361199279379402112275974497231055674416297849823140431774704091600567371124848022749381005628622725748743131185636698080984028830142181682754065514786258830252639409476688340746294945821835283137829542292278634413062058907073295693184591093490220027039786373011379089055486765684832365463569864601486765795475788575369194121357952052220405578745161357463006926939807443667414619715047142204697799877452871620430905893491499951951140598329884101049609883521460597892741850749725624522468347852426966613164263138508180255886110327479465736708030657}
r = RSA(keys)
print(r.decrypt(r.encrypt("does this work??", keys), keys))