import tkinter as tk
from tkinter import *
from enum import Enum
import copy
import math
from parsers.shunting_parser import shunting_yard_evaluator



''' NOTES

change how the buttons are displayed to make it easier to resize the display - DONE

allow the display to be resized by making the buttons change size depending on the current size of the gui - DONE

SWAP MEMORY BUTTONS WITH BRACKET AND MODULUS BUTTONS ON THE DISPLAY TO KEEP FUNCTIONALITY IN NON-SCIENTIFIC MODE

add buttons to create additional dynamic displays that will show the full equation and current number when they get too big - WORKAROUND

put the brackets into a split button, and add an absolute value button to fill in the gap - MAKE ABSOLUTE VALUE BUTTON WORK SIMILAR TO EXPONENT BUTTON - or make it work by treating it as a function with brackets and just displaying different brackets than what is put into the equation

make split button placing work universally (make it work no matter how many buttons fill one space) - DONE

add a history function

show the location where the typing is happening in the equation with something

numbers big enough to trigger scientific notation break it, this is because computers can't do math properly (6.02 * 10 ^ (23) = 601999999999999995805696.000000) ???

make 'backspace' work like regular backspace (bug: if an operator is deleted, the number at the end of the equation text won't be in the display text.)
perhaps make a class variable list in the 'Gui' class, and every time the user makes an input, 
create a new class object with the same attribute values, and store it in the class variable.
when the user presses 'backspace' load the last element in the class variable list, and then pop it out.
clear this list whenever the user clears the equation or presses 'calculate'

use the above concept to create a way for the user to see the session history, and load the answers for that.
make a separate class variable list that only stores a new element when the user hits 'calculate'

'''

class TrigFunctionType(Enum):
    Sine = 'sine'
    Cosine = 'cosine'
    Tangent = 'tangent'

class ClearType(Enum):
    Clear = 'clear'
    Backspace = 'backspace'

class HistoryUpdateType(Enum):
    Add = 'add'
    Remove = 'remove'
    Clear = 'clear'

class SplitType(Enum):
    Horizontal = 'horizontal'
    Vertical = 'vertical'

class BracketType(Enum):
    Left = 'left'
    Right = 'right'

class AbsoluteType(Enum):
    Left = 'left'
    Right = 'right'
    
class DisplayTextUpdateType(Enum):
    Replace = 'replace'
    Insert = 'insert'
    InsertCheckEmpty = 'replace_check_empty'

class UpdateType(Enum):
    FullUpdate = 'full_update'
    ClearDisplayText = 'clear_display_text'
    FullReplace = 'full_replace'



# function to convert text to superscript.
def get_super(x):

    normal  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=().'

    super_s = 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧'

    res     = x.maketrans(('').join(normal), ('').join(super_s))

    return x.translate(res)


class Logic:

    def __init__(self) -> None:

        self.equation = ['']
        self.bracket_num = 0
        self.exponent = False
        self.bracket_exponent_depth = 0
        self.output = ''
        self.memory = []


# main class to handle all the gui stuff
class Gui:

    history = []
    temp_history = []

    def __init__(self, parent) -> None:
        
        self.parent = parent
        self.trig_toggle = False
        self.is_radians = False
        self.equation_text = ['']
        self.display_text  = ['', '']
        self.logic = None
        self.gui_columns = []
        self.previous_column_count = 0



    # this function allows the object to be converted to a dictionary of key-value pairs for the variables
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value



    def clear_gui(self):

        # this will delete every widget except for the one that lets the user switch the calculator type
        for widget in self.parent.winfo_children():
            if type(widget) != OptionMenu:
                widget.destroy()



    def initialize_gui(self):
        
        # initialize gui
        self.clear_gui()

        self.parent.title('Calculator')

        self.min_gui_width = 400
        self.min_gui_height = 675
        self.parent.geometry('700x675')

        # update the window
        self.parent.update()

        self.logic = Logic()

        self.parent.bind("<KeyRelease>", self.keybindings)
        self.parent.bind("<Configure>", self.on_resize)

        self.parent.resizable(True, False)

        self.create_gui()

        self.build_gui()



    # function to create all of the objects that will be placed on the gui
    def create_gui(self):        

        # create display text labels
        self.equation = tk.Label(self.parent, text = '')
        self.equation.configure(font=('Arial', 40, ''))

        self.display = tk.Label(self.parent, text = '0')
        self.display.configure(font=('Arial', 75, 'bold'))

        # clear column array
        self.gui_columns = []

        # create button information
        self.equal          = tk.Button(self.parent, text='=',                  anchor='center', bg='DarkSlateGray2', command=lambda:self.calculate_equation())

        # column 1
        self.absolute_left  = tk.Button(self.parent, text='|',                  anchor='center', bg='gainsboro',      command=lambda:self.put_absolute())
        self.absolute_right = tk.Button(self.parent, text='|',                  anchor='center', bg='gainsboro',      command=lambda:self.put_brackets(BracketType.Right))
        self.pie            = tk.Button(self.parent, text='pi',                 anchor='center', bg='gainsboro',      command=lambda:self.put_pi())
        self.ee             = tk.Button(self.parent, text='e',                  anchor='center', bg='gainsboro',      command=lambda:self.put_e())
        self.log            = tk.Button(self.parent, text='log',                anchor='center', bg='gainsboro',      command=lambda:self.put_log())
        self.unit_toggle    = tk.Button(self.parent, text='Deg',                anchor='center', bg='gainsboro',      command=lambda:self.toggle_unit_type())
        self.gui_column_1   = [(self.absolute_left, self.absolute_right, SplitType.Vertical), self.pie, self.ee, self.log, self.unit_toggle]
        self.gui_columns.append(self.gui_column_1)

        # column 2
        self.open_b         = tk.Button(self.parent, text='(',                  anchor='center', bg='gainsboro',      command=lambda:self.put_brackets(BracketType.Left))
        self.close_b        = tk.Button(self.parent, text=')',                  anchor='center', bg='gainsboro',      command=lambda:self.put_brackets(BracketType.Right))
        self.shift          = tk.Button(self.parent, text='Inv',                anchor='center', bg='gainsboro',      command=lambda:self.toggle_trig_type())
        self.sine           = tk.Button(self.parent, text='sin',                anchor='center', bg='gainsboro',      command=lambda:self.put_trig_function(TrigFunctionType.Sine))
        self.cosine         = tk.Button(self.parent, text='cos',                anchor='center', bg='gainsboro',      command=lambda:self.put_trig_function(TrigFunctionType.Cosine))
        self.tangent        = tk.Button(self.parent, text='tan',                anchor='center', bg='gainsboro',      command=lambda:self.put_trig_function(TrigFunctionType.Tangent))
        self.gui_column_2   = [(self.open_b, self.close_b, SplitType.Vertical), self.shift, self.sine, self.cosine, self.tangent]
        self.gui_columns.append(self.gui_column_2)

        # column 3
        self.modulus        = tk.Button(self.parent, text='%',                  anchor='center', bg='gainsboro',      command=lambda:self.put_operator(' % '))
        self.factorial      = tk.Button(self.parent, text='x!',                 anchor='center', bg='gainsboro',      command=lambda:self.put_factorial())
        self.exponent       = tk.Button(self.parent, text='x' + get_super('y'), anchor='center', bg='gainsboro',      command=lambda:self.put_exponential())
        self.squared        = tk.Button(self.parent, text='x' + get_super('2'), anchor='center', bg='gainsboro',      command=lambda:self.put_exponential(2))
        self.sqrt           = tk.Button(self.parent, text='sqrt',               anchor='center', bg='gainsboro',      command=lambda:self.put_square_root())
        self.gui_column_3   = [self.modulus, self.factorial, self.exponent, self.squared, self.sqrt]
        self.gui_columns.append(self.gui_column_3)

        # column 4
        self.mem_clear      = tk.Button(self.parent, text='MC',                 anchor='center', bg='gainsboro',      command=lambda:self.memory_clear())
        self.num7           = tk.Button(self.parent, text='7',                  anchor='center', bg='white',          command=lambda:self.put_number(7))
        self.num4           = tk.Button(self.parent, text='4',                  anchor='center', bg='white',          command=lambda:self.put_number(4))
        self.num1           = tk.Button(self.parent, text='1',                  anchor='center', bg='white',          command=lambda:self.put_number(1))
        self.integer        = tk.Button(self.parent, text='+/-',                anchor='center', bg='white',          command=lambda:self.toggle_number_sign())
        self.gui_column_4   = [self.mem_clear, self.num7, self.num4, self.num1, self.integer]
        self.gui_columns.append(self.gui_column_4)
        
        # column 5
        self.mem_store      = tk.Button(self.parent, text='MS',                 anchor='center', bg='gainsboro',      command=lambda:self.memory_store())
        self.num8           = tk.Button(self.parent, text='8',                  anchor='center', bg='white',          command=lambda:self.put_number(8))
        self.num5           = tk.Button(self.parent, text='5',                  anchor='center', bg='white',          command=lambda:self.put_number(5))
        self.num2           = tk.Button(self.parent, text='2',                  anchor='center', bg='white',          command=lambda:self.put_number(2))
        self.num0           = tk.Button(self.parent, text='0',                  anchor='center', bg='white',          command=lambda:self.put_number(0))
        self.gui_column_5   = [self.mem_store, self.num8, self.num5, self.num2, self.num0]
        self.gui_columns.append(self.gui_column_5)
        
        # column 6
        self.mem_recall     = tk.Button(self.parent, text='MR',                 anchor='center', bg='gainsboro',      command=lambda:self.memory_recall())
        self.num9           = tk.Button(self.parent, text='9',                  anchor='center', bg='white',          command=lambda:self.put_number(9))
        self.num6           = tk.Button(self.parent, text='6',                  anchor='center', bg='white',          command=lambda:self.put_number(6))
        self.num3           = tk.Button(self.parent, text='3',                  anchor='center', bg='white',          command=lambda:self.put_number(3))
        self.decimal        = tk.Button(self.parent, text='.',                  anchor='center', bg='white',          command=lambda:self.put_decimal())
        self.gui_column_6   = [self.mem_recall, self.num9, self.num6, self.num3, self.decimal]
        self.gui_columns.append(self.gui_column_6)

        # column 7
        self.clear          = tk.Button(self.parent, text='CLR',                anchor='center', bg='lightcoral',     command=lambda:self.clear_data(ClearType.Clear))
        self.backspace      = tk.Button(self.parent, text='DEL',                anchor='center', bg='lightcoral',     command=lambda:self.clear_data(ClearType.Backspace))
        self.divide         = tk.Button(self.parent, text='/',                  anchor='center', bg='gainsboro',      command=lambda:self.put_operator(' / '))
        self.multiply       = tk.Button(self.parent, text='x',                  anchor='center', bg='gainsboro',      command=lambda:self.put_operator(' * '))
        self.minus          = tk.Button(self.parent, text='-',                  anchor='center', bg='gainsboro',      command=lambda:self.put_operator(' _ '))
        self.plus           = tk.Button(self.parent, text='+',                  anchor='center', bg='gainsboro',      command=lambda:self.put_operator(' + '))
        self.gui_column_7   = [(self.clear, self.backspace, SplitType.Horizontal), self.divide, self.multiply, self.minus, self.plus]
        self.gui_columns.append(self.gui_column_7)



        # configure button fonts
        self.equal.configure(font=('Arial', 25, 'bold'))

        for column in self.gui_columns:
            for button in column:
                # check for split buttons
                if type(button) == tuple:
                    for i in range(0, len(button) - 1):
                        button[i].configure(font=('Arial', 25, 'bold'))
                else:
                    button.configure(font=('Arial', 25, 'bold'))



        # variable to help attach the round option to the text
        self.round_label = tk.Label(self.parent, text = 'Round to              decimal points')
        self.round_label.configure(font=('Arial', 15, 'bold'))

        # decimal changer
        self.round_choice = StringVar(self.parent)
        self.round_choice.set(10)

        self.round_numbers = tk.Spinbox(self.parent, from_ = 0, to = 100, textvariable = self.round_choice)
        self.round_numbers.configure(font=('Arial', 15, 'bold'))



    # function to place every element on the gui
    def build_gui(self):

        # determine the column count, with a max of 7
        column_count = math.floor(self.parent.winfo_width() / 100) * (self.parent.winfo_width() < 800) + 7 * (self.parent.winfo_width() >= 800)

        if self.previous_column_count != column_count:
            self.clear_gui()
            self.create_gui()


        # create display text labels
        display_offset = 10
        
        self.equation.place(x = self.parent.winfo_width() - display_offset, y = 10, anchor = 'ne')

        self.display.place(x = self.parent.winfo_width() - display_offset, y = 80, anchor = 'ne')



        # place buttons
        self.button_width = lambda gui_width = self.parent.winfo_width(): gui_width / column_count
        self.button_height = 70

        self.equal.place(x = 0, y = self.parent.winfo_height() - self.button_height * 1, width = self.parent.winfo_width(), height = self.button_height)

        for index, column in enumerate(self.gui_columns[7 - column_count:7]):
            row_num = 6
            for button in column:

                # check for split buttons
                if type(button) == tuple:
                    if button[-1] == SplitType.Horizontal:

                        # place first button
                        button[0].place(x = self.button_width() * index, 
                                        y = self.parent.winfo_height() - self.button_height * row_num, 
                                        width = self.button_width(), 
                                        height = self.button_height / (len(button) - 1))

                        # place rest of buttons
                        for i in range(1, len(button) - 1):
                            button[i].place(x = self.button_width() * index, 
                                            y = self.parent.winfo_height() - self.button_height * row_num + self.button_height / (len(button) - 1) * i, 
                                            width = self.button_width(),  
                                            height = self.button_height / (len(button) - 1))
                    


                    elif button[-1] == SplitType.Vertical:

                        # place first button
                        button[0].place(x = self.button_width() * index, 
                                        y = self.parent.winfo_height() - self.button_height * row_num, 
                                        width = self.button_width() / (len(button) - 1), 
                                        height = self.button_height)

                        # place rest of buttons
                        for i in range(1, len(button) - 1):
                            button[i].place(x = self.button_width() * index + self.button_width() / (len(button) - 1) * i, 
                                            y = self.parent.winfo_height() - self.button_height * row_num, 
                                            width = self.button_width() / (len(button) - 1), 
                                            height = self.button_height)

                else:
                    button.place(x = self.button_width() * index, y = self.parent.winfo_height() - self.button_height * row_num, width = self.button_width(), height = self.button_height)
                row_num -= 1



        # additional graphical setup
        

        # button to open history


        if column_count >= 5:

            # variable to help attach the round option to the text
            round_x = self.parent.winfo_width() - 330

            self.round_label.place(x = round_x, y = self.parent.winfo_height() - self.button_height * 6 - self.button_height / 2)

            # decimal changer
            self.round_numbers.place(x = round_x + 100, y = self.parent.winfo_height() - self.button_height * 6 - self.button_height / 2, width = 65)



        # variable to determine whether or not the buttons need to be cleared
        self.previous_column_count = column_count



    # function to update the display when the window is resized
    def on_resize(self, event):

        # check if the parent window is being adjusted
        if event.widget == self.parent:

            if self.parent.winfo_width() < self.min_gui_width or self.parent.winfo_height() < self.min_gui_height:

                self.parent.geometry(f"{max(self.parent.winfo_width(), self.min_gui_width)}x{max(self.parent.winfo_height(), self.min_gui_height)}")

            # update window
            self.parent.update()

            # print info
            print(f"resize detected. new window size: {self.parent.winfo_width()}x{self.parent.winfo_height()}")

            # rebuild gui
            self.build_gui()



    # a function to handle all key inputs
    def keybindings(self, input):

        print(f"key: {input}")

        try: temp = input.keysym
        except:print('keybinding error')

        try: 
            print(f"input.state: {input.state}")
            # check if 'shift' is held
            if input.state == 1:
                print(f"input.keysym: {input.keysym}")
                match input.keysym:

                    case 'exclam': self.put_factorial()
                    case 'numbersign': self.put_square_root()
                    case 'percent': self.put_operator(' % ')
                    case 'asciicircum': self.put_exponential()
                    case 'asterisk': self.put_operator(' * ')
                    case 'parenleft': self.put_brackets(BracketType.Left)
                    case 'parenright': self.put_brackets(BracketType.Right)
                    case 'underscore': self.toggle_number_sign()
                    case 'plus': self.put_operator(' + ')
                    case 'BackSpace': self.clear_data(ClearType.Clear)
                    case 'M': self.memory_store()

                return
            
            # check if 'ctrl' is held
            elif input.state == 4:

                if input.keysym in '1234567890': self.put_exponential(int(input.keysym))

                match input.keysym:

                    case 's': self.put_trig_function(TrigFunctionType.Sine)
                    case 'c': self.put_trig_function(TrigFunctionType.Cosine)
                    case 't': self.put_trig_function(TrigFunctionType.Tangent)
                    case 'a': self.put_previous_answer()
                    case 'u': self.toggle_unit_type()
                    case 'e': self.put_e()
                    case 'l': self.put_log()
                    case 'p': self.put_pi()
                    case 'm': self.memory_clear()

                return
        except: print('exception triggered')

        if input.keysym in '1234567890': self.put_number(int(input.keysym))

        match input.keysym:
            case 'BackSpace': self.clear_data(ClearType.Backspace)
            case 'minus':     self.put_operator(' _ ')
            case 'Return':    self.calculate_equation()
            case 'slash':     self.put_operator(' / ')
            case 'period':    self.put_decimal()
            case 'm':         self.memory_recall()



    # the function bound to the 'equals' button to output a result for an equation.
    def calculate_equation(self):

        print(f"equation: {('').join(self.logic.equation)}")

        # assemble equation list into a string
        equation_str = ('').join(self.logic.equation)

        # this is necessary
        if equation_str == '9 + 10': answer = '21'

        # give the equation parser the equation string and set the output to a variable
        else: answer = shunting_yard_evaluator(equation_str, self.is_radians)

        if not answer:

            print('Could not calculate answer')
            
            return
        
        try: 
            answer = float(answer)
            print(f"output: {answer:f}")
        except:
            print(f"output: {answer}")
        

        # round the output to the specified number of decimal places
        self.logic.output = str(round(float(answer), int(self.round_choice.get())))



        # edit display strings
        self.equation_text += ' = ' + self.logic.output

        self.display_text = self.logic.output

        self.logic.bracket_num = 0

        self.logic.exponent = False

        self.logic.bracket_exponent_depth = 0

        # clear temp history
        self.update_history(HistoryUpdateType.Clear)

        # update display
        self.update_text(display_text_update_type=DisplayTextUpdateType.Insert)



        # reset variables
        self.equation_text = self.logic.output

        self.logic.equation = self.logic.output

    

    def update_text(self, display_text_update_type: DisplayTextUpdateType = DisplayTextUpdateType.Replace, strings_to_insert = None, string_index = None, update_type: UpdateType = UpdateType.FullUpdate):

        if strings_to_insert is None:

            strings_to_insert = ('', '', '')

        if string_index is None:

            string_index = (len(self.logic.equation), len(self.equation_text), len(self.display_text))

            d = self.logic.bracket_num
        
        else: d = 0

        # simplify variables
        a = self.logic.equation
        b = self.equation_text
        c = self.display_text
        e = self.logic.exponent

        # edit main equation variables
        self.logic.equation = list(('').join(a[0:string_index[0] - d]) + strings_to_insert[0] + ('').join(a[string_index[0] - d:len(a)]))

        try:

            if e: self.equation_text = list(('').join(b[0:string_index[1] - d]) + get_super(strings_to_insert[1]) + ('').join(b[string_index[1] - d:len(b)]))

            else: self.equation_text = list(('').join(b[0:string_index[1] - d]) + strings_to_insert[1] + ('').join(b[string_index[1] - d:len(b)]))

        except:print('well fuck')


        if display_text_update_type == DisplayTextUpdateType.Replace:

            self.display_text = list(strings_to_insert[2])

            self.display_text.append('')



        elif display_text_update_type == DisplayTextUpdateType.Insert: 
            
            self.display_text = list(('').join(c[0:string_index[2]]) + strings_to_insert[2] + ('').join(c[string_index[2]:len(c)]))



        elif display_text_update_type == DisplayTextUpdateType.InsertCheckEmpty:

            self.display_text = list(('').join(c[0:string_index[2]]) + strings_to_insert[2] + ('').join(c[string_index[2]:len(c)]))

            if ('').join(self.display_text).strip() == '':
                update = UpdateType.ClearDisplayText



        if update_type == UpdateType.FullUpdate:

            # update display
            self.display.configure(text = ('').join(self.display_text))

            self.equation.configure(text = ('').join(self.equation_text))



        elif update_type == UpdateType.ClearDisplayText:

            # update display
            self.display.configure(text = '0')

            self.equation.configure(text = ('').join(self.equation_text))

        

        elif update_type == UpdateType.FullReplace:

            self.display.configure(text = strings_to_insert[0])

            self.equation.configure(text = strings_to_insert[1])
            
        else:pass



    # function to update the history variables
    def update_history(self, history_update_type: HistoryUpdateType):

        if history_update_type == HistoryUpdateType.Add:
            
            # this loads all the variables in 'self' and copies them if possible and puts them in a new object
            temp = dict(self)

            for attr, value in temp.items():
                try:
                    temp[attr] = copy.deepcopy(value)

                except:
                    temp[attr] = value



            Gui.history.append(temp)
            Gui.temp_history.append(temp)
        
        elif history_update_type == HistoryUpdateType.Remove:
            Gui.temp_history.pop()

        elif history_update_type == HistoryUpdateType.Clear:
            Gui.temp_history = []



    # function bound to the clear equation button that clears the variables and display.
    def clear_data(self, clear_type: ClearType):

        if clear_type == ClearType.Clear:

            # reset variables
            self.logic.equation = ['']

            self.equation_text = ['']

            self.display_text = ['', '']

            self.logic.bracket_num = 0

            self.logic.exponent = False

            self.logic.bracket_exponent_depth = 0

            self.update_history(HistoryUpdateType.Clear)

            # update display
            self.display.configure(text = '0')

            self.equation.configure(text = '')



        elif clear_type == ClearType.Backspace:

            if len(Gui.temp_history) <= 1:
                self.clear_data(ClearType.Clear)
                return
            
            for attr, value in Gui.temp_history[-1].items():
                setattr(self, attr, value)

            self.update_history(HistoryUpdateType.Remove)

            self.update_text(display_text_update_type=DisplayTextUpdateType.InsertCheckEmpty)



    # function bound to the invert button to allow inverse functions to be used.
    def toggle_trig_type(self):

        # flip the variable whenever the button is pressed
        self.trig_toggle = not self.trig_toggle

        # change the button text to inverted functions
        if self.trig_toggle:

            self.sine.   configure(text='sin' + get_super('-1'))
            self.cosine. configure(text='cos' + get_super('-1'))
            self.tangent.configure(text='tan' + get_super('-1'))

            self.sine.   place(x = self.button_width() * 1, y = self.parent.winfo_height() - self.button_height * 4, width = self.button_width(), height = self.button_height)
            self.cosine. place(x = self.button_width() * 1, y = self.parent.winfo_height() - self.button_height * 3, width = self.button_width(), height = self.button_height)
            self.tangent.place(x = self.button_width() * 1, y = self.parent.winfo_height() - self.button_height * 2, width = self.button_width(), height = self.button_height)



        # change the button text to normal functions
        else:

            self.sine.   configure(text='sin')
            self.cosine. configure(text='cos')
            self.tangent.configure(text='tan')

            self.sine.   place(x = self.button_width() * 1, y = self.parent.winfo_height() - self.button_height * 4, width = self.button_width(), height = self.button_height)
            self.cosine. place(x = self.button_width() * 1, y = self.parent.winfo_height() - self.button_height * 3, width = self.button_width(), height = self.button_height)
            self.tangent.place(x = self.button_width() * 1, y = self.parent.winfo_height() - self.button_height * 2, width = self.button_width(), height = self.button_height)

    

    def toggle_unit_type(self):
        
        self.is_radians = not self.is_radians

        if self.is_radians:
            
            self.unit_toggle.configure(text='Rad')

            self.unit_toggle.place(x = 0, y = self.parent.winfo_height() - self.button_height * 2, width = self.button_width(), height = self.button_height)
        
        else:
            
            self.unit_toggle.configure(text='Deg')

            self.unit_toggle.place(x = 0, y = 525, width = self.button_width(), height = self.button_height)
            


    # the function bound to the addition button to tell the calculate function which mathematical operation to perform when it is pressed.
    def put_operator(self, operation = None):

        # update history
        self.update_history(HistoryUpdateType.Add)

        try:

            if self.equation_text[-2 - self.logic.bracket_num] not in list('sctSCTlf^#/*%+_' + get_super('sctSCTlf^#/*%+_')):

                if operation == ' _ ': 
                    
                    self.update_text(strings_to_insert=(operation, ' - ', ''), update_type=UpdateType.ClearDisplayText)

                

                else:

                    # add operator to equation and display strings
                    self.update_text(strings_to_insert=(operation, operation, ''), update_type=UpdateType.ClearDisplayText)

        except: # ask ryan which format looks better

            if operation == ' _ ':

                self.update_text(strings_to_insert=(operation, ' - ', ''), update_type=UpdateType.ClearDisplayText)

            

            else:

                # add operator to equation and display strings
                self.update_text(strings_to_insert=(operation, operation, ''), update_type=UpdateType.ClearDisplayText)



    # function bound to the decimal button to allow decimal numbers to be inputted.
    def put_decimal(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        if self.display_text == '':

            # put the decimal in the equation and display strings
            self.update_text(display_text_update_type=DisplayTextUpdateType.Insert, strings_to_insert=('0.', '0.', '0.'))



        elif '.' not in self.display_text:

            # put the decimal in the equation and display strings
            self.update_text(display_text_update_type=DisplayTextUpdateType.Insert, strings_to_insert=('.', '.', '.'))



    # function bound to the integer button to allow the user to toggle a number between positive and toggle_number_sign.
    def toggle_number_sign(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        try:

            # check to see if there is anything in the display text
            if self.display_text == ['']:

                # add the integer sign to the number if there is nothing else in the equation
                self.update_text(strings_to_insert=('-', '-', '-'))

                return

            

            # find where display text is within the equation text
            if self.logic.exponent:
                display_text_index = ('').join(self.equation_text).rfind(('').join([get_super(x) for x in self.display_text]))
            else:
                display_text_index = ('').join(self.equation_text).rfind(('').join(self.display_text))
            equation_text_index = ('').join(self.logic.equation).rfind(('').join(self.display_text))



            if  '-' not in self.display_text:

                if self.equation_text[display_text_index] != '-':

                    # put an integer sign on the number if it doesn't have one
                    self.update_text(display_text_update_type=DisplayTextUpdateType.Insert, strings_to_insert=('-', '-', '-'), string_index=(equation_text_index, display_text_index, 0)) 



            else:

                # remove the integer sign from the number
                self.logic.equation.pop(equation_text_index)

                self.equation_text.pop(display_text_index)

                self.display_text.pop(0)



                # update display
                self.update_text(display_text_update_type=DisplayTextUpdateType.InsertCheckEmpty)



        except:

            # add the integer sign to the number if there is nothing else in the equation
            self.update_text(display_text_update_type=DisplayTextUpdateType.Insert, strings_to_insert=('-', '-', '-'))

    

    # function to input numbers.
    def put_number(self, x):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # allow for bracket multiplication without pressing the multiplication button
        if self.logic.equation[-1 - self.logic.bracket_num] in list(')' + get_super(')')):

            for i in list(' * '): self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)

        # put the number in the equation and display strings
        self.update_text(display_text_update_type=DisplayTextUpdateType.Insert, strings_to_insert=(str(x), str(x), str(x)))



    # function bound to the exponent button that allows for exponents to be used.
    def put_exponential(self, ctrl_exp = -1):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # check if a keybinding was used
        if ctrl_exp != -1:

            # put the exponent sign and exponent number in the equation and display strings
            self.update_text(strings_to_insert=(' ^ ' + str(ctrl_exp), get_super('(' + str(ctrl_exp) + ')'), ''), update_type=UpdateType.ClearDisplayText)

        

        else:

            self.logic.exponent = True

            # put exponent sign in equation
            self.update_text(strings_to_insert=(' ^ ()', get_super('()'), ''), update_type=UpdateType.ClearDisplayText)

            # increase bracket number counter
            self.logic.bracket_num += 1



    # function bound to the sqrt button that adds square root
    def put_square_root(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # add the sqrt function indicator to the equation and display strings
        self.update_text(strings_to_insert=('#()', 'sqrt()', ''), update_type=UpdateType.ClearDisplayText)

        # allow for more brackets
        self.logic.bracket_num += 1



    # function bound to the factorial button to allow for factorials to be used.
    def put_factorial(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # put the factorial sign in the equation and display strings
        self.update_text(strings_to_insert=('!', '!', ''), update_type=UpdateType.ClearDisplayText)



    # function bound to the memory recall button to display the number stored in memory.
    def memory_recall(self):

        # add the number stored in memory to the equation and display strings
        self.update_text(strings_to_insert=(self.logic.memory, self.logic.memory, self.logic.memory))



    # function bound to the memory clear button that will clear the number stored in the memory.
    def memory_clear(self):

        # clear the memory variable
        self.logic.memory = []

        # reset button color
        self.mem_store.configure(bg = 'gainsboro')



    # function bound to the memory add button to set the memory number to the number displayed.
    def memory_store(self):

        try: 
            memory = float(('').join(self.display_text))
            print(f"memory: {memory:f}")
        except: 
            memory = ('').join(self.display_text)
            print(f"memory: {memory}")


        # assign a number to the memory variable
        self.logic.memory = ('').join(self.display_text)

        # update button color to show that memory is being used
        self.mem_store.configure(bg = 'pale green')



    # function bound to the brackets button to add them to the display.
    def put_brackets(self, bracket_type: BracketType):

        # update history
        self.update_history(HistoryUpdateType.Add)

        if bracket_type == BracketType.Left:

            # allow for bracket multiplication without pressing the multiplication button
            if self.logic.equation[-1 - self.logic.bracket_num] in list('1234567890)' + get_super('1234567890)')):

                for i in list(' * '): self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)

            # add an open bracket to the equation and display strings
            self.update_text(strings_to_insert=('()', '()', ''), update_type=UpdateType.ClearDisplayText)

            # keep track of brackets
            self.logic.bracket_num += 1

            if self.logic.exponent:

                self.logic.bracket_exponent_depth += 1



        elif bracket_type == BracketType.Right:

            if self.equation_text[-1 - self.logic.bracket_num + 1] in list('1234567890)' + get_super('1234567890)')):

                # start typing outside one more layer of brackets
                if self.logic.bracket_num > 0:

                    self.logic.bracket_num -= 1

                    if self.logic.exponent:

                        if self.logic.bracket_exponent_depth:
                            
                            self.logic.bracket_exponent_depth -= 1

                        else:

                            self.logic.exponent = not self.logic.exponent



                    # display numbers within brackets
                    self.update_text(display_text_update_type=DisplayTextUpdateType.Replace, update_type=UpdateType.ClearDisplayText)



    # function bound to the trigonometry buttons to allow them to be used.
    def put_trig_function(self, trig_function_type: TrigFunctionType):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # allow for bracket multiplication without pressing the multiplication button
        if self.logic.equation[-1 - self.logic.bracket_num] in list('1234567890)' + get_super('1234567890)')):

            for i in list(' * '): self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)

        # add an alternate function for inverse trigonometry functions
        if self.trig_toggle:

            if trig_function_type == TrigFunctionType.Sine:

                # add the inverse sine indicator to the equation and display strings
                self.update_text(strings_to_insert=('S()', 'sin' + get_super('-1') + '()', ''), update_type=UpdateType.ClearDisplayText)



            elif trig_function_type == TrigFunctionType.Cosine:
                
                # add the inverse cosine indicator to the equation and display strings
                self.update_text(strings_to_insert=('C()', 'cos' + get_super('-1') + '()', ''), update_type=UpdateType.ClearDisplayText)



            elif trig_function_type == TrigFunctionType.Tangent:
                
                # add the inverse tangent indicator to the equation and display strings
                self.update_text(strings_to_insert=('T()', 'tan' + get_super('-1') + '()', ''), update_type=UpdateType.ClearDisplayText)



        else:

            if trig_function_type == TrigFunctionType.Sine:

                # add the sine indicator to the equation and display strings
                self.update_text(strings_to_insert=('s()', 'sin()', ''), update_type=UpdateType.ClearDisplayText)



            elif trig_function_type == TrigFunctionType.Cosine:
                
                # add the cosine indicator to the equation and display strings
                self.update_text(strings_to_insert=('c()', 'cos()', ''), update_type=UpdateType.ClearDisplayText)



            elif trig_function_type == TrigFunctionType.Tangent:
                
                # add the tangent indicator to the equation and display strings
                self.update_text(strings_to_insert=('t()', 'tan()', ''), update_type=UpdateType.ClearDisplayText)

        # update bracket counter
        self.logic.bracket_num += 1



    def put_absolute(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # allow for bracket multiplication without pressing the multiplication button
        if self.logic.equation[-1 - self.logic.bracket_num] in list('1234567890)' + get_super('1234567890)')):

            for i in list(' * '): self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)

        

        # add data to equation and display strings
        self.update_text(strings_to_insert=('a()', '||', ''), update_type=UpdateType.ClearDisplayText)

        # update bracket counter
        self.logic.bracket_num += 1



    # function bound to the pi button to allow for the pi number to be accessed easily.
    def put_pi(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # add the pi number to the equation and display strings
        self.update_text(strings_to_insert=('3.14159265359', 'pi', '3.14159265359'))



    # function bound to the e button to allow for eulers number to be accessed easily.
    def put_e(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # add eulers number to the equation and display strings
        self.update_text(strings_to_insert=('2.71828182846', 'e', '2.71828182846'))



    # function bound to the log button to allow for logarithms to be used.
    def put_log(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # allow for bracket multiplication without pressing the multiplication button
        if self.logic.equation[-1] in list('1234567890)' + get_super('1234567890)')):

            for i in list(' * '): self.logic.equation.insert(len(self.logic.equation) - self.logic.bracket_num, i)

        # add the log function indicator to the equation and display strings
        self.update_text(strings_to_insert=('l()', 'log()', ''), update_type=UpdateType.ClearDisplayText)

        # allow for more brackets
        self.logic.bracket_num += 1



    # function bound to the answer button to allow for the previous answer to be used.
    def put_previous_answer(self):

        # update history
        self.update_history(HistoryUpdateType.Add)

        # add the previous answer to the equation and display strings
        self.update_text(strings_to_insert=(self.logic.output, self.logic.output, self.logic.output))



def main():
    
    pass



if __name__ == "__main__":

    main()