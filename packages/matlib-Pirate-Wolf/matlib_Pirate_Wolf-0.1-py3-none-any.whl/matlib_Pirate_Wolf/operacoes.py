def som(x, y):
    """Add Function"""
    return x + y

def sub(x, y):
    """Subtract Function"""
    return x - y

def vez(x, y):
    """Multiply Function"""
    return x * y

def div(x, y):
    """Divide Function"""
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y