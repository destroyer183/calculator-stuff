import tkinter as tk
from tkinter import *
# import keyboard
import os
# from scientific_parser import scientific_parser
from shunting_parser import shunting_yard_evaluator


TRIG_FUNCTION_SIN = 0
TRIG_FUNCTION_COS = 1
TRIG_FUNCTION_TAN = 2

# likely bug: when deleting stuff, if an operator is deleted, while the last item in the equation will be a number, that number won't be in the display string, 
# which could cause errors with the decimal and exponent buttons.


# things to update:

# multiplying functions without pressing '*' doesn't work

# MAKE SURE THAT YOU CAN'T ADD MULTIPLE OPERATORS IN A ROW!!!

# LEARN CLASSES

# allow the exponent button to be toggled to allow for complex equations to be superscripted

# make shift+backspace work like regular backspace (bug: if an operator is deleted, the number at the end of the equation text won't be in the display text.)

# MAKE IT ONLY WORK IF IT IS ON THE TOP LAYER OF THE SCREEN



# things this needs to do to integrate the complex parser:

# have separate display options for scientific calculator, factoring calculator, quadratic calculator, and trig calculator
# have proper inputs for each display option
# possibly have separate dict lists for each kind of calculations
# allow the display size to change

# ideal order of completion:

# create button to switch between displays - DONE
# create GUIs for different displays
# create the necessary button functions
# create the necessary variables
# create logic for parser
# link parser & display




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
        
    # create a 'Scientific' object so that the functions can be used, or change what type of functions it contains.

    # the function bound to the 'equals' button to output a result for an equation.


# a function to handle all key inputs
def keybindings(logic):

    pass
    # keyboard.add_hotkey('shift+=',   lambda:logic.meth(' + '))
    # keyboard.add_hotkey('shift+8',   lambda:logic.meth(' * '))
    # keyboard.add_hotkey('shift+5',   lambda:logic.meth(' % '))
    # keyboard.add_hotkey('ctrl+0',    lambda:logic.exponential(0))
    # keyboard.add_hotkey('ctrl+1',    lambda:logic.exponential(1))
    # keyboard.add_hotkey('ctrl+2',    lambda:logic.exponential(2))
    # keyboard.add_hotkey('ctrl+3',    lambda:logic.exponential(3))
    # keyboard.add_hotkey('ctrl+4',    lambda:logic.exponential(4))
    # keyboard.add_hotkey('ctrl+5',    lambda:logic.exponential(5))
    # keyboard.add_hotkey('ctrl+6',    lambda:logic.exponential(6))
    # keyboard.add_hotkey('ctrl+7',    lambda:logic.exponential(7))
    # keyboard.add_hotkey('ctrl+8',    lambda:logic.exponential(8))
    # keyboard.add_hotkey('ctrl+9',    lambda:logic.exponential(9))
    # keyboard.add_hotkey('shift+0',   lambda:logic.brackets(False))
    # keyboard.add_hotkey('shift+1',   lambda:logic.factorials())
    # keyboard.add_hotkey('shift+6',   lambda:logic.exponential())
    # keyboard.add_hotkey('shift+3',   lambda:logic.square_root())
    # keyboard.add_hotkey('shift+9',   lambda:logic.brackets(True))
    # keyboard.add_hotkey('ctrl+s',    lambda:logic.trigonometry(True))
    # keyboard.add_hotkey('ctrl+c',    lambda:logic.trigonometry(False))
    # keyboard.add_hotkey('ctrl+t',    lambda:logic.trigonometry())
    # keyboard.add_hotkey('ctrl+a',    lambda:logic.answer())
    # keyboard.add_hotkey('ctrl+e',    lambda:logic.e())
    # keyboard.add_hotkey('ctrl+l',    lambda:logic.logarithm())
    # keyboard.add_hotkey('ctrl+p',    lambda:logic.pi())
    # keyboard.add_hotkey('shift+-',   lambda:logic.negative())
    # keyboard.add_hotkey('shift+m',   lambda:logic.memorystore())
    # keyboard.add_hotkey('ctrl+m',    lambda:logic.memoryclear())
    # keyboard.add_hotkey('shift+backspace', lambda:logic.clear(False))
    # keyboard.add_hotkey('enter',     lambda:logic.calculate())
    # keyboard.add_hotkey('m',         lambda:logic.memoryrecall())
    # keyboard.add_hotkey('-',         lambda:logic.meth(' _ '))
    # keyboard.add_hotkey('/',         lambda:logic.meth(' / '))
    # keyboard.add_hotkey('.',         lambda:logic.assign_decimal())
    # keyboard.add_hotkey('0',         lambda:logic.assign(0))
    # keyboard.add_hotkey('1',         lambda:logic.assign(1))
    # keyboard.add_hotkey('2',         lambda:logic.assign(2))
    # keyboard.add_hotkey('3',         lambda:logic.assign(3))
    # keyboard.add_hotkey('4',         lambda:logic.assign(4))
    # keyboard.add_hotkey('5',         lambda:logic.assign(5))
    # keyboard.add_hotkey('6',         lambda:logic.assign(6))
    # keyboard.add_hotkey('7',         lambda:logic.assign(7))
    # keyboard.add_hotkey('8',         lambda:logic.assign(8))
    # keyboard.add_hotkey('9',         lambda:logic.assign(9))
    # keyboard.add_hotkey('backspace', lambda:logic.clear())






        # check if the last thing entered in was an operator
        # check if the last thing is a bracket, if it is, go inside the bracket instead of deleting it
            # figure out how to show this



# main class to handle all the gui stuff
class Window:


    def __init__(self, parent) -> None:
        
        self.parent = parent
        self.option_choices = None
        self.shift_toggle = False
        self.root = None
        self.equation_text = ['']
        self.display_text  = ['', '']

    
    def calculate(self, roundchoice):

        equation_str = ('').join(self.logic.equation)

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

        self.bracket_num = 0

        self.update_text(type=2)

        self.equation_text = self.logic.output

        self.logic.equation = self.logic.output


    def put_number(self, x: int):

        self.update_text(type=1, string=[str(x), str(x), str(x)])
        
    def put_pi(self):

        self.update_text(string=['3.14159265359', 'pi', '3.14159265359'])

    def put_e(self):

        self.update_text(string=['2.71828182846', 'e', '2.71828182846'])

    def put_logarithm(self):

        self.update_text(string=['l()', 'log()', ''], update=1)

        self.logic.bracket_num += 1

    def put_trigonometry(self, trig_function: int):

        self.logic.bracket_num += 1

        if self.shift_toggle:

            if trig_function == TRIG_FUNCTION_SIN:

                self.update_text(string=['S()', 'sin' + get_super('-1') + '()', ''], update=1)

            elif trig_function == TRIG_FUNCTION_COS:
                
                self.update_text(string=['C()', 'cos' + get_super('-1') + '()', ''], update=1)

            elif trig_function == TRIG_FUNCTION_TAN:
                
                self.update_text(string=['T()', 'tan' + get_super('-1') + '()', ''], update=1)
                
            return


        if trig_function == TRIG_FUNCTION_SIN:

            self.update_text(string=['s()', 'sin()', ''], update=1)

        elif trig_function == TRIG_FUNCTION_COS:
            
            self.update_text(string=['c()', 'cos()', ''], update=1)

        elif trig_function == TRIG_FUNCTION_TAN:
            
            self.update_text(string=['t()', 'tan()', ''], update=1)


    def put_exponential(self, ctrlexp = -1):

        self.logic.bracket_num += 1

        if ctrlexp != -1:

            self.update_text(string=[' ^ ' + str(ctrlexp), get_super('(' + str(ctrlexp) + ')'), ''], update=1)

        else:

            self.logic.exponent = not self.logic.exponent

            self.update_text(string=['0', ('').join(Window.equation_text) + get_super('(y)')], update=2)
            self.update_text(string=[' ^ ()', get_super('()'), ''], update=3)


    def put_square_root(self):

        self.update_text(string=['#()', 'sqrt()', ''], update=1)

        self.logic.bracket_num += 1


    def put_factorials(self):

        # put the factorial sign in the equation and display strings
        self.update_text(string=['!', '!', ''], update=1)



    def handle_operator(self, operation: str = None):

        try:

            if self.equation_text[-2 - self.logic.bracket_num] not in 'sctSCTlf^#/*%+_':

                if operation == ' _ ': 
                    
                    self.update_text(string=[operation, ' - ', ''], update=1)
                else:

                    self.update_text(string=[operation, operation, ''], update=1)

        except: 

            if operation == ' _ ':

                self.update_text(string=[operation, ' - ', ''], update=1)

            else:

                self.update_text(string=[operation, operation, ''], update=1)


    def assign_decimal(self):

        if Window.display_text == '':

            self.gui.update_text(type=1, string=['0.', '0.', '0.'])

        elif '.' not in Window.display_text:

            self.gui.update_text(type=1, string=['.', '.', '.'])


    # function bound to the integer button to allow the user to toggle a number between positive and negative.
    def negative(self):
        
        try:

            # check to see if there is anything in the display text
            if Window.display_text == ['']:

                # add the integer sign to the number if there is nothing else in the equation
                self.gui.update_text(string=['-', '-', '-'])

            

            # find where display text is within the equation text
            index = ('').join(Window.equation_text).find(('').join(Window.display_text))



            if  '-' not in Window.display_text:

                if Window.equation_text[index] != '-':

                    # put an integer sign on the number if it doesn't have one
                    self.gui.update_text(type=1, string=['-', '-', '-'], index=[index, index, 0]) 



            else:

                # remove the integer sign from the number
                Scientific.equation.pop(index)

                Window.equation_text.pop(index)

                Window.display_text.pop(0)



        except:

            # add the integer sign to the number if there is nothing else in the equation
            self.gui.update_text(type=1, string=['-', '-', '-'])





    def memoryrecall(self):

        self.update_text(string=[self.logic.memory, self.logic.memory, self.logic.memory])


    def memorystore(self):

        print(f"memory: {('').join(self.display_text)}")

        self.logic.memory = self.display_text

    def memoryclear(self):

        self.logic.memory = []

    def toggle_shift(self):

        self.shift_toggle = not self.shift_toggle

        if self.shift_toggle:

            self.sine.   configure(text='sin' + get_super('-1'))
            self.cosine. configure(text='cos' + get_super('-1'))
            self.tangent.configure(text='tan' + get_super('-1'))

            self.sine.   place(x = 100, y = 375, width = 100, height = 75)
            self.cosine. place(x = 100, y = 450, width = 100, height = 75)
            self.tangent.place(x = 100, y = 525, width = 100, height = 75)

        else:

            self.sine.   configure(text='sin')
            self.cosine. configure(text='cos')
            self.tangent.configure(text='tan')

            self.sine.   place(x = 100, y = 375, width = 100, height = 75)
            self.cosine. place(x = 100, y = 450, width = 100, height = 75)
            self.tangent.place(x = 100, y = 525, width = 100, height =  75)


    def brackets(self, type):

        if type:

            # allow for bracket multiplication without pressing the multiplication button
            if self.logic.equation[-1] in list('1234567890)'):

                for i in list(' * '): 
                    
                    self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)

            self.logic.bracket_num += 1

            self.update_text(string=['()', '()', ''], update=1)

        else:

            if self.equation_text[-1 - self.logic.bracket_num] in '1234567890.-)':

                # start typing outside one more layer of brackets
                if self.logic.bracket_num > 0:

                    self.logic.bracket_num -= 1

                    # display numbers within brackets
                    self.update_text(type=2, update=1)



    def answer(self):

        self.update_text(string=[self.logic.output, self.logic.output, self.logic.output])




    def scientific(self):

        print('this gets run')

        self.parent.title('Calculator')

        self.parent.geometry('700x675')

        self.logic = Scientific()

        print(f"self.logic: {self.logic}")

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
        self.equal          = tk.Button(self.parent, text='=',    anchor='center', bg='DarkSlateGray2', command=lambda:self.calculate(self.round_choice))

        # column 1
        self.mem_clear      = tk.Button(self.parent, text='MC',   anchor='center', bg='gainsboro',      command=self.memoryclear)
        self.pie            = tk.Button(self.parent, text='pi',   anchor='center', bg='gainsboro',      command=self.put_pi)
        self.ee             = tk.Button(self.parent, text='e',    anchor='center', bg='gainsboro',      command=self.put_e)
        self.log            = tk.Button(self.parent, text='log',  anchor='center', bg='gainsboro',      command=self.put_logarithm)
        self.ans            = tk.Button(self.parent, text='Ans',  anchor='center', bg='gainsboro',      command=self.answer)

        # column 2
        self.mem_add        = tk.Button(self.parent, text='MS',   anchor='center', bg='gainsboro',      command=self.memorystore)
        self.shift          = tk.Button(self.parent, text='Inv',  anchor='center', bg='gainsboro',      command=lambda:self.toggle_shift())
        self.sine           = tk.Button(self.parent, text='sin',  anchor='center', bg='gainsboro',      command=lambda:self.put_trigonometry(TRIG_FUNCTION_SIN))
        self.cosine         = tk.Button(self.parent, text='cos',  anchor='center', bg='gainsboro',      command=lambda:self.put_trigonometry(TRIG_FUNCTION_COS))
        self.tangent        = tk.Button(self.parent, text='tan',  anchor='center', bg='gainsboro',      command=lambda:self.put_trigonometry(TRIG_FUNCTION_TAN))

        # column 3
        self.mem_recall     = tk.Button(self.parent, text='MR',                 anchor='center', bg='gainsboro',      command=self.memoryrecall)
        self.factorial      = tk.Button(self.parent, text='x!',                 anchor='center', bg='gainsboro',      command=self.put_factorials)
        self.exponent       = tk.Button(self.parent, text='x' + get_super('y'), anchor='center', bg='gainsboro',      command=self.put_exponential)
        self.squared        = tk.Button(self.parent, text='x' + get_super('2'), anchor='center', bg='gainsboro',      command=lambda:self.put_exponential(2))
        self.sqrt           = tk.Button(self.parent, text='sqrt',               anchor='center', bg='gainsboro',      command=self.put_square_root)

        # column 4
        self.open_b         = tk.Button(self.parent, text='(',   anchor='center', bg='gainsboro',      command=lambda:self.brackets(True))
        self.num7           = tk.Button(self.parent, text='7',   anchor='center', bg='white',          command=lambda:self.put_number(7))
        self.num4           = tk.Button(self.parent, text='4',   anchor='center', bg='white',          command=lambda:self.put_number(4))
        self.num1           = tk.Button(self.parent, text='1',   anchor='center', bg='white',          command=lambda:self.put_number(1))
        self.integer        = tk.Button(self.parent, text='+/-', anchor='center', bg='white',          command=self.negative)
        
        # column 5
        self.close_b        = tk.Button(self.parent, text=')',   anchor='center', bg='gainsboro',      command=lambda:self.brackets(False))
        self.num8           = tk.Button(self.parent, text='8',   anchor='center', bg='white',          command=lambda:self.put_number(8))
        self.num5           = tk.Button(self.parent, text='5',   anchor='center', bg='white',          command=lambda:self.put_number(5))
        self.num2           = tk.Button(self.parent, text='2',   anchor='center', bg='white',          command=lambda:self.put_number(2))
        self.num0           = tk.Button(self.parent, text='0',   anchor='center', bg='white',          command=lambda:self.put_number(0))
        
        # column 6
        self.modulus        = tk.Button(self.parent, text='%',   anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' % '))
        self.num9           = tk.Button(self.parent, text='9',   anchor='center', bg='white',          command=lambda:self.put_number(9))
        self.num6           = tk.Button(self.parent, text='6',   anchor='center', bg='white',          command=lambda:self.put_number(6))
        self.num3           = tk.Button(self.parent, text='3',   anchor='center', bg='white',          command=lambda:self.put_number(3))
        self.decimal        = tk.Button(self.parent, text='.',   anchor='center', bg='white',          command=self.assign_decimal)

        # column 7
        self.clear_data     = tk.Button(self.parent, text='CE',  anchor='center', bg='lightcoral',     command=lambda:self.clear())
        self.divide         = tk.Button(self.parent, text='/',   anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' / '))
        self.multiply       = tk.Button(self.parent, text='x',   anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' * '))
        self.minus          = tk.Button(self.parent, text='-',   anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' _ '))
        self.plus           = tk.Button(self.parent, text='+',   anchor='center', bg='gainsboro',      command=lambda:self.handle_operator(' + '))



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


    

    def update_text(self, type = 0, string = None, index = None, update = 0):

        if string is None:

            string = ['', '', '']

        if index is None:

            index = [len(self.logic.equation), len(self.equation_text), len(self.display_text)]

        # simplify variables
        a = self.logic.equation
        b = self.equation_text
        c = self.display_text
        d = self.logic.bracket_num
        e = self.logic.exponent

        if type == 0:

            # edit main equation variables
            self.logic.equation = list(('').join(a[0:index[0] - d]) + string[0] + ('').join(a[index[0] - d:len(a)]))

            try:

                if e: 
                    self.equation_text = get_super(list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)])))

                else: 
                    self.equation_text = list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)]))

            except:pass

            self.display_text = list(string[2])
            self.display_text.append('')

        
        elif type == 1:

            # edit main equation variables
            self.logic.equation = list(('').join(a[0:index[0] - d]) + string[0] + ('').join(a[index[0] - d:len(a)]))

            try:

                if e: 
                    self.equation_text = get_super(list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)])))

                else: 
                    self.equation_text = list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)]))

            except:pass

            self.display_text = list(('').join(c[0:index[2]]) + string[2] + ('').join(c[index[2]:len(c)]))



        if update == 0:

            # update display
            self.display.configure(text = ('').join(c))

            self.equation.configure(text = ('').join(b))



        elif update == 1:

            # update display
            self.display.configure(text = '0')

            self.equation.configure(text = ('').join(b))

        

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





def main():

    root = tk.Tk()

    main_window = Window(root)

    main_window.scientific()
    
    try:
        root.mainloop()
        
    except KeyboardInterrupt:
        pass

    

if __name__ == '__main__':

    if os.name == 'nt':
        try:
            import ctypes
            
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
            success   = ctypes.windll.user32.SetProcessDPIAware()
        except:pass 

    main()