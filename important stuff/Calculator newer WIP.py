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

    def __init__(self, gui) -> None:
        
        self.gui = gui
        
    def scientific(self):

        self.gui = Scientific_gui.Scientific(self.gui)

        self.gui.create_gui()

        # options to switch between calculators
        self.gui.parent.options = OptionMenu(self.gui.parent, Window.option_choices, 'Scientific', 'Quadratic', 'Factoring')
        self.gui.parent.options.configure(font=('Arial', 15, 'bold'))
        self.gui.parent.options.place(x = 10, y = 185)




    # Factoring calculator display configuration
    def factoring(self):



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
    def quadratic(self):

        pass



    # Trigonometric calculator display configuration
    def trigonometry(self):

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

    Window.option_choices = StringVar(Window.root.gui)
    Window.option_choices.trace('w', options_callback)
    Window.option_choices.set('Scientific')

    # run the gui
    Window.root.gui.parent.mainloop()

    

if __name__ == '__main__':

    main()