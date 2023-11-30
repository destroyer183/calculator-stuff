import math
import time

# might have to replace every 'token' variable with 'token'

LEFT = True
RIGHT = False

NUMBER = 0
OPERATOR = 0
BRACKET = 3
FUNCTION = 1
COMMA = 5
LEFT_BRACKET = 2
RIGHT_BRACKET = 3



class Token:

    def __init__(self, type: int, precedence: int, associativity: bool, value, apply=None) -> None:
        
        self.type  = type
        self.precedence = precedence
        self.associativity = associativity
        self.value = value
        self.apply = apply




TOKENS = [

    Token(FUNCTION, 5, LEFT,  value='s', apply=lambda x: math.sin(math.radians(float(x)))),
    Token(FUNCTION, 5, LEFT,  value='c', apply=lambda x: math.cos(math.radians(float(x)))),
    Token(FUNCTION, 5, LEFT,  value='t', apply=lambda x: math.tan(math.radians(float(x)))),
    Token(FUNCTION, 5, LEFT,  value='S', apply=lambda x: math.degrees(math.asin(float(x)))),
    Token(FUNCTION, 5, LEFT,  value='C', apply=lambda x: math.degrees(math.acos(float(x)))),
    Token(FUNCTION, 5, LEFT,  value='T', apply=lambda x: math.degrees(math.atan(float(x)))),
    Token(FUNCTION, 5, LEFT,  value='l', apply=lambda x: math.log((float(x)))),
    Token(FUNCTION, 4, LEFT,  value='f', apply=lambda x: math.factorial((int(x)))),
    Token(FUNCTION, 2, LEFT,  value='#', apply=lambda x: float(x) ** 0.5),
    
    Token(OPERATOR, 3, RIGHT, value='^', apply=lambda a,b: float(a) ** float(b)),
    Token(OPERATOR, 1, LEFT,  value='%', apply=lambda a,b: float(a) % float(b)),
    Token(OPERATOR, 1, LEFT,  value='/', apply=lambda a,b: float(a) / float(b)),
    Token(OPERATOR, 1, LEFT,  value='*', apply=lambda a,b: float(a) * float(b)),
    Token(OPERATOR, 0, LEFT,  value='+', apply=lambda a,b: float(a) + float(b)),
    Token(OPERATOR, 0, LEFT,  value='_', apply=lambda a,b: float(a) - float(b)),

    Token(LEFT_BRACKET, 0, RIGHT, value='('),
    Token(RIGHT_BRACKET, 0, LEFT, value=')')

    ]

def shunting_yard_parser(equation):

    # set dict variable to inputted equation
    in_stack = list(equation)

    # print current equation
    print(f"equation: {('').join(in_stack)}")

    out_stack = shunting_yard_converter(in_stack)

    print('')
    print(f"original equation: {('').join(equation)}")

    temp_stack = []

    for i in out_stack:

        if type(i) == Token:

            temp_stack.append(i.value)

        else: temp_stack.append(i)

    print(f"equation in RPN notation: {(' ').join(temp_stack)}")

    hist = shunting_yard_evaluator(in_stack)

    x = ('').join(hist)

    hist = x.strip()

    print(f"answer: {hist}")

    return hist



def get_token(value: str):

    for i in TOKENS:

        if i.value == value:

            return i 
        
    return value
        


def shunting_yard_converter(equation):

    in_stack = list(equation)
    op_stack = []
    out_stack = []

    # step 1 is to convert factorials into a bracket function like sin() and cos()
    for index, char, in enumerate(in_stack):

        # look for factorial sign
        if char == '!':

            # set end of function
            in_stack[index] = ')'

            # look for start of number next to factorial sign
            for i in range(index, 0, -1):

                # if a space is found, the number has ended
                if in_stack[i] not in '1234567890.-':

                    # set start of equation
                    in_stack.insert(i - 1, 'f(')

                    break

            # print info
            print(f"original equation: {('').join(equation)}")

            print(f"factorials fixed: {('').join(in_stack)}")


    # fix syntax
    x = ('').join(in_stack)

    in_stack = list(x)



    # loop through list until it is empty
    while in_stack:

        # create temporary list
        temp_stack = []

        try: print(f"char: {in_stack[0]}, char2: {token.value}")
        except: print(f"char: {in_stack[0]}")

        try: 

            if type(token) != str and token.value != ')': token = get_token(in_stack.pop(0))
                
            else: token = get_token(in_stack.pop(0))
        
        except: token = get_token(in_stack.pop(0))



        # remove spaces
        if token == ' ':

            continue



        # check if first character is part of a number
        elif type(token) == str:

            if token in '1234567890.-':

                try:

                    # loop through each character in the stack until a character isn't part of a number
                    while token in '1234567890.-':

                        # add number to temporary list
                        temp_stack.append(token)

                        token = get_token(in_stack.pop(0))

                except:pass

                # add temporary list to out stack
                out_stack.append(('').join(temp_stack))
                print_stacks(in_stack, op_stack, out_stack, print_type = True)
                try: print(f"char: {token.value}, char3: {in_stack[0]}, this")
                except: print(f"char: {token}, this")

                

        try:

            # check if char is a function
            if token.type == FUNCTION:

                # add function to output stack
                op_stack.append(token)
                print_stacks(in_stack, op_stack, out_stack, print_type = True)

            

            # check if there is an operator
            elif token.type == OPERATOR:

                # loop through output stack to ensure order of operations is followed
                while op_stack and op_stack[-1].value != '(' and (
                        op_stack[-1].precedence > token.precedence or 
                        (op_stack[-1].precedence == token.precedence and 
                        token.associativity)):

                    # pop last operator of op stack on to the out stack
                    out_stack.append(op_stack.pop())
                    print_stacks(in_stack, op_stack, out_stack, print_type = True)

                print('operator stack changed')

                # pop char on to op stack
                op_stack.append(token)
                print_stacks(in_stack, op_stack, out_stack, print_type = True)



            # check if char is a left bracket
            elif token.type == LEFT_BRACKET:

                # pop in_stack[0] on to op stack
                op_stack.append(token)



            # check if char is a right bracket
            elif token.type == RIGHT_BRACKET:

                print('right bracket found')

                print_stacks(in_stack, op_stack, out_stack, print_type = True)

                # loop through op stack until a left bracket is found
                while op_stack and op_stack[-1].type != LEFT_BRACKET:

                    # pop op stack to out stack
                    out_stack.append(op_stack.pop())
                    print_stacks(in_stack, op_stack, out_stack, print_type = True)

                print('l bracket removed')

                # remove left bracket
                op_stack.pop()
                print_stacks(in_stack, op_stack, out_stack, print_type = True)

        except: 
            try: print(f"error at char = {token.value}")
            except: print(f"error at char = {token}")

        # time.sleep(5)


        
    # put the op stack on to the out stack
    while op_stack:

        out_stack.append(op_stack.pop())
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

    if not print_type:

        print(f"number 1: {stacks[0]}")
        print(f"number 2: {stacks[1]}")



def shunting_yard_evaluator(equation):

    stack = shunting_yard_converter(equation)

    temp_stack = []

    for i in stack:

        if type(i) == Token:

            temp_stack.append(i.value)

        else: temp_stack.append(i)

    print(f"stack: {temp_stack}")

    hist = []

    while stack:

        i = stack.pop(0)

        try: print(f"char: {i.value}")
        except: print(f"char: {i}")

        # check if first item is an operator
        if type(i) == str:

            # if it isn't, add it to the number stack
            hist.append(i)

        

        # do something else if it is an operator
        else:

            # find what numbers correspond to the operator
            a, b, hist = find_numbers(i.type, hist)

            # solve section of equation
            if i.type: hist.append(str(i.apply(a)))

            else: hist.append(str(i.apply(a, b)))

            temp_stack = []

            for i in stack:

                if type(i) == Token:

                    temp_stack.append(i.value)

                else: temp_stack.append(i)

            print(f"output: {hist}")
            print(f"remaining equation: {temp_stack}")

    return hist




def find_numbers(type, hist):

    # print all numbers
    print(f"all numbers: {hist}")

    if type: return hist.pop(-1), None, hist

    else: return hist.pop(-2), hist.pop(-1), hist
    


if __name__ == '__main__':

    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _  2 ^ (5 _ 2)) / 15'

    '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    '53.06666666666667'

    '4 3 f 52 73 64 # * 2 / + 220 _ * 2 5 2 _ ^ _ 15 / +'
    '4 3 f 52 73 64 # * 2 / + 220 _ * 2 5 2 _ ^ _ 15 / +'

    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    # run parser with inputted equation
    output = shunting_yard_evaluator(equation)

    print(f"output: {('').join(output)}")