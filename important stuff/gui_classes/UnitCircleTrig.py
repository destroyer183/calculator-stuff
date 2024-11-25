import tkinter as tk
from tkinter import *
from enum import Enum
import math



''' NOTES

put the gui switching option menu in the top right - DONE

put the trig calculator switching option menu in the top left - DONE

put a button for deg/rad in the top middle, only if top left is occupied - DONE

put an automatic/manual button in the bottom left - DONE
put the 'calculate' button in the bottom middle - DONE
put the clear button in the bottom right - DONE

data that should be controllable: alpha, theta, x, y, r, deg/rad, ratios for sin, cos, tan, csc, sec, cot, and arc length. 12 total things.

make two columns - DONE
column on the left will be: 
    r - 'yellow' (255, 255, 0) '#ffff00'
    x - (255, 210, 0) '#ffd200'
    y - 'orange' (255, 165, 0) '#ffa500'
    theta - (255, 83, 0) '#ff5300'
    alpha - 'red' (255, 0, 0) '#ff0000'
    arc - (255, 0, 128) '#ff0080'

column on the right will be: 
    sin - 'purple' (255, 0, 255) '#ff00ff'
    cos - (128, 0, 255) '#8000ff'
    tan - 'blue' (0, 0, 255) '#0000ff'
    csc - (0, 255, 255) '#00ffff'
    sec - 'green' (0, 255, 0) '#00ff00'
    cot - (128, 255, 0) '#80ff00'

have a 'case' button to toggle between cases when partial information is given and the angle could be in multiple quadrants

make buttons to put things like pi, square roots, fractions, undefined, in the text boxes.
alternatively, detect what the user is typing, and if they type 'pi' replace it with the symbol for pi, and do the same with square root.
fractions and 'undefined' can be represented with '/' and 'u' and don't need to be replaced with anything.

https://youtu.be/dUkCgTOOpQ0?t=116 - vid for visualizing the 6 trig ratios

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
        self.mode_toggle = False

        self.coordinate_labels = {'(1,0)': '', '(0,1)': '', '(-1,0)': '', '(0,-1)': ''}

        self.left_data_column  = {'r': {}, 'x': {}, 'y': {}, 'theta': {}, 'alpha': {}, 'arc': {}}
        self.right_data_column = {'sin': {}, 'cos': {}, 'tan': {}, 'csc': {}, 'sec': {}, 'cot': {}}

        # text/symbol for each data label
        self.left_data_symbols  = {'r': 'r', 'x': 'x', 'y': 'y', 'theta': '\u03B8', 'alpha': '\u03B1', 'arc': 'arc'}
        self.right_data_symbols = {'sin': 'sin\u03B8', 'cos': 'cos\u03B8', 'tan': 'tan\u03B8', 'csc': 'csc\u03B8', 'sec': 'sec\u03B8', 'cot': 'cot\u03B8'}

        # RGB color codes for each label
        self.left_data_colors  = {'r': '#ffff00', 'x': '#ffd200', 'y': '#ffa500', 'theta': '#ff5300', 'alpha': '#ff0000', 'arc': '#ff0080'}
        self.right_data_colors = {'sin': '#ff00ff', 'cos': '#8000ff', 'tan': '#0000ff', 'csc': '#00ffff', 'sec': '#00ff00', 'cot': '#80ff00'}

        # initialize the necessary keys for each nested dictionary
        for key in self.left_data_column:  self.left_data_column[key]  = {'frame': '', 'label': '', 'box': ''}
        for key in self.right_data_column: self.right_data_column[key] = {'frame': '', 'label': '', 'box': ''}



    def clear_gui(self):

        self.parent.unbind("<Configure>")
        self.parent.unbind("<KeyRelease>")

        # this will delete every widget except for the ones that let the user switch the calculator and trig type
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

        # bind keypresses to trigger the keybinding handler function
        self.parent.bind("<KeyRelease>", self.keybindings)

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
        self.coordinate_labels['(1,0)']. place(x = 408, y = 273, anchor = 'sw')
        self.coordinate_labels['(0,1)']. place(x = 283, y = 148, anchor = 'sw')
        self.coordinate_labels['(-1,0)'].place(x = 148, y = 273, anchor = 'se')
        self.coordinate_labels['(0,-1)'].place(x = 283, y = 408, anchor = 'nw')

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



        # input mode button to switch between automatic calculation and manual calculation
        self.calculation_mode_button = tk.Button(self.parent, text = 'Automatic', anchor = 'center', bg = 'white', command = lambda: self.swap_calculation_mode())
        self.calculation_mode_button.configure(font = ('Arial', 15, 'bold'))
        self.calculation_mode_button.place(x = math.ceil(self.parent.winfo_width() / 2) + 7, y = self.parent.winfo_height() - 5, anchor = 'sw')       

        # calculate button for manual mode
        self.calculate_button = tk.Button(self.parent, text = 'Calculate', anchor = 'center', bg = 'white', command = lambda: self.text_boxes_callback(None))
        self.calculate_button.configure(font = ('Arial', 15, 'bold'))

        # button to reset the inputted data
        self.reset_button = tk.Button(self.parent, text = 'Clear', anchor = 'center', bg = 'white', command = lambda: self.clear_data())
        self.reset_button.configure(font = ('Arial', 15, 'bold'))
        self.reset_button.place(x = self.parent.winfo_width() - 5, y = self.parent.winfo_height() - 5, anchor = 'se')



        # prevent gui from being resized in both the x and y axis
        self.parent.resizable(False, False)
        
        # place the option menus that allow the user to switch between guis and trig calculators
        self.parent.trig_options.place(x = math.ceil(self.parent.winfo_width() / 2) + 5, y = 3)
        self.parent.options.place(x = self.parent.winfo_width() - 3, y = 3, anchor = 'ne')



    # function to create and configure the input fields
    def create_input_fields(self):

        # make frames, labels, and input boxes for each data input field
        for key in self.left_data_column:
            self.left_data_column[key]['frame'] = tk.Frame(self.parent, width = 202)
            self.left_data_column[key]['label'] = tk.Label(self.left_data_column[key]['frame'], text = f"{self.left_data_symbols[key]} = ", fg = self.left_data_colors[key], justify = RIGHT)
            self.left_data_column[key]['box']   = tk.Text(self.left_data_column[key]['frame'], width = 8, height = 1, bg = 'white')

        for key in self.right_data_column:
            self.right_data_column[key]['frame'] = tk.Frame(self.parent)
            self.right_data_column[key]['label'] = tk.Label(self.right_data_column[key]['frame'], text = f"{self.right_data_symbols[key]} = ", fg = self.right_data_colors[key], justify = RIGHT)
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
        current_offset = 80

        # loop through all of the input fields in the left column
        for group in self.left_data_column.values():

            # pack the label and box into the frame, and then place the frame on the gui
            group['box'].pack(side = RIGHT)
            group['label'].pack(side = RIGHT)
            group['frame'].place(x = self.parent.winfo_width() / 8 * 5 - 10, y = current_offset, anchor = 'n')

            group['box'].edit_modified(False)

            # incrament the currrent vertical offset
            current_offset += vertical_offset

        # reset vertical offset
        current_offset = 80

        # loop through all of the input fields in the right column
        for group in self.right_data_column.values():

            # pack the label and box into the frame, and then place the frame on the gui
            group['box'].pack(side = RIGHT)
            group['label'].pack(side = RIGHT)
            group['frame'].place(x = self.parent.winfo_width() / 8 * 7 - 35, y = current_offset, anchor = 'n')

            group['box'].edit_modified(False)

            # incrament the current vertical offset
            current_offset += vertical_offset

        # refresh gui
        self.parent.update()



    # function to adjust the input field frames to all be the same size
    def adjust_input_fields(self):

        # variable to store the width of the widest input field frame in the left column
        largest_frame_left = 0

        # loop through every input frame in the left column
        for group in self.left_data_column.values():
            
            # configure the width and height of the current input field frame
            group['frame'].configure(width = group['label'].winfo_width() + group['box'].winfo_width(), height = max(group['label'].winfo_height(), group['box'].winfo_height()))

            # check if the current frame is wider than the widest recorded frame
            if group['frame'].winfo_width() > largest_frame_left:

                # update the widest recorded frame to be the current frame
                largest_frame_left = group['frame'].winfo_width()

        # variable to store the width of the widest input field frame in the right column
        largest_frame_right = 0

        # loop through every input frame in both the left and right columns
        for group in self.right_data_column.values():
            
            # configure the width and height of the current input field frame
            group['frame'].configure(width = group['label'].winfo_width() + group['box'].winfo_width(), height = max(group['label'].winfo_height(), group['box'].winfo_height()))

            # check if the current frame is wider than the widest recorded frame
            if group['frame'].winfo_width() > largest_frame_right:

                # update the widest recorded frame to be the current frame
                largest_frame_right = group['frame'].winfo_width()

        # variable to incrament the vertical offset of each input field
        vertical_offset = 60

        # variable to hold the vertical offset of the next input field to be placed
        current_offset = 80

        

        # loop through all of the input fields in the left column
        for group in self.left_data_column.values():

            # pack the label and box into the frame, and then place the frame on the gui
            group['box'].pack(side = RIGHT)
            group['label'].pack(side = RIGHT)

            # print(group['frame'].winfo_width() / 2)

            group['frame'].place(x = self.parent.winfo_width() / 8 * 5 - 10, y = current_offset, width = largest_frame_left, anchor = 'n')

            # incrament the currrent vertical offset
            current_offset += vertical_offset

        # reset vertical offset
        current_offset = 80

        # loop through all of the input fields in the right column
        for group in self.right_data_column.values():

            # pack the label and box into the frame, and then place the frame on the gui
            group['box'].pack(side = RIGHT)
            group['label'].pack(side = RIGHT)
            group['frame'].place(x = self.parent.winfo_width() / 8 * 7 - 35, y = current_offset, width = largest_frame_right, anchor = 'n')

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
        self.canvas.create_oval(399, 274, 407, 282, fill = 'black')
        self.canvas.create_oval(274, 149, 282, 157, fill = 'black')
        self.canvas.create_oval(149, 274, 157, 282, fill = 'black')
        self.canvas.create_oval(274, 399, 282, 407, fill = 'black')

        # create unit circle, radius of 125px
        self.canvas.create_oval(153, 153, 403, 403, fill = None, outline = 'black')



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

        try: temp = input.keysym
        except:return

        print(f"keysm type: {type(input.keysym)}")

        if input.char == "\r": self.text_boxes_callback(None)
        else: self.text_boxes_callback(input)



    # function to tell the parser to calculate the triangle when information in the text boxes is updated or when the 'calculate' button is pressed
    def text_boxes_callback(self, x = None):

        print(f"x: {x}")

        # if the mode is set to manual, and if x is not none (a key was pressed) exit the function
        if self.mode_toggle and x is not None: return



    # function to clear all of the data
    def clear_data(self):

        # delete the data in all of the boxes
        for box in [x for x in self.left_data_column.values()] + [x for x in self.right_data_column.values()]:
            box.delete(1.0, tk.END)
            box.edit_modified(False)

        # put a '1' in the 'r' box since that generally doesn't change.
        self.left_data_column['r']['box'].insert(tk.END, '1')
        self.left_data_column['r']['box'].edit_modified(False)

        

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



    # function to switch between automatic and manual calculation modes
    def swap_calculation_mode(self):
        
        self.mode_toggle = not self.mode_toggle

        if self.mode_toggle:

            self.calculation_mode_button.configure(text = 'Manual')
            self.calculate_button.place(x = math.ceil(self.parent.winfo_width() / 4) * 3, y = self.parent.winfo_height() - 50, anchor = 's')

        if not self.mode_toggle:

            self.calculation_mode_button.configure(text = 'Automatic')
            self.calculate_button.place_forget()