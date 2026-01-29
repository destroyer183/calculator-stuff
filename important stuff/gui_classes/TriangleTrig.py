import tkinter as tk
from enum import Enum
import math
from parsers.triangle_trig_parser import Logic, Data



''' NOTES

if the user inputs 4 values, like 3 sides and 1 angle, and the triangle wouldn't technically be possible, make code to check for this.

add thingy that points to the 'clear' button if someone keeps trying to change values after they were calculated
use the flash() method whenever the user tries to edit a text box after things have been calculated - https://www.tutorialspoint.com/python/tk_button.htm

allow the user to input angles over 180* by using modulus

there's still a problem with the impossible triangle detection, as part of it is based in the 'solve_triangle()' function, which means that unnecesary stuff gets calculated.



make an option menu for switching trig types, and make it work just like the main gui switcher, but only display two options



use curly brackets to allow the user to input equations into the text boxes by passing the contents to the shunting parser.

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



class InputBox:

    def __init__(self, tk_box):

        self.tk_box: tk.Text = tk_box
        self.sci_parser_indices: tuple[int, int] = (-1, -1)
        self.sci_parser_toggle: bool = False



class Gui:

    is_ambiguous = False

    def __init__(self, parent: tk.Tk, master) -> None:

        Gui.is_ambiguous = True

        self.parent: tk.Tk = parent
        self.master = master
        self.ambiguous_triangle = False
        self.mode_toggle = False
        self.sci_parsing: bool = False
        self.logic = Logic(False, 'Logic')
        self.ambiguous = Logic(True, 'ambiguous')



    def clear_gui(self):

        self.parent.unbind("<Configure>")
        self.parent.unbind("<KeyRelease>")

        # this will delete every widget except for the one that lets the user switch the calculator type
        for widget in self.parent.winfo_children():
            if type(widget) != tk.OptionMenu:
                widget.destroy()



    def initialize_gui(self):

        self.parent.title('Trigonometry Calculator')

        self.create_gui()



    def create_gui(self):

        # clear gui
        self.clear_gui()

        # set gui size
        self.parent.geometry('650x850')

        # update the window
        self.parent.update()

        # bind keypresses to trigger the keybinding handler function
        self.parent.bind("<KeyRelease>", self.keybindings)

        # create canvas object
        self.canvas = tk.Canvas(self.parent, width = 650, height = 654)

        # put canvas on gui
        self.canvas.pack(fill = tk.BOTH)

        # create divider bar by making a rectangle on the canvas
        self.canvas.create_rectangle(0, 650, 650, 654, fill = 'black')

        # triangle reset button
        self.reset_button = tk.Button(self.parent, text = 'Clear', anchor = 'center', bg = 'white', command = lambda: self.clear_data())
        self.reset_button.configure(font = ('Arial', 15, 'bold'))
        self.reset_button.place(x = 5, y = 660)

        # input mode button
        self.mode_button = tk.Button(self.parent, text = 'Automatic', anchor = 'center', bg = 'white', command = lambda: self.swap_modes())
        self.mode_button.configure(font = ('Arial', 15, 'bold'))
        self.mode_button.place(x = self.parent.winfo_width() - 5, y = 660, anchor = 'ne')

        # ambiguous case switcher button
        self.ambiguous_button = tk.Button(self.parent, text = 'case 1', anchor = 'center', bg = 'white', command = lambda: self.ambiguous_toggle())
        self.ambiguous_button.configure(font = ('Arial', 15, 'bold'))

        # error text label
        self.error_text = tk.Label(self.parent, text = '')
        self.error_text.configure(font = ('Arial', 25, 'bold'))
        
        # calculate button for manual mode
        self.calculate = tk.Button(self.parent, text = 'Calculate', anchor = 'center', bg = 'white', command = lambda: self.text_boxes_callback(None))
        self.calculate.configure(font = ('Arial', 15, 'bold'))

        # option menu to switch between the two types of trig calculators
        self.master.trig_options.configure(font = ('Arial', 15, 'bold'))

        # configure option menu for switching guis
        self.master.options.configure(font = ('Arial', 15, 'bold'))
        
        # make lists to store the angle and side length input boxes
        self.angle_boxes = [InputBox(tk.Text())] * 3
        self.length_boxes = [InputBox(tk.Text())] * 3

        # make labels for the angle and side length input boxes
        self.angle_text1  = tk.Label(self.parent, text = 'A = \nB = \nC = ', justify = tk.RIGHT)
        self.length_text1 = tk.Label(self.parent, text = 'a = \nb = \nc = ', justify = tk.RIGHT)

        # make input boxes for angles and side lengths
        self.angle_boxes[0].tk_box  = tk.Text(self.parent, width = 8, height = 1, bg = 'white')
        self.angle_boxes[1].tk_box  = tk.Text(self.parent, width = 8, height = 1, bg = 'white')
        self.angle_boxes[2].tk_box  = tk.Text(self.parent, width = 8, height = 1, bg = 'white')
        self.length_boxes[0].tk_box = tk.Text(self.parent, width = 8, height = 1, bg = 'white')
        self.length_boxes[1].tk_box = tk.Text(self.parent, width = 8, height = 1, bg = 'white')
        self.length_boxes[2].tk_box = tk.Text(self.parent, width = 8, height = 1, bg = 'white')

        # configure input box labels
        self.angle_text1. configure(font = ('Arial', 26, 'bold'))
        self.length_text1.configure(font = ('Arial', 26, 'bold'))

        # configure input boxes
        self.angle_boxes[0].tk_box. configure(font = ('Arial', 20))
        self.angle_boxes[1].tk_box. configure(font = ('Arial', 20))
        self.angle_boxes[2].tk_box. configure(font = ('Arial', 20))
        self.length_boxes[0].tk_box.configure(font = ('Arial', 20))
        self.length_boxes[1].tk_box.configure(font = ('Arial', 20))
        self.length_boxes[2].tk_box.configure(font = ('Arial', 20))

        # place ange and side length labels
        self.angle_text1. place(x = ReferenceCoordinates.ANGLE_TEXT_REFX.value,  y = 705)
        self.length_text1.place(x = ReferenceCoordinates.LENGTH_TEXT_REFX.value, y = 705)

        # place input boxes
        self.angle_boxes[0].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 709)
        self.angle_boxes[1].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 751)
        self.angle_boxes[2].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 792)
        self.length_boxes[0].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 709)
        self.length_boxes[1].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 751)
        self.length_boxes[2].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 792)

        # make dictionary to hold triangle information labels
        self.labels: dict[str, tk.Label] = {'A': tk.Label(), 'B': tk.Label(), 'C': tk.Label(), 'a': tk.Label(), 'b': tk.Label(), 'c': tk.Label()}

        # make labels for each triangle label value
        for key in self.labels.keys():

            self.labels[key] = tk.Label(self.parent, text = key, anchor = 'center', width = 1, height = 1)
            self.labels[key].configure(font = ('Arial', 24, 'bold'))

        # update boxes to show that they have not been edited
        for box in self.angle_boxes + self.length_boxes:

            box.tk_box.edit_modified(False)



        # reset all information
        self.clear_data()

        # prevent user from resizing the gui in both x and y axis
        self.parent.resizable(False, False)

        # lift option menus above canvas
        self.master.options.lift()
        self.master.trig_options.lift()

        # place the option menus that allow the user to switch between guis and trig calculators
        self.master.options.place(x = self.parent.winfo_width() - 5, y = 5, anchor = 'ne')
        self.master.trig_options.place(x = 5, y = 5)



    def begin_sci_parsing(self):

        self.sci_parsing = True

        for box in self.angle_boxes + self.length_boxes:
            if "{" in box.tk_box.get(1.0, tk.END) and not box.sci_parser_toggle:

                box.sci_parser_indices = (len(box.tk_box.get(1.0, tk.END)) - 1, -1)




    def keybindings(self, input: tk.Event):

        print(type(input))

        try: temp = input.keysym
        except:return

        print(f"keysm type: {type(input.keysym)}")

        if input.char == "\r": self.text_boxes_callback(None)
        elif input.keycode == 27: self.clear_data()
        elif input.char == "m": self.swap_modes()
        elif input.char == "t" and self.ambiguous_triangle: self.ambiguous_toggle()
        elif input.char == "{": 
            self.begin_sci_parsing()
        elif input.char == "}": 
            pass
        elif input.char in "1234567890.-" and not self.sci_parsing:
            self.text_boxes_callback(input)



    # function to tell the parser to calculate the triangle when information in the text boxes is updated or when the 'calculate' button is pressed
    def text_boxes_callback(self, x = None):

        print(f"x: {x}")

        if self.mode_toggle and x is not None: return

        for box in self.angle_boxes + self.length_boxes:

            if box.tk_box.edit_modified():

                if box.tk_box.get(1.0, tk.END).strip() == '': 
                    box.tk_box.delete(1.0, tk.END)
                    box.tk_box.edit_modified(False)
                    continue

                temp = float(box.tk_box.get(1.0, tk.END))
                print(f"yes: {temp}")

                # idk why this is here but it is probably needed so I'm leaving it
                try:
                    if box != self.last_modified:

                        # loop through all boxes, and reset the previous last modified box
                        for item in self.angle_boxes + self.length_boxes:
                            item.tk_box.edit_modified(False)

                        self.last_modified = box

                except: self.last_modified = box

                box.tk_box.edit_modified(False)

                for i in range(len(self.logic.angles)):
                    try:
                        self.logic.angles[i] = float(self.angle_boxes[i].tk_box.get(1.0, tk.END))
                    except:pass

                for i in range(len(self.logic.lengths)):
                    try:
                        self.logic.lengths[i] = float(self.length_boxes[i].tk_box.get(1.0, tk.END))
                    except:pass

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

                    self.ambiguous_toggle(Data.NONE)

                else: self.ambiguous_toggle(Data.DELETE)

                self.logic.calculate_triangle(ambiguous)

                self.place_triangle(self.logic.calculate_triangle(ambiguous))



    def swap_modes(self):

        self.mode_toggle = not self.mode_toggle

        if self.mode_toggle:
            
            self.mode_button.configure(text = 'Manual')
            self.calculate.place(x = 550, y = 750, anchor = 'n')

            self.angle_text1. place(x = ReferenceCoordinates.ANGLE_TEXT_REFX.value  - 75, y = 705)
            self.length_text1.place(x = ReferenceCoordinates.LENGTH_TEXT_REFX.value - 75, y = 705)

            self.angle_boxes[0].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value  - 75, y = 709)
            self.angle_boxes[1].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value  - 75, y = 751)
            self.angle_boxes[2].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value  - 75, y = 792)
            self.length_boxes[0].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value - 75, y = 709)
            self.length_boxes[1].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value - 75, y = 751)
            self.length_boxes[2].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value - 75, y = 792)

        else:

            self.mode_button.configure(text = 'Automatic')
            self.calculate.place_forget()

            self.angle_text1. place(x = ReferenceCoordinates.ANGLE_TEXT_REFX.value,  y = 705)
            self.length_text1.place(x = ReferenceCoordinates.LENGTH_TEXT_REFX.value, y = 705)
    
            self.angle_boxes[0].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 709)
            self.angle_boxes[1].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 751)
            self.angle_boxes[2].tk_box. place(x = ReferenceCoordinates.ANGLE_BOX_REFX.value,  y = 792)
            self.length_boxes[0].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 709)
            self.length_boxes[1].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 751)
            self.length_boxes[2].tk_box.place(x = ReferenceCoordinates.LENGTH_BOX_REFX.value, y = 792)



    def clear_data(self):

        for box in self.angle_boxes + self.length_boxes:
            box.tk_box.delete(1.0, tk.END)
            box.tk_box.edit_modified(False)

        try:self.canvas.delete(self.triangle)
        except:pass

        self.logic.angles = [60, 60, 60]
        self.logic.lengths = [1, 1, 1]

        self.ambiguous_toggle(Data.DELETE)

        self.place_triangle(self.logic.calculate_triangle(False), no = True)

        self.text_boxes_callback(1)

        Gui.is_ambiguous = False
        


    def edit_triangle(self, type):

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

                self.angle_boxes[index].tk_box.delete(1.0, tk.END)
                self.angle_boxes[index].tk_box.insert(tk.END, data.angles[index])
                self.angle_boxes[index].tk_box.edit_modified(False)

        for index in range(len(self.length_boxes)):

            if self.length_boxes[index] != self.last_modified:

                self.length_boxes[index].tk_box.delete(1.0, tk.END)
                self.length_boxes[index].tk_box.insert(tk.END, data.lengths[index])
                self.length_boxes[index].tk_box.edit_modified(False)
    


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



    def ambiguous_toggle(self, mode = Data.NONE):

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



    def place_labels(self, type, data: Logic | None = None):

        if data == None: data = self.logic

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