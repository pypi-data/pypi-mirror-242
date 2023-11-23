class Calculator:
    def __init__(self):
        self.memory = 0

    def add(self, num):
        """
        Adds a number to the memory.
        """
        self.memory += num
        return self.memory

    def subtract(self, num):
        """
        Subtracts a number from the memory.
        """
        self.memory -= num
        return self.memory

    def multiply(self, num):
        """
        Multiplies the memory by a number.
        """
        self.memory *= num
        return self.memory

    def divide(self, num):
        """
        Divides the memory by a number.
        """
        if num != 0:
            self.memory /= num
        else:
            raise ValueError("Cannot divide by zero")
        return self.memory

    def root(self, n):
        """
        Takes the nth root of the memory.
        """
        if n != 0:
            self.memory = self.memory ** (1/n)
        else:
            raise ValueError("Cannot take the root of zero")
        return self.memory

    def reset_memory(self):
        """
        Resets the memory to zero.
        """
        self.memory = 0
        return self.memory