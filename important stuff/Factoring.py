import tkinter as tk
from tkinter import *
import keyboard


# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)



class Logic:

    def __init__(self) -> None:
        
        pass



class Gui:

    def __init__(self, parent) -> None:

        self.parent = parent

        pass


    def create_gui(self):

        self.parent.title('Factoring Calculator')

        self.parent.geometry('700x675')

        self.logic = Logic()

        self.keybindings()
        


    def keybindings(self):

        pass


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