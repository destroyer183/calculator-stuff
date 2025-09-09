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



# dictionaries
dict                     = {}
dict['bracket equation'] = {}
dict['normal equation']  = {}
dict['brackets done']    = False
dict['bracket equation']['start'] = 0

# this stores information about each type of operator to allow for them to be correctly solved in the right order with less for loops
dict['precedence'] = {'s': 5, 'c': 5, 't': 5, 'l': 5, 'S': 5, 'C': 5, 'T': 5, '!': 4, '^': 3, '#': 2, '/': 1, '*': 1, '%': 1, '+': 0, '_': 0}
dict['type']       = {'s': 1, 'c': 1, 't': 1, 'l': 1, 'S': 1, 'C': 1, 'T': 1, '!': 2, '^': 0, '#': 1, '/': 0, '*': 0, '%': 0, '+': 0, '_': 0}






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

    Token(token_type = TokenType.LeftBracket,  precedence = 0, math_operation = MathOperation.Null, value = '('),
    Token(token_type = TokenType.RightBracket, precedence = 0, math_operation = MathOperation.Null, value = ')')

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


# create class to store general information
class ScientificParser:

    # initialization function that takes in arguments for the equation, brackets done boolean, and bracket start index.
    def __init__(self, equation) -> None:
        
        # assign function arguments to object attributes
        self.equation = equation
        self.bracket_equation = ''
        self.brackets_done = False
        self.bracket_start = 0
        self.bracket_end = 0

    
    # main function that solves equations
    def evaluate(self):

        # try/catch block to catch unnecessary errors
        try:

            # if there aren't any brackets, change variable to confirm this
            if '(' not in self.equation: 

                self.brackets_done = True



            # do something else if there are brackets
            else:
                
                self.brackets_done = False

                # loop through each character in the whole equation
                for char in range(len(self.equation)):

                    # look for closed bracket symbol
                    if self.equation[char] == ")":

                        # save a variable with the index of where the bracket ends
                        dict['bracket equation']['end'] = char

                        break
                        


                # make separate variable with none of the equation beyond the closed bracket
                bracket_equation = bracket_equation[0:dict['bracket equation']['end']]


                
                # loop through each character in the whole equation
                for char in range(len(bracket_equation)):

                    # look for open bracket symbol
                    if bracket_equation[char] == "(":

                        # save a variable with the index of where the last open bracket is
                        dict['bracket equation']['start'] = char



                # make separate variable only contain the inner-most brackets of the main equation
                bracket_equation = bracket_equation[dict['bracket equation']['start'] + 1:len(bracket_equation)]

        except:pass


        # print bracket equation
        print(bracket_equation)

        # evaluate what is within the brackets
        bedmas(bracket_equation)

        # remove the brackets with what they evaluated to
        replace_brackets()



# main function that is called when an equation needs to be solved
def scientific_parser(input_equation):

    # create parser object and pass in input equation
    parser = ScientificParser(input_equation)

    # begin evaluating the equation
    output = evaluate(dict['equation'])

    # return solved equation
    return output






# function to remove any solved brackets
def replace_brackets():

    # change main equation to a list
    dict['equation'] = list(dict['equation'])

    # check if all brackets have been solved
    if dict['brackets done']:

        # clear input equation
        dict['equation'] = []



    # do something different if brackets haven't been solved
    else:

        # loop through everything within the inner-most brackets
        for i in range(dict['bracket equation']['start'], dict['bracket equation']['end'] + 1, 1):

            # delete inner-most brackets and everything within them
            dict['equation'].pop(dict['bracket equation']['start'])



    # insert evaluation of brackets where the brackets were
    dict['equation'].insert(dict['bracket equation']['start'], str(dict['algebra equation']))

    # change main equation back into a string
    dict['equation'] = ('').join(dict['equation'])

    # print current equation
    print(f"next equation: {dict['equation']}")

    # RECURSIVE LOOP EXIT CONDITION
    # try to convert main equation to a single number, if it works, the entiere equation has been solved
    try: dict['equation'] = float(dict['equation'])

    # if conversion errors, loop through equation again to evaluate the rest of it
    except: evaluate(dict['equation'])
        
    

# function to evaluate equation based on bedmas
def bedmas(algebra_equation):

    # set variable to inputted equation
    dict['algebra equation'] = algebra_equation

    try:

        # create variables
        precedence = -1

        location = None

        type = None

        # loop through the equation
        for index, char in enumerate(dict['algebra equation']):

            # check if an operator has been found
            if char in dict['precedence']:

                # if a negative number is the first thing in the list, it can cause issues. this prevents that.
                if not index and char == '-':

                    continue

                # check if the precedence of the char is higher than the last one found
                if dict['precedence'][char] > precedence:

                    # change precedence to newly found char
                    precedence = dict['precedence'][char]

                    # set location of char
                    location = index

                    # set type of number location
                    type = dict['type'][char]

        if location != None:

            # if an operator is found, run find_numbers() and give it the location of the operator(index), and how it should look for it
            find_numbers(location, type)

            # once the number(s) next to the operator have been identified, run solve() and give it the location of the operator in the equation
            solve(dict['algebra equation'][location])

    except:pass



# function to find numbers that corespond to nearby operators
def find_numbers(index, type):

    # clear variables
    dict['normal equation']['number 1'] = ''

    dict['normal equation']['number 2'] = ''

    # check for method of location
    if type == 0:

        # look for a number to the left of the operator
        for a in range(index - 2, -1, -1):

            # locate the end of the number
            if dict['algebra equation'][a] != ' ':

                # save the index of the left-most digit found at this time
                dict['normal equation']['start'] = a

                # add the most recently found digit to the entire number
                dict['normal equation']['number 1'] = dict['algebra equation'][a] + dict['normal equation']['number 1']
                
            # exit loop once entire number has been found
            else:break



        # look for a number to the right of the operator
        for b in range(index + 2, len(dict['algebra equation']), 1):

            if dict['algebra equation'][b] != ' ':

                dict['normal equation']['end'] = b

                dict['normal equation']['number 2'] += dict['algebra equation'][b]

            else:break


        
        # print numbers
        print(f"number 1: {dict['normal equation']['number 1']}")

        print(f"number 2: {dict['normal equation']['number 2']}")

        print('')


    
    if type == 1:

        # only look for number to the right of the operator
        for c in range(index + 1, len(dict['algebra equation']), 1):

            if dict['algebra equation'][c] != ' ':

                # save the start of the number
                dict['normal equation']['start'] = index

                # save the index of the right-most digit found
                dict['normal equation']['end']   = c

                dict['normal equation']['number 1'] += dict['algebra equation'][c]

            else:break



        print(f"number 1: {dict['normal equation']['number 1']}")

        print('')

    

    if type == 2:

        # look for a number to the left of the operator
        for a in range(index - 1, -1, -1):

            # locate the end of the number
            if dict['algebra equation'][a] != ' ':

                # save the index of the left-most digit found at this time
                dict['normal equation']['start'] = a

                # save the index of the right-most digit
                dict['normal equation']['end'] = index

                # add the most recently found digit to the entire number
                dict['normal equation']['number 1'] = dict['algebra equation'][a] + dict['normal equation']['number 1']
                
            # exit loop once entire number has been found
            else:break



        print(f"number 1: {dict['normal equation']['number 1']}")

        print('')



# simple function to evaluate two or one numbers and an operator
def solve(operation):

    # print text to show where the process currently is
    print('solving...')

    # logarithm
    if operation == 'l':

        dict['normal equation']['output'] = math.log(float(dict['normal equation']['number 1']))



    # sine
    if operation == 's':

        dict['normal equation']['output'] = math.sin(math.radians(float(dict['normal equation']['number 1'])))



    # cosine
    if operation == 'c':

        dict['normal equation']['output'] = math.cos(math.radians(float(dict['normal equation']['number 1'])))



    # tangent
    if operation == 't':

        dict['normal equation']['output'] = math.tan(math.radians(float(dict['normal equation']['number 1'])))



    # inverse sine
    if operation == 'S':

        dict['normal equation']['output'] = math.degrees(math.asin(float(dict['normal equation']['number 1'])))



    # inverse cosine
    if operation == 'C':

        dict['normal equation']['output'] = math.degrees(math.acos(float(dict['normal equation']['number 1'])))



    # inverse tangent
    if operation == 'T':

        dict['normal equation']['output'] = math.degrees(math.atan(float(dict['normal equation']['number 1'])))



    # factorial
    if operation == '!':

        dict['normal equation']['output'] = math.factorial(int(dict['normal equation']['number 1']))



    # exponent
    if operation == '^':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) ** float(dict['normal equation']['number 2'])



    # square root
    if operation == '#':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) ** 0.5



    # modulus
    if operation == '%':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) % float(dict['normal equation']['number 2'])



    # division
    if operation == '/':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) / float(dict['normal equation']['number 2'])



    # multiplication
    if operation == '*':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) * float(dict['normal equation']['number 2'])



    # addition
    if operation == '+':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) + float(dict['normal equation']['number 2'])



    # subtraction
    if operation == '_':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) - float(dict['normal equation']['number 2'])


    
    # turn equation into a list
    dict['algebra equation'] = list(dict['algebra equation'])

    # loop through the start and end indexs of previously solved equation
    for i in range(dict['normal equation']['start'], dict['normal equation']['end'] + 1, 1):

        # remove two/one numbers and an operator from the equation
        dict['algebra equation'].pop(dict['normal equation']['start'])

    # insert solved number where equation was
    dict['algebra equation'].insert(dict['normal equation']['start'], str(dict['normal equation']['output']))

    # turn equation back into a string
    dict['algebra equation'] = ('').join(dict['algebra equation'])

    # print variables to show location of process
    print(dict['algebra equation'])

    print('')

    # repeat bedmas to solve the rest of the equation
    bedmas(dict['algebra equation'])



def main():

    input_equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    '4 + (3! * (52 + 73 * #(64) / 2 - 220) - 2 ^ (5 - 2)) / 15'

    '53.06666666666667'

    # run parser with inputted equation
    scientific_parser(input_equation)



# use the parser without the GUI
if __name__ == '__main__':
    
    main()