import tkinter as tk
from tkinter import *
import keyboard
import math



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

    print('finding...')

    for index in range(len(container) - 1, -1, -1):

        print(f"index: {index}")

        if container[index] == value: return index

    #  find() = [0, 1, 2, 3, 4, 0, 1, 2]
    x         = [1, 2, 3, 4, 5, 1, 2, 3]
    # rfind() = [5, 6, 7, 3, 4, 5, 6, 7]




class Logic:

    def __init__(self) -> None:

        self.angles  = []
        self.lengths = []
        self.coordinates   = {"A": [0, 0], "B": [0, 0], "C": [0, 0]}
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
            if index == 0: array, i = self.angles, 1
            if index == 1: array, i = self.angles, 2
            if index == 2: array, i = self.angles, 0

        elif info == 'adjacent angle right':
            if index == 0: array, i = self.angles, 2
            if index == 1: array, i = self.angles, 0
            if index == 2: array, i = self.angles, 1

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

            if self.angles[index] != 0 or self.lengths[index] != 0: count += 1

        if count < 3: return 0, 0

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
            if max(self.lengths) >= 2 * (self.lengths[0] + self.lengths[1] + self.lengths[2] - max(self.lengths)): return 1, 0


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

            print('fuck')

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
        self.lengths = [x * scale_ratio for x in self.lengths]

        # calculate coordinates for the triangle points
        self.coordinates["A"] = [0.0, self.lengths[2] * math.sin(math.radians(self.angles[0]))]
        self.coordinates["B"] = [self.lengths[2] * math.cos(math.radians(self.angles[0])), 0.0]
        self.coordinates["C"] = [self.lengths[1], self.lengths[2] * math.sin(math.radians(self.angles[0]))]

        # calculate the necessary coordinate offsets
        x_offset = 325 - (max([x[0] for x in self.coordinates.values()]) + min([x[0] for x in self.coordinates.values()])) / 2
        y_offset = 325 - (max([y[1] for y in self.coordinates.values()]) + min([y[1] for y in self.coordinates.values()])) / 2


        # offset the coordinates to center the triangle
        for point in self.coordinates.values():

            point[0] += x_offset
            point[1] += y_offset


    
    def calculate_triangle(self):

        # check if triangle is solvable
        output, self.ambiguous = self.check_triangle()

        if output != 'yes': return output

        # solve triangle
        self.solve_triangle()
            
        # calculate coordinates
        self.build_triangle()

        return self.coordinates



    def calculate_labels(self):

        # don't use the center of the triangle to calculate these values

        return # self.angle_labels, self.length_labels




class Gui:

    detect_update = None

    def __init__(self, parent) -> None:

        self.parent = parent



    # function to detect optionmenu changes
    def text_boxes_callback(self, some_value_idk):

        for box in self.angle_boxes + self.length_boxes:

            if box.edit_modified():

                self.logic.angles = [x.get(1.0, tk.END) for x in self.angle_boxes]
                self.logic.lengths = [x.get(1.0, tk.END) for x in self.length_boxes]

                for index in range(len(self.logic.angles)):
                    try: self.logic.angles[index] = float(self.logic.angles[index])
                    except: self.logic.angles[index] = 0

                for index in range(len(self.logic.lengths)):
                    try: self.logic.lengths[index] = float(self.logic.lengths[index])
                    except: self.logic.lengths[index] = 0

                self.place_triangle(self.logic.calculate_triangle())

                box.edit_modified(False)



    def clear_gui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()



    def create_gui(self):

        self.clear_gui()

        self.parent.title('Trigonometry Calculator')

        self.parent.geometry('650x850')

        self.logic = Logic()

        keyboard.hook(self.text_boxes_callback)

        self.keybindings()

        self.reset_button = tk.Button(self.parent, text='Reset', anchor='center', bg='white', command=lambda:self.default_values())
        self.reset_button.configure(font=('Arial', 15, 'bold'))
        self.reset_button.place(x = 5, y = 655)



        # add button to rotate triangle

        self.canvas = Canvas(self.parent, width = 650, height = 654)

        self.canvas.pack(fill = BOTH)

        self.canvas.create_rectangle(0, 650, 650, 654, fill='black')

        self.make_angle_text()

        self.make_length_text()

        self.default_values()

        self.text_boxes_callback(-2147483648)        




        # change the shape of the triangle to match the inputted values

        # limit the size of the triangle

        # have a reset button

        # have text boxes at the bottom for each side length and angle value

        self.parent.resizable(False, False)



    def initialize_triangle(self):

        points = [100, 519.86, 325, 130.14, 550, 519.86]

        self.triangle = self.canvas.create_polygon(points, outline='black', fill='white', width=5)

        # median of angle A: (100, -519.86) (437.5, -325)
        # slope: 0.577
        # y-int: -577.4375
        # equation: y = 0.577x - 577.4375

        # median of angle C: (212.5, -325) (550, -519.86)
        # slope: -0.577
        # y-int: -202.51
        # equation: y = -0.577x -202.51

        # midpoint: (325, -389.974)



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

            box.edit_modified(False)




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

            box.edit_modified(False)



    def default_values(self):

        self.angle_boxes[0].delete(1.0, tk.END)
        self.angle_boxes[1].delete(1.0, tk.END)
        self.angle_boxes[2].delete(1.0, tk.END)
        self.length_boxes[0].delete(1.0, tk.END)
        self.length_boxes[1].delete(1.0, tk.END)
        self.length_boxes[2].delete(1.0, tk.END)

        self.angle_boxes[0].insert(tk.END, 60)
        self.angle_boxes[1].insert(tk.END, 60)
        self.angle_boxes[2].insert(tk.END, 60)
        self.length_boxes[0].insert(tk.END, 1)
        self.length_boxes[1].insert(tk.END, 1)
        self.length_boxes[2].insert(tk.END, 1)



    def impossible_triangle(self):

        try: self.canvas.delete(self.triangle)
        except:pass

        self.error_text = tk.Label(self.parent, text='Triangle does not exist.')
        self.error_text.configure(font=['Arial', 25, 'bold'])
        self.error_text.place(x = 125, y = 325)

        # hide labels


    
    def unsolvable_triangle(self):

        try: self.canvas.delete(self.triangle)
        except:pass

        self.error_text = tk.Label(self.parent, text='not enough information.')
        self.error_text.configure(font=['Arial', 25, 'bold'])
        self.error_text.place(x = 125, y = 325)



    



    def place_triangle(self, coordinates):

        if coordinates == 0:
            self.unsolvable_triangle()
            return

        if coordinates == 1:
            self.impossible_triangle()
            return

        points = [coordinates["A"][0], coordinates["A"][1], coordinates["B"][0], coordinates["B"][1], coordinates["C"][0], coordinates["C"][1]]

        try: self.canvas.delete(self.triangle)
        except:pass
        try: 
            self.error_text.place_forget()
            print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
        except:pass

        self.triangle = self.canvas.create_polygon(points, outline='black', fill='white', width=3)

        self.place_labels()



    def place_labels(self):

        pass




    




        


    def keybindings(self):

        pass




def main():

    #  find() = [0, 1, 2, 3, 4, 0, 1, 2]
    x         = [1, 2, 3, 4, 5, 1, 2, 3]
    # rfind() = [5, 6, 7, 3, 4, 5, 6, 7]
    x = [0, 1, 0]
    
    print(f"rfind 2: {rfind(x, 0)}")

if __name__ == '__main__':
    main()