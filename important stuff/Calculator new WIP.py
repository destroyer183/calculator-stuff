import tkinter as tk
from tkinter import *
import keyboard
import os
from scientific_parser import scientific_parser
from shunting_yard_parser import shunting_yard_parser



# likely bug: when deleting stuff, if an operator is deleted, while the last item in the equation will be a number, that number won't be in the display string, 
# which could cause errors with the decimal and exponent buttons.


# things to update:

# iINTEGER BUTTON IS STILL BUGGED FFS

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

# variables
dict             = {}
dict['operator'] = {}
dict['numbers']  = {}
dict['gui']      = {}

dict['numbers']['equation']   = ['']
dict['numbers']['output']     = ''
dict['numbers']['memory']     = []
dict['numbers']['bracketnum'] = 0
dict['numbers']['exponent']   = False

dict['gui']['equation text'] = ['']
dict['gui']['display text']  = ['', '']
dict['gui']['buttons']       = {}
dict['gui']['shift']         = False



# the function bound to the 'equals' button to output a result for an equation.
def calculate():

    # assemble equation list into a string
    dict['numbers']['equation'] = ('').join(dict['numbers']['equation'])

    # give the equation parser the equation string and set the output to a variable
    dict['numbers']['output'] = shunting_yard_parser(dict['numbers']['equation'])

    # round the output to the specified number of decimal places
    dict['numbers']['output'] = str(round(float(dict['numbers']['output']), int(dict['numbers']['roundchoice'].get())))



    # edit display strings
    dict['gui']['equation text'] += ' = ' + dict['numbers']['output']

    dict['gui']['display text'] = dict['numbers']['output']

    dict['numbers']['bracketnum'] = 0



    # update display
    update(type=2)



    # reset variables
    dict['gui']['equation text'] = dict['numbers']['output']

    dict['numbers']['equation'] = dict['numbers']['output']



# function to change variable to avoid repeating code
def update(type = 0, string = None, index = None, update = 0):

    if string is None:

        string = ['', '', '']



    if index is None:

        index = [len(dict['numbers']['equation']), len(dict['gui']['equation text']), len(dict['gui']['display text'])]



    if type == 0:
        

        # simplify variables
        a = dict['numbers']['equation']
        b = dict['gui']['equation text']
        c = dict['gui']['display text']
        d = dict['numbers']['bracketnum']

        # edit main equation variables
        dict['numbers']['equation'] = list(('').join(a[0:index[0] - d]) + string[0] + ('').join(a[index[0] - d:len(a)]))

        try:

            if dict['numbers']['exponent']: dict['gui']['equation text'] = get_super(list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)])))

            else: dict['gui']['equation text'] = list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)]))

        except:pass

        dict['gui']['display text'] = list(string[2])

        dict['gui']['display text'].append('')


    
    elif type == 1:

        a = dict['numbers']['equation']
        b = dict['gui']['equation text']
        c = dict['gui']['display text']
        d = dict['numbers']['bracketnum']

        # edit main equation variables
        dict['numbers']['equation'] = list(('').join(a[0:index[0] - d]) + string[0] + ('').join(a[index[0] - d:len(a)]))

        try:

            if dict['numbers']['exponent']: dict['gui']['equation text'] = get_super(list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)])))

            else: dict['gui']['equation text'] = list(('').join(b[0:index[1] - d]) + string[1] + ('').join(b[index[1] - d:len(b)]))

        except:pass

        dict['gui']['display text'] = list(('').join(c[0:index[2]]) + string[2] + ('').join(c[index[2]:len(c)]))



    if update == 0:

        # update display
        dict['gui']['display'].configure(text = ('').join(dict['gui']['display text']))

        dict['gui']['equation'].configure(text = ('').join(dict['gui']['equation text']))



    elif update == 1:

        # update display
        dict['gui']['display'].configure(text = '0')

        dict['gui']['equation'].configure(text = ('').join(dict['gui']['equation text']))

    else:pass



# the function bound to the addition button to tell the calculate function which mathematical operation to perform when it is pressed.
def meth(operation = None):

    try:

        if dict['gui']['equation text'][-2 - dict['numbers']['bracketnum']] not in 'sctSCTlf^#/*%+_':

            if operation == ' _ ':

                update(string=[operation, ' - ', ''], update=1)

            

            else:

                # add addition sign to equation and display strings
                update(string=[operation, operation, ''], update=1)

    except:

        if operation == ' _ ':

            update(string=[operation, ' - ', ''], update=1)

        

        else:

            # add addition sign to equation and display strings
            update(string=[operation, operation, ''], update=1)





# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)



# function bound to the decimal button to allow decimal numbers to be inputted.
def assign_decimal():

    if dict['gui']['display text'] == '':

        # put the decimal in the equation and display strings
        update(type=1, string=['0.', '0.', '0.'])



    elif '.' not in dict['gui']['display text']:

        # put the decimal in the equation and display strings
        update(type=1, string=['.', '.', '.'])



# function bound to the integer button to allow the user to toggle a number between positive and negative.
def negative():
    
    try:

        # check to see if there is anything in the display text
        if dict['gui']['display text'] == ['']:

            # add the integer sign to the number if there is nothing else in the equation
            update(string=['-', '-', '-'])



        elif  '-' not in dict['gui']['display text']:

            # find where display text is within the equation text
            index = ('').join(dict['gui']['equation text']).find(('').join(dict['gui']['display text']))



            if dict['gui']['equation text'][index] != '-':

                # put an integer sign on the number if it doesn't have one
                update(type=1, string=['-', '-', '-'], index=[index, index, 0]) 



        else:

            # remove the integer sign from the number
            dict['numbers']['equation'].pop(index)

            dict['gui']['equation text'].pop(index)

            dict['gui']['display text'].pop(0)



    except:

        # add the integer sign to the number if there is nothing else in the equation
        update(type=1, string=['-', '-', '-'])

   

# function to input numbers.
def assign(x):

    # put the number in the equation and display strings
    update(type=1, string=[str(x), str(x), str(x)])



# function bound to the exponent button that allows for exponents to be used.
def exponent(ctrlexp = -1):

    # check if a keybinding was used
    if ctrlexp != -1:

        # put the exponent sign and exponent number in the equation and display strings
        update(string=[' ^ ' + str(ctrlexp), get_super('(' + str(ctrlexp) + ')'), ''], update=1)

        # increase bracket number counter
        dict['numbers']['bracketnum'] += 1

    

    else:

        dict['numbers']['exponent'] = not dict['numbers']['exponent']

        # update display
        dict['gui']['display'].configure(text = '0')

        dict['gui']['equation'].configure(text = ('').join(dict['gui']['equation text']) + get_super('(y)'))



        # put exponent sign in equation
        update(string=[' ^ ()', get_super('()'), ''], update=2)

        # increase bracket number counter
        dict['numbers']['bracketnum'] += 1



# function bound to the sqrt button that adds square root
def square_root():

    # add the sqrt function indicator to the equation and display strings
    update(string=['#()', 'sqrt()', ''], update=1)

    # allow for more brackets
    dict['numbers']['bracketnum'] += 1



# function bound to the factorial button to allow for factorials to be used.
def factorials():

    # put the factorial sign in the equation and display strings
    update(string=['!', '!', ''], update=1)



# function bound to the memory recall button to display the number stored in memory.
def memoryrecall():

    # add the number stored in memory to the equation and display strings
    update(string=[dict['numbers']['memory'], dict['numbers']['memory'], dict['numbers']['memory']])



# function bound to the memory clear button that will clear the number stored in the memory.
def memoryclear():

    # clear the memory variable
    dict['numbers']['memory'] = []



# function bound to the memory add button to set the memory number to the number displayed.
def memorystore():

    print(f"memory: {('').join(dict['gui']['display text'])}")

    # assign a number to the memory variable
    dict['numbers']['memory'] = dict['gui']['display text']



# function bound to the brackets button to add them to the display.
def brackets(type):

    if type:

        # allow for bracket multiplication without pressing the multiplication button
        if dict['numbers']['equation'][-1] in list('1234567890)'):

            for i in list(' * '): dict['numbers']['equation'].insert(len(dict['numbers']['equation']) - dict['numbers']['bracketnum'], i)



        # add an open bracket to the equation and display strings
        update(string=['()', '()', ''], update=1)



        # keep track of brackets
        dict['numbers']['bracketnum'] += 1



    else:

        if dict['gui']['equation text'][-1 - dict['numbers']['bracketnum']] in '1234567890.-':

            # start typing outside one more layer of brackets
            if dict['numbers']['bracketnum'] > 0:

                dict['numbers']['bracketnum'] -= 1

                # display numbers within brackets
                update(type=2, update=1)



# function bound to the trigonometry buttons to allow them to be used.
def trigonometry(type = 0):

    # add an alternate function for inverse trigonometry functions
    if dict['gui']['shift']:

        if type:

            # add the inverse sine indicator to the equation and display strings
            update(string=['S()', 'sin' + get_super('-1') + '()', ''], update=1)



        elif not type:
            
            # add the inverse cosine indicator to the equation and display strings
            update(string=['C()', 'cos' + get_super('-1') + '()', ''], update=1)



        else:
            
            # add the inverse tangent indicator to the equation and display strings
            update(string=['T()', 'tan' + get_super('-1') + '()', ''], update=1)



    else:

        if type:

            # add the sine indicator to the equation and display strings
            update(string=['s()', 'sin()', ''], update=1)



        elif not type:
            
            # add the cosine indicator to the equation and display strings
            update(string=['c()', 'cos()', ''], update=1)



        else:
            
            # add the tangent indicator to the equation and display strings
            update(string=['t()', 'tan()', ''], update=1)

    # allow for more brackets
    dict['numbers']['bracketnum'] += 1



# function bound to the pi button to allow for the pi number to be accessed easily.
def pi():

    # add the pi number to the equation and display strings
    update(string=['3.14159265359', 'pi', '3.14159265359'])



# function bound to the e button to allow for eulers number to be accessed easily.
def e():

    # add eulers number to the equation and display strings
    update(string=['2.71828182846', 'e', '2.71828182846'])



# function bound to the log button to allow for logarithms to be used.
def logarithm():

    # add the log function indicator to the equation and display strings
    update(string=['l()', 'log()', ''], update=1)

    # allow for more brackets
    dict['numbers']['bracketnum'] += 1



# function bound to the answer button to allow for the previous answer to be used.
def answer():

    # add the previous answer to the equation and display strings
    update(string=[dict['numbers']['output'], dict['numbers']['output'], dict['numbers']['output']])



# function bound to the invert button to allow inverse functions to be used.
def shifte():

    # flip the variable whenever the button is pressed
    dict['gui']['shift'] = not dict['gui']['shift']

    # change the button text to inverted functions
    if dict['gui']['shift']:

        dict['gui']['buttons']['sine']    = tk.Button(root, text='sin' + get_super('-1'), anchor='center', bg='gainsboro', command=lambda:trigonometry(True))
        dict['gui']['buttons']['cosine']  = tk.Button(root, text='cos' + get_super('-1'), anchor='center', bg='gainsboro', command=lambda:trigonometry(False))
        dict['gui']['buttons']['tangent'] = tk.Button(root, text='tan' + get_super('-1'), anchor='center', bg='gainsboro', command=lambda:trigonometry())

        dict['gui']['buttons']['sine'].   configure(font=('Arial', 25, 'bold'))
        dict['gui']['buttons']['cosine']. configure(font=('Arial', 25, 'bold'))
        dict['gui']['buttons']['tangent'].configure(font=('Arial', 25, 'bold'))

        dict['gui']['buttons']['sine'].   place(x = 100, y = 375, width = 100, height = 75)
        dict['gui']['buttons']['cosine']. place(x = 100, y = 450, width = 100, height = 75)
        dict['gui']['buttons']['tangent'].place(x = 100, y = 525, width = 100, height = 75)



    # change the button text to normal functions
    else:

        dict['gui']['buttons']['sine']    = tk.Button(root, text='sin', anchor='center', bg='gainsboro', command=lambda:trigonometry(True))
        dict['gui']['buttons']['cosine']  = tk.Button(root, text='cos', anchor='center', bg='gainsboro', command=lambda:trigonometry(False))
        dict['gui']['buttons']['tangent'] = tk.Button(root, text='tan', anchor='center', bg='gainsboro', command=lambda:trigonometry())

        dict['gui']['buttons']['sine'].   configure(font=('Arial', 25, 'bold'))
        dict['gui']['buttons']['cosine']. configure(font=('Arial', 25, 'bold'))
        dict['gui']['buttons']['tangent'].configure(font=('Arial', 25, 'bold'))

        dict['gui']['buttons']['sine'].   place(x = 100, y = 375, width = 100, height = 75)
        dict['gui']['buttons']['cosine']. place(x = 100, y = 450, width = 100, height = 75)
        dict['gui']['buttons']['tangent'].place(x = 100, y = 525, width = 100, height = 75)



# a function to handle all key inputs
def keybindings():

    if   keyboard.is_pressed('shift+=')  :meth(' + ')
    elif keyboard.is_pressed('shift+8')  :meth(' * ')
    elif keyboard.is_pressed('shift+5')  :meth(' % ')
    elif keyboard.is_pressed('ctrl+0')   :exponent(0)
    elif keyboard.is_pressed('ctrl+1')   :exponent(1)
    elif keyboard.is_pressed('ctrl+2')   :exponent(2)
    elif keyboard.is_pressed('ctrl+3')   :exponent(3)
    elif keyboard.is_pressed('ctrl+4')   :exponent(4)
    elif keyboard.is_pressed('ctrl+5')   :exponent(5)
    elif keyboard.is_pressed('ctrl+6')   :exponent(6)
    elif keyboard.is_pressed('ctrl+7')   :exponent(7)
    elif keyboard.is_pressed('ctrl+8')   :exponent(8)
    elif keyboard.is_pressed('ctrl+9')   :exponent(9)
    elif keyboard.is_pressed('shift+0')  :brackets(False)
    elif keyboard.is_pressed('shift+1')  :factorials()
    elif keyboard.is_pressed('shift+6')  :exponent()
    elif keyboard.is_pressed('shift+3')  :square_root()
    elif keyboard.is_pressed('shift+9')  :brackets(True)
    elif keyboard.is_pressed('ctrl+s')   :trigonometry(True)
    elif keyboard.is_pressed('ctrl+c')   :trigonometry(False)
    elif keyboard.is_pressed('ctrl+t')   :trigonometry()
    elif keyboard.is_pressed('ctrl+a')   :answer()
    elif keyboard.is_pressed('ctrl+e')   :e()
    elif keyboard.is_pressed('ctrl+l')   :logarithm()
    elif keyboard.is_pressed('ctrl+p')   :pi()
    elif keyboard.is_pressed('shift+-')  :negative()
    elif keyboard.is_pressed('shift+m')  :memorystore()
    elif keyboard.is_pressed('ctrl+m')   :memoryclear()
    elif keyboard.is_pressed('shift+backspace'):clear(False)
    elif keyboard.is_pressed('enter')    :calculate()
    elif keyboard.is_pressed('m')        :memoryrecall()
    elif keyboard.is_pressed('-')        :meth(' _ ')
    elif keyboard.is_pressed('/')        :meth(' / ')
    elif keyboard.is_pressed('.')        :assign_decimal()
    elif keyboard.is_pressed('0')        :assign(0)
    elif keyboard.is_pressed('1')        :assign(1)
    elif keyboard.is_pressed('2')        :assign(2)
    elif keyboard.is_pressed('3')        :assign(3)
    elif keyboard.is_pressed('4')        :assign(4)
    elif keyboard.is_pressed('5')        :assign(5)
    elif keyboard.is_pressed('6')        :assign(6)
    elif keyboard.is_pressed('7')        :assign(7)
    elif keyboard.is_pressed('8')        :assign(8)
    elif keyboard.is_pressed('9')        :assign(9)
    elif keyboard.is_pressed('backspace'):clear()



# function bound to the clear equation button that clears the variables and display.
def clear(type = True):

    if type:

        # reset variables
        dict['numbers']['equation'] = ['']

        dict['gui']['equation text'] = ['']

        dict['gui']['display text'] = ['', '']

        dict['numbers']['bracketnum'] = 0



        # update display
        dict['gui']['display'].configure(text = '0')

        dict['gui']['equation'].configure(text = '')



    else:

        # check if there is anything in the display text variable
        if dict['gui']['equation text'][-1] in '1234567890.-':

            # delete last digit in each variable
            dict['numbers']['equation'].pop()

            dict['gui']['equation text'].pop()

            # only delete from the display text if there is stuff to delete
            if len(dict['gui']['display text']) != 0:

                dict['gui']['display text'].pop()

            # update display
            update(type=2)



        # check if there is an operator in the right-most position in the equation
        elif dict['gui']['equation text'][-1] == ' ':

            # delete last operator
            dict['numbers']['equation'] = dict['numbers']['equation'][0:-3]

            dict['gui']['equation text'] = dict['gui']['equation text'][0:-3]

            # update display
            update(type=2)


        # check if the last thing entered in was an operator
        # check if the last thing is a bracket, if it is, go inside the bracket instead of deleting it
            # figure out how to show this

        pass



# function to detect optionmenu changes
def options_callback(var, index, mode):

    print(dict['gui']['option choices'].get())

    if dict['gui']['option choices'].get() == 'Scientific':

        scientific()



# scientific calculator display configuration
def scientific():

    # sizing
    root.geometry('700x675')

    # graphical setup
    dict['gui']['equation'] = tk.Label(root, text = '')
    dict['gui']['equation'].configure(font=('Arial', 40, ''))
    dict['gui']['equation'].place(x = 0, y = 10)

    dict['gui']['display'] = tk.Label(root, text = '0')
    dict['gui']['display'].configure(font=('Arial', 75, 'bold'))
    dict['gui']['display'].place(x = 0, y = 80)

    dict['gui']['roundlabel'] = tk.Label(root, text = 'Round to              decimal points')
    dict['gui']['roundlabel'].configure(font=('Arial', 15, 'bold'))
    dict['gui']['roundlabel'].place(x = 370, y = 190)



    # decimal changer
    dict['numbers']['roundchoice'] = StringVar(root)
    dict['numbers']['roundchoice'].set(11)

    dict['gui']['roundnumbers'] = OptionMenu(root, dict['numbers']['roundchoice'], 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    dict['gui']['roundnumbers'].configure(font=('Arial', 15, 'bold'))
    dict['gui']['roundnumbers'].place(x = 470, y = 185)



    # options to switch between calculators
    dict['gui']['options'] = OptionMenu(root, dict['gui']['option choices'], 'Scientific', 'Quadratic', 'Factoring')
    dict['gui']['options'].configure(font=('Arial', 15, 'bold'))
    dict['gui']['options'].place(x = 10, y = 185)



    # create button information
    dict['gui']['buttons']['equal']          = tk.Button(root, text='=',                  anchor='center', bg='DarkSlateGray2', command=lambda:calculate())

    # column 7
    dict['gui']['buttons']['clear']          = tk.Button(root, text='CE',                 anchor='center', bg='lightcoral',     command=lambda:clear())
    dict['gui']['buttons']['divide']         = tk.Button(root, text='/',                  anchor='center', bg='gainsboro',      command=lambda:meth(' / '))
    dict['gui']['buttons']['multiply']       = tk.Button(root, text='x',                  anchor='center', bg='gainsboro',      command=lambda:meth(' * '))
    dict['gui']['buttons']['minus']          = tk.Button(root, text='-',                  anchor='center', bg='gainsboro',      command=lambda:meth(' _ '))
    dict['gui']['buttons']['plus']           = tk.Button(root, text='+',                  anchor='center', bg='gainsboro',      command=lambda:meth(' + '))

    # column 6
    dict['gui']['buttons']['modulus']        = tk.Button(root, text='%',                  anchor='center', bg='gainsboro',      command=lambda:meth(' % '))
    dict['gui']['buttons']['num9']           = tk.Button(root, text='9',                  anchor='center', bg='white',          command=lambda:assign(9))
    dict['gui']['buttons']['num6']           = tk.Button(root, text='6',                  anchor='center', bg='white',          command=lambda:assign(6))
    dict['gui']['buttons']['num3']           = tk.Button(root, text='3',                  anchor='center', bg='white',          command=lambda:assign(3))
    dict['gui']['buttons']['decimal']        = tk.Button(root, text='.',                  anchor='center', bg='white',          command=lambda:assign_decimal())

    # column 5
    dict['gui']['buttons']['close brackets'] = tk.Button(root, text=')',                  anchor='center', bg='gainsboro',      command=lambda:brackets(False))
    dict['gui']['buttons']['num8']           = tk.Button(root, text='8',                  anchor='center', bg='white',          command=lambda:assign(8))
    dict['gui']['buttons']['num5']           = tk.Button(root, text='5',                  anchor='center', bg='white',          command=lambda:assign(5))
    dict['gui']['buttons']['num2']           = tk.Button(root, text='2',                  anchor='center', bg='white',          command=lambda:assign(2))
    dict['gui']['buttons']['num0']           = tk.Button(root, text='0',                  anchor='center', bg='white',          command=lambda:assign(0))

    # column 4
    dict['gui']['buttons']['open brackets']  = tk.Button(root, text='(',                  anchor='center', bg='gainsboro',      command=lambda:brackets(True))
    dict['gui']['buttons']['num7']           = tk.Button(root, text='7',                  anchor='center', bg='white',          command=lambda:assign(7))
    dict['gui']['buttons']['num4']           = tk.Button(root, text='4',                  anchor='center', bg='white',          command=lambda:assign(4))
    dict['gui']['buttons']['num1']           = tk.Button(root, text='1',                  anchor='center', bg='white',          command=lambda:assign(1))
    dict['gui']['buttons']['integer']        = tk.Button(root, text='+/-',                anchor='center', bg='white',          command=lambda:negative())

    # column 3
    dict['gui']['buttons']['memory recall']  = tk.Button(root, text='MR',                 anchor='center', bg='gainsboro',      command=lambda:memoryrecall())
    dict['gui']['buttons']['factorial']      = tk.Button(root, text='x!',                 anchor='center', bg='gainsboro',      command=lambda:factorials())
    dict['gui']['buttons']['exponent']       = tk.Button(root, text='x' + get_super('y'), anchor='center', bg='gainsboro',      command=lambda:exponent())
    dict['gui']['buttons']['squared']        = tk.Button(root, text='x' + get_super('2'), anchor='center', bg='gainsboro',      command=lambda:exponent(2))
    dict['gui']['buttons']['square root']    = tk.Button(root, text='sqr',                anchor='center', bg='gainsboro',      command=lambda:square_root())

    # column 2
    dict['gui']['buttons']['memory add']     = tk.Button(root, text='MS',                 anchor='center', bg='gainsboro',      command=lambda:memorystore())
    dict['gui']['buttons']['shift']          = tk.Button(root, text='Inv',                anchor='center', bg='gainsboro',      command=lambda:shifte())
    dict['gui']['buttons']['sine']           = tk.Button(root, text='sin',                anchor='center', bg='gainsboro',      command=lambda:trigonometry(True))
    dict['gui']['buttons']['cosine']         = tk.Button(root, text='cos',                anchor='center', bg='gainsboro',      command=lambda:trigonometry(False))
    dict['gui']['buttons']['tangent']        = tk.Button(root, text='tan',                anchor='center', bg='gainsboro',      command=lambda:trigonometry())

    # column 1
    dict['gui']['buttons']['memory clear']   = tk.Button(root, text='MC',                 anchor='center', bg='gainsboro',      command=lambda:memoryclear())
    dict['gui']['buttons']['pi']             = tk.Button(root, text='pi',                 anchor='center', bg='gainsboro',      command=lambda:pi())
    dict['gui']['buttons']['e']              = tk.Button(root, text='e',                  anchor='center', bg='gainsboro',      command=lambda:e())
    dict['gui']['buttons']['log']            = tk.Button(root, text='log',                anchor='center', bg='gainsboro',      command=lambda:logarithm())
    dict['gui']['buttons']['answer']         = tk.Button(root, text='Ans',                anchor='center', bg='gainsboro',      command=lambda:answer())



    # create button fonts
    dict['gui']['buttons']['equal'].         configure(font=('Arial', 25, 'bold'))

    # column 7
    dict['gui']['buttons']['clear'].         configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['divide'].        configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['multiply'].      configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['minus'].         configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['plus'].          configure(font=('Arial', 25, 'bold'))

    # column 6
    dict['gui']['buttons']['modulus'].       configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num9'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num6'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num3'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['decimal'].       configure(font=('Arial', 25, 'bold'))

    # column 5
    dict['gui']['buttons']['close brackets'].configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num8'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num5'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num2'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num0'].          configure(font=('Arial', 25, 'bold'))

    # column 4
    dict['gui']['buttons']['open brackets']. configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num7'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num4'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['num1'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['integer'].       configure(font=('Arial', 25, 'bold'))

    # column 3
    dict['gui']['buttons']['memory recall']. configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['factorial'].     configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['exponent'].      configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['squared'].       configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['square root'].   configure(font=('Arial', 25, 'bold'))

    # column 2
    dict['gui']['buttons']['memory add'].    configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['shift'].         configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['sine'].          configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['cosine'].        configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['tangent'].       configure(font=('Arial', 25, 'bold'))

    # column 1
    dict['gui']['buttons']['memory clear'].  configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['pi'].            configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['e'].             configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['log'].           configure(font=('Arial', 25, 'bold'))
    dict['gui']['buttons']['answer'].        configure(font=('Arial', 25, 'bold'))


    
    # place buttons
    dict['gui']['buttons']['equal'].         place(x = 0,   y = 600, width = 700, height = 75)

    # column 7
    dict['gui']['buttons']['clear'].         place(x = 600, y = 225, width = 100, height = 75)
    dict['gui']['buttons']['divide'].        place(x = 600, y = 300, width = 100, height = 75)
    dict['gui']['buttons']['multiply'].      place(x = 600, y = 375, width = 100, height = 75)
    dict['gui']['buttons']['minus'].         place(x = 600, y = 450, width = 100, height = 75)
    dict['gui']['buttons']['plus'].          place(x = 600, y = 525, width = 100, height = 75)

    # column 6
    dict['gui']['buttons']['modulus'].       place(x = 500, y = 225, width = 100, height = 75)
    dict['gui']['buttons']['num9'].          place(x = 500, y = 300, width = 100, height = 75)
    dict['gui']['buttons']['num6'].          place(x = 500, y = 375, width = 100, height = 75)
    dict['gui']['buttons']['num3'].          place(x = 500, y = 450, width = 100, height = 75)
    dict['gui']['buttons']['decimal'].       place(x = 500, y = 525, width = 100, height = 75)

    # column 5
    dict['gui']['buttons']['close brackets'].place(x = 400, y = 225, width = 100, height = 75)
    dict['gui']['buttons']['num8'].          place(x = 400, y = 300, width = 100, height = 75)
    dict['gui']['buttons']['num5'].          place(x = 400, y = 375, width = 100, height = 75)
    dict['gui']['buttons']['num2'].          place(x = 400, y = 450, width = 100, height = 75)
    dict['gui']['buttons']['num0'].          place(x = 400, y = 525, width = 100, height = 75)

    # column 4
    dict['gui']['buttons']['open brackets']. place(x = 300, y = 225, width = 100, height = 75)
    dict['gui']['buttons']['num7'].          place(x = 300, y = 300, width = 100, height = 75)
    dict['gui']['buttons']['num4'].          place(x = 300, y = 375, width = 100, height = 75)
    dict['gui']['buttons']['num1'].          place(x = 300, y = 450, width = 100, height = 75)
    dict['gui']['buttons']['integer'].       place(x = 300, y = 525, width = 100, height = 75)

    # column 3
    dict['gui']['buttons']['memory recall']. place(x = 200, y = 225, width = 100, height = 75)
    dict['gui']['buttons']['factorial'].     place(x = 200, y = 300, width = 100, height = 75)
    dict['gui']['buttons']['exponent'].      place(x = 200, y = 375, width = 100, height = 75)
    dict['gui']['buttons']['squared'].       place(x = 200, y = 450, width = 100, height = 75)
    dict['gui']['buttons']['square root'].   place(x = 200, y = 525, width = 100, height = 75)

    # column 2
    dict['gui']['buttons']['memory add'].    place(x = 100, y = 225, width = 100, height = 75)
    dict['gui']['buttons']['shift'].         place(x = 100, y = 300, width = 100, height = 75)
    dict['gui']['buttons']['sine'].          place(x = 100, y = 375, width = 100, height = 75)
    dict['gui']['buttons']['cosine'].        place(x = 100, y = 450, width = 100, height = 75)
    dict['gui']['buttons']['tangent'].       place(x = 100, y = 525, width = 100, height = 75)

    # column 1
    dict['gui']['buttons']['memory clear'].  place(x = 0,   y = 225, width = 100, height = 75)
    dict['gui']['buttons']['pi'].            place(x = 0,   y = 300, width = 100, height = 75)
    dict['gui']['buttons']['e'].             place(x = 0,   y = 375, width = 100, height = 75)
    dict['gui']['buttons']['log'].           place(x = 0,   y = 450, width = 100, height = 75)
    dict['gui']['buttons']['answer'].        place(x = 0,   y = 525, width = 100, height = 75)



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
    dict['gui']['option choices'] = StringVar(root)
    dict['gui']['option choices'].trace('w', options_callback)
    dict['gui']['option choices'].set('Scientific')



    # keybindings
    keyboard.hook(lambda _:keybindings())

    # prevent calculator from being resized
    root.resizable(False, False)

    # run the gui
    root.mainloop()

if __name__ == '__main__':

    main()