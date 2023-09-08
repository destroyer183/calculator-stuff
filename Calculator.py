import tkinter as tk
from tkinter import *
import keyboard
import os

# setup
root = tk.Tk()

root.title("Calculator")

root.geometry('350x500')

if os.name == "nt":
    try:
        import ctypes
        
        awareness = ctypes.c_int()
        errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
        success = ctypes.windll.user32.SetProcessDPIAware()
    except:pass 

# variables
output = 0
input1 = 0
input2 = 0
memory = 0
addition = False
subtraction = False
multiplication = False
division = False
firstnum = True

# graphical setup
equation = tk.Label(root, text = "")
equation.configure(font=("Arial", 20, ""))
equation.place(x = 0, y = 0)

display = tk.Label(root, text = "")
display.configure(font=("Arial", 40, "bold"))
display.place(x = 0, y = 40)

roundlabel = tk.Label(root, text = "Round to                      decimal points")
roundlabel.place(x = 150, y = 120)

roundchoice = StringVar(root)
roundchoice.set(10)

# the function bound to the "equals" button to output a result for an equation.
def calculate():
    global output, input1, input2, display, equation, firstnum
    if division      : input1 = float(input1) / float(input2)
    if multiplication: input1 = float(input1) * float(input2)
    if addition      : input1 = float(input1) + float(input2)
    if subtraction   : input1 = float(input1) - float(input2)
    output = input1

    input1 = round(input1, int(roundchoice.get()))
    output = round(output, int(roundchoice.get()))

    firstnum = True

    # displaying the numbers and outputs
    display.configure(text= output)
    equation.configure(text= equation.cget("text") + " =")
    print(output)

# the function bound to the addition button to tell the calculate function which mathematical operation to perform when it is pressed.
def math(operation):
    global output, input1, input2, firstnum, addition, subtraction, multiplication, division, display, equation
    # this section checks if another operation is already being used with two numbers, and this will perform that equation, and then allow the user to continue.
    # this allows more than two numbers to be inputted before calculating the output.
    if output == 0:
        if operation == 1: addition       = True
        if operation == 2: subtraction    = True
        if operation == 3: multiplication = True
        if operation == 4: division       = True

        if input1 != 0 and input2 != 0:
            if division      : input1   = float(input1) / float(input2); input2 = 0
            if multiplication: input1   = float(input1) * float(input2); input2 = 0
            if addition      : input1   = float(input1) + float(input2); input2 = 0
            if subtraction   : input1   = float(input1) - float(input2); input2 = 0
            firstnum                    = False
            input1                      = round(float(input1), int(roundchoice.get()))
        
    # this sets which function will be used when the equals button is pressed.
        firstnum = False
        if addition      : equation.configure(text= equation.cget("text") + " + "); subtraction, multiplication, division       = False
        if subtraction   : equation.configure(text= equation.cget("text") + " - "); addition,    multiplication, division       = False
        if multiplication: equation.configure(text= equation.cget("text") + " x "); addition,    subtraction,    division       = False
        if division      : equation.configure(text= equation.cget("text") + " / "); addition,    subtraction,    multiplication = False
        display.configure(text= "0")
        
    # this section checks if an equation has been completed, and it will make the output the first number in the equation with the correct operation sign next to it.
    else:
        if addition           : addition       = False
        if subtraction        : subtraction    = False
        if multiplication     : multiplication = False
        if division           : division       = False
        input2 = 0
        output = 0

# function bound to the decimal button to allow decimal numbers to be inputted.
def assigndecimal():
    if firstnum:
        # this checks if the number already has a decimal to avoid multiple decimal points which would cause issues.
        if "." not in str(input1): input1 = str(input1) + "."
        equation.configure(text= equation.cget("text") + ".")
        display.configure(text=input1)

    else:
        if "." not in str(input2): input2 = str(input2) + "."
        display.configure(text=input2)
    print(input1)
    print(input2)

# function bound to the integer button to allow the user to use both positive and negative integers.
def assigninteger():
    global input1, input2
    # this checks if the negative sign needs to be on the exponent number and will change it accordingly.
    if firstnum: input1 *= -1; display.configure(text= str(input1))
    else       : input2 *= -1; display.configure(text=input2)
    print(input1)
    print(input2)

# function bound to the zero button to input numbers.
def assign(x):
    global input1, input2
    # this checks which number needs to be changed based on a boolean value.
    if firstnum:
        if input1 == 0: input1 += x
        else          : input1 = input1 * 10 + x
        display.configure(text=input1)
        equation.configure(text= equation.cget("text") + str(x))

    else:
        if input2 == 0: input2 += x
        else          : input2 = input2 * 10 + x
        display.configure(text=input2)
        equation.configure(text= equation.cget("text") + str(x))
    print(input1)
    print(input2)

# a function to handle all key inputs
def keybindings():
    if keyboard.is_pressed("shift+="):math(1)
    if keyboard.is_pressed("-")      :math(2)
    if keyboard.is_pressed("shift+8"):math(3)
    if keyboard.is_pressed("/")      :math(4)
    if keyboard.is_pressed(".")      :assigndecimal()
    if keyboard.is_pressed("shift+-"):assigninteger()
    if keyboard.is_pressed("enter")  :calculate()
    if keyboard.is_pressed("0")      :assign(0)
    if keyboard.is_pressed("1")      :assign(1)
    if keyboard.is_pressed("2")      :assign(2)
    if keyboard.is_pressed("3")      :assign(3)
    if keyboard.is_pressed("4")      :assign(4)
    if keyboard.is_pressed("5")      :assign(5)
    if keyboard.is_pressed("6")      :assign(6)
    if keyboard.is_pressed("7")      :assign(7)
    if keyboard.is_pressed("8")      :assign(8)
    if keyboard.is_pressed("9")      :assign(9)
    if keyboard.is_pressed("esc")    :clearall()

# function bound to the clear equation button that clears the variables and display.
def clearall():
    global output, input1, input2, addition, subtraction, multiplication, division, firstnum
    output         = 0
    input1         = 0
    input2         = 0
    addition       = False
    subtraction    = False
    multiplication = False
    division       = False
    firstnum       = True

    display.configure(text="")
    equation.configure(text="")

# function bound to the memory recall button to display the number stored in memory.
def memoryrecall():
    global input1, input2
    # this checks which number needs to be changed based on a boolean value.
    if firstnum: input1 = memory; display.configure(text=input1); equation.configure(text=equation.cget("text") + str(input1))
    else       : input2 = memory; display.configure(text=input2); equation.configure(text=equation.cget("text") + str(input2))

# function bound to the memory clear button that will clear the number stored in the memory.
def memoryclear():
    global memory
    memory = 0

# function bound to the memory add button to set the memory number to the number displayed.
def memoryadd():
    global memory
    memory = float(display.cget("text"))

def main():

    roundnumbers = OptionMenu(root, roundchoice, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    roundnumbers.place(x = 205, y = 110)

    # create buttons
    # create buttons
    equal      = tk.Button(root, text="=",   anchor='center', bg='DarkSlateGray2', command=lambda:calculate())
    plus       = tk.Button(root, text="+",   anchor='center', bg='gainsboro',      command=lambda:math(1))
    minus      = tk.Button(root, text="-",   anchor='center', bg='gainsboro',      command=lambda:math(2))
    multiply   = tk.Button(root, text="x",   anchor='center', bg='gainsboro',      command=lambda:math(3))
    divide     = tk.Button(root, text="/",   anchor='center', bg='gainsboro',      command=lambda:math(4))
    decimal    = tk.Button(root, text=".",   anchor='center', bg='white',          command=lambda:assigndecimal())
    integer    = tk.Button(root, text="+/-", anchor='center', bg='white',          command=lambda:assigninteger())
    num0       = tk.Button(root, text="0",   anchor='center', bg='white',          command=lambda:assign(0))
    num1       = tk.Button(root, text="1",   anchor='center', bg='white',          command=lambda:assign(1))
    num2       = tk.Button(root, text="2",   anchor='center', bg='white',          command=lambda:assign(2))
    num3       = tk.Button(root, text="3",   anchor='center', bg='white',          command=lambda:assign(3))
    num4       = tk.Button(root, text="4",   anchor='center', bg='white',          command=lambda:assign(4))
    num5       = tk.Button(root, text="5",   anchor='center', bg='white',          command=lambda:assign(5))
    num6       = tk.Button(root, text="6",   anchor='center', bg='white',          command=lambda:assign(6))
    num7       = tk.Button(root, text="7",   anchor='center', bg='white',          command=lambda:assign(7))
    num8       = tk.Button(root, text="8",   anchor='center', bg='white',          command=lambda:assign(8))
    num9       = tk.Button(root, text="9",   anchor='center', bg='white',          command=lambda:assign(9))
    clear      = tk.Button(root, text="CE",  anchor='center', bg='lightcoral',     command=lambda:clearall())
    memrecall  = tk.Button(root, text="MR",  anchor='center', bg='gainsboro',      command=lambda:memoryrecall())
    memclear   = tk.Button(root, text="MC",  anchor='center', bg='gainsboro',      command=lambda:memoryclear())
    memadd     = tk.Button(root, text="MS",  anchor='center', bg='gainsboro',      command=lambda:memoryadd())

    # create button fonts
    equal.     configure(font=("Arial", 20, "bold"))
    plus.      configure(font=("Arial", 20, "bold"))
    minus.     configure(font=("Arial", 20, "bold"))
    multiply.  configure(font=("Arial", 20, "bold"))
    divide.    configure(font=("Arial", 20, "bold"))
    decimal.   configure(font=("Arial", 20, "bold"))
    integer.   configure(font=("Arial", 20, "bold"))
    num0.      configure(font=("Arial", 20, "bold"))
    num1.      configure(font=("Arial", 20, "bold"))
    num2.      configure(font=("Arial", 20, "bold"))
    num3.      configure(font=("Arial", 20, "bold"))
    num4.      configure(font=("Arial", 20, "bold"))
    num5      .configure(font=("Arial", 20, "bold"))
    num6.      configure(font=("Arial", 20, "bold"))
    num7.      configure(font=("Arial", 20, "bold"))
    num8.      configure(font=("Arial", 20, "bold"))
    num9.      configure(font=("Arial", 20, "bold"))
    clear.     configure(font=("Arial", 20, "bold"))
    memrecall. configure(font=("Arial", 20, "bold"))
    memclear.  configure(font=("Arial", 20, "bold"))
    memadd.    configure(font=("Arial", 20, "bold"))

    # place buttons
    equal.    place(x = 0,     y = 430, height = 60, width = 350)
    plus.     place(x = 262.5, y = 380, height = 60, width = 87.5)
    minus.    place(x = 262.5, y = 320, height = 60, width = 87.5)
    multiply. place(x = 262.5, y = 260, height = 60, width = 87.5)
    divide.   place(x = 262.5, y = 200, height = 60, width = 87.5)
    decimal.  place(x = 175,   y = 380, height = 60, width = 87.5)
    integer.  place(x = 0,     y = 380, height = 60, width = 87.5)
    num0.     place(x = 87.5,  y = 380, height = 60, width = 87.5)
    num3.     place(x = 175,   y = 320, height = 60, width = 87.5)
    num1.     place(x = 0,     y = 320, height = 60, width = 87.5)
    num2.     place(x = 87.5,  y = 320, height = 60, width = 87.5)
    num6.     place(x = 175,   y = 260, height = 60, width = 87.5)
    num4.     place(x = 0,     y = 260, height = 60, width = 87.5)
    num5.     place(x = 87.5,  y = 260, height = 60, width = 87.5)
    num9.     place(x = 175,   y = 200, height = 60, width = 87.5)
    num7.     place(x = 0,     y = 200, height = 60, width = 87.5)
    num8.     place(x = 87.5,  y = 200, height = 60, width = 87.5)
    clear.    place(x = 262.5, y = 140, height = 60, width = 87.5)
    memrecall.place(x = 175,   y = 140, height = 60, width = 87.5)
    memclear. place(x = 0,     y = 140, height = 60, width = 87.5)
    memadd.   place(x = 87.5,  y = 140, height = 60, width = 87.5)

    # keybindings
    keyboard.on_press_key("=" or "-" or "/" or "." or "enter" or "0" or "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" or "esc", lambda _:keybindings())

    root.resizable(False, False)
    root.mainloop()
    
if __name__ == "__main__":
    main()