import unittest
from part_1_task_7 import GaloisField

class TestGaloisField(unittest.TestCase):
    def setUp(self):
        self.gf1 = GaloisField(2, 3)  
        self.gf2 = GaloisField(3, 2) 

    """"на простоые числа"""
    def test_is_prime(self):
        self.assertTrue(GaloisField.is_prime(2))  
        self.assertTrue(GaloisField.is_prime(11))  
        self.assertFalse(GaloisField.is_prime(34))  
        self.assertFalse(GaloisField.is_prime(10))  
    
    """"елементы не принадлежат заданнолму полю"""
    def test_validate_element(self):
        self.assertRaises(ValueError, self.gf1.validate_element, 333) 
        self.assertRaises(ValueError, self.gf2.validate_element, 144)  
        self.assertRaises(ValueError, self.gf1.validate_element, 18)  
        self.assertRaises(ValueError, self.gf2.validate_element, -13)  

    def test_addition(self):
        self.assertEqual(self.gf1.__add__(5, 1), 4)  
        self.assertEqual(self.gf2.__add__(2, 2), 1)  
        
    def test_subtraction(self):
        self.assertEqual(self.gf1.__sub__(4, 3), 7)  
        self.assertEqual(self.gf2.__sub__(2, 1), 1)  
        
    def test_multiplication(self):
        self.assertEqual(self.gf1.__mul__(4, 3), 4)  
        self.assertEqual(self.gf2.__mul__(2, 2), 1)  
        
    def test_division(self):
        self.assertEqual(self.gf1.__truediv__(2, 2), 1)  
        self.assertEqual(self.gf2.__truediv__(2, 1), 2)  
        
    def test_exponentiation(self):
        self.assertEqual(self.gf1.__power__(2, 2), 4)  
        self.assertEqual(self.gf2.__power__(5, 2), 8)  
    
    def test_extended_gcd(self):
        gcd, x, y = self.gf1.extended_gcd(10, 6) 
        self.assertEqual(gcd, 2)
        self.assertEqual(x, -1)
        self.assertEqual(y, 1)
        
        gcd, x, y = self.gf2.extended_gcd(5, 3) 
        self.assertEqual(gcd, 1)
        self.assertEqual(x, 2)
        self.assertEqual(y, -3)
        
    def test_multiplicative_inverse(self):
        # Обратный элемент к 3 в GF(2^3) равен 5, так как 3*5 = 1 mod 2^3
        self.assertEqual(self.gf1.multiplicative_inverse(3), 5)
        
        # Обратный элемент к 2 в GF(3^2) равен 2, так как 2*2 = 1 mod 3^2
        self.assertEqual(self.gf2.multiplicative_inverse(2), 2)
        
        # Обратный элемент к 0 не существует
        self.assertRaises(ValueError, self.gf1.multiplicative_inverse, 0)    


if __name__ == '__main__':
    unittest.main()