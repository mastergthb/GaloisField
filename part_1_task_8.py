
class GaloisFieldPoly:
    """"задаём поле с помошью неприводимого полинома"""
    def __init__(self, coef):
        self.coef = coef
        self.p = max(self.coef) + 1
        self.n = len(self.coef) - 1
        self.size = self.p ** self.n

    def add_polynomials(self, polynomial1, polynomial2):
        "реализовываем метод сложения в полиномиальной форме"
        result = []
        for coeff1, coeff2 in zip(self.extend_polynomial(polynomial1), self.extend_polynomial(polynomial2)):
            result.append((coeff1 + coeff2) % self.p) 
        return result

    def __add__(self, num1, num2):
        """"Создаём метод __add__ с которым удобнее работать с числами и который применим в поле, задаваемом как p**n"""
        polynomial1, polynomial2 = self.number_to_polynomial(num1), self.number_to_polynomial(num2)
        sum = self.add_polynomials(polynomial1,polynomial2)
        return self.polynomial_to_integer(sum)

    def subtract_polynomials(self, polynomial1, polynomial2):
        "реализовываем метод вычитания в полиномиальной форме"
        result = []
        for coeff1, coeff2 in zip(self.extend_polynomial(polynomial1), self.extend_polynomial(polynomial2)):
            result.append((coeff1 - coeff2) % self.p) 
        return result

    def __sub__(self, num1, num2):
        """"Создаём метод __sub__ с которым удобнее работать с числами и который применим в поле, задаваемом как p**n"""
        polynomial1, polynomial2 = self.number_to_polynomial(num1), self.number_to_polynomial(num2)
        sum = self.subtract_polynomials(polynomial1,polynomial2)
        return self.polynomial_to_integer(sum)


    def __mul__(self, num1, num2):
        """"Создаём метод __sub__ с которым удобнее работать с числами и который применим в поле, задаваемом как p**n"""
        poly1,poly2 = self.number_to_polynomial(num1),self.number_to_polynomial(num2)
        sub_mul = self.multiply_polynomials(poly1,poly2)
        mul_poly = self.gf_poly_mod(sub_mul)
        return self.polynomial_to_integer(mul_poly)
    
    def __truediv__(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на 0")
        b_inv = self.multiplicative_inverse(b)
        return self.__mul__(a,b_inv)
    
    def power(self, polynomial, k):
        """реализуем метод для возведения в степень полиномальном представлении, где polynomial - элемент, возводимый в степень,
        а к - степень"""
        polynomial = self.number_to_polynomial(polynomial)
        result = [1] 
        while k > 0:
            if k % 2 == 1:
                result = self.multiply_polynomials(result, polynomial)
            k //= 2
            polynomial = self.multiply_polynomials(polynomial, polynomial)
        return self.polynomial_to_integer(self.gf_poly_mod(result))
    
    def __power__(self,num1,num2):
        """"Создаём метод __power__ с которым удобнее работать с числами и который применим в поле, задаваемом как p**n, где num1 - число, num2- его степень"""
        power = self.power(num1,num2)
        return power
    
    def multiply_polynomials(self, polynomial1, polynomial2):
        "реализовываем метод умножения в полиномиальной форме, этот метод возвращает полином"
        result = [0] * (len(polynomial1) + len(polynomial2) - 1)
        for i in range(len(polynomial1)):
            for j in range(len(polynomial2)):
                result[i+j] += polynomial1[i] * polynomial2[j]
        for i in range(len(result)):
            result[i] %= self.p
        return result
    

    def gf_poly_mod(self, polynomial1):
        """"приводим полином, полученный в multiply_polynomials к полю GF(p**n) (остаток от деления
        двух полиномов в GF) """
        polynomial1 = polynomial1[::-1]
        self.coef = self.coef[::-1]
        while len(polynomial1) >= len(self.coef):
            coeff = polynomial1[-1] // self.coef[-1]  
            diff = len(polynomial1) - len(self.coef)

            for i in range(len(self.coef)):
                polynomial1[diff + i] -= coeff * self.coef[i]
                polynomial1[diff + i] %= self.p  
            while len(polynomial1) > 0 and polynomial1[-1] == 0:         #если возвращает неверный результат, смотри реверсы списка коэффициентов полинома
                polynomial1.pop()

        return polynomial1[::-1]
    
    
    def number_to_polynomial(self, number):
        """переводим число в полиномиальное представление"""
        polynomial = []
        while number > 0:
            polynomial.append(number % self.p)
            number //= self.p
        return polynomial[::-1]

    def polynomial_to_integer(self, polynomial):
        """"переводим полином в числовое представление  """
        reversed_poly = polynomial[::-1]
        integer = 0 
        for i in range(self.n):
            if len(reversed_poly) == i:
                break
            integer += reversed_poly[i] * self.p**i
        return integer

    def extend_polynomial(self, poly):
        """"приводим полиномы к одному размеру для проведения операций, вставляя в начало 0"""
        while len(poly) < self.n:
            poly.insert(0, 0)
        return poly 
    
    def extended_gcd(self, a, b):
        """расширенный алгоритм евклида"""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x
        
    def multiplicative_inverse(self, element):
        """поиск обратного элемента в поле через расширенный алгоритм евклида
        !!!не удалось получить правильное представление обратного числа в общем случае 
        для поля p**n, или поля, заданного полиномом(скорее всего нужно было реализовать расширенный алгоритм
        евклида для двух полиномов), поэтому __div__ возвращает математически
        неверное значение"""
        gcd, x, y = self.extended_gcd(element,self.size)
        if gcd != 1:
            raise ValueError("Обратный элемент не существует")
        return x % self.size
    
    

    