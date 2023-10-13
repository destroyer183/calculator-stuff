import math



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

    
    def solve(self, a, b):

        if self.type: return self.apply(a)

        else: return self.apply(a, b)



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



def get_token(value: str):

    for i in TOKENS:

        if i.value == value:

            return i 
        
    return value
        


def shunting_yard_converter(equation):

    in_stack = list(equation)
    op_stack = []
    out_stack = []

    for index, char, in enumerate(in_stack):

        if char == '!':

            in_stack[index] = ')'

            for i in range(index, 0, -1):

                if in_stack[i] not in '1234567890.-':

                    in_stack.insert(i - 1, 'f(')

                    break


    x = ('').join(in_stack)
    in_stack = list(x)


    while in_stack:

        temp_stack = []

        try: 

            if type(token) != str:

                if token.value != ')':

                    token = get_token(in_stack.pop(0))
                
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

            if token.type == FUNCTION:

                op_stack.append(token)

            

            elif token.type == OPERATOR:

                while op_stack and op_stack[-1].value != '(' and (
                        op_stack[-1].precedence > token.precedence or 
                        (op_stack[-1].precedence == token.precedence and 
                        token.associativity)):

                    out_stack.append(op_stack.pop())

                op_stack.append(token)



            elif token.type == LEFT_BRACKET:

                op_stack.append(token)



            elif token.type == RIGHT_BRACKET:

                token = get_token(in_stack.pop(0))

                while op_stack and op_stack[-1].type != LEFT_BRACKET:

                    out_stack.append(op_stack.pop())

                op_stack.pop()

        except:pass


        
    while op_stack:

        out_stack.append(op_stack.pop())

    return out_stack



def shunting_yard_evaluator(equation):

    stack = shunting_yard_converter(equation)

    hist = []

    while stack:

        i = stack.pop(0)

        if type(i) == str:

            hist.append(i)

        else:

            a, b, hist = find_numbers(i.type, hist)

            if i.type: hist.append(str(i.apply(a)))

            else: hist.append(str(i.apply(a, b)))

    x = ('').join(hist)

    hist = x.strip()

    return hist



def find_numbers(type, hist):

    if type: return hist.pop(-1), None, hist

    else: return hist.pop(-2), hist.pop(-1), hist
    


if __name__ == '__main__':

    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _  2 ^ (5 _ 2)) / 15'

    shunting_yard_evaluator(equation)