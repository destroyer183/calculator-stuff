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

    def __init__(self, type: int, precedence: int, associativity: bool, value) -> None:
        
        self.type  = type
        self.precedence = precedence
        self.associativity = associativity
        self.value = value

    def math(self, is_radians, x, y):

        match self.value:

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

    Token(TokenType.FUNCTION, 5, Associativity.LEFT,  MathOperation.Sine),
    Token(TokenType.FUNCTION, 5, Associativity.LEFT,  MathOperation.Cosine),
    Token(TokenType.FUNCTION, 5, Associativity.LEFT,  MathOperation.Tangent),
    Token(TokenType.FUNCTION, 5, Associativity.LEFT,  MathOperation.aSine),
    Token(TokenType.FUNCTION, 5, Associativity.LEFT,  MathOperation.aCosine),
    Token(TokenType.FUNCTION, 5, Associativity.LEFT,  MathOperation.aTangent),
    Token(TokenType.FUNCTION, 5, Associativity.LEFT,  MathOperation.Logarithm),
    Token(TokenType.FUNCTION, 4, Associativity.LEFT,  MathOperation.Factorial),
    Token(TokenType.FUNCTION, 2, Associativity.LEFT,  MathOperation.SquareRoot),
    
    Token(TokenType.OPERATOR, 3, Associativity.RIGHT, MathOperation.Exponential),
    Token(TokenType.OPERATOR, 1, Associativity.LEFT,  MathOperation.Modulo),
    Token(TokenType.OPERATOR, 1, Associativity.LEFT,  MathOperation.Division),
    Token(TokenType.OPERATOR, 1, Associativity.LEFT,  MathOperation.Multiplication),
    Token(TokenType.OPERATOR, 0, Associativity.LEFT,  MathOperation.Addition),
    Token(TokenType.OPERATOR, 0, Associativity.LEFT,  MathOperation.Subtraction),

    Token(TokenType.LEFT_BRACKET, 0, Associativity.RIGHT, '('),
    Token(TokenType.RIGHT_BRACKET, 0, Associativity.LEFT, ')')

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
                        token.associativity == Associativity.RIGHT)):

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

    if type: return hist.pop(-1), None, hist

    else: return hist.pop(-2), hist.pop(-1), hist
    


if __name__ == '__main__':

    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    # equation = 's(s(60))'

    is_radians = False

    output = shunting_yard_evaluator(equation, is_radians)

    print(f"output: {('').join(output)}") 