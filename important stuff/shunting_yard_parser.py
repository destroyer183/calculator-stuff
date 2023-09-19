import math

# this equation parser will convert inputs into reverse polish notation, and then solve the equation.

# how it works: https://en.m.wikipedia.org/wiki/Shunting_yard_algorithm 
# how to solve RPN equations: https://www.youtube.com/watch?v=qN8LPIcY6K4&t 


dict = {}
dict['precedence']      = {'s': 5, 'c': 5, 't': 5, 'l': 5, 'S': 5, 'C': 5, 'T': 5, 'f': 4, '^': 3, '#': 2, '/': 1, '*': 1, '%': 1, '+': 0, '_': 0, '(': 0, ')': 0}
dict['type']            = {'s': 1, 'c': 1, 't': 1, 'l': 1, 'S': 1, 'C': 1, 'T': 1, 'f': 1, '^': 0, '#': 1, '/': 0, '*': 0, '%': 0, '+': 0, '_': 0, '(': 2, ')': 3} # 3 means R bracket, 2 means L bracket, 1 means function, 0 means operator
dict['l associated']    = {'s': 1, 'c': 1, 't': 1, 'l': 1, 'S': 1, 'C': 1, 'T': 1, 'f': 1, '^': 0, '#': 1, '/': 1, '*': 1, '%': 1, '+': 1, '_': 1, '(': 0, ')': 1}



def shunting_yard_parser(equation):

    # set dict variable to inputted equation
    dict['input stack'] = list(equation)

    # print current equation
    print(f"equation: {dict['input stack']}")

    shunting_yard_converter(dict['input stack'])

    print('')
    print(f"original equation: {equation}")
    print(f"equation in RPN notation: {('').join(dict['out stack'])}")

    shunting_yard_evaluator(dict['out stack'])

    return dict['equation']



def shunting_yard_converter(equation):

    dict['in stack'] = list(equation)
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
                if dict['in stack'][i] == ' ':

                    # set start of equation
                    dict['in stack'][i] = ' f('

                    break

            print(f"factorials fixed: {('').join(dict['in stack'])}")



    # fix syntax
    x = ('').join(dict['in stack'])

    dict['in stack'] = list(x)



    # loop through every charcter
    while dict['in stack']:

        # read a character
        char = dict['in stack'][0]

        # check if char is a number or part of a number
        if char in '1234567890.- ':

            # add number to output stack
            dict['out stack'].append(dict['in stack'].pop(0))
            print_stacks(1)



        # check if char is a function
        elif dict['type'][char] == 1:

            # add function to output stack
            dict['op stack'].append(dict['in stack'].pop(0))
            print_stacks(1)



        # check if char is an operator
        elif dict['type'][char] == 0:

            d = dict['op stack']

            # loop through output stack to ensure order of operations is followed
            while len(d) and d[-1] != '(' and (
                   dict['precedence'][d[-1]] > dict['precedence'][char] or 
                   (dict['precedence'][d[-1]] == dict['precedence'][char] and 
                    dict['l associated'][char])):

                # pop last operator of op stack on to the out stack
                dict['out stack'].append(dict['op stack'].pop())
                print_stacks(1)


            # pop char on to op stack
            dict['op stack'].append(dict['in stack'].pop(0))
            print_stacks(1)

        

        # check if char is a left bracket
        elif dict['type'][char] == 2:

            # pop char on to op stack
            dict['op stack'].append(dict['in stack'].pop(0))
            print_stacks(1)
            


        # check if char is a right bracket
        elif dict['type'][char] == 3:

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

        dict['out stack'].append(' ' + dict['op stack'].pop())
        print_stacks(1)


    # remove double spaces
    if '  ' in ('').join(dict['out stack']):

        x = ('').join(dict['out stack'])

        x = x.replace('  ', ' ')

        dict['out stack'] = list(x)

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



def shunting_yard_evaluator(equation):

    dict['equation'] = ('').join(equation)

    for index, char in enumerate(dict['equation']):

        if char in dict['type']:

            find_numbers(index, dict['type'][char])






    pass


def find_numbers(index, type):

    dict['number 1'] = ''

    dict['number 2'] = ''

    dict['eval end'] = index


    # look for a number to the left of the operator
    for a in range(index - 2, -1, -1):

        # locate the end of the number
        if dict['equation'][a] != ' ':

            # save the index of the left-most digit found at this time
            dict['eval start'] = a

            # add the most recently found digit to the entire number
            dict['number 1'] = dict['equation'][a] + dict['number 1']

            print_stacks(0)
            print('it worked')
            
        # exit loop once entire number has been found
        else:break



    # check if operator is a function or not
    if not type:

        # set up variables
        b = dict['eval start']

        dict['number 2'] = dict['number 1']

        dict['number 1'] = ''

        # look for a number to the left of the operator
        for a in range(b - 2, -1, -1):

            # locate the end of the number
            if dict['equation'][a] != ' ':

                # save the index of the left-most digit found at this time
                dict['eval start'] = a

                # add the most recently found digit to the entire number
                dict['number 1'] = dict['equation'][a] + dict['number 1']

                print_stacks(0)
                
            # exit loop once entire number has been found
            else:break






# use the parser without the GUI
if __name__ == '__main__':
    
    equation = '5 + 3! _ 5'

    '4 + (3! * (52 + 73 * #(64) / 2 - 220) - 2 ^ (5 - 2)) / 15'

    '53.06666666666667'

    # run parser with inputted equation
    shunting_yard_parser(equation)