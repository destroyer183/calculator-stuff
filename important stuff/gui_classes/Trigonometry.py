import tkinter as tk
from tkinter import *
from parsers.trig_parser import Logic, Data



''' NOTES

if the user inputs 4 values, like 3 sides and 1 angle, and the triangle wouldn't technically be possible, make code to check for this.

add thingy that points to the 'clear' button if someone keeps trying to change values after they were calculated
use the flash() method whenever the user tries to edit a text box after things have been calculated - https://www.tutorialspoint.com/python/tk_button.htm

allow the user to input angles over 180* by using modulus

there's still a problem with the impossible triangle detection, as part of it is based in the 'solve_triangle()' function, which means that unnecesary stuff gets calculated.

'''

# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)



# reference x positions to make it easier to move boxes around when the mode is changed
ANGLE_TEXT_REFX = 100
ANGLE_BOX_REFX  = 170

LENGTH_TEXT_REFX = 350
LENGTH_BOX_REFX = 420



class Gui:

    is_ambiguous = False

    def __init__(self, parent) -> None:

        Gui.is_ambiguous = True

        self.parent = parent
        self.ambiguous_triangle = False
        self.mode_toggle = False 
        self.logic = Logic(False, 'Logic')
        self.ambiguous = Logic(True, 'ambiguous')



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



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def create_gui(self):

        self.clear_gui()

        self.parent.title('Trigonometry Calculator')

        self.parent.geometry('650x850')

        self.parent.bind("<KeyRelease>", self.keybindings)

        self.canvas = Canvas(self.parent, width = 650, height = 654)

        self.canvas.pack(fill = BOTH)

        self.canvas.create_rectangle(0, 650, 650, 654, fill='black')

        self.reset_button = tk.Button(self.parent, text='Clear', anchor='center', bg='white', command=lambda:self.clear_data())
        self.reset_button.configure(font=('Arial', 15, 'bold'))
        self.reset_button.place(x = 5, y = 660)

        self.mode_button = tk.Button(self.parent, text='Automatic', anchor='center', bg='white', command=lambda:self.swap_modes())
        self.mode_button.configure(font=('Arial', 15, 'bold'))
        self.mode_button.place(x = 325, y = 660, anchor='n')

        self.ambiguous_button = tk.Button(self.parent, text='case 1', anchor='center', bg='white', command=lambda:self.ambiguous_toggle())
        self.ambiguous_button.configure(font=('Arial', 15, 'bold'))

        self.error_text = tk.Label(self.parent, text='')
        self.error_text.configure(font=('Arial', 25, 'bold'))
        
        self.calculate = tk.Button(self.parent, text='Calculate', anchor='center', bg='white', command=lambda:self.text_boxes_callback(None))
        self.calculate.configure(font=('Arial', 15, 'bold'))
        
        self.angle_boxes  = [0, 0, 0]
        self.length_boxes = [0, 0, 0]

        self.angle_text  = tk.Label(self.parent, text = 'A = \nB = \nC = ')
        self.length_text = tk.Label(self.parent, text = 'a = \nb = \nc = ')

        self.angle_boxes[0]  = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.angle_boxes[1]  = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.angle_boxes[2]  = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[0] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[1] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[2] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')

        self.angle_text. configure(font=('Arial', 26, 'bold'))
        self.length_text.configure(font=('Arial', 26, 'bold'))

        self.angle_boxes[0]. configure(font=('Arial', 20))
        self.angle_boxes[1]. configure(font=('Arial', 20))
        self.angle_boxes[2]. configure(font=('Arial', 20))
        self.length_boxes[0].configure(font=('Arial', 20))
        self.length_boxes[1].configure(font=('Arial', 20))
        self.length_boxes[2].configure(font=('Arial', 20))

        self.angle_text. place(x = ANGLE_TEXT_REFX, y = 705)
        self.length_text.place(x = LENGTH_TEXT_REFX, y = 705)

        self.angle_boxes[0]. place(x = ANGLE_BOX_REFX, y = 709)
        self.angle_boxes[1]. place(x = ANGLE_BOX_REFX, y = 751)
        self.angle_boxes[2]. place(x = ANGLE_BOX_REFX, y = 792)
        self.length_boxes[0].place(x = LENGTH_BOX_REFX, y = 709)
        self.length_boxes[1].place(x = LENGTH_BOX_REFX, y = 751)
        self.length_boxes[2].place(x = LENGTH_BOX_REFX, y = 792)

        self.labels = {'A': '', 'B': '', 'C': '', 'a': '', 'b': '', 'c': ''}

        for key in self.labels.keys():

            self.labels[key] = tk.Label(self.parent, text=key, anchor='center', width=1, height=1)
            self.labels[key].configure(font=('Arial', 24, 'bold'))

        for box in self.angle_boxes + self.length_boxes:

            box.edit_modified(False)



        self.clear_data()

        self.parent.resizable(False, False)



    def keybindings(self, input = None):

        try: temp = input.keysym
        except:return

        print(f"keysm type: {type(input.keysym)}")

        if input.char == "\r": self.text_boxes_callback(None)
        if input.keycode == 27: self.clear_data()
        if input.char == "m": self.swap_modes()
        if input.char == "t" and self.ambiguous_triangle: self.ambiguous_toggle()
        else: self.text_boxes_callback(input)



    def swap_modes(self):

        self.mode_toggle = not self.mode_toggle

        if self.mode_toggle:
            
            self.mode_button.configure(text='Manual')
            self.calculate.place(x = 550, y = 750, anchor='n')

            self.angle_text. place(x = ANGLE_TEXT_REFX  - 75, y = 705)
            self.length_text.place(x = LENGTH_TEXT_REFX - 75, y = 705)

            self.angle_boxes[0]. place(x = ANGLE_BOX_REFX  - 75, y = 709)
            self.angle_boxes[1]. place(x = ANGLE_BOX_REFX  - 75, y = 751)
            self.angle_boxes[2]. place(x = ANGLE_BOX_REFX  - 75, y = 792)
            self.length_boxes[0].place(x = LENGTH_BOX_REFX - 75, y = 709)
            self.length_boxes[1].place(x = LENGTH_BOX_REFX - 75, y = 751)
            self.length_boxes[2].place(x = LENGTH_BOX_REFX - 75, y = 792)

        else:

            self.mode_button.configure(text='Automatic')
            self.calculate.place_forget()

            self.angle_text. place(x = ANGLE_TEXT_REFX,  y = 705)
            self.length_text.place(x = LENGTH_TEXT_REFX, y = 705)
    
            self.angle_boxes[0]. place(x = ANGLE_BOX_REFX,  y = 709)
            self.angle_boxes[1]. place(x = ANGLE_BOX_REFX,  y = 751)
            self.angle_boxes[2]. place(x = ANGLE_BOX_REFX,  y = 792)
            self.length_boxes[0].place(x = LENGTH_BOX_REFX, y = 709)
            self.length_boxes[1].place(x = LENGTH_BOX_REFX, y = 751)
            self.length_boxes[2].place(x = LENGTH_BOX_REFX, y = 792)



    def clear_data(self):

        for box in self.angle_boxes + self.length_boxes:
            box.delete(1.0, tk.END)
            box.edit_modified(False)

        try:self.canvas.delete(self.triangle)
        except:pass

        self.logic.angles = [60, 60, 60]
        self.logic.lengths = [1, 1, 1]

        self.ambiguous_toggle(Data.DELETE)

        self.place_triangle(self.logic.calculate_triangle(False), no=True)

        self.text_boxes_callback(-2147483648)

        Gui.is_ambiguous = False
        


    def edit_triangle(self, type = ''):

        if type == Data.DELETE:
            self.error_text.place_forget()
            return

        elif type == Data.UNSOLVABLE:
            self.error_text.configure(text='not enough information')

        elif type == Data.IMPOSSIBLE:
            self.error_text.configure(text='triangle does not exist')

        elif type == Data.CLEAR_DATA:
            self.clear_data()
            return
        
        else:return

        try:self.canvas.delete(self.triangle)
        except:pass

        self.place_labels(type=Data.DELETE)
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

        self.triangle = self.canvas.create_polygon(points, outline='black', fill='white', width=3)

        if no: return
        self.update_text_boxes(data)



    def ambiguous_toggle(self, mode = ''):

        if mode == Data.DELETE:

            self.ambiguous_triangle = False
            self.ambiguous_button.place_forget()
            return

        if Gui.is_ambiguous:

            self.ambiguous_triangle = True
            self.ambiguous_button.configure(text='case 2')
            self.ambiguous_button.place(x = 5, y = 600)
            self.place_triangle(self.ambiguous)

        elif not Gui.is_ambiguous:

            self.ambiguous_triangle = True
            self.ambiguous_button.configure(text='case 1')
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