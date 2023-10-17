import tkinter as tk
from tkinter import *
import keyboard
import os
from shunting_parser import shunting_yard_evaluator


# things to update:

# multiplying functions without pressing '*' doesn't work

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

dict = {}

# setup
root = tk.Tk()

root.title('Calculator')

root.geometry('700x675')

# override windows scaling
if os.name == 'nt':
    try:
        import ctypes
        
        awareness = ctypes.c_int()
        errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
        success   = ctypes.windll.user32.SetProcessDPIAware()
    except:pass 



class Scientific:

    def __init__(self, type, data) -> None:

        self.type = type # types are button, text, and var
        self.data = data # the actual tk data or variable value



    # function bound to the clear equation button that clears the variables and display.
    def clear(self, type = True):

        if type:

            # reset variables
            self.equation_data.data = ['']

            self.equation_text.data = ['']

            self.display_text.data = ['', '']

            self.bracket_num.data = 0



            # update display
            self.display_data.data.configure(text = '0')

            self.equation_data.data.configure(text = '')



        else:

            # check if there is anything in the display text variable
            if self.equation_text[-1] in '1234567890.-':

                # delete last digit in each variable
                self.equation_data.data.pop()

                self.equation_text.data.pop()

                # only delete from the display text if there is stuff to delete
                if self.display_text.data:

                    self.display_text.data.pop()

                # update display
                Scientific.Scientific.update(type=2)



            # check if there is an operator in the right-most position in the equation
            elif self.equation_text.data[-1] == ' ':

                # delete last operator
                self.equation_data.data = self.equation_data.data[:-3]

                self.equation_text.data = self.equation_text.data[:-3]

                # update display
                Scientific.Scientific.update(type=2)



    # change the button text to inverted functions
    def shifte(self):

        # flip the variable whenever the button is pressed
        self.shift_data = not self.shift_data

        if self.shift_data:

            self.sine.data    = tk.Button(root, text='sin' + get_super('-1'), anchor='center', bg='gainsboro', command=lambda:Scientific.trigonometry(True))
            self.cosine.data  = tk.Button(root, text='cos' + get_super('-1'), anchor='center', bg='gainsboro', command=lambda:Scientific.trigonometry(False))
            self.tangent.data = tk.Button(root, text='tan' + get_super('-1'), anchor='center', bg='gainsboro', command=lambda:Scientific.trigonometry())

            self.sine.data.   configure(font=('Arial', 25, 'bold'))
            self.cosine.data. configure(font=('Arial', 25, 'bold'))
            self.tangent.data.configure(font=('Arial', 25, 'bold'))

            self.sine.data.   place(x = 100, y = 375, width = 100, height = 75)
            self.cosine.data. place(x = 100, y = 450, width = 100, height = 75)
            self.tangent.data.place(x = 100, y = 525, width = 100, height = 75)



        # change the button text to normal functions
        else:

            self.sine.data    = tk.Button(root, text='sin', anchor='center', bg='gainsboro', command=lambda:Scientific.trigonometry(True))
            self.cosine.data  = tk.Button(root, text='cos', anchor='center', bg='gainsboro', command=lambda:Scientific.trigonometry(False))
            self.tangent.data = tk.Button(root, text='tan', anchor='center', bg='gainsboro', command=lambda:Scientific.trigonometry())

            self.sine.data.   configure(font=('Arial', 25, 'bold'))
            self.cosine.data. configure(font=('Arial', 25, 'bold'))
            self.tangent.data.configure(font=('Arial', 25, 'bold'))

            self.sine.data.   place(x = 100, y = 375, width = 100, height = 75)
            self.cosine.data. place(x = 100, y = 450, width = 100, height = 75)
            self.tangent.data.place(x = 100, y = 525, width = 100, height = 75)



    # function to change variable to avoid repeating code
    def update(self, type = 0, string = None, index = None, update = 0):

        if string is None:

            string = ['', '', '']



        if index is None:

            index = [len(self.equation_data.data), len(self.equation_text.data), len(self.display_text.data)]



        if type == 0:
            

            # simplify variables
            a = self.equation_data.data
            b = self.equation_text.data
            c = self.display_text.data
            d = self.bracket_num.data

            # edit main equation variables
            self.equation_data.data = list(('').join(a[0:index[0] - d]) + string[0] + ('').join(a[index[0] - d:len(a)]))

            try:

                if self.exponent_data.data: self.equation_text.data = get_super(list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)])))

                else: self.equation_text.data = list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)]))

            except:pass

            self.display_text.data = list(string[2])

            self.display_text.data.append('')


        
        elif type == 1:

            a = self.equation_data.data
            b = self.equation_text.data
            c = self.display_text.data
            d = self.bracket_num.data

            # edit main equation variables
            self.equation_data.data = list(('').join(a[0:index[0] - d]) + string[0] + ('').join(a[index[0] - d:len(a)]))

            try:

                if self.exponent_dat: self.equation_text.data = get_super(list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)])))

                else: self.equation_text.data = list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)]))

            except:pass

            self.display_text.data = list(('').join(c[0:index[2]]) + string[2] + ('').join(c[index[2]:len(c)]))



        if update == 0:

            # update display
            self.display.data.configure(text = ('').join(self.display_text.data))

            self.equation.data.configure(text = ('').join(self.equation_text.data))



        elif update == 1:

            # update display
            self.display.data.configure(text = '0')

            self.equation.data.configure(text = ('').join(self.equation_text.data))

        else:pass





    # the function bound to the 'equals' button to output a result for an equation.
    def calculate(self):

        # assemble equation list into a string
        self.equation_data.data = ('').join(self.equation_data.data)

        # give the equation parser the equation string and set the output to a variable
        self.output.data = shunting_yard_evaluator(self.equation_data.data)

        # round the output to the specified number of decimal places
        self.output.data = str(round(float(self.output.data), int(self.round_choice.data.get())))



        # edit display strings
        self.equation_text.data += ' = ' + self.output.data

        self.display_text.data = self.output.data

        self.bracket_num.data = 0



        # update display
        Scientific.update(type=2)



        # reset variables
        self.equation_text.data = self.output.data

        self.equation_data.data = self.output.data






    # the function bound to the addition button to tell the calculate function which mathematical operation to perform when it is pressed.
    def meth(self, operation = None):

        try:

            if self.equation_text.data[-2 - self.bracket_num.data] not in 'sctSCTlf^#/*%+_':

                if operation == ' _ ':

                    Scientific.update(string=[operation, ' - ', ''], update=1)

                

                else:

                    # add addition sign to equation and display strings
                    Scientific.update(string=[operation, operation, ''], update=1)

        except:

            if operation == ' _ ':

                Scientific.update(string=[operation, ' - ', ''], update=1)

            

            else:

                # add addition sign to equation and display strings
                Scientific.update(string=[operation, operation, ''], update=1)



    # function bound to the decimal button to allow decimal numbers to be inputted.
    def assign_decimal(self):

        if self.display_text.data == '':

            # put the decimal in the equation and display strings
            Scientific.update(type=1, string=['0.', '0.', '0.'])



        elif '.' not in self.display_text.data:

            # put the decimal in the equation and display strings
            Scientific.update(type=1, string=['.', '.', '.'])



    # function bound to the integer button to allow the user to toggle a number between positive and negative.
    def negative(self):
        
        try:

            # check to see if there is anything in the display text
            if self.display_text.data == ['']:

                # add the integer sign to the number if there is nothing else in the equation
                Scientific.update(string=['-', '-', '-'])



            elif  '-' not in self.display_text.data:

                # find where display text is within the equation text
                index = ('').join(self.equation_text.data).find(('').join(self.display_text.data))



                if self.equation_text.data[index] != '-':

                    # put an integer sign on the number if it doesn't have one
                    Scientific.update(type=1, string=['-', '-', '-'], index=[index, index, 0]) 



            else:

                # remove the integer sign from the number
                self.equation_data.data.pop(index)

                self.equation_text.data.pop(index)

                self.display_text.data.pop(0)



        except:

            # add the integer sign to the number if there is nothing else in the equation
            Scientific.update(type=1, string=['-', '-', '-'])

    

    # function to input numbers.
    @staticmethod
    def assign(x):

        # put the number in the equation and display strings
        Scientific.update(type=1, string=[str(x), str(x), str(x)])



    # function bound to the exponent button that allows for exponents to be used.
    def exponential(self, ctrlexp = -1):

        # check if a keybinding was used
        if ctrlexp != -1:

            # put the exponent sign and exponent number in the equation and display strings
            Scientific.update(string=[' ^ ' + str(ctrlexp), get_super('(' + str(ctrlexp) + ')'), ''], update=1)

            # increase bracket number counter
            self.bracket_num.data += 1

        

        else:

            self.exponent_data.data = not self.exponent_data.data

            # update display
            self.display.data.configure(text = '0')

            self.equation.data.configure(text = ('').join(self.equation_text.data) + get_super('(y)'))



            # put exponent sign in equation
            Scientific.update(string=[' ^ ()', get_super('()'), ''], update=2)

            # increase bracket number counter
            self.bracket_num.data += 1



    # function bound to the sqrt button that adds square root
    def square_root(self):

        # add the sqrt function indicator to the equation and display strings
        Scientific.update(string=['#()', 'sqrt()', ''], update=1)

        # allow for more brackets
        self.bracket_num.data += 1



    # function bound to the factorial button to allow for factorials to be used.
    @staticmethod
    def factorials():

        # put the factorial sign in the equation and display strings
        Scientific.update(string=['!', '!', ''], update=1)



    # function bound to the memory recall button to display the number stored in memory.
    def memoryrecall(self):

        # add the number stored in memory to the equation and display strings
        Scientific.update(string=[self.memory.data, self.memory.data, self.memory.data])



    # function bound to the memory clear button that will clear the number stored in the memory.
    def memoryclear(self):

        # clear the memory variable
        self.memory.data = []



    # function bound to the memory add button to set the memory number to the number displayed.
    def memorystore(self):

        print(f"memory: {('').join(self.display_text.data)}")

        # assign a number to the memory variable
        self.memory.data = self.display_text.data



    # function bound to the brackets button to add them to the display.
    def brackets(self, type):

        if type:

            # allow for bracket multiplication without pressing the multiplication button
            if self.equation_data.data[-1] in list('1234567890)'):

                for i in list(' * '): self.equation_data.data.insert(len(self.equation_data.data) - self.bracket_num.data, i)



            # add an open bracket to the equation and display strings
            Scientific.update(string=['()', '()', ''], update=1)



            # keep track of brackets
            self.bracket_num.data += 1



        else:

            if self.equation_text.data[-1 - self.bracket_num.data] in '1234567890.-)':

                # start typing outside one more layer of brackets
                if self.bracket_num.data > 0:

                    self.bracket_num.data -= 1

                    # display numbers within brackets
                    Scientific.update(type=2, update=1)



    # function bound to the trigonometry buttons to allow them to be used.
    def trigonometry(self, type = 0):

        # add an alternate function for inverse trigonometry functions
        if self.shift_data.data:

            if type:

                # add the inverse sine indicator to the equation and display strings
                Scientific.update(string=['S()', 'sin' + get_super('-1') + '()', ''], update=1)



            elif not type:
                
                # add the inverse cosine indicator to the equation and display strings
                Scientific.update(string=['C()', 'cos' + get_super('-1') + '()', ''], update=1)



            else:
                
                # add the inverse tangent indicator to the equation and display strings
                Scientific.update(string=['T()', 'tan' + get_super('-1') + '()', ''], update=1)



        else:

            if type:

                # add the sine indicator to the equation and display strings
                Scientific.update(string=['s()', 'sin()', ''], update=1)



            elif not type:
                
                # add the cosine indicator to the equation and display strings
                Scientific.update(string=['c()', 'cos()', ''], update=1)



            else:
                
                # add the tangent indicator to the equation and display strings
                Scientific.update(string=['t()', 'tan()', ''], update=1)

        # allow for more brackets
        self.bracket_num.data += 1



    # function bound to the pi button to allow for the pi number to be accessed easily.
    @staticmethod
    def pi():

        # add the pi number to the equation and display strings
        Scientific.update(string=['3.14159265359', 'pi', '3.14159265359'])



    # function bound to the e button to allow for eulers number to be accessed easily.
    @staticmethod
    def e():

        # add eulers number to the equation and display strings
        Scientific.update(string=['2.71828182846', 'e', '2.71828182846'])



    # function bound to the log button to allow for logarithms to be used.
    def logarithm(self):

        # add the log function indicator to the equation and display strings
        Scientific.update(string=['l()', 'log()', ''], update=1)

        # allow for more brackets
        self.bracket_num.data += 1



    # function bound to the answer button to allow for the previous answer to be used.
    def answer(self):

        # add the previous answer to the equation and display strings
        Scientific.update(string=[self.output.data, self.output.data, self.output.data])



# function to detect optionmenu changes
def options_callback(var, index, mode):

    print(dict['option choices'].get())

    if dict['option choices'].get() == 'Scientific':

        scientific()



# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)



# a function to handle all key inputs
def keybindings():

    if   keyboard.is_pressed('shift+=')  :Scientific.meth(' + ')
    elif keyboard.is_pressed('shift+8')  :Scientific.meth(' * ')
    elif keyboard.is_pressed('shift+5')  :Scientific.meth(' % ')
    elif keyboard.is_pressed('ctrl+0')   :Scientific.exponential(0)
    elif keyboard.is_pressed('ctrl+1')   :Scientific.exponential(1)
    elif keyboard.is_pressed('ctrl+2')   :Scientific.exponential(2)
    elif keyboard.is_pressed('ctrl+3')   :Scientific.exponential(3)
    elif keyboard.is_pressed('ctrl+4')   :Scientific.exponential(4)
    elif keyboard.is_pressed('ctrl+5')   :Scientific.exponential(5)
    elif keyboard.is_pressed('ctrl+6')   :Scientific.exponential(6)
    elif keyboard.is_pressed('ctrl+7')   :Scientific.exponential(7)
    elif keyboard.is_pressed('ctrl+8')   :Scientific.exponential(8)
    elif keyboard.is_pressed('ctrl+9')   :Scientific.exponential(9)
    elif keyboard.is_pressed('shift+0')  :Scientific.brackets(False)
    elif keyboard.is_pressed('shift+1')  :Scientific.factorials()
    elif keyboard.is_pressed('shift+6')  :Scientific.exponential()
    elif keyboard.is_pressed('shift+3')  :Scientific.square_root()
    elif keyboard.is_pressed('shift+9')  :Scientific.brackets(True)
    elif keyboard.is_pressed('ctrl+s')   :Scientific.trigonometry(True)
    elif keyboard.is_pressed('ctrl+c')   :Scientific.trigonometry(False)
    elif keyboard.is_pressed('ctrl+t')   :Scientific.trigonometry()
    elif keyboard.is_pressed('ctrl+a')   :Scientific.answer()
    elif keyboard.is_pressed('ctrl+e')   :Scientific.e()
    elif keyboard.is_pressed('ctrl+l')   :Scientific.logarithm()
    elif keyboard.is_pressed('ctrl+p')   :Scientific.pi()
    elif keyboard.is_pressed('shift+-')  :Scientific.negative()
    elif keyboard.is_pressed('shift+m')  :Scientific.memorystore()
    elif keyboard.is_pressed('ctrl+m')   :Scientific.memoryclear()
    elif keyboard.is_pressed('shift+backspace'):Scientific.clear(False)
    elif keyboard.is_pressed('enter')    :Scientific.calculate()
    elif keyboard.is_pressed('m')        :Scientific.memoryrecall()
    elif keyboard.is_pressed('-')        :Scientific.meth(' _ ')
    elif keyboard.is_pressed('/')        :Scientific.meth(' / ')
    elif keyboard.is_pressed('.')        :Scientific.assign_decimal()
    elif keyboard.is_pressed('0')        :Scientific.assign(0)
    elif keyboard.is_pressed('1')        :Scientific.assign(1)
    elif keyboard.is_pressed('2')        :Scientific.assign(2)
    elif keyboard.is_pressed('3')        :Scientific.assign(3)
    elif keyboard.is_pressed('4')        :Scientific.assign(4)
    elif keyboard.is_pressed('5')        :Scientific.assign(5)
    elif keyboard.is_pressed('6')        :Scientific.assign(6)
    elif keyboard.is_pressed('7')        :Scientific.assign(7)
    elif keyboard.is_pressed('8')        :Scientific.assign(8)
    elif keyboard.is_pressed('9')        :Scientific.assign(9)
    elif keyboard.is_pressed('backspace'):Scientific.clear(True)
    elif keyboard.is_pressed('shift')    :Scientific.shifte()



# scientific calculator display configuration
def scientific():

    # sizing
    root.geometry('700x675')

    # variables
    shift_data    = Scientific('var', False)
    equation_text = Scientific('var', [''])
    display_text  = Scientific('var', ['', ''])
    equation_data = Scientific('var', [''])
    output        = Scientific('var', '')
    memory        = Scientific('var', [])
    bracket_num   = Scientific('var', 0)
    exponent_data = Scientific('var', False)


    # graphical setup
    equation = Scientific('text', tk.Label(root, text = ''))
    equation.data.configure(font=('Arial', 40, ''))
    equation.data.place(x = 0, y = 10)

    display = Scientific('text', tk.Label(root, text = '0'))
    display.data.configure(font=('Arial', 75, 'bold'))
    display.data.place(x = 0, y = 80)

    round_label = Scientific('text', tk.Label(root, text = 'Round to              decimal points'))
    round_label.data.configure(font=('Arial', 15, 'bold'))
    round_label.data.place(x = 370, y = 190)



    # decimal changer
    round_choice = Scientific('var', StringVar(root))
    round_choice.data.set(11)

    round_numbers = Scientific('button', OptionMenu(root, round_choice, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))
    round_numbers.data.configure(font=('Arial', 15, 'bold'))
    round_numbers.data.place(x = 470, y = 185)



    # options to switch between calculators
    options = Scientific('button', OptionMenu(root, dict['option choices'], 'Scientific', 'Quadratic', 'Factoring'))
    options.data.configure(font=('Arial', 15, 'bold'))
    options.data.place(x = 10, y = 185)



    # create button information
    equal      = Scientific('button', tk.Button(root, text='=',                  anchor='center', bg='DarkSlateGray2', command=lambda:Scientific.calculate()))

    # column 7
    clear      = Scientific('button', tk.Button(root, text='CE',                 anchor='center', bg='lightcoral', command=lambda:Scientific.clear()))
    divide     = Scientific('button', tk.Button(root, text='/',                  anchor='center', bg='gainsboro',  command=lambda:Scientific.meth(' / ')))
    multiply   = Scientific('button', tk.Button(root, text='x',                  anchor='center', bg='gainsboro',  command=lambda:Scientific.meth(' * ')))
    minus      = Scientific('button', tk.Button(root, text='-',                  anchor='center', bg='gainsboro',  command=lambda:Scientific.meth(' _ ')))
    plus       = Scientific('button', tk.Button(root, text='+',                  anchor='center', bg='gainsboro',  command=lambda:Scientific.meth(' + ')))

    # column 6
    modulus    = Scientific('button', tk.Button(root, text='%',                  anchor='center', bg='gainsboro',  command=lambda:Scientific.meth(' % ')))
    num9       = Scientific('button', tk.Button(root, text='9',                  anchor='center', bg='white',      command=lambda:Scientific.assign(9)))
    num6       = Scientific('button', tk.Button(root, text='6',                  anchor='center', bg='white',      command=lambda:Scientific.assign(6)))
    num3       = Scientific('button', tk.Button(root, text='3',                  anchor='center', bg='white',      command=lambda:Scientific.assign(3)))
    decimal    = Scientific('button', tk.Button(root, text='.',                  anchor='center', bg='white',      command=lambda:Scientific.assign_decimal()))

    # column 5
    close_b    = Scientific('button', tk.Button(root, text=')',                  anchor='center', bg='gainsboro',  command=lambda:Scientific.brackets(False)))
    num8       = Scientific('button', tk.Button(root, text='8',                  anchor='center', bg='white',      command=lambda:Scientific.assign(8)))
    num5       = Scientific('button', tk.Button(root, text='5',                  anchor='center', bg='white',      command=lambda:Scientific.assign(5)))
    num2       = Scientific('button', tk.Button(root, text='2',                  anchor='center', bg='white',      command=lambda:Scientific.assign(2)))
    num0       = Scientific('button', tk.Button(root, text='0',                  anchor='center', bg='white',      command=lambda:Scientific.assign(0)))

    # column 4
    open_b     = Scientific('button', tk.Button(root, text='(',                  anchor='center', bg='gainsboro',  command=lambda:Scientific.brackets(True)))
    num7       = Scientific('button', tk.Button(root, text='7',                  anchor='center', bg='white',      command=lambda:Scientific.assign(7)))
    num4       = Scientific('button', tk.Button(root, text='4',                  anchor='center', bg='white',      command=lambda:Scientific.assign(4)))
    num1       = Scientific('button', tk.Button(root, text='1',                  anchor='center', bg='white',      command=lambda:Scientific.assign(1)))
    integer    = Scientific('button', tk.Button(root, text='+/-',                anchor='center', bg='white',      command=lambda:Scientific.negative()))

    # column 3
    mem_recall = Scientific('button', tk.Button(root, text='MR',                 anchor='center', bg='gainsboro',  command=lambda:Scientific.memoryrecall()))
    factorial  = Scientific('button', tk.Button(root, text='x!',                 anchor='center', bg='gainsboro',  command=lambda:Scientific.factorials()))
    exponent   = Scientific('button', tk.Button(root, text='x' + get_super('y'), anchor='center', bg='gainsboro',  command=lambda:Scientific.exponential()))
    squared    = Scientific('button', tk.Button(root, text='x' + get_super('2'), anchor='center', bg='gainsboro',  command=lambda:Scientific.exponential(2)))
    sqrt       = Scientific('button', tk.Button(root, text='sqr',                anchor='center', bg='gainsboro',  command=lambda:Scientific.square_root()))

    # column 2
    mem_add    = Scientific('button', tk.Button(root, text='MS',                 anchor='center', bg='gainsboro',  command=lambda:Scientific.memorystore()))
    shift      = Scientific('button', tk.Button(root, text='Inv',                anchor='center', bg='gainsboro',  command=lambda:Scientific.shifte()))
    sine       = Scientific('button', tk.Button(root, text='sin',                anchor='center', bg='gainsboro',  command=lambda:Scientific.trigonometry(True)))
    cosine     = Scientific('button', tk.Button(root, text='cos',                anchor='center', bg='gainsboro',  command=lambda:Scientific.trigonometry(False)))
    tangent    = Scientific('button', tk.Button(root, text='tan',                anchor='center', bg='gainsboro',  command=lambda:Scientific.trigonometry()))

    # column 1
    mem_clear  = Scientific('button', tk.Button(root, text='MC',                 anchor='center', bg='gainsboro',  command=lambda:Scientific.memoryclear()))
    pie        = Scientific('button', tk.Button(root, text='pi',                 anchor='center', bg='gainsboro',  command=lambda:Scientific.pi()))
    ee         = Scientific('button', tk.Button(root, text='e',                  anchor='center', bg='gainsboro',  command=lambda:Scientific.e()))
    log        = Scientific('button', tk.Button(root, text='log',                anchor='center', bg='gainsboro',  command=lambda:Scientific.logarithm()))
    ans        = Scientific('button', tk.Button(root, text='Ans',                anchor='center', bg='gainsboro',  command=lambda:Scientific.answer()))



    # create button fonts
    equal.data.     configure(font=('Arial', 25, 'bold'))

    # column 7
    clear.data.     configure(font=('Arial', 25, 'bold'))
    divide.data.    configure(font=('Arial', 25, 'bold'))
    multiply.data.  configure(font=('Arial', 25, 'bold'))
    minus.data.     configure(font=('Arial', 25, 'bold'))
    plus.data.      configure(font=('Arial', 25, 'bold'))

    # column 6
    modulus.data.   configure(font=('Arial', 25, 'bold'))
    num9.data.      configure(font=('Arial', 25, 'bold'))
    num6.data.      configure(font=('Arial', 25, 'bold'))
    num3.data.      configure(font=('Arial', 25, 'bold'))
    decimal.data.   configure(font=('Arial', 25, 'bold'))

    # column 5
    close_b.data.   configure(font=('Arial', 25, 'bold'))
    num8.data.      configure(font=('Arial', 25, 'bold'))
    num5.data.      configure(font=('Arial', 25, 'bold'))
    num2.data.      configure(font=('Arial', 25, 'bold'))
    num0.data.      configure(font=('Arial', 25, 'bold'))

    # column 4
    open_b.data.    configure(font=('Arial', 25, 'bold'))
    num7.data.      configure(font=('Arial', 25, 'bold'))
    num4.data.      configure(font=('Arial', 25, 'bold'))
    num1.data.      configure(font=('Arial', 25, 'bold'))
    integer.data.   configure(font=('Arial', 25, 'bold'))

    # column 3
    mem_recall.data.configure(font=('Arial', 25, 'bold'))
    factorial.data. configure(font=('Arial', 25, 'bold'))
    exponent.data.  configure(font=('Arial', 25, 'bold'))
    squared.data.   configure(font=('Arial', 25, 'bold'))
    sqrt.data.      configure(font=('Arial', 25, 'bold'))

    # column 2
    mem_add.data.   configure(font=('Arial', 25, 'bold'))
    shift.data.     configure(font=('Arial', 25, 'bold'))
    sine.data.      configure(font=('Arial', 25, 'bold'))
    cosine.data.    configure(font=('Arial', 25, 'bold'))
    tangent.data.   configure(font=('Arial', 25, 'bold'))

    # column 1
    mem_clear.data. configure(font=('Arial', 25, 'bold'))
    pie.data.       configure(font=('Arial', 25, 'bold'))
    ee.data.        configure(font=('Arial', 25, 'bold'))
    log.data.       configure(font=('Arial', 25, 'bold'))
    ans.data.       configure(font=('Arial', 25, 'bold'))


    
    # place buttons
    equal.data.     place(x = 0,   y = 600, width = 700, height = 75)

    # column 7
    clear.data.     place(x = 600, y = 225, width = 100, height = 75)
    divide.data.    place(x = 600, y = 300, width = 100, height = 75)
    multiply.data.  place(x = 600, y = 375, width = 100, height = 75)
    minus.data.     place(x = 600, y = 450, width = 100, height = 75)
    plus.data.      place(x = 600, y = 525, width = 100, height = 75)

    # column 6
    modulus.data.   place(x = 500, y = 225, width = 100, height = 75)
    num9.data.      place(x = 500, y = 300, width = 100, height = 75)
    num6.data.      place(x = 500, y = 375, width = 100, height = 75)
    num3.data.      place(x = 500, y = 450, width = 100, height = 75)
    decimal.data.   place(x = 500, y = 525, width = 100, height = 75)

    # column 5
    close_b.data.   place(x = 400, y = 225, width = 100, height = 75)
    num8.data.      place(x = 400, y = 300, width = 100, height = 75)
    num5.data.      place(x = 400, y = 375, width = 100, height = 75)
    num2.data.      place(x = 400, y = 450, width = 100, height = 75)
    num0.data.      place(x = 400, y = 525, width = 100, height = 75)

    # column 4
    open_b.data.    place(x = 300, y = 225, width = 100, height = 75)
    num7.data.      place(x = 300, y = 300, width = 100, height = 75)
    num4.data.      place(x = 300, y = 375, width = 100, height = 75)
    num1.data.      place(x = 300, y = 450, width = 100, height = 75)
    integer.data.   place(x = 300, y = 525, width = 100, height = 75)

    # column 3
    mem_recall.data.place(x = 200, y = 225, width = 100, height = 75)
    factorial.data. place(x = 200, y = 300, width = 100, height = 75)
    exponent.data.  place(x = 200, y = 375, width = 100, height = 75)
    squared.data.   place(x = 200, y = 450, width = 100, height = 75)
    sqrt.data.      place(x = 200, y = 525, width = 100, height = 75)

    # column 2
    mem_add.data.   place(x = 100, y = 225, width = 100, height = 75)
    shift.data.     place(x = 100, y = 300, width = 100, height = 75)
    sine.data.      place(x = 100, y = 375, width = 100, height = 75)
    cosine.data.    place(x = 100, y = 450, width = 100, height = 75)
    tangent.data.   place(x = 100, y = 525, width = 100, height = 75)

    # column 1
    mem_clear.data. place(x = 0,   y = 225, width = 100, height = 75)
    pie.data.       place(x = 0,   y = 300, width = 100, height = 75)
    ee.data.        place(x = 0,   y = 375, width = 100, height = 75)
    log.data.       place(x = 0,   y = 450, width = 100, height = 75)
    ans.data.       place(x = 0,   y = 525, width = 100, height = 75)



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



# change the main() so that instead of containing the code for one display type, it checks which one is selected, and then runs a function that adds the correct display.

def main():

    # options to switch between calculators
    dict['option choices'] = StringVar(root)
    dict['option choices'].trace('w', options_callback)
    dict['option choices'].set('Scientific')



    # keybindings
    keyboard.hook(lambda _:keybindings())

    # prevent calculator from being resized
    root.resizable(False, False)

    # run the gui
    root.mainloop()

if __name__ == '__main__':

    main()