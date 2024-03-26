import math
from enum import Enum



''' NOTES

maybe instead of using lambda for the 'apply' attribute, use a function like the c++ version of this.

'''



class MathOperation(Enum):
    Sine = 's'
    Cosine = 'c'
    Tangent = 't'
    aSine = 'S'
    aCosine = 'C'
    aTangent = 'T'
    Logarithm = 'l'
    Factorial = 'f'
    SquareRoot = '#'
    Exponential = '^'
    Modulo = '%'
    Division = '/'
    Multiplication = '*'
    Addition = '+'
    Subtraction = '_'
    Null = None

class Associativity(Enum):
    LEFT = False
    RIGHT = True

class TokenType(Enum):
    NUMBER = 0
    OPERATOR = 1
    FUNCTION = 3
    LEFT_BRACKET = 5
    RIGHT_BRACKET = 6



class Token:

    def __init__(self, type: TokenType, precedence: int, associativity: Associativity, math_operation: MathOperation, value: str) -> None:
        
        self.type  = type
        self.precedence = precedence
        self.associativity = associativity
        self.math_operation = math_operation
        self.value = value

    def math(self, is_radians, x, y):

        match self.math_operation:

            case MathOperation.Sine:       return (math.sin(x) * is_radians) + (math.sin(math.radians(x)) * (not is_radians))
            case MathOperation.Cosine:     return (math.sin(x) * is_radians) + (math.sin(math.radians(x)) * (not is_radians))
            case MathOperation.Tangent:    return (math.sin(x) * is_radians) + (math.sin(math.radians(x)) * (not is_radians))
            case MathOperation.aSine:      return (math.sin(x) * is_radians) + (math.sin(math.radians(x)) * (not is_radians))
            case MathOperation.aCosine:    return (math.sin(x) * is_radians) + (math.sin(math.radians(x)) * (not is_radians))
            case MathOperation.aTangent:   return (math.sin(x) * is_radians) + (math.sin(math.radians(x)) * (not is_radians))
            case MathOperation.Logarithm:  return math.log(x)
            case MathOperation.Factorial:  return math.factorial(int(x))
            case MathOperation.SquareRoot: return x ** 0.5

            case MathOperation.Exponential:    return x ** y
            case MathOperation.Modulo:         return x % y
            case MathOperation.Division:       return x / y
            case MathOperation.Multiplication: return x * y
            case MathOperation.Addition:       return x + y
            case MathOperation.Subtraction:    return x - y



TOKENS = [

    Token(type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Sine,       value = 's'),
    Token(type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Cosine,     value = 'c'),
    Token(type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Tangent,    value = 't'),
    Token(type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.aSine,      value = 'S'),
    Token(type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.aCosine,    value = 'C'),
    Token(type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.aTangent,   value = 'T'),
    Token(type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Logarithm,  value = 'l'),
    Token(type = TokenType.FUNCTION, precedence = 4, associativity = Associativity.LEFT,  math_operation = MathOperation.Factorial,  value = 'f'),
    Token(type = TokenType.FUNCTION, precedence = 2, associativity = Associativity.LEFT,  math_operation = MathOperation.SquareRoot, value = '#'),
    
    Token(type = TokenType.OPERATOR, precedence = 3, associativity = Associativity.RIGHT, math_operation = MathOperation.Exponential,    value = '^'),
    Token(type = TokenType.OPERATOR, precedence = 1, associativity = Associativity.LEFT,  math_operation = MathOperation.Modulo,         value = '%'),
    Token(type = TokenType.OPERATOR, precedence = 1, associativity = Associativity.LEFT,  math_operation = MathOperation.Division,       value = '/'),
    Token(type = TokenType.OPERATOR, precedence = 1, associativity = Associativity.LEFT,  math_operation = MathOperation.Multiplication, value = '*'),
    Token(type = TokenType.OPERATOR, precedence = 0, associativity = Associativity.LEFT,  math_operation = MathOperation.Addition,       value = '+'),
    Token(type = TokenType.OPERATOR, precedence = 0, associativity = Associativity.LEFT,  math_operation = MathOperation.Subtraction,    value = '-'),

    Token(type = TokenType.LEFT_BRACKET,  precedence = 0, associativity = Associativity.RIGHT, math_operation = MathOperation.Null, value = '('),
    Token(type = TokenType.RIGHT_BRACKET, precedence = 0, associativity = Associativity.LEFT,  math_operation = MathOperation.Null, value = ')')

    ]



def get_token(value: str):

    for i in TOKENS:

        if i.value == value:

            return i 
        
    return value
        


def shunting_yard_converter(equation):

    in_stack = list(equation)
    op_stack = []
    out_stack = []

    for index, char, in enumerate(in_stack):

        if char == '!':

            in_stack[index] = ')'

            for i in range(index, 0, -1):

                if in_stack[i] not in '1234567890.-':

                    in_stack.insert(i - 1, 'f(')

                    break


    x = ('').join(in_stack)
    in_stack = list(x)


    while in_stack:

        temp_stack = []

        try: 

            if type(token) != str and token.value != ')': token = get_token(in_stack.pop(0))
                
            else: token = get_token(in_stack.pop(0))
        
        except: token = get_token(in_stack.pop(0))

        if token == ' ':

            continue

        elif type(token) == str:

            if token in '1234567890.-':

                try:

                    while token in '1234567890.-':

                        temp_stack.append(token)

                        token = get_token(in_stack.pop(0))

                except:pass

                out_stack.append(('').join(temp_stack))

                

        try:

            if token.type == TokenType.FUNCTION:

                op_stack.append(token)



            elif token.type == TokenType.OPERATOR:

                while op_stack and op_stack[-1].value != '(' and (
                        op_stack[-1].precedence > token.precedence or (
                        op_stack[-1].precedence == token.precedence and 
                        token.associativity == Associativity.LEFT)):

                    out_stack.append(op_stack.pop())

                op_stack.append(token)



            elif token.type == TokenType.LEFT_BRACKET:

                op_stack.append(token)



            elif token.type == TokenType.RIGHT_BRACKET:

                while op_stack and op_stack[-1].type != TokenType.LEFT_BRACKET:

                    out_stack.append(op_stack.pop())

                op_stack.pop()

        except:pass


        
    while op_stack:

        out_stack.append(op_stack.pop())

    for index in out_stack:
        print(index)

    return out_stack



def shunting_yard_evaluator(equation, is_radians):

    stack = shunting_yard_converter(equation)

    hist = []

    while stack:

        i = stack.pop(0)

        if type(i) == str:

            hist.append(i)

        else:

            a, b, hist = find_numbers(i.type, hist)

            hist.append(str(i.math(is_radians, float(a), float(b))))

    x = ('').join(hist)

    hist = x.strip()

    return hist



def find_numbers(type, hist):

    if type == TokenType.FUNCTION: return hist.pop(-1), 0, hist

    else: return hist.pop(-2), hist.pop(-1), hist
    


if __name__ == '__main__':

    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    equation = '(3 + 2) * 6'

    is_radians = False

    output = shunting_yard_evaluator(equation, is_radians)

    print(f"output: {('').join(output)}") 