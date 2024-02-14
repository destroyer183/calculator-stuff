import tkinter as tk
from tkinter import *
import math
import enum



''' NOTES

add thingy that points to the 'clear' button if someone keeps trying to change values after they were calculated

allow the user to input angles over 180* by using modulus

'''


MAX_SIDE_LENGTH = 450

ANGLE_TEXT_REFX = 100
ANGLE_BOX_REFX  = 170

LENGTH_TEXT_REFX = 350
LENGTH_BOX_REFX = 420

class Trig(enum.Enum):
    SIDE_ANGLE_SIDE = 'side angle side'
    SIDE_SIDE_SIDE = 'side side side'
    ANGLE = 'angle'
    SIDE = 'side'

class Info(enum.Enum):
    OPPOSITE_SIDE = 'opposite side'
    OPPOSITE_ANGLE = 'opposite angle'
    ADJACENT_SIDE_LEFT = 'adjacent side left'
    ADJACENT_SIDE_RIGHT = 'adjacent side right'
    ADJACENT_ANGLE_LEFT = 'adjacent angle left'
    ADJACENT_ANGLE_RIGHT = 'adjacent angle right'
    LEFT_SIDE = 'left side'
    RIGHT_SIDE = 'right side'
    LEFT_ANGLE = 'left angle'
    RIGHT_ANGLE = 'right angle'

class Data(enum.Enum):
    DELETE = 'delete'
    UNSOLVABLE = 'unsolvable'
    IMPOSSIBLE = 'impossible'
    CLEAR_DATA = 'clear data'

# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)



def find(container, value):

    for index, element in enumerate(container):

        if element == value: return index


def rfind(container, value):

    for index in range(len(container) - 1, -1, -1):

        if container[index] == value: return index



class Logic:

    def __init__(self, is_ambiguous = False, name = '') -> None:

        self.is_ambiguous = is_ambiguous

        self.name = name

        self.angles  = [60, 60, 60]
        self.lengths = [1, 1, 1]
        self.coordinates   = {"a": [0, 0], "b": [0, 0], "c": [0, 0]}
        self.angle_labels  = {"A": [0, 0], "B": [0, 0], "C": [0, 0]}
        self.length_labels = {"a": [0, 0], "b": [0, 0], "c": [0, 0]}



    def cos_law(self, type, index):

        if type == Trig.SIDE_ANGLE_SIDE:
            
            part_1 = self.info(Info.LEFT_SIDE, index) ** 2 + self.info(Info.RIGHT_SIDE, index) ** 2
            part_2 = 2 * self.info(Info.LEFT_SIDE, index) * self.info(Info.RIGHT_SIDE, index) * math.cos(math.radians(self.info(Info.OPPOSITE_ANGLE, index)))

            return math.sqrt(part_1 - part_2)

        if type == Trig.SIDE_SIDE_SIDE:

            numerator = self.info(Info.LEFT_SIDE, index) ** 2 + self.info(Info.RIGHT_SIDE, index) ** 2 - self.lengths[index] ** 2
            denominator = 2 * self.info(Info.LEFT_SIDE, index) * self.info(Info.RIGHT_SIDE, index)

            return math.degrees(math.acos(numerator / denominator))
        


    def sin_law(self, type, index, angle_index):

        if type == Trig.ANGLE:

            return math.degrees(math.asin(math.sin(math.radians(self.angles[angle_index])) / self.info(Info.OPPOSITE_SIDE, angle_index) * self.info(Info.OPPOSITE_SIDE, index)))
        
        elif type == Trig.SIDE:

            return math.sin(math.radians(self.info(Info.OPPOSITE_ANGLE, index))) / (math.sin(math.radians(self.angles[angle_index])) / self.info(Info.OPPOSITE_SIDE, angle_index))
        


    def info(self, request, index, return_type = 0):

        if request == Info.OPPOSITE_SIDE:
            return self.lengths[index]
        
        elif request == Info.OPPOSITE_ANGLE:
            return self.angles[index]

        elif request == Info.ADJACENT_SIDE_LEFT:
            if index == 0: array, i = self.lengths, 2
            if index == 1: array, i = self.lengths, 0
            if index == 2: array, i = self.lengths, 1

        elif request == Info.ADJACENT_SIDE_RIGHT:
            if index == 0: array, i = self.lengths, 1
            if index == 1: array, i = self.lengths, 2
            if index == 2: array, i = self.lengths, 0

        elif request == Info.ADJACENT_ANGLE_LEFT:
            if index == 0: array, i = self.angles, 2
            if index == 1: array, i = self.angles, 0
            if index == 2: array, i = self.angles, 1

        elif request == Info.ADJACENT_ANGLE_RIGHT:
            if index == 0: array, i = self.angles, 1
            if index == 1: array, i = self.angles, 2
            if index == 2: array, i = self.angles, 0

        elif request == Info.LEFT_SIDE:
            if index == 0: array, i = self.lengths, 1
            if index == 1: array, i = self.lengths, 2
            if index == 2: array, i = self.lengths, 0

        elif request == Info.RIGHT_SIDE:
            if index == 0: array, i = self.lengths, 2
            if index == 1: array, i = self.lengths, 0
            if index == 2: array, i = self.lengths, 1

        elif request == Info.LEFT_ANGLE:
            if index == 0: array, i = self.angles, 1
            if index == 1: array, i = self.angles, 2
            if index == 2: array, i = self.angles, 0

        elif request == Info.RIGHT_ANGLE:
            if index == 0: array, i = self.angles, 2
            if index == 1: array, i = self.angles, 0
            if index == 2: array, i = self.angles, 1

        if return_type: return i

        return array[i]



    def check_triangle(self):

        # calculate if triangle is solvable
        count = 0
        for index in range(len(self.angles)):
            if self.angles[index] != 0: count += 1

        for index in range(len(self.lengths)):
            if self.lengths[index] != 0: count += 1

        if not count: return Data.CLEAR_DATA, 0

        if count < 3: return Data.UNSOLVABLE, 0

        if max(self.lengths) == 0 and count <= 3: 
            self.lengths = [1, 1, 1]



        # DON'T FORGET ABOUT THE AMBIGUOUS CASE!!!
        for index in range(len(self.angles)):

            if 0 < self.angles[index] < 90 and (
                    (self.info(Info.ADJACENT_SIDE_LEFT, index)  > self.info(Info.OPPOSITE_SIDE, index) and self.info(Info.OPPOSITE_SIDE, index)) or
                    (self.info(Info.ADJACENT_SIDE_RIGHT, index) > self.info(Info.OPPOSITE_SIDE, index) and self.info(Info.OPPOSITE_SIDE, index))):

                # do something for ambiguous case
                return 'yes', True
            
        # check if triangle can exist
        if min(self.lengths):
            if max(self.lengths) >= 2 * (self.lengths[0] + self.lengths[1] + self.lengths[2] - max(self.lengths)): return Data.IMPOSSIBLE, 0

        return 'yes', False



    def solve_triangle(self, ambiguous):
        
        # all sides
        if min(self.lengths):
            for index in range(len(self.angles)):
                if not self.angles[index]: self.angles[index] = self.cos_law(Trig.SIDE_SIDE_SIDE, index)

            return
        
        # two sides one angle
        if ambiguous:

            # find variable angle
            for index in range(len(self.lengths)):

                if self.lengths[index] and not self.info(Info.OPPOSITE_ANGLE, index):

                    if self.is_ambiguous:
                        self.angles[index] = 180 - self.sin_law(Trig.ANGLE, index, find(self.angles, max(self.angles)))

                    else:
                        self.angles[index] = self.sin_law(Trig.ANGLE, index, find(self.angles, max(self.angles)))



        # calculate 3rd angle if there are already 2 angles
        if find(self.angles, 0) == rfind(self.angles, 0) or min(self.angles):

            index = self.angles.index(min(self.angles))

            self.angles[index] = 180 - self.info(Info.LEFT_ANGLE, index) - self.info(Info.RIGHT_ANGLE, index)

            # side angle angle angle
            if find(self.lengths, 0) != rfind(self.lengths, 0):

                for index in range(len(self.lengths)):

                    if not self.lengths[index]:

                        self.lengths[index] = self.sin_law(Trig.SIDE, index, self.lengths.index(max(self.lengths)))

                return



        # side angle side
        for index in range(len(self.angles)):

            if self.angles[index] and (self.info(Info.ADJACENT_SIDE_LEFT, index) and self.info(Info.ADJACENT_SIDE_RIGHT, index)):
                self.lengths[index] = self.cos_law(Trig.SIDE_ANGLE_SIDE, index)

                return self.solve_triangle(ambiguous)
            


        # side side angle
        last_side = self.lengths.index(0)

        self.lengths[last_side] = self.sin_law(Trig.SIDE, last_side, self.angles.index(max(self.angles)))

        return self.solve_triangle(ambiguous)
    


    def build_triangle(self):

        # scale side lengths
        scale_ratio = MAX_SIDE_LENGTH / max(self.lengths)
        temp = [x * scale_ratio for x in self.lengths]

        # calculate coordinates for the triangle points
        self.coordinates['a'] = [0.0, temp[2] * math.sin(math.radians(self.angles[0]))]
        self.coordinates['b'] = [temp[2] * math.cos(math.radians(self.angles[0])), 0.0]
        self.coordinates['c'] = [temp[1], temp[2] * math.sin(math.radians(self.angles[0]))]

        # calculate the necessary coordinate offsets
        x_offset = 325 - (max([x[0] for x in self.coordinates.values()]) + min([x[0] for x in self.coordinates.values()])) / 2
        y_offset = 325 - (max([y[1] for y in self.coordinates.values()]) + min([y[1] for y in self.coordinates.values()])) / 2


        # offset the coordinates to center the triangle
        for point in self.coordinates.values():

            point[0] += x_offset
            point[1] += y_offset


    
    def calculate_triangle(self, ambiguous = False):

        # check if triangle is solvable
        output, temp = self.check_triangle()

        if temp: print('triangle is ambiguous')
        else: print('triangle is not ambiguous')

        if output != 'yes': return output

        # solve triangle
        self.solve_triangle(ambiguous)
            
        # calculate coordinates
        self.build_triangle()

        return self



    def calculate_labels(self):

        offset = 35

        # calculate angle labels
        for index, key in enumerate(self.angle_labels.keys()):

            angle_coord = [x for x in self.coordinates.values()][index]

            left_coord  = [x for x in self.coordinates.values()][self.info(Info.LEFT_ANGLE, index, 1)]
            right_coord = [x for x in self.coordinates.values()][self.info(Info.RIGHT_ANGLE, index, 1)]

            try: left_alpha = math.degrees(math.atan((max(angle_coord[1], left_coord[1]) - min(angle_coord[1], left_coord[1])) / (max(angle_coord[0], left_coord[0]) - min(angle_coord[0], left_coord[0]))))
            except: left_alpha = 90
            try: right_alpha = math.degrees(math.atan((max(angle_coord[1], right_coord[1]) - min(angle_coord[1], right_coord[1])) / (max(angle_coord[0], right_coord[0]) - min(angle_coord[0], right_coord[0]))))
            except: right_alpha = 90

            if not angle_coord[0] > left_coord[0] and angle_coord[1] < left_coord[1]: left_angle = 360 - left_alpha
            elif angle_coord[0] > left_coord[0] and angle_coord[1] < left_coord[1]: left_angle = 180 + left_alpha
            elif angle_coord[0] > left_coord[0] and not angle_coord[1] < left_coord[1]: left_angle = 180 - left_alpha
            else: left_angle = left_alpha

            if not angle_coord[0] > right_coord[0] and angle_coord[1] < right_coord[1]: right_angle = 360 - right_alpha
            elif angle_coord[0] > right_coord[0] and angle_coord[1] < right_coord[1]: right_angle = 180 + right_alpha
            elif angle_coord[0] > right_coord[0] and not angle_coord[1] < right_coord[1]: right_angle = 180 - right_alpha
            else: right_angle = right_alpha

            total_angle = (left_angle + right_angle) / 2

            x_offset = offset * math.cos(math.radians(total_angle)) * -1
            y_offset = offset * math.sin(math.radians(total_angle))

            self.angle_labels[key] = [angle_coord[0] + x_offset, angle_coord[1] + y_offset]



            midpoint = [(left_coord[0] + right_coord[0]) / 2, (left_coord[1] + right_coord[1]) / 2]
            
            try: angle = math.degrees(math.atan((max(left_coord[1], right_coord[1]) - min(left_coord[1], right_coord[1])) / (max(left_coord[0], right_coord[0]) - min(left_coord[0], right_coord[0])))) + 90
            except: angle = 0

            x_offset = offset * math.cos(math.radians(angle))
            y_offset = offset * math.sin(math.radians(angle))

            if left_coord[0] < right_coord[0] and left_coord[1] < right_coord[1]:
                if x_offset < 0: x_offset *= -1
                if y_offset > 0: y_offset *= -1

            elif left_coord[0] > right_coord[0] and left_coord[1] < right_coord[1]:
                if x_offset < 0: x_offset *= -1
                if y_offset < 0: y_offset *= -1

            elif left_coord[0] < right_coord[0] and left_coord[1] > right_coord[1]:
                if x_offset > 0: x_offset *= -1
                if y_offset > 0: y_offset *= -1

            elif left_coord[0] > right_coord[0] and left_coord[1] > right_coord[1]:
                if x_offset > 0: x_offset *= -1
                if y_offset < 0: y_offset *= -1


            elif left_coord[0] == right_coord[0] and left_coord[1] == angle_coord[1] and left_coord[0] < angle_coord[0]:
                if x_offset > 0: x_offset *= -1

            elif left_coord[0] == right_coord[0] and right_coord[1] == angle_coord[1] and right_coord[0] > angle_coord[0]:
                if x_offset < 0: x_offset *= -1


            self.length_labels[key.lower()] = [midpoint[0] + x_offset, midpoint[1] + y_offset]
            


class Gui:

    is_ambiguous = False

    def __init__(self, parent) -> None:

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