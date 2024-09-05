import tkinter as tk
from tkinter import *
import keyboard
import os
from scientific_parser import scientific_parser
from shunting_parser import shunting_yard_evaluator
import Scientific_gui


''' NOTES 
likely bug: when deleting stuff, if an operator is deleted, while the last item in the equation will be a number, that number won't be in the display string, 
which could cause errors with the decimal and exponent buttons.


things to update:

multiplying functions without pressing '*' doesn't work

MAKE SURE THAT YOU CAN'T ADD MULTIPLE OPERATORS IN A ROW!!!

LEARN CLASSES

allow the exponent button to be toggled to allow for complex equations to be superscripted

make shift+backspace work like regular backspace (bug: if an operator is deleted, the number at the end of the equation text won't be in the display text.)

MAKE IT ONLY WORK IF IT IS ON THE TOP LAYER OF THE SCREEN



things this needs to do to integrate the complex parser:

have separate display options for scientific calculator, factoring calculator, quadratic calculator, and trig calculator
have proper inputs for each display option
possibly have separate dict lists for each kind of calculations
allow the display size to change

ideal order of completion:

create button to switch between displays - DONE
create GUIs for different displays
create the necessary button functions
create the necessary variables
create logic for parser
link parser & display
'''

TRIG_FUNCTION_SIN = 0
TRIG_FUNCTION_COS = 1
TRIG_FUNCTION_TAN = 2

L_BRACKET = True
R_BRACKET = False



# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)


class Scientific:

    def __init__(self) -> None:

        self.equation = ['']
        self.bracket_num = 0
        self.exponent = False
        self.output = ''
        self.memory = []
        


# main class to handle all the gui stuff
class Window:

    root = None
    option_choices = None

    def __init__(self, parent) -> None:
        
        self.parent = parent
        self.shift_toggle = False
        self.equation_text = ['']
        self.display_text  = ['', '']
        
    def scientific(self):

        self.parent.title('Calculator')

        self.parent.geometry('700x675')

        self.logic = Scientific()

        self.keybindings()

        # graphical setup
        self.equation = tk.Label(self.parent, text = '')
        self.equation.configure(font=('Arial', 40, ''))
        self.equation.place(x = 0, y = 10)

        self.display = tk.Label(self.parent, text = '0')
        self.display.configure(font=('Arial', 75, 'bold'))
        self.display.place(x = 0, y = 80)

        self.round_label = tk.Label(self.parent, text = 'Round to              decimal points')
        self.round_label.configure(font=('Arial', 15, 'bold'))
        self.round_label.place(x = 370, y = 190)

        # decimal changer
        self.round_choice = StringVar(self.parent)
        self.round_choice.set(11)

        self.round_numbers = OptionMenu(self.parent, self.round_choice, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        self.round_numbers.configure(font=('Arial', 15, 'bold'))
        self.round_numbers.place(x = 470, y = 185)

        # options to switch between calculators
        self.options = OptionMenu(self.parent, self.option_choices, 'Scientific', 'Quadratic', 'Factoring')
        self.options.configure(font=('Arial', 15, 'bold'))
        self.options.place(x = 10, y = 185)



        # create button information
        self.equal          = tk.Button(self.parent, text='=',                  anchor='center', bg='DarkSlateGray2', command=lambda:self.calculate(self.round_choice))

        # column 1
        self.mem_clear      = tk.Button(self.parent, text='MC',                 anchor='center', bg='gainsboro',      command=lambda:self.memory_clear())
        self.pie            = tk.Button(self.parent, text='pi',                 anchor='center', bg='gainsboro',      command=lambda:self.put_pi())
        self.ee             = tk.Button(self.parent, text='e',                  anchor='center', bg='gainsboro',      command=lambda:self.put_e())
        self.log            = tk.Button(self.parent, text='log',                anchor='center', bg='gainsboro',      command=lambda:self.logarithm())
        self.ans            = tk.Button(self.parent, text='Ans',                anchor='center', bg='gainsboro',      command=lambda:self.answer())

        # column 2
        self.mem_add        = tk.Button(self.parent, text='MS',                 anchor='center', bg='gainsboro',      command=lambda:self.memorystore())
        self.shift          = tk.Button(self.parent, text='Inv',                anchor='center', bg='gainsboro',      command=lambda:self.shifte())
        self.sine           = tk.Button(self.parent, text='sin',                anchor='center', bg='gainsboro',      command=lambda:self.trigonometry(TRIG_FUNCTION_SIN))
        self.cosine         = tk.Button(self.parent, text='cos',                anchor='center', bg='gainsboro',      command=lambda:self.trigonometry(TRIG_FUNCTION_COS))
        self.tangent        = tk.Button(self.parent, text='tan',                anchor='center', bg='gainsboro',      command=lambda:self.trigonometry(TRIG_FUNCTION_TAN))

        # column 3
        self.mem_recall     = tk.Button(self.parent, text='MR',                 anchor='center', bg='gainsboro',      command=lambda:self.memoryrecall())
        self.factorial      = tk.Button(self.parent, text='x!',                 anchor='center', bg='gainsboro',      command=lambda:self.put_factorials())
        self.exponent       = tk.Button(self.parent, text='x' + get_super('y'), anchor='center', bg='gainsboro',      command=lambda:self.put_exponential())
        self.squared        = tk.Button(self.parent, text='x' + get_super('2'), anchor='center', bg='gainsboro',      command=lambda:self.put_exponential(2))
        self.sqrt           = tk.Button(self.parent, text='sqrt',               anchor='center', bg='gainsboro',      command=lambda:self.put_square_root())

        # column 4
        self.open_b         = tk.Button(self.parent, text='(',                  anchor='center', bg='gainsboro',      command=lambda:self.put_brackets(L_BRACKET))
        self.num7           = tk.Button(self.parent, text='7',                  anchor='center', bg='white',          command=lambda:self.put_number(7))
        self.num4           = tk.Button(self.parent, text='4',                  anchor='center', bg='white',          command=lambda:self.put_number(4))
        self.num1           = tk.Button(self.parent, text='1',                  anchor='center', bg='white',          command=lambda:self.put_number(1))
        self.integer        = tk.Button(self.parent, text='+/-',                anchor='center', bg='white',          command=lambda:self.negative())
        
        # column 5
        self.close_b        = tk.Button(self.parent, text=')',                  anchor='center', bg='gainsboro',      command=lambda:self.put_brackets(R_BRACKET))
        self.num8           = tk.Button(self.parent, text='8',                  anchor='center', bg='white',          command=lambda:self.put_number(8))
        self.num5           = tk.Button(self.parent, text='5',                  anchor='center', bg='white',          command=lambda:self.put_number(5))
        self.num2           = tk.Button(self.parent, text='2',                  anchor='center', bg='white',          command=lambda:self.put_number(2))
        self.num0           = tk.Button(self.parent, text='0',                  anchor='center', bg='white',          command=lambda:self.put_number(0))
        
        # column 6
        self.modulus        = tk.Button(self.parent, text='%',                  anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' % '))
        self.num9           = tk.Button(self.parent, text='9',                  anchor='center', bg='white',          command=lambda:self.put_number(9))
        self.num6           = tk.Button(self.parent, text='6',                  anchor='center', bg='white',          command=lambda:self.put_number(6))
        self.num3           = tk.Button(self.parent, text='3',                  anchor='center', bg='white',          command=lambda:self.put_number(3))
        self.decimal        = tk.Button(self.parent, text='.',                  anchor='center', bg='white',          command=lambda:self.put_decimal())

        # column 7
        self.clear_data     = tk.Button(self.parent, text='CE',                 anchor='center', bg='lightcoral',     command=lambda:self.clear())
        self.divide         = tk.Button(self.parent, text='/',                  anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' / '))
        self.multiply       = tk.Button(self.parent, text='x',                  anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' * '))
        self.minus          = tk.Button(self.parent, text='-',                  anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' _ '))
        self.plus           = tk.Button(self.parent, text='+',                  anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' + '))



        # create button fonts
        self.equal.         configure(font=('Arial', 25, 'bold'))
        
        # column 1
        self.mem_clear.     configure(font=('Arial', 25, 'bold'))
        self.pie.           configure(font=('Arial', 25, 'bold'))
        self.ee.            configure(font=('Arial', 25, 'bold'))
        self.log.           configure(font=('Arial', 25, 'bold'))
        self.ans.           configure(font=('Arial', 25, 'bold'))
        
        # column 2
        self.mem_add.       configure(font=('Arial', 25, 'bold'))
        self.shift.         configure(font=('Arial', 25, 'bold'))
        self.sine.          configure(font=('Arial', 25, 'bold'))
        self.cosine.        configure(font=('Arial', 25, 'bold'))
        self.tangent.       configure(font=('Arial', 25, 'bold'))

        # column 3
        self.mem_recall.    configure(font=('Arial', 25, 'bold'))
        self.factorial.     configure(font=('Arial', 25, 'bold'))
        self.exponent.      configure(font=('Arial', 25, 'bold'))
        self.squared.       configure(font=('Arial', 25, 'bold'))
        self.sqrt.          configure(font=('Arial', 25, 'bold'))

        # column 4
        self.open_b.        configure(font=('Arial', 25, 'bold'))
        self.num7.          configure(font=('Arial', 25, 'bold'))
        self.num4.          configure(font=('Arial', 25, 'bold'))
        self.num1.          configure(font=('Arial', 25, 'bold'))
        self.integer.       configure(font=('Arial', 25, 'bold'))
        
        # column 5
        self.close_b.       configure(font=('Arial', 25, 'bold'))
        self.num8.          configure(font=('Arial', 25, 'bold'))
        self.num5.          configure(font=('Arial', 25, 'bold'))
        self.num2.          configure(font=('Arial', 25, 'bold'))
        self.num0.          configure(font=('Arial', 25, 'bold'))
        
        # column 6
        self.modulus.       configure(font=('Arial', 25, 'bold'))
        self.num9.          configure(font=('Arial', 25, 'bold'))
        self.num6.          configure(font=('Arial', 25, 'bold'))
        self.num3.          configure(font=('Arial', 25, 'bold'))
        self.decimal.       configure(font=('Arial', 25, 'bold'))

        # column 7
        self.clear_data.    configure(font=('Arial', 25, 'bold'))
        self.divide.        configure(font=('Arial', 25, 'bold'))
        self.multiply.      configure(font=('Arial', 25, 'bold'))
        self.minus.         configure(font=('Arial', 25, 'bold'))
        self.plus.          configure(font=('Arial', 25, 'bold'))



        # place buttons
        self.equal.         place(x = 0,   y = 600, width = 700, height = 75)
        
        # column 1
        self.mem_clear.     place(x = 0,   y = 225, width = 100, height = 75)
        self.pie.           place(x = 0,   y = 300, width = 100, height = 75)
        self.ee.            place(x = 0,   y = 375, width = 100, height = 75)
        self.log.           place(x = 0,   y = 450, width = 100, height = 75)
        self.ans.           place(x = 0,   y = 525, width = 100, height = 75)
        
        # column 2
        self.mem_add.       place(x = 100, y = 225, width = 100, height = 75)
        self.shift.         place(x = 100, y = 300, width = 100, height = 75)
        self.sine.          place(x = 100, y = 375, width = 100, height = 75)
        self.cosine.        place(x = 100, y = 450, width = 100, height = 75)
        self.tangent.       place(x = 100, y = 525, width = 100, height = 75)
        
        # column 3
        self.mem_recall.    place(x = 200, y = 225, width = 100, height = 75)
        self.factorial.     place(x = 200, y = 300, width = 100, height = 75)
        self.exponent.      place(x = 200, y = 375, width = 100, height = 75)
        self.squared.       place(x = 200, y = 450, width = 100, height = 75)
        self.sqrt.          place(x = 200, y = 525, width = 100, height = 75)

        # column 4
        self.open_b.        place(x = 300, y = 225, width = 100, height = 75)
        self.num7.          place(x = 300, y = 300, width = 100, height = 75)
        self.num4.          place(x = 300, y = 375, width = 100, height = 75)
        self.num1.          place(x = 300, y = 450, width = 100, height = 75)
        self.integer.       place(x = 300, y = 525, width = 100, height = 75)
        
        # column 5
        self.close_b.       place(x = 400, y = 225, width = 100, height = 75)
        self.num8.          place(x = 400, y = 300, width = 100, height = 75)
        self.num5.          place(x = 400, y = 375, width = 100, height = 75)
        self.num2.          place(x = 400, y = 450, width = 100, height = 75)
        self.num0.          place(x = 400, y = 525, width = 100, height = 75)
        
        # column 6
        self.modulus.       place(x = 500, y = 225, width = 100, height = 75)
        self.num9.          place(x = 500, y = 300, width = 100, height = 75)
        self.num6.          place(x = 500, y = 375, width = 100, height = 75)
        self.num3.          place(x = 500, y = 450, width = 100, height = 75)
        self.decimal.       place(x = 500, y = 525, width = 100, height = 75)

        # column 7
        self.clear_data.    place(x = 600, y = 225, width = 100, height = 75)
        self.divide.        place(x = 600, y = 300, width = 100, height = 75)
        self.multiply.      place(x = 600, y = 375, width = 100, height = 75)
        self.minus.         place(x = 600, y = 450, width = 100, height = 75)
        self.plus.          place(x = 600, y = 525, width = 100, height = 75)

        # prevent the calculator from being resized
        self.parent.resizable(False, False)


    
    # function bound to the invert button to allow inverse functions to be used.
    def shifte(self):

        # flip the variable whenever the button is pressed
        self.shift_toggle = not self.shift_toggle

        # change the button text to inverted functions
        if self.shift_toggle:

            self.sine.   configure(text='sin' + get_super('-1'))
            self.cosine. configure(text='cos' + get_super('-1'))
            self.tangent.configure(text='tan' + get_super('-1'))

            self.sine.   place(x = 100, y = 375, width = 100, height = 75)
            self.cosine. place(x = 100, y = 450, width = 100, height = 75)
            self.tangent.place(x = 100, y = 525, width = 100, height = 75)



        # change the button text to normal functions
        else:

            self.sine.   configure(text='sin')
            self.cosine. configure(text='cos')
            self.tangent.configure(text='tan')

            self.sine.   place(x = 100, y = 375, width = 100, height = 75)
            self.cosine. place(x = 100, y = 450, width = 100, height = 75)
            self.tangent.place(x = 100, y = 525, width = 100, height = 75)



    def update_text(self, type = 0, string = None, index = None, update = 0):

        if string is None:

            string = ['', '', '']

        if index is None:

            index = [len(self.logic.equation), len(self.equation_text), len(self.display_text)]

            d = self.logic.bracket_num
        
        else: d = 0


        # simplify variables
        a = self.logic.equation
        b = self.equation_text
        c = self.display_text
        e = self.logic.exponent

        if type == 0:

            # edit main equation variables
            self.logic.equation = list(('').join(a[0:index[0] - d]) + string[0] + ('').join(a[index[0] - d:len(a)]))

            try:

                if e: self.equation_text = get_super(list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)])))

                else: self.equation_text = list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)]))

            except:pass

            self.display_text = list(string[2])

            self.display_text.append('')


        
        elif type == 1:

            # edit main equation variables
            self.logic.equation = list(('').join(a[0:index[0] - d]) + string[0] + ('').join(a[index[0] - d:len(a)]))

            try:

                if e: self.equation_text = get_super(list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)])))

                else: self.equation_text = list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)]))

            except:pass

            self.display_text = list(('').join(c[0:index[2]]) + string[2] + ('').join(c[index[2]:len(c)]))



        if update == 0:

            # update display
            self.display.configure(text = ('').join(self.display_text))

            self.equation.configure(text = ('').join(self.equation_text))



        elif update == 1:

            # update display
            self.display.configure(text = '0')

            self.equation.configure(text = ('').join(self.equation_text))

        

        elif update == 2:

            self.display.configure(text = string[0])

            self.equation.configure(text = string[1])
            
        else:pass



    # function bound to the clear equation button that clears the variables and display.
    def clear(self, type = True):

        if type:

            # reset variables
            self.logic.equation = ['']

            self.equation_text = ['']

            self.display_text = ['', '']

            self.logic.bracket_num = 0



            # update display
            self.display.configure(text = '0')

            self.equation.configure(text = '')



        else:

            # check if there is anything in the display text variable
            if self.equation_text[-1] in '1234567890.-':

                # delete last digit in each variable
                self.logic.equation.pop()

                self.equation_text.pop()

                # only delete from the display text if there is stuff to delete
                if len(self.display_text) != 0:

                    self.display_text.pop()

                # update display
                self.update_text(type=2)



            # check if there is an operator in the right-most position in the equation
            elif self.equation_text[-1] == ' ':

                # delete last operator
                self.logic.equation = self.logic.equation[0:-3]

                self.equation_text = self.equation_text[0:-3]

                # update display
                self.update_text(type=2)

        # check if the last thing entered in was an operator
        # check if the last thing is a bracket, if it is, go inside the bracket instead of deleting it
            # figure out how to show this



    # a function to handle all key inputs
    def keybindings(self):

        keyboard.add_hotkey('shift+=',   lambda:self.handle_operator(' + '))
        keyboard.add_hotkey('shift+8',   lambda:self.handle_operator(' * '))
        keyboard.add_hotkey('shift+5',   lambda:self.handle_operator(' % '))
        keyboard.add_hotkey('ctrl+0',    lambda:self.put_exponential(0))
        keyboard.add_hotkey('ctrl+1',    lambda:self.put_exponential(1))
        keyboard.add_hotkey('ctrl+2',    lambda:self.put_exponential(2))
        keyboard.add_hotkey('ctrl+3',    lambda:self.put_exponential(3))
        keyboard.add_hotkey('ctrl+4',    lambda:self.put_exponential(4))
        keyboard.add_hotkey('ctrl+5',    lambda:self.put_exponential(5))
        keyboard.add_hotkey('ctrl+6',    lambda:self.put_exponential(6))
        keyboard.add_hotkey('ctrl+7',    lambda:self.put_exponential(7))
        keyboard.add_hotkey('ctrl+8',    lambda:self.put_exponential(8))
        keyboard.add_hotkey('ctrl+9',    lambda:self.put_exponential(9))
        keyboard.add_hotkey('shift+0',   lambda:self.put_brackets(R_BRACKET))
        keyboard.add_hotkey('shift+1',   lambda:self.put_factorials())
        keyboard.add_hotkey('shift+6',   lambda:self.put_exponential())
        keyboard.add_hotkey('shift+3',   lambda:self.put_square_root())
        keyboard.add_hotkey('shift+9',   lambda:self.put_brackets(L_BRACKET))
        keyboard.add_hotkey('ctrl+s',    lambda:self.trigonometry(TRIG_FUNCTION_SIN))
        keyboard.add_hotkey('ctrl+c',    lambda:self.trigonometry(TRIG_FUNCTION_COS))
        keyboard.add_hotkey('ctrl+t',    lambda:self.trigonometry(TRIG_FUNCTION_TAN))
        keyboard.add_hotkey('ctrl+a',    lambda:self.answer())
        keyboard.add_hotkey('ctrl+e',    lambda:self.put_e())
        keyboard.add_hotkey('ctrl+l',    lambda:self.logarithm())
        keyboard.add_hotkey('ctrl+p',    lambda:self.put_pi())
        keyboard.add_hotkey('shift+-',   lambda:self.negative())
        keyboard.add_hotkey('shift+m',   lambda:self.memorystore())
        keyboard.add_hotkey('ctrl+m',    lambda:self.memory_clear())
        keyboard.add_hotkey('shift+backspace', lambda:self.clear(False))
        keyboard.add_hotkey('enter',     lambda:self.calculate())
        keyboard.add_hotkey('m',         lambda:self.memoryrecall())
        keyboard.add_hotkey('-',         lambda:self.handle_operator(' _ '))
        keyboard.add_hotkey('/',         lambda:self.handle_operator(' / '))
        keyboard.add_hotkey('.',         lambda:self.put_decimal())
        keyboard.add_hotkey('0',         lambda:self.put_number(0))
        keyboard.add_hotkey('1',         lambda:self.put_number(1))
        keyboard.add_hotkey('2',         lambda:self.put_number(2))
        keyboard.add_hotkey('3',         lambda:self.put_number(3))
        keyboard.add_hotkey('4',         lambda:self.put_number(4))
        keyboard.add_hotkey('5',         lambda:self.put_number(5))
        keyboard.add_hotkey('6',         lambda:self.put_number(6))
        keyboard.add_hotkey('7',         lambda:self.put_number(7))
        keyboard.add_hotkey('8',         lambda:self.put_number(8))
        keyboard.add_hotkey('9',         lambda:self.put_number(9))
        keyboard.add_hotkey('backspace', lambda:self.clear())


    # the function bound to the 'equals' button to output a result for an equation.
    def calculate(self, roundchoice):

        # assemble equation list into a string
        equation_str = ('').join(self.logic.equation)

        # give the equation parser the equation string and set the output to a variable
        answer = shunting_yard_evaluator(equation_str)

        if not answer:

            print("Could not calculate answer")
            
            return
        
        print(answer)

        # round the output to the specified number of decimal places
        self.logic.output = str(round(float(answer), int(roundchoice.get())))



        # edit display strings
        self.equation_text += ' = ' + self.logic.output

        self.display_text = self.logic.output

        self.logic.bracket_num = 0



        # update display
        self.update_text(type=2)



        # reset variables
        self.equation_text = self.logic.output

        self.logic.equation = self.logic.output


    # the function bound to the addition button to tell the calculate function which mathematical operation to perform when it is pressed.
    def handle_operator(self, operation = None):

        try:

            if self.equation_text[-2 - self.logic.bracket_num] not in 'sctSCTlf^#/*%+_':

                if operation == ' _ ': 
                    
                    self.update_text(string=[operation, ' - ', ''], update=1)

                

                else:

                    # add addition sign to equation and display strings
                    self.update_text(string=[operation, operation, ''], update=1)

        except: # ask ryan which format looks better

            if operation == ' _ ':

                self.update_text(string=[operation, ' - ', ''], update=1)

            

            else:

                # add addition sign to equation and display strings
                self.update_text(string=[operation, operation, ''], update=1)



    # function bound to the decimal button to allow decimal numbers to be inputted.
    def put_decimal(self):

        if self.display_text == '':

            # put the decimal in the equation and display strings
            self.update_text(type=1, string=['0.', '0.', '0.'])



        elif '.' not in self.display_text:

            # put the decimal in the equation and display strings
            self.update_text(type=1, string=['.', '.', '.'])





    # function bound to the integer button to allow the user to toggle a number between positive and negative.
    def negative(self):
        
        try:

            # check to see if there is anything in the display text
            if self.display_text == ['']:

                # add the integer sign to the number if there is nothing else in the equation
                self.update_text(string=['-', '-', '-'])

            

            # find where display text is within the equation text
            index = ('').join(self.equation_text).rfind(('').join(self.display_text))



            if  '-' not in self.display_text:

                if self.equation_text[index] != '-':

                    # put an integer sign on the number if it doesn't have one
                    self.update_text(type=1, string=['-', '-', '-'], index=[index, index, 0]) 



            else:

                # remove the integer sign from the number
                self.logic.equation.pop(index)

                self.equation_text.pop(index)

                self.display_text.pop(0)

                self.update_text(type=2)



        except:

            # add the integer sign to the number if there is nothing else in the equation
            self.update_text(type=1, string=['-', '-', '-'])

    

    # function to input numbers.
    def put_number(self, x):

        # put the number in the equation and display strings
        self.update_text(type=1, string=[str(x), str(x), str(x)])



    # function bound to the exponent button that allows for exponents to be used.
    def put_exponential(self, ctrlexp = -1):

        # check if a keybinding was used
        if ctrlexp != -1:

            # put the exponent sign and exponent number in the equation and display strings
            self.update_text(string=[' ^ ' + str(ctrlexp), get_super('(' + str(ctrlexp) + ')'), ''], update=1)

            # increase bracket number counter
            self.logic.bracket_num += 1

        

        else:

            self.logic.exponent = not self.logic.exponent

            # update display
            self.update_text(string=['0', ('').join(self.equation_text) + get_super('(y)')], update=2)



            # put exponent sign in equation
            self.update_text(string=[' ^ ()', get_super('()'), ''], update=3)

            # increase bracket number counter
            self.logic.bracket_num += 1



    # function bound to the sqrt button that adds square root
    def put_square_root(self):

        # add the sqrt function indicator to the equation and display strings
        self.update_text(string=['#()', 'sqrt()', ''], update=1)

        # allow for more brackets
        self.logic.bracket_num += 1



    # function bound to the factorial button to allow for factorials to be used.
    def put_factorials(self):

        # put the factorial sign in the equation and display strings
        self.update_text(string=['!', '!', ''], update=1)



    # function bound to the memory recall button to display the number stored in memory.
    def memoryrecall(self):

        # add the number stored in memory to the equation and display strings
        self.update_text(string=[self.logic.memory, self.logic.memory, self.logic.memory])



    # function bound to the memory clear button that will clear the number stored in the memory.
    def memory_clear(self):

        # clear the memory variable
        self.logic.memory = []



    # function bound to the memory add button to set the memory number to the number displayed.
    def memorystore(self):

        print(f"memory: {('').join(self.display_text)}")

        # assign a number to the memory variable
        self.logic.memory = self.display_text



    # function bound to the brackets button to add them to the display.
    def put_brackets(self, type):

        if type:

            # allow for bracket multiplication without pressing the multiplication button
            if self.logic.equation[-1] in '1234567890)':

                for i in list(' * '): self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)



            # add an open bracket to the equation and display strings
            self.update_text(string=['()', '()', ''], update=1)



            # keep track of brackets
            self.logic.bracket_num += 1



        else:

            if self.equation_text[-1 - self.logic.bracket_num] in '1234567890.-)':

                # start typing outside one more layer of brackets
                if self.logic.bracket_num > 0:

                    self.logic.bracket_num -= 1

                    # display numbers within brackets
                    self.update_text(type=2, update=1)



    # function bound to the trigonometry buttons to allow them to be used.
    def trigonometry(self, trig_function = 0):

        # allow for bracket multiplication without pressing the multiplication button
        if self.logic.equation[-1] in '1234567890)':

            for i in list(' * '): self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)

        # add an alternate function for inverse trigonometry functions
        if self.shift_toggle:

            if trig_function == TRIG_FUNCTION_SIN:

                # add the inverse sine indicator to the equation and display strings
                self.update_text(string=['S()', 'sin' + get_super('-1') + '()', ''], update=1)



            elif trig_function == TRIG_FUNCTION_COS:
                
                # add the inverse cosine indicator to the equation and display strings
                self.update_text(string=['C()', 'cos' + get_super('-1') + '()', ''], update=1)



            elif trig_function == TRIG_FUNCTION_TAN:
                
                # add the inverse tangent indicator to the equation and display strings
                self.update_text(string=['T()', 'tan' + get_super('-1') + '()', ''], update=1)

            return



        if trig_function == TRIG_FUNCTION_SIN:

            # add the sine indicator to the equation and display strings
            self.update_text(string=['s()', 'sin()', ''], update=1)



        elif trig_function == TRIG_FUNCTION_COS:
            
            # add the cosine indicator to the equation and display strings
            self.update_text(string=['c()', 'cos()', ''], update=1)



        elif trig_function == TRIG_FUNCTION_TAN:
            
            # add the tangent indicator to the equation and display strings
            self.update_text(string=['t()', 'tan()', ''], update=1)

        # allow for more brackets
        self.logic.bracket_num += 1



    # function bound to the pi button to allow for the pi number to be accessed easily.
    def put_pi(self):

        # add the pi number to the equation and display strings
        self.update_text(string=['3.14159265359', 'pi', '3.14159265359'])



    # function bound to the e button to allow for eulers number to be accessed easily.
    def put_e(self):

        # add eulers number to the equation and display strings
        self.update_text(string=['2.71828182846', 'e', '2.71828182846'])



    # function bound to the log button to allow for logarithms to be used.
    def logarithm(self):

        # allow for bracket multiplication without pressing the multiplication button
        if self.logic.equation[-1] in '1234567890)':

            for i in list(' * '): self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)

        # add the log function indicator to the equation and display strings
        self.update_text(string=['l()', 'log()', ''], update=1)

        # allow for more brackets
        self.logic.bracket_num += 1



    # function bound to the answer button to allow for the previous answer to be used.
    def answer(self):

        # add the previous answer to the equation and display strings
        self.update_text(string=[self.logic.output, self.logic.output, self.logic.output])




# Factoring calculator display configuration
def Factoring():



    # type in equations or use buttons?

    # things needed to type in equations:
        # something to understand syntax that can change
        # something to understand different variable names
        # something to understand polynomials of very different lengths


    
    # things needed to use buttons:
        # a way to enter in all letters as variables




    # have an input where a polynomial of any size can be factored
    # have an output that says what type of polynomial was inputted
    # have an output that says what the factored form of the polynomial is

    pass



# Quadratic calculator display configuration
def Quadratic():

    pass



# Trigonometric calculator display configuration
def Trigonometry():

    pass


# function to detect optionmenu changes
def options_callback(var, index, mode):

    print(f"current type: {Window.option_choices.get()}")

    if Window.option_choices.get() == 'Scientific':

        Window.root.scientific()


def main():

    Window.root = Window(tk.Tk())

    # override windows scaling
    if os.name == 'nt':
        try:
            import ctypes
            
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
            success   = ctypes.windll.user32.SetProcessDPIAware()
        except:pass 

    Window.option_choices = StringVar(Window.root.parent)
    Window.option_choices.trace('w', options_callback)
    Window.option_choices.set('Scientific')

    # run the gui
    Window.root.parent.mainloop()

    

if __name__ == '__main__':

    main()