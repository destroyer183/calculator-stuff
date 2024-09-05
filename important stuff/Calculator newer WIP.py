import tkinter as tk
from tkinter import *
import os
import Scientific
import Factoring
import Quadratic
import Trigonometry
import Variable


''' NOTES 

things to update:

allow the exponent button to be toggled to allow for complex equations to be superscripted

make 'backspace' work like regular backspace (bug: if an operator is deleted, the number at the end of the equation text won't be in the display text.)
perhaps make a class variable list in the 'Gui' class, and every time the user makes an input, 
create a new class object with the same attribute values, and store it in the class variable.
when the user presses 'backspace' load the last element in the class variable list, and then pop it out.
clear this list whenever the user clears the equation

use the above concept to create a way for the user to see the session history, and load the answers for that.
make a separate class variable list that only stores a new element when the user hits 'calculate'

MAKE IT ONLY WORK IF IT IS ON THE TOP LAYER OF THE SCREEN





MAKE SOMETHING TO SOLVE FOR A VARIABLE






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



# main class to handle all the gui stuff
class Window:

    instance: "Window" = None
    option_choices = None

    def __init__(self, gui) -> None:
        
        self.gui = Scientific.Gui(gui)
        
    # scientific calculator display configuration
    def make_gui(self, gui_type):

        if   gui_type == 'Scientific'  : self.gui = Scientific.Gui(self.gui.parent)
        elif gui_type == 'Factoring'   : self.gui = Factoring.Gui(self.gui.parent)
        elif gui_type == 'Quadratic'   : self.gui = Quadratic.Gui(self.gui.parent)
        elif gui_type == 'Trigonometry': self.gui = Trigonometry.Gui(self.gui.parent)
        elif gui_type == 'Variable'    : self.gui = Variable.Gui(self.gui.parent)

        self.gui.create_gui()

        # options to switch between calculators
        self.gui.parent.options = OptionMenu(self.gui.parent, Window.option_choices, 'Scientific', 'Factoring', 'Quadratic', 'Trigonometry', 'Variable')
        self.gui.parent.options.configure(font=('Arial', 15, 'bold'))

        if   gui_type == 'Scientific'  : self.gui.parent.options.place(x = 10, y = 185)
        elif gui_type == 'Factoring'   : self.gui.parent.options.place(x = 10, y = 185)
        elif gui_type == 'Quadratic'   : self.gui.parent.options.place(x = 10, y = 185)
        elif gui_type == 'Trigonometry': self.gui.parent.options.place(x = 472, y = 660)
        elif gui_type == 'Variable'    : self.gui.parent.options.place(x = 10, y = 185)

        

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

    Window.instance.make_gui(Window.option_choices.get())



def main():

    Window.instance = Window(tk.Tk())

    # override windows scaling
    if os.name == 'nt':
        try:
            import ctypes
            
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
            success   = ctypes.windll.user32.SetProcessDPIAware()
        except:pass 
 
    Window.option_choices = StringVar(Window.instance.gui.parent)
    Window.option_choices.trace('w', options_callback)
    Window.option_choices.set('Scientific')

    # run the gui
    Window.instance.gui.parent.mainloop()

    

if __name__ == '__main__':

    main()