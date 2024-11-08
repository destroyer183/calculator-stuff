import tkinter as tk
from tkinter import *
from enum import Enum
import math
from parsers.trig_parser import Logic, Data



''' NOTES

if the user inputs 4 values, like 3 sides and 1 angle, and the triangle wouldn't technically be possible, make code to check for this.

add thingy that points to the 'clear' button if someone keeps trying to change values after they were calculated
use the flash() method whenever the user tries to edit a text box after things have been calculated - https://www.tutorialspoint.com/python/tk_button.htm

allow the user to input angles over 180* by using modulus

there's still a problem with the impossible triangle detection, as part of it is based in the 'solve_triangle()' function, which means that unnecesary stuff gets calculated.



notes for unit circle mode:

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



make a new file for the unit circle trig calculator, but make it accessible only from the triangle trig calculator

'''

# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)



# reference x positions to make it easier to move boxes around when the mode is changed
class ReferenceCoordinates(Enum):
   ANGLE_TEXT_REFX  = 100
   ANGLE_BOX_REFX   = 170
   LENGTH_TEXT_REFX = 350
   LENGTH_BOX_REFX  = 420

class AngleUnits(Enum):
    Degrees = 'degrees'
    Radians = 'radians'



class Gui:

    is_ambiguous = False

    def __init__(self, parent, master) -> None:

        Gui.is_ambiguous = True

        self.parent = parent
        self.master = master
        self.ambiguous_triangle = False
        self.mode_toggle = False 
        self.logic = Logic(False, 'Logic')
        self.ambiguous = Logic(True, 'ambiguous')



    def clear_gui(self):

        self.parent.unbind("<Configure>")
        self.parent.unbind("<KeyRelease>")

        # this will delete every widget except for the one that lets the user switch the calculator type
        for widget in self.parent.winfo_children():
            if type(widget) != OptionMenu:
                widget.destroy()



    def initialize_gui(self):

        self.parent.title('Trigonometry Calculator')

        self.create_triangle_gui()
        # self.create_unit_circle_gui()

    

    def create_triangle_gui(self):

        # clear gui
        self.clear_gui()

        # set gui size
        self.parent.geometry('650x850')

        # update the window
        self.parent.update()

        # bind keypresses to trigger the keybinding handler function
        self.parent.bind("<KeyRelease>", self.keybindings)

        # create canvas object
        self.canvas = Canvas(self.parent, width = 650, height = 654)

        # put canvas on gui
        self.canvas.pack(fill = BOTH)

        # create divider bar by making a rectangle on the canvas
        self.canvas.create_rectangle(0, 650, 650, 654, fill = 'black')

        # triangle reset button
        self.reset_button = tk.Button(self.parent, text = 'Clear', anchor = 'center', bg = 'white', command = lambda: self.clear_data())
        self.reset_button.configure(font = ('Arial', 15, 'bold'))
        self.reset_button.place(x = 5, y = 660)

        # input mode button
        self.mode_button = tk.Button(self.parent, text = 'Automatic', anchor = 'center', bg = 'white', command = lambda: self.swap_modes())
        self.mode_button.configure(font = ('Arial', 15, 'bold'))
        self.mode_button.place(x = 325, y = 660, anchor='n')

        # ambiguous case switcher button
        self.ambiguous_button = tk.Button(self.parent, text = 'case 1', anchor = 'center', bg = 'white', command = lambda: self.ambiguous_toggle())
        self.ambiguous_button.configure(font = ('Arial', 15, 'bold'))

        # error text label
        self.error_text = tk.Label(self.parent, text = '')
        self.error_text.configure(font = ('Arial', 25, 'bold'))
        
        # calculate button for manual mode
        self.calculate = tk.Button(self.parent, text = 'Calculate', anchor = 'center', bg = 'white', command = lambda: self.text_boxes_callback(None))
        self.calculate.configure(font = ('Arial', 15, 'bold'))

        # configure option menu for switching guis
        self.parent.options.configure(font = ('Arial', 15, 'bold'))
        
        # make lists to store the angle and side length input boxes
        self.angle_boxes  = [0, 0, 0]
        self.length_boxes = [0, 0, 0]

        # make labels for the angle and side length input boxes
        self.angle_text  = tk.Label(self.parent, text = 'A = \nB = \nC = ')
        self.length_text = tk.Label(self.parent, text = 'a = \nb = \nc = ')

        # make input boxes for angles and side lengths
        self.angle_boxes[0]  = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.angle_boxes[1]  = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.angle_boxes[2]  = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[0] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[1] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[2] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')

        # configure input box labels
        self.angle_text. configure(font = ('Arial', 26, 'bold'))
        self.length_text.configure(font = ('Arial', 26, 'bold'))

        # configure input boxes
        self.angle_boxes[0]. configure(font = ('Arial', 20))
        self.angle_boxes[1]. configure(font = ('Arial', 20))
        self.angle_boxes[2]. configure(font = ('Arial', 20))
        self.length_boxes[0].configure(font = ('Arial', 20))
        self.length_boxes[1].configure(font = ('Arial', 20))
        self.length_boxes[2].configure(font = ('Arial', 20))

        # place ange and side length labels
        self.angle_text. place(x = ReferenceCoordinates.ANGLE_TEXT_REFX.value,  y = 705)
        self.length_text.place(x = ReferenceCoordinates.LENGTH_TEXT_REFX.value, y = 705)

        # place input boxes
        self.angle_boxes[0]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 709)
        self.angle_boxes[1]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 751)
        self.angle_boxes[2]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 792)
        self.length_boxes[0].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 709)
        self.length_boxes[1].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 751)
        self.length_boxes[2].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 792)

        # make dictionary to hold triangle information labels
        self.labels = {'A': '', 'B': '', 'C': '', 'a': '', 'b': '', 'c': ''}

        # make labels for each triangle label value
        for key in self.labels.keys():

            self.labels[key] = tk.Label(self.parent, text = key, anchor = 'center', width = 1, height = 1)
            self.labels[key].configure(font = ('Arial', 24, 'bold'))

        # update boxes to show that they have not been edited
        for box in self.angle_boxes + self.length_boxes:

            box.edit_modified(False)



        # reset all information
        self.clear_data()

        # prevent user from resizing the gui in both x and y axis
        self.parent.resizable(False, False)

        # place option menu that allows the user to switch between guis
        self.parent.options.place(x = 472, y = 660)



    def create_unit_circle_gui(self):
        
        # clear gui
        self.clear_gui()

        # set gui size
        self.parent.geometry('1111x553')

        # update the window
        self.parent.update()

        # configure option menu for switching guis
        self.parent.options.configure(font = ('Arial', 15, 'bold'))

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
        self.unit_toggle.place(x = math.ceil(self.parent.winfo_width() / 2) + 7, y = 5)

        # prevent user from resizing the gui in both the x and y axis
        self.parent.resizable(False, False)
        
        # place option menu that allows the user to switch between guis
        self.parent.options.place(x = self.parent.winfo_width() - 3, y = 3, anchor = 'ne')



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

        try: temp = input.keysym
        except:return

        print(f"keysm type: {type(input.keysym)}")

        if input.char == "\r": self.text_boxes_callback(None)
        if input.keycode == 27: self.clear_data()
        if input.char == "m": self.swap_modes()
        if input.char == "t" and self.ambiguous_triangle: self.ambiguous_toggle()
        else: self.text_boxes_callback(input)


    # function to detect optionmenu changes
    def text_boxes_callback(self, x = None):

        print(f"x: {x}")

        for box in self.angle_boxes + self.length_boxes:

            if box.edit_modified():

                try: temp = float(box.get(1.0, tk.END))
                except: box.delete(len(box.get(1.0, tk.END)) - 1.0, tk.END); return

                print('yes')

                if self.mode_toggle and x is not None: return

                try: 
                    if box != self.last_modified:

                        # loop through all boxes, and reset the previous last modified box
                        for item in self.angle_boxes + self.length_boxes:
                            item.edit_modified(False)

                        self.last_modified = box

                except: self.last_modified = box

                box.edit_modified(False)

                self.logic.angles = [x.get(1.0, tk.END) for x in self.angle_boxes]
                self.logic.lengths = [x.get(1.0, tk.END) for x in self.length_boxes]

                for index in range(len(self.logic.angles)):
                    try: self.logic.angles[index] = float(self.logic.angles[index])
                    except: self.logic.angles[index] = 0

                for index in range(len(self.logic.lengths)):
                    try: self.logic.lengths[index] = float(self.logic.lengths[index])
                    except: self.logic.lengths[index] = 0

                output, ambiguous = self.logic.check_triangle()

                if ambiguous:

                    self.ambiguous.angles = 1 * self.logic.angles
                    self.ambiguous.lengths = 1 * self.logic.lengths

                    self.ambiguous.calculate_triangle(ambiguous)

                    self.ambiguous_toggle()

                else: self.ambiguous_toggle(Data.DELETE)

                self.logic.calculate_triangle(ambiguous)

                self.place_triangle(self.logic.calculate_triangle(ambiguous))



    


    def swap_modes(self):

        self.mode_toggle = not self.mode_toggle

        if self.mode_toggle:
            
            self.mode_button.configure(text = 'Manual')
            self.calculate.place(x = 550, y = 750, anchor = 'n')

            self.angle_text. place(x = ReferenceCoordinates.ANGLE_TEXT_REFX.value  - 75, y = 705)
            self.length_text.place(x = ReferenceCoordinates.LENGTH_TEXT_REFX.value - 75, y = 705)

            self.angle_boxes[0]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value  - 75, y = 709)
            self.angle_boxes[1]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value  - 75, y = 751)
            self.angle_boxes[2]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value  - 75, y = 792)
            self.length_boxes[0].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value - 75, y = 709)
            self.length_boxes[1].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value - 75, y = 751)
            self.length_boxes[2].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value - 75, y = 792)

        else:

            self.mode_button.configure(text = 'Automatic')
            self.calculate.place_forget()

            self.angle_text. place(x = ReferenceCoordinates.ANGLE_TEXT_REFX.value,  y = 705)
            self.length_text.place(x = ReferenceCoordinates.LENGTH_TEXT_REFX.value, y = 705)
    
            self.angle_boxes[0]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 709)
            self.angle_boxes[1]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 751)
            self.angle_boxes[2]. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 792)
            self.length_boxes[0].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 709)
            self.length_boxes[1].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 751)
            self.length_boxes[2].place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 792)



    def clear_data(self):

        for box in self.angle_boxes + self.length_boxes:
            box.delete(1.0, tk.END)
            box.edit_modified(False)

        try:self.canvas.delete(self.triangle)
        except:pass

        self.logic.angles = [60, 60, 60]
        self.logic.lengths = [1, 1, 1]

        self.ambiguous_toggle(Data.DELETE)

        self.place_triangle(self.logic.calculate_triangle(False), no = True)

        self.text_boxes_callback(-2147483648)

        Gui.is_ambiguous = False
        


    def edit_triangle(self, type = ''):

        if type == Data.DELETE:
            self.error_text.place_forget()
            return

        elif type == Data.UNSOLVABLE:
            self.error_text.configure(text = 'not enough information')

        elif type == Data.IMPOSSIBLE:
            self.error_text.configure(text = 'triangle does not exist')

        elif type == Data.CLEAR_DATA:
            self.clear_data()
            return
        
        else:return

        try:self.canvas.delete(self.triangle)
        except:pass

        self.place_labels(type = Data.DELETE)
        self.error_text.place(x = 125, y = 325)
        return 1

        

    def update_text_boxes(self, data):

        for index in range(len(self.angle_boxes)):

            if self.angle_boxes[index] != self.last_modified:

                self.angle_boxes[index].delete(1.0, tk.END)
                self.angle_boxes[index].insert(tk.END, data.angles[index])
                self.angle_boxes[index].edit_modified(False)

        for index in range(len(self.length_boxes)):

            if self.length_boxes[index] != self.last_modified:

                self.length_boxes[index].delete(1.0, tk.END)
                self.length_boxes[index].insert(tk.END, data.lengths[index])
                self.length_boxes[index].edit_modified(False)
    


    def place_triangle(self, data, no = False):

        if self.edit_triangle(data): return

        self.place_labels(data)

        points = [data.coordinates["a"][0], data.coordinates["a"][1], data.coordinates["b"][0], data.coordinates["b"][1], data.coordinates["c"][0], data.coordinates["c"][1]]

        try: self.canvas.delete(self.triangle)
        except:pass
        try: self.edit_triangle(Data.DELETE)
        except:pass

        self.triangle = self.canvas.create_polygon(points, outline = 'black', fill = 'white', width = 3)

        if no: return
        self.update_text_boxes(data)



    def ambiguous_toggle(self, mode = ''):

        if mode == Data.DELETE:

            self.ambiguous_triangle = False
            self.ambiguous_button.place_forget()
            return

        if Gui.is_ambiguous:

            self.ambiguous_triangle = True
            self.ambiguous_button.configure(text = 'case 2')
            self.ambiguous_button.place(x = 5, y = 600)
            self.place_triangle(self.ambiguous)

        elif not Gui.is_ambiguous:

            self.ambiguous_triangle = True
            self.ambiguous_button.configure(text = 'case 1')
            self.ambiguous_button.place(x = 5, y = 600)
            self.place_triangle(self.logic)
        
        Gui.is_ambiguous = not Gui.is_ambiguous



    def place_labels(self, data = True, type = ''):

        if data == True: data = self.logic

        if type == Data.DELETE:

            for key in self.labels.keys():

                self.labels[key].place_forget()

        else: 

            data.calculate_labels()

            for key in self.labels.keys():

                self.labels[key].place(x = (data.angle_labels | data.length_labels)[key][0] - 12, y = (data.angle_labels | data.length_labels)[key][1] - 21)



def main():

    pass

if __name__ == '__main__':
    
    main()