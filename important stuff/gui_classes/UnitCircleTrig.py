import tkinter as tk
from tkinter import *
from enum import Enum
import math



''' NOTES

put the gui switching option menu in the top right - DONE

put the trig calculator switching option menu in the top left - DONE

put a button for deg/rad in the top middle, only if top left is occupied - DONE

put an automatic/manual button in the bottom left
put the 'calculate' button in the bottom middle
put the clear button in the bottom right

data that should be controllable: alpha, theta, x, y, r, deg/rad, ratios for sin, cos, tan, csc, sec, cot, and arc length. 12 total things.

make two columns
column on the left will be r, x, y, theta, alpha, arc
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
        self.is_radians = False
        self.coordinate_labels = {'(1,0)': '', '(0,1)': '', '(-1,0)': '', '(0,-1)': ''}
        self.left_data_column  = {'r': {}, 'x': {}, 'y': {}, 'theta': {}, 'alpha': {}, 'arc': {}}
        self.right_data_column = {'sin': {}, 'cos': {}, 'tan': {}, 'csc': {}, 'sec': {}, 'cot': {}}

        # initialize the necessary keys for each nested dictionary
        for key in self.left_data_column:  self.left_data_column[key]  = {'frame': '', 'label': '', 'box': ''}
        for key in self.right_data_column: self.right_data_column[key] = {'frame': '', 'label': '', 'box': ''}



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

        # refresh the window
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

        # create coordinate labels in degrees
        self.coordinate_labels['(1,0)']  = tk.Label(self.parent)
        self.coordinate_labels['(0,1)']  = tk.Label(self.parent)
        self.coordinate_labels['(-1,0)'] = tk.Label(self.parent)
        self.coordinate_labels['(0,-1)'] = tk.Label(self.parent)

        # configure labels
        for label in self.coordinate_labels.values():
            label.configure(font = ('Arial', 10, 'bold'))

        # place labels
        self.coordinate_labels['(1,0)']. place(x = 483, y = 273, anchor = 'sw')
        self.coordinate_labels['(0,1)']. place(x = 283, y = 73,  anchor = 'sw')
        self.coordinate_labels['(-1,0)'].place(x = 73,  y = 273, anchor = 'se')
        self.coordinate_labels['(0,-1)'].place(x = 283, y = 483, anchor = 'nw')

        # call function to put the labels on the unit circle
        self.create_unit_circle_labels(AngleUnits.Degrees)

        # make button to toggle units
        self.unit_toggle = tk.Button(self.parent, text = 'Deg', anchor = 'center', bg = 'white', command = lambda: self.toggle_units())
        self.unit_toggle.configure(font = ('Arial', 15, 'bold'))
        self.unit_toggle.place(x = math.ceil(self.parent.winfo_width() / 4) * 3, y = 5, anchor = 'n')



        # call function to create and configure the input fields
        self.create_input_fields()

        # call function to place the input fields
        self.place_input_fields()

        # call function to adjust the input field frames
        self.adjust_input_fields()

        
        
        # # create labels for the two columns of inputs
        # self.left_column_labels  = tk.Label(self.parent, text = 'r = \nx = \ny = \n\u03B8 = \n\u03B1 = \narc = ', justify = RIGHT)
        # self.right_column_labels = tk.Label(self.parent, text = 'sin\u03B8 = \ncos\u03B8 = \ntan\u03B8 = \ncsc\u03B8 = \nsec\u03B8 = \ncot\u03B8 = ', justify = RIGHT)

        # # configure labels for the two columns of inputs
        # self.left_column_labels.configure(font = ('Arial', 20, 'bold'), bg = 'grey')
        # self.right_column_labels.configure(font = ('Arial', 20, 'bold'), bg = 'grey')

        # # place labels for the two columns of inputs
        # self.left_column_labels. place(x = self.parent.winfo_width() / 8 * 5 - 4, y = 50, anchor = 'n')
        # self.right_column_labels.place(x = self.parent.winfo_width() / 8 * 7 - 4, y = 50, anchor = 'n')

        # prevent user from resizing the gui in both the x and y axis
        self.parent.resizable(False, False)
        
        # place the option menus that allow the user to switch between guis and trig calculators
        self.parent.options.place(x = self.parent.winfo_width() - 3, y = 3, anchor = 'ne')
        self.parent.trig_options.place(x = math.ceil(self.parent.winfo_width() / 2) + 5, y = 3)



    # function to create and configure the input fields
    def create_input_fields(self):

        # make frames, labels, and input boxes for each data input field
        for key in self.left_data_column:
            self.left_data_column[key]['frame'] = tk.Frame(self.parent, width = 202)
            self.left_data_column[key]['label'] = tk.Label(self.left_data_column[key]['frame'], text = f"{key} = ", justify = RIGHT)
            self.left_data_column[key]['box']   = tk.Text(self.left_data_column[key]['frame'], width = 8, height = 1, bg = 'white')

        for key in self.right_data_column:
            self.right_data_column[key]['frame'] = tk.Frame(self.parent)
            self.right_data_column[key]['label'] = tk.Label(self.right_data_column[key]['frame'], text = f"{key}\u03B8 = ", justify = RIGHT)
            self.right_data_column[key]['box']   = tk.Text(self.right_data_column[key]['frame'], width = 8, height = 1, bg = 'white')

        # configure the labels and boxes for data inputs
        for group in [x for x in self.left_data_column.values()] + [x for x in self.right_data_column.values()]:
            group['label'].configure(font = ('Arial', 20, 'bold'))
            group['box'].configure(font = ('Arial', 15))
            # group['frame'].configure(bg = 'grey')



    # function to place the input fields on the gui
    def place_input_fields(self):

        # variable to incrament the vertical offset of each input field
        vertical_offset = 60

        # variable to hold the vertical offset of the next input field to be placed
        current_offset = 75

        # loop through all of the input fields in the left column
        for group in self.left_data_column.values():

            # pack the label and box into the frame, and then place the frame on the gui
            group['box'].pack(side = RIGHT)
            group['label'].pack(side = RIGHT)
            group['frame'].place(x = self.parent.winfo_width() / 8 * 5 + 3, y = current_offset, anchor = 'n')

            # incrament the currrent vertical offset
            current_offset += vertical_offset

        # reset vertical offset
        current_offset = 75

        # loop through all of the input fields in the right column
        for group in self.right_data_column.values():

            # pack the label and box into the frame, and then place the frame on the gui
            group['box'].pack(side = RIGHT)
            group['label'].pack(side = RIGHT)
            group['frame'].place(x = self.parent.winfo_width() / 8 * 7, y = current_offset, anchor = 'n')

            # incrament the current vertical offset
            current_offset += vertical_offset

        # refresh gui
        self.parent.update()



    # function to adjust the input field frames to all be the same size
    def adjust_input_fields(self):

        # variable to store the width of the widest input field frame
        largest_frame = 0

        # loop through every input frame in both the left and right columns
        for group in [x for x in self.left_data_column.values()] + [x for x in self.right_data_column.values()]:
            
            # configure the width and height of the current input field frame
            group['frame'].configure(width = group['label'].winfo_width() + group['box'].winfo_width(), height = max(group['label'].winfo_height(), group['box'].winfo_height()))

            print(f"label width: {group['label'].winfo_width()}")
            # check if the current frame is wider than the widest recorded frame
            if group['frame'].winfo_width() > largest_frame:

                # update the widest recorded frame to be the current frame
                largest_frame = group['frame'].winfo_width()

        print(f"largest frame: {largest_frame}")

        # variable to incrament the vertical offset of each input field
        vertical_offset = 60

        # variable to hold the vertical offset of the next input field to be placed
        current_offset = 75

        # loop through all of the input fields in the left column
        for group in self.left_data_column.values():

            # pack the label and box into the frame, and then place the frame on the gui
            group['box'].pack(side = RIGHT)
            group['label'].pack(side = RIGHT)
            group['frame'].place(x = self.parent.winfo_width() / 8 * 5 + 3, y = current_offset, width = largest_frame, anchor = 'n')

            # incrament the currrent vertical offset
            current_offset += vertical_offset

        # reset vertical offset
        current_offset = 75

        # loop through all of the input fields in the right column
        for group in self.right_data_column.values():

            # pack the label and box into the frame, and then place the frame on the gui
            group['box'].pack(side = RIGHT)
            group['label'].pack(side = RIGHT)
            group['frame'].place(x = self.parent.winfo_width() / 8 * 7, y = current_offset, width = largest_frame, anchor = 'n')

            # incrament the current vertical offset
            current_offset += vertical_offset

        # refresh gui
        self.parent.update()



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

        # create coordinate labels in degrees
        if unit_type == AngleUnits.Degrees:
            self.coordinate_labels['(1,0)']. configure(text = '0\u00b0, 360\u00b0')
            self.coordinate_labels['(0,1)']. configure(text = '90\u00b0')
            self.coordinate_labels['(-1,0)'].configure(text = '180\u00b0')
            self.coordinate_labels['(0,-1)'].configure(text = '270\u00b0')

        # create coordinate labels in radians
        elif unit_type == AngleUnits.Radians:
            self.coordinate_labels['(1,0)']. configure(text = '0, 2\u03C0')
            self.coordinate_labels['(0,1)']. configure(text = '\u03C0/2')
            self.coordinate_labels['(-1,0)'].configure(text = '\u03C0')
            self.coordinate_labels['(0,-1)'].configure(text = '3\u03C0/2')



    def keybindings(self, input = None):

        pass



    # function to toggle the units between degrees and radians
    def toggle_units(self):
        
        # switch unit variable
        self.is_radians = not self.is_radians

        if self.is_radians:

            self.unit_toggle.configure(text = 'Rad')
            
            self.create_unit_circle_labels(AngleUnits.Radians)

        else:

            self.unit_toggle.configure(text = 'Deg')
            
            self.create_unit_circle_labels(AngleUnits.Degrees)