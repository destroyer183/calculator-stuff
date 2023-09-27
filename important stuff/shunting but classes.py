import math


LEFT = False 
RIGHT = True

NUMBER = 0
OPERATOR = 0
BRACKET = 3
FUNCTION = 1
COMMA = 5
LEFT_BRACKET = 2
RIGHT_BRACKET = 3






class Token:

    def __init__(self, type: int, precedence: int, associativity: bool, value, apply=None) -> None:
        
        self.type  = type
        self.precedence = precedence
        self.associativity = associativity
        self.value = value
        self.apply = apply



TOKENS = [

    Token(FUNCTION, 5, LEFT,  value='s', apply=lambda x: math.sin(math.radians(x))),
    Token(FUNCTION, 5, LEFT,  value='c', apply=lambda x: math.cos(math.radians(x))),
    Token(FUNCTION, 5, LEFT,  value='t', apply=lambda x: math.tan(math.radians(x))),
    Token(FUNCTION, 5, LEFT,  value='S', apply=lambda x: math.degrees(math.asin(x))),
    Token(FUNCTION, 5, LEFT,  value='C', apply=lambda x: math.degrees(math.acos(x))),
    Token(FUNCTION, 5, LEFT,  value='T', apply=lambda x: math.degrees(math.atan(x))),
    Token(FUNCTION, 5, LEFT,  value='l', apply=lambda x: math.log((x))),
    Token(FUNCTION, 4, LEFT,  value='f', apply=lambda x: math.factorial((x))),
    Token(FUNCTION, 2, LEFT,  value='#', apply=lambda x: x ** 0.5),
    
    Token(OPERATOR, 3, RIGHT, value='^', apply=lambda a,b: a ** b),
    Token(OPERATOR, 1, LEFT,  value='%', apply=lambda a,b: a % b),
    Token(OPERATOR, 1, LEFT,  value='/', apply=lambda a,b: a / b),
    Token(OPERATOR, 1, LEFT,  value='*', apply=lambda a,b: a * b),
    Token(OPERATOR, 0, LEFT,  value='+', apply=lambda a,b: a + b),
    Token(OPERATOR, 0, LEFT,  value='_', apply=lambda a,b: a - b),

    Token(LEFT_BRACKET, 0, RIGHT, value='('),
    Token(RIGHT_BRACKET, 0, LEFT, value=')')

    ]


