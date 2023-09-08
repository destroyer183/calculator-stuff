import math
import time



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



def equation_parser(equation):

    dict['equation'] = equation

    print('equaton: ' + dict['equation'])

    evaluate(dict['equation'])

    print('answer: ' + str(dict['equation']))

    dict['brackets done'] = False

    return dict['equation']



def evaluate(bracket_equation):

    dict['bracket equation']['equation'] = bracket_equation

    try:

        if '(' not in dict['bracket equation']['equation']: 

            dict['brackets done'] = True



        if '(' in dict['bracket equation']['equation']:

            for char in range(len(dict['bracket equation']['equation'])):

                if dict['bracket equation']['equation'][char] == ")":

                    dict['bracket equation']['end'] = char

                    break
                    
            dict['bracket equation']['equation'] = dict['bracket equation']['equation'][0:dict['bracket equation']['end']]



            for char in range(len(dict['bracket equation']['equation'])):

                if dict['bracket equation']['equation'][char] == "(":

                    dict['bracket equation']['start'] = char

            dict['bracket equation']['equation'] = dict['bracket equation']['equation'][dict['bracket equation']['start'] + 1:len(dict['bracket equation']['equation'])]

    except:pass



    print(dict['bracket equation']['equation'])

    bedmas(dict['bracket equation']['equation'])

    replace_brackets()



def replace_brackets():

    dict['equation'] = list(dict['equation'])

    if dict['brackets done']:

        dict['equation'] = []

    else:

        for i in range(dict['bracket equation']['start'], dict['bracket equation']['end'] + 1, 1):

            dict['equation'].pop(dict['bracket equation']['start'])

    dict['equation'].insert(dict['bracket equation']['start'], str(dict['algebra equation']))

    string = ''

    for x in dict['equation']:

        string += x

    dict['equation'] = string

    print('next equation: ' + dict['equation'])

    try: dict['equation'] = float(dict['equation'])

    except: evaluate(dict['equation'])
        
    

def bedmas(algebra_equation):

    dict['algebra equation'] = algebra_equation

    try:

        for char in range(len(dict['algebra equation'])):

            if dict['algebra equation'][char] == 's' or dict['algebra equation'][char] == 'c' or dict['algebra equation'][char] == 't' or dict['algebra equation'][char] == 'l':

                find_numbers(char, '2')

                solve(dict['algebra equation'][char])



        for char in range(len(dict['algebra equation'])):

            if dict['algebra equation'][char] == 'S' or dict['algebra equation'][char] == 'C' or dict['algebra equation'][char] == 'T':

                find_numbers(char, '2')

                solve(dict['algebra equation'][char])



        for char in range(len(dict['algebra equation'])):

            if dict['algebra equation'][char] == '!':

                find_numbers(char, '2')

                solve(dict['algebra equation'][char])



        for char in range(len(dict['algebra equation'])):

            if dict['algebra equation'][char] == "^":

                find_numbers(char, '1')

                solve(dict['algebra equation'][char])



        for char in range(len(dict['algebra equation'])):

            if dict['algebra equation'][char] == '#':

                find_numbers(char, '2')

                solve(dict['algebra equation'][char])



        for char in range(len(dict['algebra equation'])):

            if dict['algebra equation'][char] == '*' or dict['algebra equation'][char] == '/' or dict['algebra equation'][char] == '%':

                find_numbers(char, '1')

                solve(dict['algebra equation'][char])



        for char in range(len(dict['algebra equation'])):

            if dict['algebra equation'][char] == '+' or dict['algebra equation'][char] == '-':

                if dict['algebra equation'][char] == '-' and char == 0:
                    
                    continue

                find_numbers(char, '1')

                solve(dict['algebra equation'][char])



    except:pass



def find_numbers(char, type):

    dict['normal equation']['number 1'] = ''

    dict['normal equation']['number 2'] = ''

    if type == '1':

        for a in range(char - 2, -1, -1):

            if dict['algebra equation'][a] != ' ':

                dict['normal equation']['start'] = a

                dict['normal equation']['number 1'] = dict['algebra equation'][a] + dict['normal equation']['number 1']
                
            else:break



        for b in range(char + 2, len(dict['algebra equation']), 1):

            if dict['algebra equation'][b] != ' ':

                dict['normal equation']['end'] = b

                dict['normal equation']['number 2'] += dict['algebra equation'][b]

            else:break


        
        print('number 1: ' + dict['normal equation']['number 1'])

        print('number 2: ' + dict['normal equation']['number 2'])

        print('')


    
    if type == '2':

        for c in range(char + 1, len(dict['algebra equation']), 1):

            if dict['algebra equation'][c] != ' ':

                dict['normal equation']['start'] = char

                dict['normal equation']['end']   = c

                dict['normal equation']['number 1'] += dict['algebra equation'][c]

            else:break



        print('number 1: ' + dict['normal equation']['number 1'])

        print(' ')



def solve(operation):

    print('solve is running')

    if operation == 'l':

        dict['normal equation']['output'] = math.log(float(dict['normal equation']['number 1']))



    if operation == 's':

        dict['normal equation']['output'] = math.sin(math.radians(float(dict['normal equation']['number 1'])))



    if operation == 'c':

        dict['normal equation']['output'] = math.cos(math.radians(float(dict['normal equation']['number 1'])))



    if operation == 't':

        dict['normal equation']['output'] = math.tan(math.radians(float(dict['normal equation']['number 1'])))



    if operation == 'S':

        dict['normal equation']['output'] = math.degrees(math.asin(float(dict['normal equation']['number 1'])))



    if operation == 'C':

        dict['normal equation']['output'] = math.degrees(math.acos(float(dict['normal equation']['number 1'])))



    if operation == 'T':

        dict['normal equation']['output'] = math.degrees(math.atan(float(dict['normal equation']['number 1'])))



    if operation == '!':

        dict['normal equation']['output'] = math.factorial(int(dict['normal equation']['number 1']))



    if operation == '^':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) ** float(dict['normal equation']['number 2'])



    if operation == '#':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) ** 0.5



    if operation == '%':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) % float(dict['normal equation']['number 2'])



    if operation == '/':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) / float(dict['normal equation']['number 2'])



    if operation == '*':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) * float(dict['normal equation']['number 2'])



    if operation == '+':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) + float(dict['normal equation']['number 2'])



    if operation == '-':

        dict['normal equation']['output'] = float(dict['normal equation']['number 1']) - float(dict['normal equation']['number 2'])



    dict['algebra equation'] = list(dict['algebra equation'])

    for i in range(dict['normal equation']['start'], dict['normal equation']['end'] + 1, 1):

        dict['algebra equation'].pop(dict['normal equation']['start'])

    dict['algebra equation'].insert(dict['normal equation']['start'], str(dict['normal equation']['output']))

    string = ''

    for x in dict['algebra equation']:

        string += x

    dict['algebra equation'] = string

    print(dict['algebra equation'])

    print('')

    bedmas(dict['algebra equation'])


equation = ''

'4 + (!3 * (52 + 73 * #64 / 2 - 220) - 2 ^ 3) / 15'

'0.9200260381967907'

# equation_parser(equation)