import math

# this equation parser will convert inputs into reverse polish notation, and then solve the equation.

# add numbers to out stack as one list item, rather than one item per character

# how it works: https://en.m.wikipedia.org/wiki/Shunting_yard_algorithm 
# how to solve RPN equations: https://www.youtube.com/watch?v=qN8LPIcY6K4&t 


dict = {}
dict['precedence']      = {'s': 5, 'c': 5, 't': 5, 'S': 5, 'C': 5, 'T': 5, 'l': 5, 'f': 4, '^': 3, '#': 2, '%': 1, '/': 1, '*': 1, '+': 0, '_': 0, '(': 0, ')': 0}
dict['type']            = {'s': 1, 'c': 1, 't': 1, 'S': 1, 'C': 1, 'T': 1, 'l': 1, 'f': 1, '^': 0, '#': 1, '%': 0, '/': 0, '*': 0, '+': 0, '_': 0, '(': 2, ')': 3} # 3 means R bracket, 2 means L bracket, 1 means function, 0 means operator
dict['l associated']    = {'s': 1, 'c': 1, 't': 1, 'S': 1, 'C': 1, 'T': 1, 'l': 1, 'f': 1, '^': 0, '#': 1, '%': 1, '/': 1, '*': 1, '+': 1, '_': 1, '(': 0, ')': 1}



def shunting_yard_parser(equation):

    # set dict variable to inputted equation
    dict['input stack'] = list(equation)

    # print current equation
    print(f"equation: {dict['input stack']}")

    shunting_yard_converter(dict['input stack'])

    print('')
    print(f"original equation: {equation}")
    print(f"equation in RPN notation: {(' ').join(dict['out stack'])}")

    shunting_yard_evaluator()

    x = ('').join(dict['hist'])

    dict['hist'] = x.strip()

    print(f"answer: {dict['hist']}")

    return dict['hist']



def shunting_yard_converter(equation):


    dict['in stack']    = list(equation)
    dict['op stack']    = []
    dict['out stack']   = []

    # step 1 is to convert factorials into a bracket function like sin() and cos()
    for index, char, in enumerate(dict['in stack']):

        # look for factorial sign
        if char == '!':

            # set end of function
            dict['in stack'][index] = ')'

            # look for start of number next to factorial sign
            for i in range(index, 0, -1):

                # if a space is found, the number has ended
                if dict['in stack'][i] not in '1234567890.-':

                    # set start of equation
                    dict['in stack'].insert(i - 1, 'f(')

                    break

            # print info
            print(f"original equation: {equation}")

            print(f"factorials fixed: {('').join(dict['in stack'])}")


    # fix syntax
    x = ('').join(dict['in stack'])

    dict['in stack'] = list(x)



    # loop through list until it is empty
    while dict['in stack']:

        # create temproary list
        temp_stack = []

        print(f"char: {dict['in stack'][0]}")

        # remove spaces
        if dict['in stack'][0] == ' ':

            dict['in stack'].pop(0)



        # check if first character is part of a number
        elif dict['in stack'][0] in '1234567890.-':

            try:

                # loop through each character in the stack until a character isn't part of a number
                while dict['in stack'][0] in '1234567890.-':

                    # add number to temporary list
                    temp_stack.append(dict['in stack'].pop(0))
            
            except:pass

            # add temporary list to out stack
            dict['out stack'].append(('').join(temp_stack))
            print_stacks(1)

            

        # check if char is a function
        elif dict['type'][dict['in stack'][0]] == 1:

            # add function to output stack
            dict['op stack'].append(dict['in stack'].pop(0))
            print_stacks(1)


        # check if there is an operator
        elif dict['type'][dict['in stack'][0]] == 0:

            d = dict['op stack']

            # loop through output stack to ensure order of operations is followed
            while len(d) and d[-1] != '(' and (
                    dict['precedence'][d[-1]] > dict['precedence'][dict['in stack'][0]] or 
                    (dict['precedence'][d[-1]] == dict['precedence'][dict['in stack'][0]] and 
                    dict['l associated'][dict['in stack'][0]])):

                # pop last operator of op stack on to the out stack
                dict['out stack'].append(dict['op stack'].pop())
                print_stacks(1)



            # pop char on to op stack
            dict['op stack'].append(dict['in stack'].pop(0))
            print_stacks(1)



        # check if char is a left bracket
        elif dict['type'][dict['in stack'][0]] == 2:

            # pop dict['in stack'][0] on to op stack
            dict['op stack'].append(dict['in stack'].pop(0))



        # check if char is a right bracket
        elif dict['type'][dict['in stack'][0]] == 3:

            # remove right bracket
            dict['in stack'].pop(0)
            print_stacks(1)

            # loop through op stack until a left bracket is found
            while dict['op stack'] and dict['op stack'][-1] != '(':

                # pop op stack to out stack
                dict['out stack'].append(dict['op stack'].pop())
                print_stacks(1)

            # remove left bracket
            dict['op stack'].pop()
            print_stacks(1)



    # put the op stack on to the out stack
    while dict['op stack']:

        dict['out stack'].append(dict['op stack'].pop())
        print_stacks(1)



# print information
def print_stacks(type):

    if type:

        print('')
        print(f"input stack: {dict['in stack']}")
        print(f"operator stack: {dict['op stack']}")
        print(f"output stack: {dict['out stack']}")

    if not type:

        print('')
        print(f"number 1: {dict['number 1']}")
        print(f"number 2: {dict['number 2']}")



def shunting_yard_evaluator():

    # set up number stack
    dict['hist'] = []

    # loop through output stack
    while dict['out stack']:

        # check if first item is an operator
        if dict['out stack'][0] not in dict['type']:

            # if it isn't, add it to the number stack
            dict['hist'].append(dict['out stack'].pop(0))

        

        # do something else if it is an operator
        else:

            # find what numbers correspond to the operator
            find_numbers(dict['type'][dict['out stack'][0]])

            # solve section of equation
            solve(dict['out stack'][0])

            # remove operator from stack
            dict['out stack'].pop(0)



def find_numbers(type):

    # print all numbers
    print(f"all numbers: {dict['hist']}")

    # set up variables
    dict['number 1'] = ''

    dict['number 2'] = ''


    if type:

        dict['number 1'] = dict['hist'].pop(-1)


    
    else:

        dict['number 1'] = dict['hist'].pop(-2)

        dict['number 2'] = dict['hist'].pop(-1)

    print_stacks(0)


def solve(operation):

    # print text to show where the process currently is
    print('')
    print('solving...')
    print(f"operator/function: {operation}")
    print(f"number 1: {dict['number 1']}")
    print(f"number 2: {dict['number 2']}")



    # sine
    if operation == 's':

        dict['output'] = math.sin(math.radians(float(dict['number 1'])))



    # cosine
    if operation == 'c':

        dict['output'] = math.cos(math.radians(float(dict['number 1'])))



    # tangent
    if operation == 't':

        dict['output'] = math.tan(math.radians(float(dict['number 1'])))



    # inverse sine
    if operation == 'S':

        dict['output'] = math.degrees(math.asin(float(dict['number 1'])))



    # inverse cosine
    if operation == 'C':

        dict['output'] = math.degrees(math.acos(float(dict['number 1'])))



    # inverse tangent
    if operation == 'T':

        dict['output'] = math.degrees(math.atan(float(dict['number 1'])))



    # logarithm
    if operation == 'l':

        dict['output'] = math.log(float(dict['number 1']))



    # factorial
    if operation == 'f':

        dict['output'] = math.factorial(int(dict['number 1']))



    # exponent
    if operation == '^':

        dict['output'] = float(dict['number 1']) ** float(dict['number 2'])



    # square root
    if operation == '#':

        dict['output'] = float(dict['number 1']) ** 0.5



    # modulus
    if operation == '%':

        dict['output'] = float(dict['number 1']) % float(dict['number 2'])



    # division
    if operation == '/':

        dict['output'] = float(dict['number 1']) / float(dict['number 2'])



    # multiplication
    if operation == '*':

        dict['output'] = float(dict['number 1']) * float(dict['number 2'])



    # addition
    if operation == '+':

        dict['output'] = float(dict['number 1']) + float(dict['number 2'])



    # subtraction
    if operation == '_':

        dict['output'] = float(dict['number 1']) - float(dict['number 2'])



    # add solution to output stack
    dict['hist'].append(str(dict['output']))

    print('')

    # print info
    print(f"output: {dict['hist']}")
    print(f"remaining equation: {dict['out stack']}")






# use the parser without the GUI
if __name__ == '__main__':
    
    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _  2 ^ (5 _ 2)) / 15'

    '5 + 3! _ 5'

    '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    '53.06666666666667'

    # run parser with inputted equation
    shunting_yard_parser(equation)