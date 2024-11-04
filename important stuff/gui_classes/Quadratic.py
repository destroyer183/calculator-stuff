import tkinter as tk
from tkinter import *
from parsers.quadratic_parser import Logic



# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)



class Gui:

    def __init__(self, parent, master) -> None:

        self.parent = parent
        self.master = master

    

    def clear_gui(self):

        for widget in self.parent.winfo_children():
            if type(widget) != OptionMenu:
                widget.destroy()



    def initialize_gui(self):

        self.clear_gui()

        self.parent.title('Quadratic Calculator')

        self.parent.geometry('700x675')

        self.logic = Logic()

        self.keybindings()

        self.create_gui()

    

    def create_gui(self):

        self.label = tk.Label(self.parent, text='WIP')
        self.label.configure(font=('Arial', 50, 'bold'))
        self.label.place(x = 275, y = 290)

        # configure option menu that allows the user to switch between guis
        self.parent.options.configure(font=('Arial', 15, 'bold'))
        
        # prevent user from resizing the gui in both x and y axis
        self.parent.resizable(False, False)

        # place option menu that allows the user to switch between guis
        self.parent.options.place(x = 10, y = 185)
        


    def keybindings(self):

        pass