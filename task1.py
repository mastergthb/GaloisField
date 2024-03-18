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