import math
import time

# stuff to do:

# finish commenting

# use brackets to allow equations to be used as exponents

# use a dict to store the precedence of each operator to clean up the bedmas function (save the index of the highest priority operator)

# fix factorial syntax

# implement this: https://en.m.wikipedia.org/wiki/Shunting_yard_algorithm
    # how to evaluate RPN notation: https://www.youtube.com/watch?v=qN8LPIcY6K4&t

# formatting
# use math operators for everything (don't just put numbers next to brackets for multiplying brackets)
# put spaces in between every number and every operator
# exponents will be represented by ^ instead of **
# square root will be represented by #



# dictionaries
dict                     = {}
dict['bracket equation'] = {}
dict['normal equation']  = {}
dict['brackets done']    = False
dict['bracket equation']['start'] = 0



# main function that is called when an equation needs to be solved
def scientific_parser(equation):

    # set dict variable to inputted equation
    dict['equation'] = equation

    # print current equation
    print('equaton: ' + dict['equation'])

    # begin evaluating the equation
    evaluate(dict['equation'])

    # print the finished equation
    print('answer: ' + str(dict['equation']))

    # reset variable
    dict['brackets done'] = False

    # return solved equation
    return dict['equation']



# main function that solves equations
def evaluate(bracket_equation):

    # assign dict variable to inputted equation
    dict['bracket equation']['equation'] = bracket_equation

    try:

        # if there aren't any brackets, change variable to confirm this
        if '(' not in dict['bracket equation']['equation']: 

            dict['brackets done'] = True



        # do something else if there are brackets
        else:

            # loop through each character in the whole equation
            for char in range(len(dict['bracket equation']['equation'])):

                # look for closed bracket symbol
                if dict['bracket equation']['equation'][char] == ")":

                    # save a variable with the index of where the bracket ends
                    dict['bracket equation']['end'] = char

                    break
                    


            # make separate variable with none of the equation beyond the closed bracket
            dict['bracket equation']['equation'] = dict['bracket equation']['equation'][0:dict['bracket equation']['end']]


            
            # loop through each character in the whole equation
            for char in range(len(dict['bracket equation']['equation'])):

                # look for open bracket symbol
                if dict['bracket equation']['equation'][char] == "(":

                    # save a variable with the index of where the last open bracket is
                    dict['bracket equation']['start'] = char



            # make separate variable only contain the inner-most brackets of the main equation
            dict['bracket equation']['equation'] = dict['bracket equation']['equation'][dict['bracket equation']['start'] + 1:len(dict['bracket equation']['equation'])]

    except:pass


    # print bracket equation
    print(dict['bracket equation']['equation'])

    # evaluate what is within the brackets
    bedmas(dict['bracket equation']['equation'])

    # remove the brackets with what they evaluated to
    replace_brackets()



# function to remove any solved brackets
def replace_brackets():

    print('algebra equation again:', dict['algebra equation'])

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

    print('type:', type(dict['equation']))
    print(dict['algebra equation'])
    print(dict['equation'])
    print(dict['bracket equation']['start'])
    print(type(dict['bracket equation']['start']))
    time.sleep(10)

    # print current equation
    print('next equation: ' + dict['equation'])

    # RECURSIVE LOOP EXIT CONDITION
    # try to convert main equation to a single number, if it works, the entiere equation has been solved
    try: dict['equation'] = float(dict['equation'])

    # if conversion errors, loop through equation again to evaluate the rest of it
    except: evaluate(dict['equation'])
        
    

# function to evaluate equation based on bedmas
def bedmas(algebra_equation):

    # set variable to inputted equation
    dict['algebra equation'] = algebra_equation
    print('algebra equation:', dict['algebra equation'])

    try:

        # loop through every character in the current equation
        for index, char in enumerate(dict['algebra equation']):

            # look for a trig operator
            if char == 's' or char == 'c' or char == 't' or char == 'l':

                # if an operator is found, run find_numbers() and give it the location of the operator(index), and how it should look for it
                find_numbers(index, '2')

                # once the number(s) next to the operator have been identified, run solve() and give it the location of the operator in the equation
                solve(dict['algebra equation'][index])



        # loop through every character in the current equation
        for index, char in enumerate(dict['algebra equation']):

            # look for an inverse trig operator
            if char == 'S' or char == 'C' or char == 'T':

                find_numbers(index, '2')

                solve(dict['algebra equation'][index])



        # loop through every character in the current equation
        for index, char in enumerate(dict['algebra equation']):

            # look for a factorial sign
            if char == '!':

                find_numbers(index, '2')

                solve(dict['algebra equation'][index])



        # loop through every character in the current equation
        for index, char in enumerate(dict['algebra equation']):

            # look for an exponent sign
            if char == '^':

                find_numbers(index, '1')

                solve(dict['algebra equation'][index])



        # loop through every character in the current equation
        for index, char in enumerate(dict['algebra equation']):

            # look for square root sign
            if char == '#':

                find_numbers(index, '2')

                solve(dict['algebra equation'][index])



        # loop through every character in the current equation
        for index, char in enumerate(dict['algebra equation']):

            # look for multiplication, division, or modulus sign
            if char == '*' or char == '/' or char == '%':

                find_numbers(index, '1')

                solve(dict['algebra equation'][index])



        # loop through every character in the current equation
        for index, char in enumerate(dict['algebra equation']):

            print('index:', index, 'char:', char)

            # look for addition or subraction sign
            if char == '+' or char == '-':

                # ignore subtraction sign if it is found at the first place, as it represents an integer sign of a number rather than an operator in this case
                if char == '-' and index == 0:

                    print('it is happening')

                    print(index)

                    continue

                print(index)
                print(dict['algebra equation'])
                print(dict['algebra equation'][index])
                print(char)

                find_numbers(index, '1')

                solve(dict['algebra equation'][index])



    except:pass



# function to find numbers that corespond to nearby operators
def find_numbers(index, type):

    # clear variables
    dict['normal equation']['number 1'] = ''

    dict['normal equation']['number 2'] = ''

    # check for method of location
    if type == '1':

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
        print('number 1: ' + dict['normal equation']['number 1'])

        print('number 2: ' + dict['normal equation']['number 2'])

        print('')


    
    if type == '2':

        # only look for number to the right of the operator
        for c in range(index + 1, len(dict['algebra equation']), 1):

            if dict['algebra equation'][c] != ' ':

                # save the start of the number
                dict['normal equation']['start'] = index

                # save the index of the right-most digit found
                dict['normal equation']['end']   = c

                dict['normal equation']['number 1'] += dict['algebra equation'][c]

            else:break



        print('number 1: ' + dict['normal equation']['number 1'])

        print(' ')



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
    if operation == '-':

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

# use the parser without the GUI
if __name__ == '__main__':
    
    equation = '5 + -364'

    '4 + (!3 * (52 + 73 * #64 / 2 - 220) - 2 ^ (5 - 2)) / 15'

    '53.06666666666667'

    # run parser with inputted equation
    scientific_parser(equation)