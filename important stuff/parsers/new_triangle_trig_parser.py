from enum import Enum
import math
import sys



# the max pixel side length for the triangle displayed
MAX_SIDE_LENGTH = 450



class Data(Enum):
    DELETE = 'delete'
    UNSOLVABLE = 'unsolvable'
    IMPOSSIBLE = 'impossible'
    CLEAR_DATA = 'clear data'
    NONE = 'none'

    def __float__(self) -> float:
        return 0.0



# find item in a container
def find(container, value):

    for index, element in enumerate(container):

        if element == value: return index



# find an item in a container but loop backwards
def rfind(container, value):

    for index in range(len(container) - 1, -1, -1):

        if container[index] == value: return index



# class for the logic of the trig calculations
class Logic:

    def __init__(self, is_ambiguous = False, name = '') -> None:

        from gui_classes.TriangleTrig import Gui

        print(f"gui ambiguous: {Gui.is_ambiguous}")

        # variable to store whether or not a triangle is ambiguous, 
        # there will be two instances of this class, one that is for the ambiguous triangle, the other for the normal triangle.
        self.is_ambiguous = is_ambiguous

        # data for the triangle
        self.angles:  list[float] = [60, 60, 60]
        self.lengths: list[float] = [1, 1, 1]
        self.coordinates:   dict[str, list[float]] = {"a": [0, 0], "b": [0, 0], "c": [0, 0]}
        self.angle_labels:  dict[str, list[float]] = {"A": [0, 0], "B": [0, 0], "C": [0, 0]}
        self.length_labels: dict[str, list[float]] = {"a": [0, 0], "b": [0, 0], "c": [0, 0]}



    # function to check if the triangle is solvable
    def check_triangle(self):
        pass



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


    
    def calculate_triangle(self):
        pass



    def calculate_labels(self):

        offset = 35

        # calculate angle labels
        for index, key in enumerate(self.angle_labels.keys()):

            angle_coord = [x for x in self.coordinates.values()][index]

            left_coord  = [x for x in self.coordinates.values()][self.info(Info.LEFT_ANGLE,  index, 1)]
            right_coord = [x for x in self.coordinates.values()][self.info(Info.RIGHT_ANGLE, index, 1)]

            try: left_alpha = math.degrees(math.atan((max(angle_coord[1], left_coord[1]) - min(angle_coord[1], left_coord[1])) / (max(angle_coord[0], left_coord[0]) - min(angle_coord[0], left_coord[0]))))
            except: left_alpha = 90
            try: right_alpha = math.degrees(math.atan((max(angle_coord[1], right_coord[1]) - min(angle_coord[1], right_coord[1])) / (max(angle_coord[0], right_coord[0]) - min(angle_coord[0], right_coord[0]))))
            except: right_alpha = 90

            if not angle_coord[0] > left_coord[0] and     angle_coord[1] < left_coord[1]: left_angle = 360 - left_alpha
            elif   angle_coord[0] > left_coord[0] and     angle_coord[1] < left_coord[1]: left_angle = 180 + left_alpha
            elif   angle_coord[0] > left_coord[0] and not angle_coord[1] < left_coord[1]: left_angle = 180 - left_alpha
            else:  left_angle = left_alpha

            if not angle_coord[0] > right_coord[0] and     angle_coord[1] < right_coord[1]: right_angle = 360 - right_alpha
            elif   angle_coord[0] > right_coord[0] and     angle_coord[1] < right_coord[1]: right_angle = 180 + right_alpha
            elif   angle_coord[0] > right_coord[0] and not angle_coord[1] < right_coord[1]: right_angle = 180 - right_alpha
            else:  right_angle = right_alpha

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
            