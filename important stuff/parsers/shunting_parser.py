import math
from enum import Enum



''' NOTES

'''



# enums
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
    Negative = '-'
    Null = None

class Associativity(Enum):
    Left = 'left'
    Right = 'right'

class TokenType(Enum):
    Number = 0
    Operator = 1
    Function = 3
    LeftBracket = 5
    RightBracket = 6



# create class for every math operation token
class Token:

    # initialization function that takes in arguments for the token type, token precedence, token associativity, math operation, and value.
    def __init__(self, token_type: TokenType, precedence: int, associativity: Associativity, math_operation: MathOperation, value: str) -> None:
        
        # assign function arguments to object attributes
        self.token_type = token_type
        self.precedence = precedence
        self.associativity = associativity
        self.math_operation = math_operation
        self.value = value



    # function to perform various math functions depending on the inputs
    # takes in arguments for:
    # a boolean representation of whether or not to calculate with radians instead of degrees
    # two floats, x and y which are the numbers that will be used in the calculation
    def math(self, is_radians: bool, x: float, y: float):

        # match case to determine which math operation to use
        match self.math_operation:

            case MathOperation.Sine:       return (math.sin(x)  * is_radians) + (math.sin(math.radians(x))  * (not is_radians))
            case MathOperation.Cosine:     return (math.cos(x)  * is_radians) + (math.cos(math.radians(x))  * (not is_radians))
            case MathOperation.Tangent:    return (math.tan(x)  * is_radians) + (math.tan(math.radians(x))  * (not is_radians))
            case MathOperation.aSine:      return (math.asin(x) * is_radians) + (math.asin(math.radians(x)) * (not is_radians))
            case MathOperation.aCosine:    return (math.acos(x) * is_radians) + (math.acos(math.radians(x)) * (not is_radians))
            case MathOperation.aTangent:   return (math.atan(x) * is_radians) + (math.atan(math.radians(x)) * (not is_radians))
            case MathOperation.Logarithm:  return math.log(x, 10)
            case MathOperation.Absolute:   return abs(x)
            case MathOperation.Factorial:  return math.factorial(int(x))
            case MathOperation.SquareRoot: return x ** 0.5
            case MathOperation.Negative:   return -x

            case MathOperation.Exponential:    return x ** y
            case MathOperation.Modulo:         return x % y
            case MathOperation.Division:       return x / y
            case MathOperation.Multiplication: return x * y
            case MathOperation.Addition:       return x + y
            case MathOperation.Subtraction:    return x - y



# create tokens for every math operation available on calculator
TOKENS = [

    Token(token_type = TokenType.Function, precedence = 5, associativity = Associativity.Left,  math_operation = MathOperation.Sine,       value = 's'),
    Token(token_type = TokenType.Function, precedence = 5, associativity = Associativity.Left,  math_operation = MathOperation.Cosine,     value = 'c'),
    Token(token_type = TokenType.Function, precedence = 5, associativity = Associativity.Left,  math_operation = MathOperation.Tangent,    value = 't'),
    Token(token_type = TokenType.Function, precedence = 5, associativity = Associativity.Left,  math_operation = MathOperation.aSine,      value = 'S'),
    Token(token_type = TokenType.Function, precedence = 5, associativity = Associativity.Left,  math_operation = MathOperation.aCosine,    value = 'C'),
    Token(token_type = TokenType.Function, precedence = 5, associativity = Associativity.Left,  math_operation = MathOperation.aTangent,   value = 'T'),
    Token(token_type = TokenType.Function, precedence = 5, associativity = Associativity.Left,  math_operation = MathOperation.Logarithm,  value = 'l'),
    Token(token_type = TokenType.Function, precedence = 5, associativity = Associativity.Left,  math_operation = MathOperation.Absolute,   value = 'a'),
    Token(token_type = TokenType.Function, precedence = 4, associativity = Associativity.Left,  math_operation = MathOperation.Factorial,  value = 'f'),
    Token(token_type = TokenType.Function, precedence = 2, associativity = Associativity.Left,  math_operation = MathOperation.SquareRoot, value = '#'),
    Token(token_type = TokenType.Function, precedence = 2, associativity = Associativity.Left,  math_operation = MathOperation.Negative,   value = '-'),
    
    Token(token_type = TokenType.Operator, precedence = 3, associativity = Associativity.Right, math_operation = MathOperation.Exponential,    value = '^'),
    Token(token_type = TokenType.Operator, precedence = 1, associativity = Associativity.Left,  math_operation = MathOperation.Modulo,         value = '%'),
    Token(token_type = TokenType.Operator, precedence = 1, associativity = Associativity.Left,  math_operation = MathOperation.Division,       value = '/'),
    Token(token_type = TokenType.Operator, precedence = 1, associativity = Associativity.Left,  math_operation = MathOperation.Multiplication, value = '*'),
    Token(token_type = TokenType.Operator, precedence = 0, associativity = Associativity.Left,  math_operation = MathOperation.Addition,       value = '+'),
    Token(token_type = TokenType.Operator, precedence = 0, associativity = Associativity.Left,  math_operation = MathOperation.Subtraction,    value = '_'),

    Token(token_type = TokenType.LeftBracket,  precedence = 0, associativity = Associativity.Right, math_operation = MathOperation.Null, value = '('),
    Token(token_type = TokenType.RightBracket, precedence = 0, associativity = Associativity.Left,  math_operation = MathOperation.Null, value = ')')

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
        


# function to convert standard equation strings into reverse polish notation using the shunting yard algorithm
def shunting_yard_converter(equation: str):

    # create variables for input stack, operator stack, and output stack
    in_stack = list(equation)
    op_stack = []
    out_stack = []

    # loop over input stack by index and element, this is to find any factorials and change the format of them.
    for index, char, in enumerate(in_stack):

        # check for factorial symbol
        if char == '!':

            # replace factorial symbol with right bracket
            in_stack[index] = ')'

            # check if previous character was a right bracket
            # this case will allow factorials to work on brackets of any depth, allowing something like (((1 + 2) + 3) + 4)! to work properly
            if in_stack[index - 1] == ')':

                # create bracket counter
                bracket_count = 0
                
                # loop backwards starting at one character before the factorial symbol was found
                for i in range(index - 1, -1, -1):

                    # check if current character is right bracket
                    if in_stack[i] == ')':

                        # incrament bracket counter
                        bracket_count += 1



                    # check if current character is left bracket
                    elif in_stack[i] == '(':

                        # decrament bracket counter
                        bracket_count -= 1

                        # check if the number of left brackets has cancelled out the number of right brackets
                        if bracket_count == 0:

                            # insert the proper factorial format symbol at the position before the last left bracket, or at index 0 in case the last left bracket was at index 0
                            in_stack.insert(max(0, i - 1), 'f(')

                            # exit loop
                            break



            # triggers if the character before the factorial symbol was not a right bracket
            else:

                # loop backwards starting at one character before the factorial symbol was found
                for i in range(index - 1, -1, -1):

                    # check if the current index is 0
                    if i == 0:

                        # insert the proper factorial format symbol at the start of the stack
                        in_stack.insert(0, 'f(')

                        # exit loop
                        break



                    # check if the current character is not part of a number
                    elif in_stack[i] not in '1234567890.':

                        # insert the proper factorial format symbol at one index higher than where a non-number character was found
                        in_stack.insert(i + 1, 'f(')

                        # exit loop
                        break


    # join and then split list to make sure it is a list with only single-character elements
    x = ('').join(in_stack)
    in_stack = list(x)


    # loop while the 'in_stack' has items in it
    while in_stack:

        # create temporary stack
        # this will store numbers character by character when they are found
        temp_stack = []

        # # try/except to prevent unnecessary crashes
        # try: 

        #     # get token from 'in_stack' at index 0 if the previous token was not a string and was not a right bracket
        #     if type(token) != str and token.value != ')':
        #         token = get_token(in_stack.pop(0))
                
        #     # triggers if the above condidtion evaluated to false
        #     else:
        #         token = get_token(in_stack.pop(0))
        
        # # except in case the code above crashes
        # except:
        #     token = get_token(in_stack.pop(0))
        token = get_token(in_stack.pop(0))

        # if token is whitespace, skip current iteration and start next iteration
        if token == ' ':

            continue

        # check if the current token is a string
        elif type(token) == str:

            # check if current token is part of a number
            if token in '1234567890.':

                # try/except to prevent unnecessary crashes
                try:

                    # keep looping while the current token is part of a number
                    # this takes each character of a number and puts it into a temporary stack to then be added to the output stack
                    while token in '1234567890.':

                        # add current token to temp stack
                        temp_stack.append(token)

                        # get new token
                        token = get_token(in_stack.pop(0))

                # except in case the above code crashes
                except:pass

                # join the temp stack into one whole number and append it to the output stack
                out_stack.append(('').join(temp_stack))

                

        # try/except to avoid unnecessary crashes
        try:

            # check if the current token type is 'Function'
            if token.token_type == TokenType.Function:

                # append token to operator stack
                op_stack.append(token)


            # check if the current token type is 'Operator'
            elif token.token_type == TokenType.Operator:
                
                # keep looping while:
                # operator stack is not empty and the last element in the operator stack is not a left bracket, and (
                # the precedence of the last token in the operator stack is greater than the precedence of the current token, or (
                # the precedence of the last token in the operator stack is equal to the precedence of the current token and the associativity of the current token is left))
                while op_stack and op_stack[-1].value != '(' and (
                        op_stack[-1].precedence > token.precedence or (
                        op_stack[-1].precedence == token.precedence and 
                        token.associativity == Associativity.Left)):

                    # pop element from operator stack and append it to the output stack
                    out_stack.append(op_stack.pop())

                # append current token to the operator stack
                op_stack.append(token)



            # check if the current token type is 'LeftBracket'
            elif token.token_type == TokenType.LeftBracket:

                # append the current token to the operator stack
                op_stack.append(token)



            # check if the current token type is 'RightBracket'
            elif token.token_type == TokenType.RightBracket:

                # keep looping while the operator stack is not empty and the token type of the last token in the operator stack is not 'LeftBracket'
                while op_stack and op_stack[-1].token_type != TokenType.LeftBracket:

                    # pop element from operator stack and append it to the output stack
                    out_stack.append(op_stack.pop())

                # pop last element from operator stack
                op_stack.pop()

        # except to prevent any unnecessary crashes
        except:pass


    # keep looping while the operator stack is not empty
    while op_stack:

        # po element from operator stack and append it to the output stack
        out_stack.append(op_stack.pop())

    # print out every element in the output stack
    for index in out_stack:
        print(index)

    

    # return the output stack
    return out_stack



# main function to evaluate an equation, takes in arguments for the string equation and a boolean representation of whether or not to use radians or not 
def shunting_yard_evaluator(equation: str, is_radians: bool):

    # conver the equation to reverse polish notation and store it in a variable
    stack = shunting_yard_converter(equation)

    # create list for number history
    hist = []

    # keep looping while 'stack' is not empty
    while stack:

        # remove first element from 'stack' and store it in a variable
        item = stack.pop(0)

        # check if the type of 'item' is a string
        if type(item) == str:

            # append 'item' to number history
            hist.append(item)

        # only triggers if 'item' is not a string
        else:

            # call 'find_numbers' to get the necessary numbers for a calculation, and to get the updated history
            a, b, hist = find_numbers(item.token_type, hist)

            # perform calculation, then convert the output to a string and append it to the history
            hist.append(str(item.math(is_radians, float(a), float(b))))

    # join history into a single string and strip any whitespace
    hist = ('').join(hist).strip()

    # return history
    return hist



# function to find the numbers necessary for a calculation, takes in arguments for the token type as a 'TokenType', and the history as a 'list'
def find_numbers(token_type: TokenType, hist: list):

    # return only one number from the history if the token type is 'Function' and also return the updated history
    if token_type == TokenType.Function: return hist.pop(-1), 0, hist

    # if the token type is not 'Function' return two numbers from the history and also return the updated history
    else: return hist.pop(-2), hist.pop(-1), hist
    


def main():

    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    equation = '-(3.141259265359)'

    is_radians = False

    output = shunting_yard_evaluator(equation, is_radians)

    output = ('').join(output)

    try: 
        output = float(output)
        print(f"output: {output:f}") 
    except: print(f"output: {output}")



if __name__ == '__main__':

    main()