from enum import Enum
import math
import sys



# the max pixel side length for the triangle displayed
MAX_SIDE_LENGTH = 450



# enums
class Trig(Enum):
    SIDE_ANGLE_SIDE = 'side angle side'
    SIDE_SIDE_SIDE = 'side side side'
    ANGLE = 'angle'
    SIDE = 'side'

class Info(Enum):
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

class Data(Enum):
    DELETE = 'delete'
    UNSOLVABLE = 'unsolvable'
    IMPOSSIBLE = 'impossible'
    CLEAR_DATA = 'clear data'



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

        from gui_classes.Trigonometry import Gui

        print(f"gui ambiguous: {Gui.is_ambiguous}")

        # variable to store whether or not a triangle is ambiguous, 
        # there will be two instances of this class, one that is for the ambiguous triangle, the other for the normal triangle.
        self.is_ambiguous = is_ambiguous

        # data for the triangle
        self.angles  = [60, 60, 60]
        self.lengths = [1, 1, 1]
        self.coordinates   = {"a": [0, 0], "b": [0, 0], "c": [0, 0]}
        self.angle_labels  = {"A": [0, 0], "B": [0, 0], "C": [0, 0]}
        self.length_labels = {"a": [0, 0], "b": [0, 0], "c": [0, 0]}



    # calculations for cosine law
    def cos_law(self, type, index):

        # check if the side-angle-side cosine law is being used
        if type == Trig.SIDE_ANGLE_SIDE:
            
            # sum the squares of the two given sides
            part_1 = self.info(Info.LEFT_SIDE, index) ** 2 + self.info(Info.RIGHT_SIDE, index) ** 2

            # multiply the two given sides together and then multiply by two and then multiply by the cosine of the given angle
            part_2 = 2 * self.info(Info.LEFT_SIDE, index) * self.info(Info.RIGHT_SIDE, index) * math.cos(math.radians(self.info(Info.OPPOSITE_ANGLE, index)))

            # return the square root of part 1 minus part 2
            return math.sqrt(part_1 - part_2)

        # check if the side-side-side cosine law is being used
        if type == Trig.SIDE_SIDE_SIDE:

            # calculate the numerator of the equation, left side squared plus right side squared minus opposite side squared
            numerator = self.info(Info.LEFT_SIDE, index) ** 2 + self.info(Info.RIGHT_SIDE, index) ** 2 - self.lengths[index] ** 2

            # calculate the denominator of the equation, two times the left side times the right side
            denominator = 2 * self.info(Info.LEFT_SIDE, index) * self.info(Info.RIGHT_SIDE, index)

            # return the inverse sine of the numerator divided by the denominator
            return math.degrees(math.acos(numerator / denominator))
        

 
    # function to calculate sine law
    def sin_law(self, type, index, angle_index):

        try:

            # check if an angle is being calculated
            if type == Trig.ANGLE:

                # return the inverse sine of the sine of the given angle divided by the opposite side, divided by the opposite side of the angle we are solving for.
                return math.degrees(math.asin(math.sin(math.radians(self.angles[angle_index])) / self.info(Info.OPPOSITE_SIDE, angle_index) * self.info(Info.OPPOSITE_SIDE, index)))
            
            # check if a side is being solved
            elif type == Trig.SIDE:

                # return the sine of the opposite angle divided by (the sine of the given angle divided by the opposite side)
                return math.sin(math.radians(self.info(Info.OPPOSITE_ANGLE, index))) / (math.sin(math.radians(self.angles[angle_index])) / self.info(Info.OPPOSITE_SIDE, angle_index))

        except ValueError:
            err_type, value, traceback = sys.exc_info()
            print(f"\nVALUE ERROR ENCOUNTERED:\nerror type: {err_type}\nvalue: {value}\ntraceback: {traceback}\n")
            return Data.IMPOSSIBLE



    # function to return information about the current triangle
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

        # return just the index of the requested information
        if return_type: return i

        # return the requested information
        return array[i]



    # function to check if the triangle is solvable
    def check_triangle(self):

        # count the amount of given information
        count = 0
        for index in range(len(self.angles)):
            if self.angles[index] != 0: count += 1

        for index in range(len(self.lengths)):
            if self.lengths[index] != 0: count += 1

        # if the count is zero, return an identifier that tells the calculator to clear the current data
        if not count: return Data.CLEAR_DATA, 0

        # if the count is less than three, return an identifier that tells the calculator that there isnt enough information to solve the triangle
        if count < 3: return Data.UNSOLVABLE, 0

        # if there aren't any given sides, automatically fill in values for the sides.
        if max(self.lengths) == 0 and count <= 3: 
            self.lengths = [1, 1, 1]



        # loop over the angles to check for ambiguous case
        for index in range(len(self.angles)):

            # check if the current angle is less than 90 degrees, and
            # the adjacent left side is longer than the opposite side, and the opposite side isn't zero, or
            # the adjacent right side is longer than the opposite side, and the opposite side isn't zero
            if 0 < self.angles[index] < 90 and (
                    (self.info(Info.ADJACENT_SIDE_LEFT, index)  > self.info(Info.OPPOSITE_SIDE, index) and self.info(Info.OPPOSITE_SIDE, index)) or
                    (self.info(Info.ADJACENT_SIDE_RIGHT, index) > self.info(Info.OPPOSITE_SIDE, index) and self.info(Info.OPPOSITE_SIDE, index))):

                # return an identifier that tells the calculator that the inputted data is ambiguous
                return 'yes', True
            
        # if there are 3 given side lengths, check if the side lengths won't display a triangle with connected edges
        if min(self.lengths):
            if max(self.lengths) >= (self.lengths[0] + self.lengths[1] + self.lengths[2] - max(self.lengths)): 
                return Data.IMPOSSIBLE, 0


        

        # if nothing else triggers, return identifier that tells the calculator the triangle is solvable.
        return 'yes', False



    # function to solve the remaining values for the triangle
    def solve_triangle(self, ambiguous):
        
        # check if all sides are given
        if min(self.lengths):

            # iterate through every angle value
            for index in range(len(self.angles)):

                # if the angle value isn't given, solve the angle value.
                if not self.angles[index]: self.angles[index] = self.cos_law(Trig.SIDE_SIDE_SIDE, index)

            # return to avoid extra calculations that will create incorrect values
            return 'solved'
        
        # check if there is an ambiguous angle
        if ambiguous:

            # loop through every angle
            for index in range(len(self.lengths)):

                # check if a given side has no given value for the opposite angle
                if self.lengths[index] and not self.info(Info.OPPOSITE_ANGLE, index):

                    # check if the current triangle is supposed to be the ambiguous case or not 
                    if self.is_ambiguous:

                        # calculate obtuse angle for ambiguous triangle

                        output = self.sin_law(Trig.ANGLE, index, find(self.angles, max(self.angles)))

                        if output == Data.IMPOSSIBLE: return output

                        self.angles[index] = 180 - output

                    else:

                        # calculate acute angle for ambiguous triangle
                        output = self.sin_law(Trig.ANGLE, index, find(self.angles, max(self.angles)))

                        if output == Data.IMPOSSIBLE: return output

                        self.angles[index] = output



        # calculate 3rd angle if there are already 2 angles
        if find(self.angles, 0) == rfind(self.angles, 0) or min(self.angles):

            index = self.angles.index(min(self.angles))

            self.angles[index] = 180 - self.info(Info.LEFT_ANGLE, index) - self.info(Info.RIGHT_ANGLE, index)

            # side angle angle angle
            if find(self.lengths, 0) != rfind(self.lengths, 0):

                for index in range(len(self.lengths)):

                    if not self.lengths[index]:

                        output = self.sin_law(Trig.SIDE, index, self.lengths.index(max(self.lengths)))

                        if output == Data.IMPOSSIBLE: return output

                        self.lengths[index] = output

                return 'solved'



        # side angle side
        for index in range(len(self.angles)):

            if self.angles[index] and (self.info(Info.ADJACENT_SIDE_LEFT, index) and self.info(Info.ADJACENT_SIDE_RIGHT, index)):
                self.lengths[index] = self.cos_law(Trig.SIDE_ANGLE_SIDE, index)

                return self.solve_triangle(ambiguous)
            


        # side side angle
        if max(self.angles) == (self.angles[0] + self.angles[1] + self.angles[2]):

            known_angle = self.angles.index(max(self.angles))

            # get side that doesn't have a known opposite angle
            for side in self.lengths:

                if side and not self.info(Info.OPPOSITE_ANGLE, self.lengths.index(side)):

                    opposite_side = self.lengths.index(side)

            output = self.sin_law(Trig.ANGLE, opposite_side, known_angle)

            if output == Data.IMPOSSIBLE: return output

            self.angles[opposite_side] = output

 
        
        # side angle angle
        else:

            known_side = self.lengths.index(max(self.lengths))

            # get angle that doesn't have a known opposite side
            for angle in self.angles:

                if angle and not self.info(Info.OPPOSITE_SIDE, self.angles.index(angle)):

                    opposite_angle = self.angles.index(angle)

            output = self.sin_law(Trig.SIDE, known_side, opposite_angle)

            if output == Data.IMPOSSIBLE: return output

            self.lengths[opposite_angle] = output



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
        output = self.solve_triangle(ambiguous)

        if output != 'solved': return output
            
        # calculate coordinates
        self.build_triangle()

        return self



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