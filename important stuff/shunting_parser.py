import math



''' NOTES

maybe instead of using lambda for the 'apply' attribute, use a function like the c++ version of this.

'''


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

    def __init__(self, type: int, precedence: int, associativity: bool, value) -> None:
        
        self.type  = type
        self.precedence = precedence
        self.associativity = associativity
        self.value = value

    def math(self, is_radians, x, y = 0):

        if is_radians:
            if self.value == 's':  return math.sin(float(x))
            if self.value == 'c':  return math.cos(float(x))
            if self.value == 't':  return math.tan(float(x))
            if self.value == 'S': return math.asin(float(x))
            if self.value == 'C': return math.acos(float(x))
            if self.value == 'T': return math.atan(float(x))

        else: 
            if self.value == 's':  return math.sin(math.radians(float(x)))
            if self.value == 'c':  return math.cos(math.radians(float(x)))
            if self.value == 't':  return math.tan(math.radians(float(x)))
            if self.value == 'S': return math.degrees(math.asin(float(x)))
            if self.value == 'C': return math.degrees(math.acos(float(x)))
            if self.value == 'T': return math.degrees(math.atan(float(x)))

        if self.value == 'l': return math.log(float(x))
        if self.value == 'f': return math.factorial(int(x))
        if self.value == '#': return float(x) ** 0.5

        if self.value == '^': return float(x) ** float(y)
        if self.value == '%': return float(x) % float(y)
        if self.value == '/': return float(x) / float(y)
        if self.value == '*': return float(x) * float(y)
        if self.value == '+': return float(x) + float(y)
        if self.value == '_': return float(x) - float(y)

        



TOKENS = [

    Token(FUNCTION, 5, LEFT,  value='s'),
    Token(FUNCTION, 5, LEFT,  value='c'),
    Token(FUNCTION, 5, LEFT,  value='t'),
    Token(FUNCTION, 5, LEFT,  value='S'),
    Token(FUNCTION, 5, LEFT,  value='C'),
    Token(FUNCTION, 5, LEFT,  value='T'),
    Token(FUNCTION, 5, LEFT,  value='l'),
    Token(FUNCTION, 4, LEFT,  value='f'),
    Token(FUNCTION, 2, LEFT,  value='#'),
    
    Token(OPERATOR, 3, RIGHT, value='^'),
    Token(OPERATOR, 1, LEFT,  value='%'),
    Token(OPERATOR, 1, LEFT,  value='/'),
    Token(OPERATOR, 1, LEFT,  value='*'),
    Token(OPERATOR, 0, LEFT,  value='+'),
    Token(OPERATOR, 0, LEFT,  value='_'),

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

            if type(token) != str and token.value != ')': token = get_token(in_stack.pop(0))
                
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
                        op_stack[-1].precedence > token.precedence or (
                        op_stack[-1].precedence == token.precedence and 
                        token.associativity)):

                    out_stack.append(op_stack.pop())

                op_stack.append(token)



            elif token.type == LEFT_BRACKET:

                op_stack.append(token)



            elif token.type == RIGHT_BRACKET:

                while op_stack and op_stack[-1].type != LEFT_BRACKET:

                    out_stack.append(op_stack.pop())

                op_stack.pop()

        except:pass


        
    while op_stack:

        out_stack.append(op_stack.pop())

    for index in out_stack:
        print(index)

    return out_stack



def shunting_yard_evaluator(equation, is_radians):

    stack = shunting_yard_converter(equation)

    hist = []

    while stack:

        i = stack.pop(0)

        if type(i) == str:

            hist.append(i)

        else:

            a, b, hist = find_numbers(i.type, hist)

            hist.append(str(i.math(is_radians, a, b)))

    x = ('').join(hist)

    hist = x.strip()

    return hist



def find_numbers(type, hist):

    if type: return hist.pop(-1), None, hist

    else: return hist.pop(-2), hist.pop(-1), hist
    


if __name__ == '__main__':

    equation = '4 + (3! * (52 + 73 * #(64) / 2 _ 220) _ 2 ^ (5 _ 2)) / 15'

    # equation = 's(s(60))'

    is_radians = False

    output = shunting_yard_evaluator(equation, is_radians)

    print(f"output: {('').join(output)}") 