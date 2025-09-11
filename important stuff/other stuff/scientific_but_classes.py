import math
from enum import Enum

# stuff to do:

# LEARN CLASSES


# implement this: https://en.m.wikipedia.org/wiki/Shunting_yard_algorithm
    # how to evaluate RPN notation: https://www.youtube.com/watch?v=qN8LPIcY6K4&t

# put the converter and the solver in separate files

# formatting
# use math operators for everything (don't just put numbers next to brackets for multiplying brackets)
# put spaces in between every number and every operator
# exponents will be represented by ^ instead of **
# square root will be represented by #


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

class TokenType(Enum):
    Number = 0
    Operator = 1
    Function = 3
    LeftBracket = 5
    RightBracket = 6



# create class for every math operation token
class Token:

    # initialization function that takes in arguments for the token type, token precedence, math operation, and value.
    def __init__(self, token_type: TokenType, precedence: int,  math_operation: MathOperation, value: str) -> None:
        
        # assign function arguments to object attributes
        self.token_type = token_type
        self.precedence = precedence
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
            case MathOperation.aSine:      return (math.asin(x) * is_radians) + (math.degrees(math.asin(x)) * (not is_radians))
            case MathOperation.aCosine:    return (math.acos(x) * is_radians) + (math.degrees(math.acos(x)) * (not is_radians))
            case MathOperation.aTangent:   return (math.atan(x) * is_radians) + (math.degrees(math.atan(x)) * (not is_radians))
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

    Token(token_type = TokenType.Function, precedence = 5, math_operation = MathOperation.Sine,       value = 's'),
    Token(token_type = TokenType.Function, precedence = 5, math_operation = MathOperation.Cosine,     value = 'c'),
    Token(token_type = TokenType.Function, precedence = 5, math_operation = MathOperation.Tangent,    value = 't'),
    Token(token_type = TokenType.Function, precedence = 5, math_operation = MathOperation.aSine,      value = 'S'),
    Token(token_type = TokenType.Function, precedence = 5, math_operation = MathOperation.aCosine,    value = 'C'),
    Token(token_type = TokenType.Function, precedence = 5, math_operation = MathOperation.aTangent,   value = 'T'),
    Token(token_type = TokenType.Function, precedence = 5, math_operation = MathOperation.Logarithm,  value = 'l'),
    Token(token_type = TokenType.Function, precedence = 5, math_operation = MathOperation.Absolute,   value = 'a'),
    Token(token_type = TokenType.Function, precedence = 4, math_operation = MathOperation.Factorial,  value = 'f'),
    Token(token_type = TokenType.Function, precedence = 2, math_operation = MathOperation.SquareRoot, value = '#'),
    Token(token_type = TokenType.Function, precedence = 2, math_operation = MathOperation.Negative,   value = '-'),
    
    Token(token_type = TokenType.Operator, precedence = 3, math_operation = MathOperation.Exponential,    value = '^'),
    Token(token_type = TokenType.Operator, precedence = 1, math_operation = MathOperation.Modulo,         value = '%'),
    Token(token_type = TokenType.Operator, precedence = 1, math_operation = MathOperation.Division,       value = '/'),
    Token(token_type = TokenType.Operator, precedence = 1, math_operation = MathOperation.Multiplication, value = '*'),
    Token(token_type = TokenType.Operator, precedence = 0, math_operation = MathOperation.Addition,       value = '+'),
    Token(token_type = TokenType.Operator, precedence = 0, math_operation = MathOperation.Subtraction,    value = '_'),

    # Token(token_type = TokenType.LeftBracket,  precedence = 0, math_operation = MathOperation.Null, value = '('),
    # Token(token_type = TokenType.RightBracket, precedence = 0, math_operation = MathOperation.Null, value = ')')

]



# function to return a token based on a string argument
def get_token(value: str):

    # if value is a string, return nothing to remove the string
    if value == ' ': return ''

    # loop over every math operation token
    for i in TOKENS:

        # check if token value is equal to the string argument inputted
        if i.value == value:

            # return token if match is found
            return i 
        
    # return string argument if no match is found
    return value



# create class to store general information
class ScientificParser:

    # initialization function that takes in arguments for the equation, brackets done boolean, and bracket start index.
    def __init__(self, equation: str, is_radians: bool) -> None:
        
        # assign function arguments to object attributes
        self.is_radians: bool = is_radians
        self.equation: list = [x for x in equation]
        self.bracket_equation: list = []
        self.algebra_equation: list = []
        self.brackets_done = False
        self.bracket_start = 0
        self.bracket_end = 0
        self.algebra_start = 0
        self.algebra_end = 0


    # function to adjust the notation of factorial to allow the parser to evaluate it properly
    def factorial_adjuster(self):
        
        # loop over input equation by index and element, this is to find any factorials and change the format of them.
        for index, char, in enumerate(self.equation):

            # check for factorial symbol
            if char == '!':

                # replace factorial symbol with right bracket
                self.equation[index] = ')'

                # check if previous character was a right bracket
                # this case will allow factorials to work on brackets of any depth, allowing something like (((1 + 2) + 3) + 4)! to work properly
                if self.equation[index - 1] == ')':

                    # create bracket counter
                    bracket_count = 0
                    
                    # loop backwards starting at one character before the factorial symbol was found
                    for i in range(index - 1, -1, -1):

                        # check if current character is right bracket
                        if self.equation[i] == ')':

                            # incrament bracket counter
                            bracket_count += 1



                        # check if current character is left bracket
                        elif self.equation[i] == '(':

                            # decrament bracket counter
                            bracket_count -= 1

                            # check if the number of left brackets has cancelled out the number of right brackets
                            if bracket_count == 0:

                                # insert the proper factorial format symbol at the position before the last left bracket, or at index 0 in case the last left bracket was at index 0
                                self.equation.insert(max(0, i - 1), 'f(')

                                # exit loop
                                break



                # triggers if the character before the factorial symbol was not a right bracket
                else:

                    # loop backwards starting at one character before the factorial symbol was found
                    for i in range(index - 1, -1, -1):

                        # check if the current index is 0
                        if i == 0:

                            # insert the proper factorial format symbol at the start of the equation
                            self.equation.insert(0, 'f(')

                            # exit loop
                            break



                        # check if the current character is not part of a number
                        elif self.equation[i] not in '1234567890.':

                            # insert the proper factorial format symbol at one index higher than where a non-number character was found
                            self.equation.insert(i + 1, 'f(')

                            # exit loop
                            break

        # convert operators in equation to tokens
        self.equation = [get_token(x) for x in ('').join(self.equation)]



    # main function that solves equations
    def evaluate(self):

        # call function to adjust factorial format if unconverted factorial is found in equation
        if '!' in self.equation: self.factorial_adjuster()

        # create attribute to store a bracket subset of the input equation
        self.bracket_equation = self.equation

        # if there aren't any brackets, change variable to confirm this
        if '(' not in self.equation:

            self.brackets_done = True



        # do something else if there are brackets
        else:

            # loop through each character in the whole equation
            for i in range(len(self.bracket_equation)):

                # check if current character is a token
                if type(self.bracket_equation[i]) != Token:

                    # look for closed bracket symbol
                    if self.bracket_equation[i] == ')':

                        # save a variable with the index of where the bracket ends
                        self.bracket_end = i

                        # exit loop
                        break
                    


            # remove equation past the end bracket
            self.bracket_equation = self.bracket_equation[:self.bracket_end]
            


            # loop through each character in the whole equation
            for i in range(len(self.bracket_equation)):

                # check if current character is a token
                if type(self.bracket_equation[i]) != Token:
            
                    # look for open bracket symbol
                    if self.bracket_equation[i] == '(':

                        # save a variable with the index of where the last open bracket is
                        self.bracket_start = i



            # make separate variable only contain the inner-most brackets of the main equation
            self.bracket_equation = self.bracket_equation[self.bracket_start + 1:]



        # print equation
        print_equation(self.bracket_equation, 'equation: ')

        # evaluate what is within the brackets
        self.bedmas(self.bracket_equation)

        # remove the brackets with what they evaluated to
        self.replace_brackets()

        # convert finished equation to a float and return it
        return float(('').join(self.equation))



    # function to remove any solved brackets
    def replace_brackets(self):

        # check if all brackets have been solved
        if self.brackets_done:

            # clear input equation
            self.equation = []

        # print equation
        print_equation(self.equation, 'next equation: ')

        # insert evaluation of brackets where the brackets were
        self.equation[self.bracket_start:self.bracket_end + 1] = self.algebra_equation

        # check if there is more than one element in the equation, and continue solving if there is.
        if len(self.equation) != 1: self.evaluate()



    # function to evaluate equation based on bedmas
    def bedmas(self, algebra_equation):

        # set variable to inputted equation
        self.algebra_equation = algebra_equation

        # create variables
        precedence = -1

        location = None

        item: Token = None

        # loop through the equation
        for index, char in enumerate(self.algebra_equation):

            # check if an operator has been found
            if type(char) == Token:

                char: Token = char

                # if a negative number is the first thing in the list, it can cause issues. this prevents that.
                if not index and char == '-':

                    continue

                # check if the precedence of the char is higher than the last one found
                if char.precedence > precedence:

                    # change precedence to newly found char
                    precedence = char.precedence

                    # set location of char
                    location = index

                    # set item to token
                    item = char



        if location != None:

            print_equation(self.algebra_equation, '\ncurrent equation: ')

            # if an operator is found, run find_numbers() and give it the location of the operator(index), and how it should look for it
            num1, num2 = self.find_numbers(location, item.token_type)

            output = item.math(self.is_radians, float(num1), float(num2))

            # once the number(s) next to the operator have been identified, run solve() and give it the location of the operator in the equation
            self.replace_algebra(output)




    # function to find numbers that corespond to nearby operators
    def find_numbers(self, index, token_type):

        # set variables
        num1 = ''
        num2 = ''

        # check for method of location
        if token_type == TokenType.Operator:

            # look for a number to the left of the operator
            for i in range(index - 1, -1, -1):

                # locate the end of the number
                if type(self.algebra_equation[i]) != Token:

                    # save the index of the left-most digit found at this time
                    self.algebra_start = i

                    # add the most recently found digit to the entire number
                    num1 = self.algebra_equation[i] + num1
                    
                # exit loop once entire number has been found
                else:break



            # look for a number to the right of the operator
            for j in range(index + 1, len(self.algebra_equation), 1):

                if type(self.algebra_equation[j]) != Token:

                    self.algebra_end = j

                    num2 += self.algebra_equation[j]

                else:break

            # print numbers
            print(f"number 1: {num1}")
            print(f"number 2: {num2}")
            
            # return numbers found
            return num1, num2


        
        if token_type == TokenType.Function:

            # only look for number to the right of the operator
            for i in range(index + 1, len(self.algebra_equation), 1):

                if type(self.algebra_equation[i]) != Token:

                    # save the start of the number
                    self.algebra_start = index

                    # save the index of the right-most digit found
                    self.algebra_end = i

                    num1 += self.algebra_equation[i]

                else:break

            # print number
            print(f"number 1: {num1}")

            # return numbers found
            return num1, 0




    # simple function to evaluate two or one numbers and an operator
    def replace_algebra(self, output):
        
        # loop through the start and end indexs of previously solved equation
        for i in range(self.algebra_start, self.algebra_end + 1, 1):

            # remove two/one numbers and an operator from the equation
            self.algebra_equation.pop(self.algebra_start)

        # insert solved number where equation was
        self.algebra_equation.insert(self.algebra_start, str(output))

        # repeat bedmas to solve the rest of the equation
        self.bedmas(self.algebra_equation)



# main function that is called when an equation needs to be solved
def scientific_parser(input_equation, is_radians):

    print(f"input equation: {input_equation}")

    # create parser object and pass in input equation
    parser = ScientificParser(input_equation, is_radians)

    # begin evaluating the equation
    output = parser.evaluate()

    print(output)

    # return solved equation
    return output



# function to print out the equation
def print_equation(equation: list, prefix: str = ''):

    output = ''

    for item in equation:
        if type(item) == Token:
            output += item.value
        else:
            output += item
    
    print(prefix + output)



def main():

    print('')

    input_equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    '4 + (3! * (52 + 73 * #(64) / 2 - 220) - 2 ^ (5 - 2)) / 15'

    '53.06666666666667'

    # run parser with inputted equation
    scientific_parser(input_equation, False)



# use the parser without the GUI
if __name__ == '__main__':
    
    main()