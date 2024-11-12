import tkinter as tk
from tkinter import *
from enum import Enum
import math



''' NOTES

put the gui switching option menu in the top right

if triangle trig and unit circle trig are made together, make an option menu to switch between them and put it in the top left

put a button for deg/rad in the top middle, only if top left is occupied

put an automatic/manual button in the bottom left
put the 'calculate' button in the bottom middle
put the clear button in the bottom right

data that should be controllable: alpha, theta, x, y, r, deg/rad, ratios for sin, cos, tan, csc, sec, cot, and arc length. 12 total things.

make two columns
column on the left will be theta, alpha, arc length, x, y, r
column on the right will be sin, cos, tan, csc, sec, cot

'''



class AngleUnits(Enum):
    Degrees = 'degrees'
    Radians = 'radians'



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

        self.parent.unbind("<Configure>")
        self.parent.unbind("<KeyRelease>")

        # this will delete every widget except for the one that lets the user switch the calculator type
        for widget in self.parent.winfo_children():
            if type(widget) != OptionMenu:
                widget.destroy()

    

    def initialize_gui(self):

        self.parent.title('Trigonometry Calculator')

        self.create_gui()



    def create_gui(self):
        
        # clear gui
        self.clear_gui()

        # set gui size
        self.parent.geometry('1111x553')

        # update the window
        self.parent.update()

        # configure option menu for switching guis
        self.parent.options.configure(font = ('Arial', 15, 'bold'))
        self.parent.trig_options.configure(font = ('Arial', 15, 'bold'))

        # create canvas to draw shapes on the gui
        self.canvas = Canvas(self.parent, width = 558, height = 557)

        # put canvas on the gui
        self.canvas.place(x = -2, y = -2)

        # call function to create the coordinate plane and the unit circle
        self.create_unit_circle()

        # call function to put the labels on the unit circle
        self.create_unit_circle_labels(AngleUnits.Degrees)

        # make button to toggle units
        self.unit_toggle = tk.Button(self.parent, text = 'Deg', anchor = 'center', bg = 'white', command = lambda: None)
        self.unit_toggle.configure(font = ('Arial', 15, 'bold'))
        self.unit_toggle.place(x = math.ceil(self.parent.winfo_width() / 4) * 3, y = 5, anchor = 'n')

        # prevent user from resizing the gui in both the x and y axis
        self.parent.resizable(False, False)
        
        # place the option menus that allow the user to switch between guis and trig calculators
        self.parent.options.place(x = self.parent.winfo_width() - 3, y = 3, anchor = 'ne')
        self.parent.trig_options.place(x = math.ceil(self.parent.winfo_width() / 2) + 5, y = 3)



    # function to create the x and y axis, and the unit circle
    def create_unit_circle(self):

        # create x and y axis lines
        self.canvas.create_line(0, 278, 555, 278, fill = 'grey')
        self.canvas.create_line(278, 0, 278, 555, fill = 'grey')

        # create divider bar by putting a rectangle on the canvas
        self.canvas.create_rectangle(555, 0, 559, 558, fill = 'black')

        # create points for coordinate labels
        self.canvas.create_oval(474, 274, 482, 282, fill = 'black') # (1,0)
        self.canvas.create_oval(274, 74,  282, 82,  fill = 'black') # (0,1)
        self.canvas.create_oval(74,  274, 82,  282, fill = 'black') # (-1,0)
        self.canvas.create_oval(274, 474, 282, 482, fill = 'black') # (0,-1)

        # create unit circle
        self.canvas.create_oval(78, 78, 478, 478, fill = None, outline = 'black')



    # function to create the unit circle labels
    def create_unit_circle_labels(self, unit_type: AngleUnits):

        # create dictionary to hold coordinate labels
        self.coordinate_labels = {'(1,0)': '', '(0,1)': '', '(-1,0)': '', '(0,-1)': ''}

        # create coordinate labels in degrees
        if unit_type == AngleUnits.Degrees:
            self.coordinate_labels['(1,0)']  = tk.Label(self.parent, text = '0\u00b0, 360\u00b0')
            self.coordinate_labels['(0,1)']  = tk.Label(self.parent, text = '90\u00b0')
            self.coordinate_labels['(-1,0)'] = tk.Label(self.parent, text = '180\u00b0')
            self.coordinate_labels['(0,-1)'] = tk.Label(self.parent, text = '270\u00b0')

        # create coordinate labels in radians
        elif unit_type == AngleUnits.Radians:
            self.coordinate_labels['(1,0)']  = tk.Label(self.parent, text = '0, 2\u03C0')
            self.coordinate_labels['(0,1)']  = tk.Label(self.parent, text = '\u03C0/2')
            self.coordinate_labels['(-1,0)'] = tk.Label(self.parent, text = '\u03C0')
            self.coordinate_labels['(0,-1)'] = tk.Label(self.parent, text = '3\u03C0/2')

        for label in self.coordinate_labels.values():

            label.configure(font = ('Arial', 10, 'bold'))

        self.coordinate_labels['(1,0)']. place(x = 483, y = 273, anchor = 'sw')
        self.coordinate_labels['(0,1)']. place(x = 283, y = 73,  anchor = 'sw')
        self.coordinate_labels['(-1,0)'].place(x = 73,  y = 273, anchor = 'se')
        self.coordinate_labels['(0,-1)'].place(x = 283, y = 483, anchor = 'nw')



    def keybindings(self, input = None):

        pass