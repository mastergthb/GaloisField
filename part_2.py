import argparse 
from part_1_task_7 import GaloisField
from part_1_task_8 import GaloisFieldPoly
import json
import yaml

class GaloisFieldOperational:

    def __init__(self, data):
        if 'p' in data and 'n' in data:
            self.galois_field = GaloisField(data.get("p"), data.get("n"))
        elif 'polynomial' in data:
            self.galois_field = GaloisFieldPoly(data.get("polynomial"))
        else:
            raise ValueError("Invalid data format")
    
        self.elem1 = data.get("elem1")
        self.elem2 = data.get("elem2")
        self.operation = data['operation']
    
    def process_operation(self):
        try:
            if self.operation == '+':
                return self.galois_field.__add__(self.elem1, self.elem2)
            elif self.operation == '-':
                return self.galois_field.__sub__(self.elem1, self.elem2)
            elif self.operation == '*':
                return self.galois_field.__mul__(self.elem1, self.elem2)
            elif self.operation == '/':
                return self.galois_field.__truediv__(self.elem1, self.elem2)
            elif self.operation == '^':
                return self.galois_field.__power__(self.elem1, self.elem2)
            else:
                return f"Unsupported operation: {self.operation}"
        except Exception as e:
            return f"Error occurred: {e}"
        
def process_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            data = json.load(file)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            data = yaml.safe_load(file)
        else:
            print(f"Unsupported file format: {file_path}")
            return
        for item in data:
            gf = GaloisFieldOperational(item)
            result = gf.process_operation()
            print(f"Result of operation {gf.operation} between {gf.elem1} and {gf.elem2}: {result}")


def main():
    parser = argparse.ArgumentParser(description='Process JSON or YAML files for Galois Field operations.')
    parser.add_argument('file_path', type=str, help='Path to the JSON or YAML file')
    args = parser.parse_args()
    
    process_file(args.file_path)

if __name__ == "__main__":
    main()