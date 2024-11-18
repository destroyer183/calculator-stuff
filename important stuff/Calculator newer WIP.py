import tkinter as tk
from tkinter import *
import os
from gui_classes import Scientific, Factoring, Quadratic, TriangleTrig, UnitCircleTrig, Variable
import sys
from enum import Enum


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

command to compile:
pyinstaller --onefile --windowed --add-data=.:"gui_classes" --add-data=.:"parsers" -p gui_classes/ -p parsers/ "Calculator newer WIP.py"
'''

class GuiOptionChoices(Enum):
    Scientific     = 'Scientific'
    Factoring      = 'Factoring'
    Quadratic      = 'Quadratic'
    Trigonometry   = 'Trigonometry'
    TriangleTrig   = 'Triangle Trig'
    UnitCircleTrig = 'Unit Circle Trig'
    Variable       = 'Variable'



# if running from source, update the path to the parent directory
if __package__ is None and not hasattr(sys, 'frozen'):
    import os.path
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.realpath(path))



# main class to handle all the gui stuff
class Window:

    instance: "Window" = None
    option_choices = None
    trig_option_choices = None

    def __init__(self, gui) -> None:
        
        self.gui = Scientific.Gui(gui, Window)



    def full_clear_gui(self):

        self.gui.parent.unbind("<KeyRelease>")
        self.gui.parent.unbind("<Configure>")

        for widget in self.gui.parent.winfo_children():
            widget.destroy()
        


    # gui selection function
    def choose_gui(self):

        self.full_clear_gui()

        # make option menu to switch between calculators
        self.gui.parent.options = OptionMenu(self.gui.parent, Window.option_choices, 
                                             GuiOptionChoices.Scientific.value, 
                                             GuiOptionChoices.Factoring.value, 
                                             GuiOptionChoices.Quadratic.value, 
                                             GuiOptionChoices.Trigonometry.value, 
                                             GuiOptionChoices.Variable.value)

        match self.gui_type:
            case GuiOptionChoices.Scientific    : self.gui = Scientific.Gui(self.gui.parent, Window)
            case GuiOptionChoices.Factoring     : self.gui = Factoring.Gui(self.gui.parent, Window)
            case GuiOptionChoices.Quadratic     : self.gui = Quadratic.Gui(self.gui.parent, Window)
            case GuiOptionChoices.Trigonometry  : self.choose_trig_gui()
            case GuiOptionChoices.Variable      : self.gui = Variable.Gui(self.gui.parent, Window)

        # call function to make the gui
        self.gui.initialize_gui()



    # gui selection function for trig calculator types
    def choose_trig_gui(self):

        match self.gui_type:
            case GuiOptionChoices.Trigonometry  : self.gui = UnitCircleTrig.Gui(self.gui.parent, Window)
            case GuiOptionChoices.TriangleTrig  : self.gui = TriangleTrig.Gui(self.gui.parent, Window)
            case GuiOptionChoices.UnitCircleTrig: self.gui = UnitCircleTrig.Gui(self.gui.parent, Window)

        # make trig option menu to switch between trig calculator types
        self.gui.parent.trig_options = OptionMenu(self.gui.parent, Window.trig_option_choices,
                                                  GuiOptionChoices.TriangleTrig.value,
                                                  GuiOptionChoices.UnitCircleTrig.value)

        # call function to make the gui
        self.gui.initialize_gui()



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
    def options_callback(self, var, index, mode):

        print(f"current type: {Window.option_choices.get()}")

        # get option choice
        temp = Window.option_choices.get()

        # iterate over all possible option choices until a match is found
        for option in GuiOptionChoices:
            if option.value == temp:

                # set 'self.gui_type' to the matching option choice
                self.gui_type = option

        Window.instance.choose_gui()


    
    # function to detect trig optionmenu changes
    def trig_options_callback(self, var, index, mode):

        print(f"current trig type: {Window.trig_option_choices.get()}")

        # get trig option choice
        temp = Window.trig_option_choices.get()

        # iterate over all possible trig option choices until a match is found
        for option in GuiOptionChoices:
            if option.value == temp:

                # set 'self.gui_type' to the matching option choice
                self.gui_type = option

        Window.instance.choose_trig_gui()



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
    Window.trig_option_choices = StringVar(Window.instance.gui.parent)
    Window.trig_option_choices.set(GuiOptionChoices.UnitCircleTrig.value)
    Window.trig_option_choices.trace('w', Window.instance.trig_options_callback)

    Window.option_choices = StringVar(Window.instance.gui.parent)
    Window.option_choices.trace('w', Window.instance.options_callback)
    Window.option_choices.set(GuiOptionChoices.Trigonometry.value)



    # run the gui
    Window.instance.gui.parent.mainloop()

    

if __name__ == '__main__':

    main()