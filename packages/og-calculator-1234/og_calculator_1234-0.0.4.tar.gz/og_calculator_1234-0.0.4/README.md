# What does this calculator do
A calculator that can perform addition, subtraction, multiplication, division, and nth root. It stores the result of each calculation in memory. Calculator memory starts at 0 and resets to 0.
User first selects the operator (+, -, *, /, nth root, get memory, store to memory, reset memory), then inputs a new number. The calculation is made between the number stored in memory and the new number input by the user.
If the user selects get memory or reset memory then they do not need to input a new number.
If the user tries to divide by 0 or calculate nth root of a negative number then the calculator will return an error message.

## Installation
pip install og-calculator-1234

### Functions
The calculator module contains a class with methods to perform calculations, a print statement showing a menu of options to the user, and if loops to handle user input and pass values to the calculator methods.

**Menu of options**
```
    calc = Calculator()
    print("Welcome to the Calculator!")
    while True:
        print("Current Memory:", calc.get_memory())
        print("Select operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. nth root")
        print("6. Get Memory")
        print("7. Store to Memory")
        print("8. Reset Memory")
        print("9. Exit")
```

**1. Add**
Adds the input number to the number stored in memory.
```
def add(self, x):
    self.memory += x
    return self.memory
```
```
    if choice == '1':
            num = float(input("Enter number to add: "))
            print("Result:", calc.add(num))
```

**2. Subtract**
Subtracts the input number from the number stored in memory.
```
def subtract(self, x):
    self.memory -= x
    return self.memory
```
```
elif choice == '2':
    num = float(input("Enter number to subtract: "))
    print("Result:", calc.subtract(num))
```

**3. Multiply**
Multiplies the number stored in memory by the input number.
```
def multiply(self, x):
    self.memory *= x
    return self.memory
```
```
elif choice == '3':
    num = float(input("Enter number to multiply: "))
    print("Result:", calc.multiply(num))
```

**4. Divide**
Divides the number stored in memory by the input number.
```
def divide(self, x):
    if x != 0:
        self.memory /= x
        return self.memory
    else:
        return "Error! Division by zero."
```
```
elif choice == '4':
    num = float(input("Enter number to divide: "))
    print("Result:", calc.divide(num))
```

**5. nth root**
Takes the input number as the nth root of the number stored in memory.
```
def nth_root(self, x):
    if self.memory >= 0 and x >= 0:
        return self.memory ** (1 / x)
    else:
        raise ValueError("Cannot calculate nth root of a negative number.")
```
```
elif choice == '5':
    num = float(input("Enter number for nth root: "))
    print("Result:", calc.nth_root(num))
```

**6. Get memory**
Shows the number currently stored in memory.
```
    def get_memory(self):
        return self.memory
```
```
        elif choice == '6':
            print("Memory currently stores:", calc.memory)
```

**7. Store to memory**
Stores the input number in memory. This overwrites the number previously stored in memory.
```
        elif choice == '7':
            num = float(input("Enter number to store in memory: "))
            calc.memory = num
            print("Memory set to:", calc.memory)
```

**8. Reset memory**
Resets memory to 0.
```
    def reset_memory(self):
        self.memory = 0
        return "Memory reset to 0."
```

**9. Exit**
Exits the if loop of the calculator module