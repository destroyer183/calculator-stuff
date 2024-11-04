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
    Absolute = 'a'
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

    def __init__(self, token_type: TokenType, precedence: int, associativity: Associativity, math_operation: MathOperation, value: str) -> None:
        
        self.token_type  = token_type
        self.precedence = precedence
        self.associativity = associativity
        self.math_operation = math_operation
        self.value = value

    def math(self, is_radians, x, y):

        match self.math_operation:

            case MathOperation.Sine:       return (math.sin(x)  * is_radians) + (math.sin(math.radians(x))  * (not is_radians))
            case MathOperation.Cosine:     return (math.cos(x)  * is_radians) + (math.cos(math.radians(x))  * (not is_radians))
            case MathOperation.Tangent:    return (math.tan(x)  * is_radians) + (math.tan(math.radians(x))  * (not is_radians))
            case MathOperation.aSine:      return (math.asin(x) * is_radians) + (math.asin(math.radians(x)) * (not is_radians))
            case MathOperation.aCosine:    return (math.acos(x) * is_radians) + (math.acos(math.radians(x)) * (not is_radians))
            case MathOperation.aTangent:   return (math.atan(x) * is_radians) + (math.atan(math.radians(x)) * (not is_radians))
            case MathOperation.Logarithm:  return math.log(x)
            case MathOperation.Absolute:   return abs(x)
            case MathOperation.Factorial:  return math.factorial(int(x))
            case MathOperation.SquareRoot: return x ** 0.5

            case MathOperation.Exponential:    return x ** y
            case MathOperation.Modulo:         return x % y
            case MathOperation.Division:       return x / y
            case MathOperation.Multiplication: return x * y
            case MathOperation.Addition:       return x + y
            case MathOperation.Subtraction:    return x - y



TOKENS = [

    Token(token_type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Sine,       value = 's'),
    Token(token_type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Cosine,     value = 'c'),
    Token(token_type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Tangent,    value = 't'),
    Token(token_type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.aSine,      value = 'S'),
    Token(token_type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.aCosine,    value = 'C'),
    Token(token_type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.aTangent,   value = 'T'),
    Token(token_type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Logarithm,  value = 'l'),
    Token(token_type = TokenType.FUNCTION, precedence = 5, associativity = Associativity.LEFT,  math_operation = MathOperation.Absolute,   value = 'a'),
    Token(token_type = TokenType.FUNCTION, precedence = 4, associativity = Associativity.LEFT,  math_operation = MathOperation.Factorial,  value = 'f'),
    Token(token_type = TokenType.FUNCTION, precedence = 2, associativity = Associativity.LEFT,  math_operation = MathOperation.SquareRoot, value = '#'),
    
    Token(token_type = TokenType.OPERATOR, precedence = 3, associativity = Associativity.RIGHT, math_operation = MathOperation.Exponential,    value = '^'),
    Token(token_type = TokenType.OPERATOR, precedence = 1, associativity = Associativity.LEFT,  math_operation = MathOperation.Modulo,         value = '%'),
    Token(token_type = TokenType.OPERATOR, precedence = 1, associativity = Associativity.LEFT,  math_operation = MathOperation.Division,       value = '/'),
    Token(token_type = TokenType.OPERATOR, precedence = 1, associativity = Associativity.LEFT,  math_operation = MathOperation.Multiplication, value = '*'),
    Token(token_type = TokenType.OPERATOR, precedence = 0, associativity = Associativity.LEFT,  math_operation = MathOperation.Addition,       value = '+'),
    Token(token_type = TokenType.OPERATOR, precedence = 0, associativity = Associativity.LEFT,  math_operation = MathOperation.Subtraction,    value = '_'),

    Token(token_type = TokenType.LEFT_BRACKET,  precedence = 0, associativity = Associativity.RIGHT, math_operation = MathOperation.Null, value = '('),
    Token(token_type = TokenType.RIGHT_BRACKET, precedence = 0, associativity = Associativity.LEFT,  math_operation = MathOperation.Null, value = ')')

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

            if token.token_type == TokenType.FUNCTION:

                op_stack.append(token)



            elif token.token_type == TokenType.OPERATOR:

                while op_stack and op_stack[-1].value != '(' and (
                        op_stack[-1].precedence > token.precedence or (
                        op_stack[-1].precedence == token.precedence and 
                        token.associativity == Associativity.LEFT)):

                    out_stack.append(op_stack.pop())

                op_stack.append(token)



            elif token.token_type == TokenType.LEFT_BRACKET:

                op_stack.append(token)



            elif token.token_type == TokenType.RIGHT_BRACKET:

                while op_stack and op_stack[-1].token_type != TokenType.LEFT_BRACKET:

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

            a, b, hist = find_numbers(i.token_type, hist)

            hist.append(str(i.math(is_radians, float(a), float(b))))

    x = ('').join(hist)

    hist = x.strip()

    return hist



def find_numbers(token_type, hist):

    if token_type == TokenType.FUNCTION: return hist.pop(-1), 0, hist

    else: return hist.pop(-2), hist.pop(-1), hist
    


if __name__ == '__main__':

    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    equation = '35.43 _ 36.33'

    is_radians = False

    output = shunting_yard_evaluator(equation, is_radians)

    output = ('').join(output)

    try: 
        output = float(output)
        print(f"output: {output:f}") 
    except: print(f"output: {output}")