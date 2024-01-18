import unittest

class findGCF(unittest.TestCase):
   def test_negative_num(self):
      result = func(4, -12)
      self.assertEqual(result, 4, "The GCF of 4, and -12 is 4, but the function printed: {}".format(result))
   
   def test_double_zeros(self):
      result = func(0, 0)
      self.assertEqual(result, None, "The GCF of 0 and 0 is None, but the function printed: {}".format(result))


def func( m, n ):
   if m == 0 and n == 0:
      return None
   
   m = abs(m)
   n= abs(n)
    
   while n != 0:
      r = m % n
      m = n
      n = r
   return m
 

