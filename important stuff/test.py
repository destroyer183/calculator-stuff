from scientific_parser import *

dict = {'algebra equation':list('4 + 312.0 + 292.0 - 220 - 32.0 - 0.13333333333333333')}

dict['precedence'] = {'s': 5, 'c': 5, 't': 5, 'l': 5, 'S': 5, 'C': 5, 'T': 5, '!': 4, '^': 3, '#': 2, '/': 1, '*': 1, '%': 1, '+': 0, '-': 0}

dict['type']       = {'s': 1, 'c': 1, 't': 1, 'l': 1, 'S': 1, 'C': 1, 'T': 1, '!': 1, '^': 0, '#': 1, '/': 0, '*': 0, '%': 0, '+': 0, '-': 0}



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
            print(f'precedence: {precedence}')

            # set location of char
            location = index
            print(f'location: {location}')

            # set type of number location
            type = dict['type'][char]
            print(f'type: {type}')

if location != None:

    # if an operator is found, run find_numbers() and give it the location of the operator(index), and how it should look for it
    find_numbers(location, type)

    # once the number(s) next to the operator have been identified, run solve() and give it the location of the operator in the equation
    solve(dict['algebra equation'][location])