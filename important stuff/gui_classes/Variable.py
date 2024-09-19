import tkinter as tk
from tkinter import *
from parsers.variable_parser import Logic



# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)



class Gui:

    def __init__(self, parent) -> None:

        self.parent = parent



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()
    


    def initialize_gui(self):

        self.clear_gui()

        self.parent.title('Variable Calculator')

        self.parent.geometry('700x675')

        self.logic = Logic()

        self.keybindings()

        self.initialize_gui()



    def create_gui(self):

        self.label = tk.Label(self.parent, text='WIP')
        self.label.configure(font=('Arial', 50, 'bold'))
        self.label.place(x = 275, y = 290)
        


    def keybindings(self):

        pass