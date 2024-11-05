import math
from enum import Enum



''' NOTES

(-2)^4 = 16, but -2^4 = 16, and this is wrong because exponents come before negatives, this may require a lot of work to fix sadly. IT ALWAYS TREATS IT AS IF IT IS THE FIRST EXAMPLE

FACTORIAL FORMAT CONVERTER HAS ALWAYS BEEN BROKEN. SOMETHING LIKE (2 + 3)! DOES NOT WORK PROPERLY AND SOMEHOW EVALUATES TO 8. MAKE SURE THIS WORKS FOR THINGS LIKE (((1 + 2) + 3) + 4)!

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



# create class for every math operation token
class Token:

    # initialization function that takes in arguments for the token type, token precedence, token associativity, math operation, and value.
    def __init__(self, token_type: TokenType, precedence: int, associativity: Associativity, math_operation: MathOperation, value: str) -> None:
        
        # assign function arguments to object attributes
        self.token_type  = token_type
        self.precedence = precedence
        self.associativity = associativity
        self.math_operation = math_operation
        self.value = value



    # function to perform various math functions depending on the inputs
    def math(self, is_radians, x, y):

        # match case to determine which math operation to use
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



# create tokens for every math operation available on calculator
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



# function to return a token based on a string argument
def get_token(value: str):

    # loop over every math operation token
    for i in TOKENS:

        # check if token value is equal to the string argument inputted
        if i.value == value:

            # return token if match is found
            return i 
        
    # return string argument if no match is found
    return value
        


# function to convert standard equations into reverse polish notation using the shunting yard algorithm
def shunting_yard_converter(equation):

    # create variables for input stack, operator stack, and output stack
    in_stack = list(equation)
    op_stack = []
    out_stack = []

    # loop over input stack by index and element, this is to find any factorials and change the format of them.
    for index, char, in enumerate(in_stack):

        if char == '!':

            in_stack[index] = ')'

            if in_stack[index - 1] == ')':

                bracket_count = 0
                
                for i in range(index - 1, -1, -1):

                    if in_stack[i] == ')':

                        bracket_count += 1



                    elif in_stack[i] == '(':

                        bracket_count -= 1

                        if bracket_count == 0:

                            in_stack.insert(max(0, i - 1), 'f(')

                            break



            else:

                for i in range(index - 1, -1, -1):

                    if i == 0:

                        in_stack.insert(0, 'f(')

                        break



                    elif in_stack[i] not in '1234567890.-':

                        print(f"i: {in_stack[i]}")

                        in_stack.insert(i + 1, 'f(')

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

    
    print_stacks(in_stack, op_stack, out_stack, print_type = True)

    return out_stack



# print information
def print_stacks(*stacks, print_type):

    if print_type:

        print('')
        print(f"input stack: {('').join(stacks[0])}")
        print(f"operator stack: {[x.value for x in stacks[1]]}")

        temp_stack = []

        for i in stacks[2]:

            if type(i) == Token:

                temp_stack.append(i.value)

            else: temp_stack.append(i)

        print(f"output stack: {temp_stack}")



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

    equation = '( _ 2) ^ 2'

    # use the same symbol to denote negatives, but make it apply to a number differently. 
    # treat the symbol as an operator rather than as a part of the number, that way it can be applied to the number in the appropriate order with other tokens.

    is_radians = False

    output = shunting_yard_evaluator(equation, is_radians)

    output = ('').join(output)

    try: 
        output = float(output)
        print(f"output: {output:f}") 
    except: print(f"output: {output}")