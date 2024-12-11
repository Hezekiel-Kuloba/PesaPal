class BigInt:
    def __init__(self, value: str):
        # Ensure valid input (only digits)
        if not value.isdigit() and not (value.startswith('-') and value[1:].isdigit()):
            raise ValueError("Invalid number format")
        self.value = value.lstrip('0') or '0'
        if self.value == '':
            self.value = '0'

    def __str__(self):
        return self.value

    def add(self, other):
        a, b = self.value.zfill(len(other.value)), other.value.zfill(len(self.value))
        carry = 0
        result = []
        for i in range(len(a) - 1, -1, -1):
            s = int(a[i]) + int(b[i]) + carry
            result.append(str(s % 10))
            carry = s // 10
        if carry:
            result.append(str(carry))
        return BigInt(''.join(result[::-1]))

    def subtract(self, other):
        a, b = self.value.zfill(len(other.value)), other.value.zfill(len(self.value))
        borrow = 0
        result = []
        for i in range(len(a) - 1, -1, -1):
            diff = int(a[i]) - int(b[i]) - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            result.append(str(diff))
        return BigInt(''.join(result[::-1]).lstrip('0') or '0')

    def multiply(self, other):
        a = self.value
        b = other.value
        result = [0] * (len(a) + len(b))
        for i in range(len(a) - 1, -1, -1):
            for j in range(len(b) - 1, -1, -1):
                mul = int(a[i]) * int(b[j]) + result[i + j + 1]
                result[i + j + 1] = mul % 10
                result[i + j] += mul // 10
        result = ''.join(map(str, result))
        return BigInt(result.lstrip('0') or '0')

    def divide(self, other):
        dividend = int(self.value)
        divisor = int(other.value)
        quotient = dividend // divisor
        return BigInt(str(quotient))

    def modulus(self, other):
        dividend = int(self.value)
        divisor = int(other.value)
        mod = dividend % divisor
        return BigInt(str(mod))

    def factorial(self):
        result = BigInt('1')
        for i in range(2, int(self.value) + 1):
            result = result.multiply(BigInt(str(i)))
        return result

    def exponentiate(self, other):
        result = BigInt('1')
        for _ in range(int(other.value)):
            result = result.multiply(self)
        return result

def repl():
    print("Welcome to the Arbitrary Precision Integer Calculator!")
    print("Type 'exit' to quit.")
    while True:
        expr = input(">> ").strip()
        if expr.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        try:
            tokens = expr.split()
            if len(tokens) == 3:
                num1 = BigInt(tokens[0])
                num2 = BigInt(tokens[2])
                op = tokens[1]
                if op == '+':
                    print(num1.add(num2))
                elif op == '-':
                    print(num1.subtract(num2))
                elif op == '*':
                    print(num1.multiply(num2))
                elif op == '/':
                    print(num1.divide(num2))
                elif op == '%':
                    print(num1.modulus(num2))
                elif op == '**':
                    print(num1.exponentiate(num2))
                else:
                    print("Unknown operator!")
            elif len(tokens) == 2 and tokens[0].lower() == 'factorial':
                num = BigInt(tokens[1])
                print(num.factorial())
            else:
                print("Invalid input format.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()

