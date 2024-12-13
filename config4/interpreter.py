import struct
import json
#python3 interpreter.py --binary output.bin --result output.json --range 0:1020
class UVM:
    def __init__(self):
        self.memory = [0] * 1024  # Инициализация памяти
    
    def execute(self, binary_path, result_path, memory_range):
        with open(result_path, 'r') as file:
        	data = json.load(file)
        
        self.memory = list(data.values())
        
        with open(binary_path, 'rb') as binary_file:
            data = binary_file.read()

        i = 0
        while i + 3 <= len(data):  
            command = data[i]
            if command == 15:  
                _, b, c = struct.unpack('>B B H', data[i:i+4])
                self.memory[b] = c
                i += 4
            elif command == 59:  
                _, b, c = struct.unpack('>B B I', data[i:i+6])
                self.memory[b] = self.memory[c]
                i += 6
            elif command == 11:  
                _, b, c = struct.unpack('>B B I', data[i:i+6])
                self.memory[c] = self.memory[b]
                i += 6
            elif command == 63:  
                _, b, c = struct.unpack('>B B B', data[i:i+3])
                source_value = self.memory[c]
                self.memory[b] = -int(source_value)
                i += 3
            else:
                raise ValueError(f"Unknown command: {command}")
        
        # Сохранение диапазона памяти в файл
        result = {f"memory[{addr}]": value for addr, value in enumerate(self.memory[memory_range[0]:memory_range[1]])}
        with open(result_path, 'w') as result_file:
            json.dump(result, result_file, indent=4)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, help="Path to the binary file")
    parser.add_argument("--result", required=True, help="Path to the result file")
    parser.add_argument("--range", required=True, help="Memory range (start:end)")

    args = parser.parse_args()
    memory_range = list(map(int, args.range.split(":")))

    uvm = UVM()  # Создание объекта класса
    uvm.execute(args.binary, args.result, memory_range)
