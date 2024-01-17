import tkinter as tk
from tkinter import *
import keyboard
import os
import math
from equation_parser import *

# brainstorming
# how do I reconfigure the buttons to work properly with the equation parser
# every time a number or operator is pressed, add the operator and then a space (with a few exceptions like factorials)
# every time a closed bracket is pressed, add it in one space to the left of the end

# setup
root = tk.Tk()

root.title('Calculator')

root.geometry('525x500')

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

dict['numbers']['equation']    = ''
dict['numbers']['output']      = 0
dict['numbers']['memory']      = 0

dict['operator']['addition']       = False
dict['operator']['subtraction']    = False
dict['operator']['multiplication'] = False
dict['operator']['division']       = False
dict['operator']['exponent']       = False

dict['gui']['equation text'] = ''
dict['gui']['display text']  = ''

# graphical setup
dict['gui']['equation'] = tk.Label(root, text = '')
dict['gui']['equation'].configure(font=('Arial', 20, ''))
dict['gui']['equation'].place(x = 0, y = 0)

dict['gui']['display'] = tk.Label(root, text = '')
dict['gui']['display'].configure(font=('Arial', 40, 'bold'))
dict['gui']['display'].place(x = 0, y = 40)

dict['gui']['roundlabel'] = tk.Label(root, text = 'Round to                      decimal points')
dict['gui']['roundlabel'].place(x = 325, y = 120)

dict['numbers']['roundchoice'] = StringVar(root)
dict['numbers']['roundchoice'].set(10)

dict['gui']['roundnumbers'] = OptionMenu(root, dict['numbers']['roundchoice'], 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
dict['gui']['roundnumbers'].place(x = 380, y = 110)



# the function bound to the 'equals' button to output a result for an equation.
def calculate():

    dict['numbers']['output'] = equation_parser(dict['numbers']['equation'])

    dict['numbers']['output'] = str(round(float(dict['numbers']['output']), int(dict['numbers']['roundchoice'].get())))

    # displaying the numbers and outputs
    dict['gui']['display'].configure(text= dict['numbers']['output'])

    dict['gui']['equation'].configure(text = dict['gui']['equation text'])



# the function bound to the addition button to tell the calculate function which mathematical operation to perform when it is pressed.
def meth(operation):

    if operation == 1:

        dict['numbers']['equation'] += '+ '

        dict['gui']['equation text'] += '+ '

        dict['gui']['display text'] = ''



    if operation == 2:

        dict['numbers']['equation'] += '- '

        dict['gui']['equation text'] += '- '

        dict['gui']['display text'] = ''



    if operation == 3:

        dict['numbers']['equation'] += '* '

        dict['gui']['equation text'] += '* '

        dict['gui']['display text'] = ''



    if operation == 4:

        dict['numbers']['equation'] += '/ '

        dict['gui']['equation text'] += '/ '

        dict['gui']['display text'] = ''

    

    dict['gui']['display'].configure(text = '0')

    dict['gui']['equation'].configure(text = dict['gui']['equation text'])



# function to convert to superscript
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(''.join(normal), ''.join(super_s))

    return x.translate(res)



# function bound to the decimal button to allow decimal numbers to be inputted.
def assigndecimal():

    if '.' not in dict['gui']['display text']:

        dict['numbers']['equation'] += '.'

        dict['gui']['equation text'] += '.'

        dict['gui']['display text']  += '.'



    dict['gui']['display'].configure(text = dict['gui']['display text'])

    dict['gui']['equation'].configure(text = dict['gui']['equation text'])



# function bound to the integer button to allow the user to toggle a number between positive and negative.
def assigninteger():

    if dict['gui']['equation text'][-1] == ' ':

        dict['numbers']['equation'] += '-'

        dict['gui']['equation text'] += '-'

        dict['gui']['display text']  += '-'



    elif dict['gui']['equation text'][-1] == '-':

        dict['numbers']['equation'].pop(-1)

        dict['gui']['equation text'].pop(-1)

        dict['gui']['display text'].pop(-1)

    

    elif dict['gui']['equation text'][-1] in '1234567890.':

        for i in range(len(dict['gui']['equation text']), 0, -1):

            if dict['gui']['equation text'][i] == ' ':

                dict['numbers']['equation'].insert(i, '-')

                dict['gui']['equation text'].insert(i, '-')

                dict['gui']['display text'].insert(0, '-')



            if dict['gui']['equation text'][i] == '-':

                dict['numbers']['equation'].pop(i)

                dict['gui']['equation text'].pop(i)

                dict['gui']['display text'].pop(i)



    dict['gui']['display'].configure(text = dict['gui']['display text'])

    dict['gui']['equation'].configure(text = dict['gui']['equation text'])

            

# function to input numbers.
def assign(x):

    dict['numbers']['equation'] += str(x) + ' '

    dict['gui']['equation text'] += str(x) + ' '

    dict['gui']['display text']  += str(x)

    dict['gui']['display'].configure(text = dict['gui']['display text'])



# function bound to the exponent button that allows for exponents to be used.
def exponent(ctrlexp):

    if ctrlexp != -1:

        dict['numbers']['equation'] += '^ ' + str(ctrlexp)

        dict['gui']['equation text'] += '^ ' + str(ctrlexp)

        dict['gui']['display text'] = str(ctrlexp)

    

    else:

        dict['numbers']['equation'] += '^ '

        dict['gui']['equation text'] += '^ '

        dict['gui']['display text'] = '0'



    dict['gui']['display'].configure(text = dict['gui']['display text'])

    dict['gui']['equation'].configure(text = dict['gui']['equation text'])



def factorials():

    dict['numbers']['equation'] += '!'

    dict['gui']['equation text'] += '!'

    dict['gui']['display text']  = '0'



    dict['gui']['display'].configure(text = dict['gui']['display text'])

    dict['gui']['equation'].configure(text = dict['gui']['equation text'])



# a function to handle all key inputs
def keybindings():
    if keyboard.is_pressed('shift+='):meth(1)
    if keyboard.is_pressed('-')      :meth(2)
    if keyboard.is_pressed('shift+8'):meth(3)
    if keyboard.is_pressed('/')      :meth(4)
    if keyboard.is_pressed('shift+1'):factorials()
    if keyboard.is_pressed('.')      :assigndecimal()
    if keyboard.is_pressed('shift+-'):assigninteger()
    if keyboard.is_pressed('enter')  :calculate()
    if keyboard.is_pressed('0')      :assign(0)
    if keyboard.is_pressed('1')      :assign(1)
    if keyboard.is_pressed('2')      :assign(2)
    if keyboard.is_pressed('3')      :assign(3)
    if keyboard.is_pressed('4')      :assign(4)
    if keyboard.is_pressed('5')      :assign(5)
    if keyboard.is_pressed('6')      :assign(6)
    if keyboard.is_pressed('7')      :assign(7)
    if keyboard.is_pressed('8')      :assign(8)
    if keyboard.is_pressed('9')      :assign(9)
    if keyboard.is_pressed('ctrl+0') :exponent(0)
    if keyboard.is_pressed('ctrl+1') :exponent(1)
    if keyboard.is_pressed('ctrl+2') :exponent(2)
    if keyboard.is_pressed('ctrl+3') :exponent(3)
    if keyboard.is_pressed('ctrl+4') :exponent(4)
    if keyboard.is_pressed('ctrl+5') :exponent(5)
    if keyboard.is_pressed('ctrl+6') :exponent(6)
    if keyboard.is_pressed('ctrl+7') :exponent(7)
    if keyboard.is_pressed('ctrl+8') :exponent(8)
    if keyboard.is_pressed('ctrl+9') :exponent(9)
    if keyboard.is_pressed('shift+5'):exponent(0.5)
    if keyboard.is_pressed('shift+6'):exponent(-1)
    if keyboard.is_pressed('esc')    :clearall()



# function bound to the clear equation button that clears the variables and display.
def clearall():
    dict['numbers']['equation']    = ''
    dict['numbers']['output']      = 0

    dict['operator']['addition']       = False
    dict['operator']['subtraction']    = False
    dict['operator']['multiplication'] = False
    dict['operator']['division']       = False
    dict['operator']['exponent']       = False

    dict['gui']['equation text'] = ''
    dict['gui']['display text']  = ''

    dict['gui']['display'].configure(text = '')

    dict['gui']['equation'].configure(text = '')



# function bound to the memory recall button to display the number stored in memory.
def memoryrecall():

    dict['numbers']['equation'] += dict['numbers']['memory']

    dict['gui']['equation text'] += dict['numbers']['memory']

    dict['gui']['display text'] = dict['numbers']['memory']



# function bound to the memory clear button that will clear the number stored in the memory.
def memoryclear():

    dict['numbers']['memory'] = 0



# function bound to the memory add button to set the memory number to the number displayed.
def memoryadd():

    dict['numbers']['memory'] = float(dict['gui']['display text'])



def main():

    # add a modulus button
    # add bracket buttons
    # add trig buttons

    # create buttons
    equal      = tk.Button(root, text='=',                  anchor='center', bg='DarkSlateGray2', command=lambda:calculate())
    plus       = tk.Button(root, text='+',                  anchor='center', bg='gainsboro',      command=lambda:meth(1))
    minus      = tk.Button(root, text='-',                  anchor='center', bg='gainsboro',      command=lambda:meth(2))
    multiply   = tk.Button(root, text='x',                  anchor='center', bg='gainsboro',      command=lambda:meth(3))
    divide     = tk.Button(root, text='/',                  anchor='center', bg='gainsboro',      command=lambda:meth(4))
    decimal    = tk.Button(root, text='.',                  anchor='center', bg='white',          command=lambda:assigndecimal())
    integer    = tk.Button(root, text='+/-',                anchor='center', bg='white',          command=lambda:assigninteger())
    num0       = tk.Button(root, text='0',                  anchor='center', bg='white',          command=lambda:assign(0))
    num3       = tk.Button(root, text='3',                  anchor='center', bg='white',          command=lambda:assign(3))
    num1       = tk.Button(root, text='1',                  anchor='center', bg='white',          command=lambda:assign(1))
    num2       = tk.Button(root, text='2',                  anchor='center', bg='white',          command=lambda:assign(2))
    num6       = tk.Button(root, text='6',                  anchor='center', bg='white',          command=lambda:assign(6))
    num4       = tk.Button(root, text='4',                  anchor='center', bg='white',          command=lambda:assign(4))
    num5       = tk.Button(root, text='5',                  anchor='center', bg='white',          command=lambda:assign(5))
    num9       = tk.Button(root, text='9',                  anchor='center', bg='white',          command=lambda:assign(9))
    num7       = tk.Button(root, text='7',                  anchor='center', bg='white',          command=lambda:assign(7))
    num8       = tk.Button(root, text='8',                  anchor='center', bg='white',          command=lambda:assign(8))
    factoria   = tk.Button(root, text='!x',                 anchor='center', bg='gainsboro',      command=lambda:factorials())
    squareroot = tk.Button(root, text='sqr',                anchor='center', bg='gainsboro',      command=lambda:exponent(0.5))
    squared    = tk.Button(root, text='x' + get_super('2'), anchor='center', bg='gainsboro',      command=lambda:exponent(2))
    exponente  = tk.Button(root, text='x' + get_super('y'), anchor='center', bg='gainsboro',      command=lambda:exponent(-1))
    clear      = tk.Button(root, text='CE',                 anchor='center', bg='lightcoral',     command=lambda:clearall())
    memrecall  = tk.Button(root, text='MR',                 anchor='center', bg='gainsboro',      command=lambda:memoryrecall())
    memclear   = tk.Button(root, text='MC',                 anchor='center', bg='gainsboro',      command=lambda:memoryclear())
    memadd     = tk.Button(root, text='MS',                 anchor='center', bg='gainsboro',      command=lambda:memoryadd())

    # create button fonts
    equal.     configure(font=('Arial', 20, 'bold'))
    plus.      configure(font=('Arial', 20, 'bold'))
    minus.     configure(font=('Arial', 20, 'bold'))
    multiply.  configure(font=('Arial', 20, 'bold'))
    divide.    configure(font=('Arial', 20, 'bold'))
    decimal.   configure(font=('Arial', 20, 'bold'))
    integer.   configure(font=('Arial', 20, 'bold'))
    num0.      configure(font=('Arial', 20, 'bold'))
    num3.      configure(font=('Arial', 20, 'bold'))
    num1.      configure(font=('Arial', 20, 'bold'))
    num2.      configure(font=('Arial', 20, 'bold'))
    num6.      configure(font=('Arial', 20, 'bold'))
    num4.      configure(font=('Arial', 20, 'bold'))
    num5      .configure(font=('Arial', 20, 'bold'))
    num9.      configure(font=('Arial', 20, 'bold'))
    num7.      configure(font=('Arial', 20, 'bold'))
    num8.      configure(font=('Arial', 20, 'bold'))
    factoria.  configure(font=('Arial', 20, 'bold'))
    squareroot.configure(font=('Arial', 20, 'bold'))
    squared   .configure(font=('Arial', 20, 'bold'))
    exponente. configure(font=('Arial', 20, 'bold'))
    clear.     configure(font=('Arial', 20, 'bold'))
    memrecall. configure(font=('Arial', 20, 'bold'))
    memclear.  configure(font=('Arial', 20, 'bold'))
    memadd.    configure(font=('Arial', 20, 'bold'))
    
    # place buttons
    equal.     place(x = 0,     y = 440, height = 60, width = 526)
    plus.      place(x = 437.5, y = 380, height = 60, width = 87.5)
    minus.     place(x = 437.5, y = 320, height = 60, width = 87.5)
    multiply.  place(x = 437.5, y = 260, height = 60, width = 87.5)
    divide.    place(x = 437.5, y = 200, height = 60, width = 87.5)
    decimal.   place(x = 350,   y = 380, height = 60, width = 87.5)
    integer.   place(x = 175,   y = 380, height = 60, width = 87.5)
    num0.      place(x = 262.5, y = 380, height = 60, width = 87.5)
    num3.      place(x = 350,   y = 320, height = 60, width = 87.5)
    num1.      place(x = 175,   y = 320, height = 60, width = 87.5)
    num2.      place(x = 262.5, y = 320, height = 60, width = 87.5)
    num6.      place(x = 350,   y = 260, height = 60, width = 87.5)
    num4.      place(x = 175,   y = 260, height = 60, width = 87.5)
    num5.      place(x = 262.5, y = 260, height = 60, width = 87.5)
    num9.      place(x = 350,   y = 200, height = 60, width = 87.5)
    num7.      place(x = 175,   y = 200, height = 60, width = 87.5)
    num8.      place(x = 262.5, y = 200, height = 60, width = 87.5)
    factoria.  place(x = 262.5, y = 80,  height = 60, width = 87.5)
    squareroot.place(x = 175,   y = 80,  height = 60, width = 87.5)
    squared.   place(x = 0,     y = 200, height = 60, width = 87.5)
    exponente. place(x = 87.5,  y = 200, height = 60, width = 87.5)
    clear.     place(x = 437.5, y = 140, height = 60, width = 87.5)
    memrecall. place(x = 350,   y = 140, height = 60, width = 87.5)
    memclear.  place(x = 175,   y = 140, height = 60, width = 87.5)
    memadd.    place(x = 262.5, y = 140, height = 60, width = 87.5)

    # keybindings
    keyboard.on_press_key('=' or '-' or '/' or '.' or 'enter' or '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9' or 'esc', lambda _:keybindings())

    root.resizable(False, False)
    root.mainloop()

if __name__ == '__main__':

    main()