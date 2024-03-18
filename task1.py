from part_1_task_8 import GaloisFieldPoly
class GaloisField(GaloisFieldPoly):
    """создаем класс, описывающий поле галуа, включая его методы и соответствующие проверки"""
    def __init__(self, p, n):
        if not self.is_prime(p):
            raise ValueError("p должно быть простым числом")
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n должно быть положительным целым числом")
        self._p = p
        self._n = n
        self.size = p ** n
        self.field = [i for i in range(self.size)]
        
    """"методы для валидации элементов поля"""
    @staticmethod
    def is_prime(num):
        """проверяем, что n - простое число"""
        if num < 2:
            return False
        for i in range(2, int(num / 2) + 1):
            if num % i == 0:
                return False
        return True
    
    def validate_element(self, element):
        """проверяем, что елемент принадлежит полю p^n"""
        if not isinstance(element, int) or element < 0 or element >= self.size:
            raise ValueError(f"Элемент {element} не принадлежит полю GF({self._p}^{self._n})")
        
    """"арифметические операции приведены через преобразование чисел в полиномиальную форму, поэтому реализовать их как
      "магические" методы не получилось, тк эти методы должны получать 2 числа и преобразовывать их, чтобы на выходе давать
      математически верные значения"""            
    def __add__(self, elem1, elem2):
        """"реализовываем метод для сложения, используя сложение в полиномиальной форме"""
        self.validate_element(elem1)
        self.validate_element(elem2)
        return self.polynomial_to_integer(self.add_polynomials(self.number_to_polynomial(elem1),self.number_to_polynomial(elem2)))
    
    def __sub__(self, elem1, elem2):
        """"реализовываем метод для вычитания, используя сложение в полиномиальной форме"""
        self.validate_element(elem1)
        self.validate_element(elem2)
        return self.polynomial_to_integer(self.subtract_polynomials(self.number_to_polynomial(elem1),self.number_to_polynomial(elem2)))
    
    def __mul__(self, elem1, elem2):
        """"реализовываем метод для умножения, используя умножение в полиномиальной форме
        закомментированный блок кода - то, как должна работать функция через умножение в полиномах
        но тк класс Galoisfield задаётся p**n, а не неприводимым многочленом, то для реализации
        такой функции необходимо так же реализовать метод для нахождения неприводимого многочлена, что 
        реализовать не удалось, поэтому функция возвращает (a*b / mod p**q), хотя это не совсем
        верно математически"""
        self.validate_element(elem1)
        self.validate_element(elem2)
        # poly1,poly2 = self.number_to_polynomial(elem1),self.number_to_polynomial(elem2)
        # sub_mul = self.multiply_polynomials(poly1,poly2)
        # mul_poly = self.gf_poly_mod(sub_mul)
        # return self.polynomial_to_integer(mul_poly)
        return elem1 * elem2 % self.size
    
    def __truediv__(self, elem1, elem2):
        """"реализовываем метод для деления, используя умножение на обратный элемент в полиномиальной форме
        , тк умножение через многочлены не работает правильно в поле p**n, то и операция умножение на обратное
        реализовано в обход такого умножения, и div возвращает a * reversed(b) % p**n что не совсем верно математически
        """
        self.validate_element(elem1)
        self.validate_element(elem2)
        if elem2 == 0:
            raise ZeroDivisionError("Делениен на 0")
        ele2_inv = self.multiplicative_inverse(elem2)
        return (elem1 * ele2_inv) % self.size
    
    def __eq__(self, other):
        return self._p == other._p and self._n == other._n    
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        elements = ', '.join(str(element) for element in self.field)
        return f"Elements of Galois Field GF({self._p}^{self._n}): [{elements}]"
    
    """"доступ к значениям p и n"""
    @property
    def p(self):
        return self._p
    
    @p.setter
    def p(self, value):
        self._p = value
    
    @property
    def n(self):
        return self._n
    
    @n.setter
    def n(self, value):
        self._n = value

def __power__(self, elem1,power):
        """"реализовываем метод для возведения в степень, используя умножение в полиномиальной форме
        закомментированный блок кода - то, как должна работать функция через умножение в полиномах
        но тк умножение через полиномы не работает в поле p**n, просто вернем elem1 ** power % p**n
        математически верную реализацию смотри в полиномиальной презентации"""
        # self.validate_element(elem1)
        # power = self.power(elem1,power)
        #return power
        self.validate_element(elem1)
        if power < 0:
            raise ValueError("Степень должна быть положительной")
        return (elem1 ** power) % self.size

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