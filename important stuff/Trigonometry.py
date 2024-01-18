import tkinter as tk
from tkinter import *
import keyboard
import math



''' NOTES

add thingy that points to the 'clear' button if someone keeps trying to change values after they were calculated

'''


max_side_length = 450

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

    def __init__(self) -> None:

        self.angles  = []
        self.lengths = []
        self.coordinates   = {"a": [0, 0], "b": [0, 0], "c": [0, 0]}
        self.angle_labels  = {"A": [0, 0], "B": [0, 0], "C": [0, 0]}
        self.length_labels = {"a": [0, 0], "b": [0, 0], "c": [0, 0]}



    def cos_law(self, type, index):

        if type == 'side angle side':
            
            part_1 = self.info('left side', index) ** 2 + self.info('right side', index) ** 2
            part_2 = 2 * self.info('left side', index) * self.info('right side', index) * math.cos(math.radians(self.info('opposite angle', index)))

            return math.sqrt(part_1 - part_2)

        if type == 'side side side':

            numerator = self.info('left side', index) ** 2 + self.info('right side', index) ** 2 - self.lengths[index] ** 2
            denominator = 2 * self.info('left side', index) * self.info('right side', index)

            return math.degrees(math.acos(numerator / denominator))
        


    def sin_law(self, type, index, angle_index):

        if type == 'angle':

            return math.degrees(math.asin(math.sin(math.radians(self.angles[angle_index])) / self.info('opposite side', angle_index) * self.info('opposite side', index)))
        
        elif type == 'side':

            return math.sin(math.radians(self.info('opposite angle', index))) / (math.sin(math.radians(self.angles[angle_index])) / self.info('opposite side', angle_index))
        


    def info(self, info, index, return_type = 0):

        if info == 'opposite side':
            return self.lengths[index]
        
        elif info == 'opposite angle':
            return self.angles[index]

        elif info == 'adjacent side left':
            if index == 0: array, i = self.lengths, 2
            if index == 1: array, i = self.lengths, 0
            if index == 2: array, i = self.lengths, 1

        elif info == 'adjacent side right':
            if index == 0: array, i = self.lengths, 1
            if index == 1: array, i = self.lengths, 2
            if index == 2: array, i = self.lengths, 0

        elif info == 'adjacent angle left':
            if index == 0: array, i = self.angles, 2
            if index == 1: array, i = self.angles, 0
            if index == 2: array, i = self.angles, 1

        elif info == 'adjacent angle right':
            if index == 0: array, i = self.angles, 1
            if index == 1: array, i = self.angles, 2
            if index == 2: array, i = self.angles, 0

        elif info == 'left side':
            if index == 0: array, i = self.lengths, 1
            if index == 1: array, i = self.lengths, 2
            if index == 2: array, i = self.lengths, 0

        elif info == 'right side':
            if index == 0: array, i = self.lengths, 2
            if index == 1: array, i = self.lengths, 0
            if index == 2: array, i = self.lengths, 1

        elif info == 'left angle':
            if index == 0: array, i = self.angles, 1
            if index == 1: array, i = self.angles, 2
            if index == 2: array, i = self.angles, 0

        elif info == 'right angle':
            if index == 0: array, i = self.angles, 2
            if index == 1: array, i = self.angles, 0
            if index == 2: array, i = self.angles, 1

        if return_type: return i

        return array[i]



    def check_triangle(self):

        ambiguous = False

        # calculate if triangle is solvable
        count = 0
        for index in range(len(self.angles)):
            if self.angles[index] != 0: count += 1

        for index in range(len(self.lengths)):
            if self.lengths[index] != 0: count += 1

        print(f"count: {count}")

        if not count: return 'clear data', 0

        if count < 3: return 'unsolvable', 0

        if max(self.lengths) == 0 and count <= 3: 
            self.lengths = [1, 1, 1]



        # DON'T FORGET ABOUT THE AMBIGUOUS CASE!!!
        for index in range(len(self.angles)):
            
            if self.angles[index] < 90 and (
                    self.info('adjacent side left', index) > self.info('opposite side', index) or
                    self.info('adjacent side right', index) > self.info('opposite side', index)):
                
                # do something for ambiguous case
                ambiguous = True

        # check if triangle can exist
        if min(self.lengths):
            if max(self.lengths) >= 2 * (self.lengths[0] + self.lengths[1] + self.lengths[2] - max(self.lengths)): return 'impossible', 0


        return 'yes', ambiguous
    


    def solve_triangle(self):
        
        # all sides
        if min(self.lengths):
            for index in range(len(self.angles)):
                if not self.angles[index]: self.angles[index] = self.cos_law('side side side', index)

            return
        
        # two sides one angle
        if self.ambiguous:
            pass

        print(f"angles find 0: {find(self.angles, 0)}")
        print(f"angles rfind 0: {rfind(self.angles, 0)}")

        print(f"angles: {self.angles}")

        # calculate 3rd angle if there are already 2 angles
        if find(self.angles, 0) == rfind(self.angles, 0) or min(self.angles):

            index = self.angles.index(min(self.angles))

            self.angles[index] = 180 - self.info('left angle', index) - self.info('right angle', index)

            print(f"lengths: {self.lengths}")
            print(f"lengths find 0: {find(self.lengths, 0)}")
            print(f"lengths rfind 0: {rfind(self.lengths, 0)}")

            # side angle angle angle
            if find(self.lengths, 0) != rfind(self.lengths, 0):

                for index in range(len(self.lengths)):

                    if not self.lengths[index]:

                        self.lengths[index] = self.sin_law('side', index, self.lengths.index(max(self.lengths)))

                return


        # side angle side
        for index in range(len(self.angles)):

            if self.angles[index] and (self.info('adjacent side left', index) and self.info('adjacent side right', index)):
                self.lengths[index] = self.cos_law('side angle side', index)

                return self.solve_triangle()
            


        # side side angle
        last_side = self.lengths.index(0)

        print(f"angles: {self.angles}")
        print(f"lengths: {self.lengths}")
        print(f"lengths rfind 0: {rfind(self.lengths, 0)}")

        self.lengths[last_side] = self.sin_law('side', last_side, self.angles.index(max(self.angles)))

        return self.solve_triangle()
    



    def build_triangle(self):

        # scale side lengths
        scale_ratio = max_side_length / max(self.lengths)
        self.temp = [x * scale_ratio for x in self.lengths]

        # calculate coordinates for the triangle points
        self.coordinates["a"] = [0.0, self.temp[2] * math.sin(math.radians(self.angles[0]))]
        self.coordinates["b"] = [self.temp[2] * math.cos(math.radians(self.angles[0])), 0.0]
        self.coordinates["c"] = [self.temp[1], self.temp[2] * math.sin(math.radians(self.angles[0]))]

        # calculate the necessary coordinate offsets
        x_offset = 325 - (max([x[0] for x in self.coordinates.values()]) + min([x[0] for x in self.coordinates.values()])) / 2
        y_offset = 325 - (max([y[1] for y in self.coordinates.values()]) + min([y[1] for y in self.coordinates.values()])) / 2


        # offset the coordinates to center the triangle
        for point in self.coordinates.values():

            point[0] += x_offset
            point[1] += y_offset


    
    def calculate_triangle(self):

        print('yes')

        # check if triangle is solvable
        output, self.ambiguous = self.check_triangle()

        if output != 'yes': return output

        # solve triangle
        self.solve_triangle()
            
        # calculate coordinates
        self.build_triangle()

        return self.coordinates



    def calculate_labels(self):

        offset = 35

        # calculate angle labels
        for index, key in enumerate(self.angle_labels.keys()):

            print(f"coords: {self.coordinates}")

            angle_coord = [x for x in self.coordinates.values()][index]

            point1 = [x for x in self.coordinates.values()][self.info('adjacent angle left', index, 1)]
            point2 = [x for x in self.coordinates.values()][self.info('adjacent angle right', index, 1)]

            midpoint = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]

            print(f"points: {point1}, {point2}")
            print(f"midpoint: {midpoint}\n")

            try: angle = math.degrees(math.atan((max(angle_coord[1], midpoint[1]) - min(angle_coord[1], midpoint[1])) / (max(angle_coord[0], midpoint[0]) - min(angle_coord[0], midpoint[0]))))
            except: angle = 0

            x_offset = offset * math.cos(math.radians(angle))
            y_offset = offset * math.sin(math.radians(angle))

            if midpoint[0] - angle_coord[0] > 0: x_offset *= -1
            if midpoint[1] - angle_coord[1] > 0: y_offset *= -1

            self.angle_labels[key] = [angle_coord[0] + x_offset, angle_coord[1] + y_offset]


            
            try:angle = math.degrees(math.atan((max(point1[1], point2[1]) - min(point1[1], point2[1])) / (max(point1[0], point2[0]) - min(point1[0], point2[0])))) + 90
            except: angle = 0

            x_offset = offset * math.cos(math.radians(angle))
            y_offset = offset * math.sin(math.radians(angle))

            if midpoint[0] - angle_coord[0] > 0: x_offset *= -1
            if midpoint[1] - angle_coord[1] > 0: y_offset *= -1

            self.length_labels[key.lower()] = [midpoint[0] + x_offset, midpoint[1] - y_offset]
            


class Gui:

    def __init__(self, parent) -> None:

        self.parent = parent



    # function to detect optionmenu changes
    def text_boxes_callback(self, some_value_idk):

        for box in self.angle_boxes + self.length_boxes:

            if box.data.edit_modified():

                try: 
                    if box != self.last_modified:

                        # loop through all boxes, and reset the previous last modified box
                        for item in self.angle_boxes + self.length_boxes:
                            item.data.edit_modified(False)

                        self.last_modified = box

                except: self.last_modified = box

                box.data.edit_modified(False)

                self.logic.angles = [x.data.get(1.0, tk.END) for x in self.angle_boxes]
                self.logic.lengths = [x.data.get(1.0, tk.END) for x in self.length_boxes]

                for index in range(len(self.logic.angles)):
                    try: self.logic.angles[index] = float(self.logic.angles[index])
                    except: self.logic.angles[index] = 0

                for index in range(len(self.logic.lengths)):
                    try: self.logic.lengths[index] = float(self.logic.lengths[index])
                    except: self.logic.lengths[index] = 0

                # print(f"calculate triangle: {self.logic.calculate_triangle()}")

                # self.logic.calculate_labels()

                self.place_triangle(self.logic.calculate_triangle())

                # self.place_labels()



    def clear_gui(self):

        keyboard.unhook_all_hotkeys()

        for widget in self.parent.winfo_children():
            widget.destroy()



    def create_gui(self):

        self.clear_gui()

        self.parent.title('Trigonometry Calculator')

        self.parent.geometry('650x850')

        self.logic = Logic()

        keyboard.hook(self.text_boxes_callback)

        self.reset_button = tk.Button(self.parent, text='Clear', anchor='center', bg='white', command=lambda:self.clear_data())
        self.reset_button.configure(font=('Arial', 15, 'bold'))
        self.reset_button.place(x = 5, y = 655)

        # add button to rotate triangle

        self.canvas = Canvas(self.parent, width = 650, height = 654)

        self.canvas.pack(fill = BOTH)

        self.canvas.create_rectangle(0, 650, 650, 654, fill='black')

        self.make_angle_text()

        self.make_length_text()

        self.place_labels('create')
        
        self.triangle_error('create')

        self.clear_data()





              

        # change the shape of the triangle to match the inputted values

        # limit the size of the triangle

        # have a reset button

        # have text boxes at the bottom for each side length and angle value

        self.parent.resizable(False, False)



    def make_angle_text(self):
        
        self.angle_text = tk.Label(self.parent, text = 'A = \nB = \nC = ')
        self.angle_text.configure(font=('Arial', 26, 'bold'))
        self.angle_text.place(x = 100, y = 695)

        self.angle_boxes = [0, 0, 0]

        self.angle_boxes[0] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.angle_boxes[0].configure(font=('Arial', 20))
        self.angle_boxes[0].place(x = 170, y = 699)

        self.angle_boxes[1] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.angle_boxes[1].configure(font=('Arial', 20))
        self.angle_boxes[1].place(x = 170, y = 741)

        self.angle_boxes[2] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.angle_boxes[2].configure(font=('Arial', 20))
        self.angle_boxes[2].place(x = 170, y = 782)

        for box in self.angle_boxes:

            box.data.edit_modified(False)



    def make_length_text(self):

        self.length_text = tk.Label(self.parent, text = 'a = \nb = \nc = ')
        self.length_text.configure(font=('Arial', 26, 'bold'))
        self.length_text.place(x = 350, y = 695)

        self.length_boxes = [0, 0, 0]

        self.length_boxes[0] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[0].configure(font=('Arial', 20))
        self.length_boxes[0].place(x = 420, y = 699)

        self.length_boxes[1] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[1].configure(font=('Arial', 20))
        self.length_boxes[1].place(x = 420, y = 741)

        self.length_boxes[2] = tk.Text(self.parent, height = 1, width = 8, bg = 'white')
        self.length_boxes[2].configure(font=('Arial', 20))
        self.length_boxes[2].place(x = 420, y = 782)

        for box in self.length_boxes:

            box.data.edit_modified(False)



    def clear_data(self):

        for box in self.angle_boxes + self.length_boxes:
            box.data.delete(1.0, tk.END)
            box.data.edit_modified(False)

        try:self.canvas.delete(self.triangle)
        except:pass

        self.logic.coordinates = {'a': [100.0, 519.8557158514986], 'b': [325.00000000000006, 130.14428414850133], 'c': [550.0, 519.8557158514986]}

        self.place_triangle(self.logic.coordinates, no=True)

        self.text_boxes_callback(-2147483648)
        


    def triangle_error(self, type = ''):

        if type == 'delete':

            self.error_text.place_forget()
            return

        elif type == 'unsolvable':

            self.error_text.configure(text='not enough information')

        elif type == 'impossible':

            self.error_text.configure(text='triangle does not exist')

        elif type == 'create':

            self.error_text = tk.Label(self.parent, text='')
            self.error_text.configure(font=('Arial', 25, 'bold'))
            return
        
        elif type == 'clear data':

            self.clear_data()
            return
        
        else:return

        try:self.canvas.delete(self.triangle)
        except:pass

        self.error_text.place(x = 125, y = 325)
        self.place_labels('delete')
        return 1

        

    def update_text_boxes(self):

        for index in range(len(self.angle_boxes)):

            if self.angle_boxes[index] != self.last_modified:

                self.angle_boxes[index].data.delete(1.0, tk.END)
                self.angle_boxes[index].data.insert(tk.END, self.logic.angles[index])

                self.angle_boxes[index].data.edit_modified(False)

        for index in range(len(self.length_boxes)):

            if self.length_boxes[index] != self.last_modified:

                self.length_boxes[index].data.delete(1.0, tk.END)
                self.length_boxes[index].data.insert(tk.END, self.logic.lengths[index])

                self.length_boxes[index].data.edit_modified(False)
    


    def place_triangle(self, coordinates, no = False):

        if self.triangle_error(coordinates): return

        self.place_labels()
        
        # something gotta be here for ambiguous case

        points = [coordinates["a"][0], coordinates["a"][1], coordinates["b"][0], coordinates["b"][1], coordinates["c"][0], coordinates["c"][1]]

        try: self.canvas.delete(self.triangle)
        except:pass
        try: self.triangle_error('delete')
        except:pass

        self.triangle = self.canvas.create_polygon(points, outline='black', fill='white', width=3)

        if no: return
        self.update_text_boxes()



    def place_labels(self, type = ''):

        if type == 'create':

            self.labels = {}

            for key in self.logic.angle_labels.keys():

                self.labels[key] = tk.Label(self.parent, text=key, anchor='center', width=1, height=1)
                self.labels[key].configure(font=('Arial', 25, 'bold'))

            for key in self.logic.length_labels.keys():

                self.labels[key] = tk.Label(self.parent, text=key, anchor='center', width=1, height=1)
                self.labels[key].configure(font=('Arial', 25, 'bold'))

        elif type == 'delete':

            for key in self.labels.keys():

                self.labels[key].place_forget()

        else: 

            self.logic.calculate_labels()

            print(f"angle labels: {self.logic.angle_labels}")
            print(f"length labels: {self.logic.length_labels}")
            print(f"all labels: {self.logic.angle_labels | self.logic.length_labels}")

            for key in self.labels.keys():

                print(f"label data: {self.labels[key]}")

                self.labels[key].place(x = (self.logic.angle_labels | self.logic.length_labels)[key][0] - 12.5, y = (self.logic.angle_labels | self.logic.length_labels)[key][1] - 12.5)



def main():
    pass

if __name__ == '__main__':
    main()