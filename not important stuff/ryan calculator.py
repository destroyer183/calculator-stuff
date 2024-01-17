
import sys 
import tkinter as tk

ROOT = tk.Tk()

def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()."
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾‧"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)


class Calculator():

    def __init__(self, window=None) -> None:


        if window is None:
            self.root = tk.Toplevel(ROOT)

        else:

            self.root = window
                
        # graphical setup
        self.equation = tk.Label(self.root, text = "")
        self.equation.configure(font=("Arial", 20, ""))
        self.equation.place(x = 0, y = 0)

        self.display = tk.Label(self.root, text = "display")
        self.display.configure(font=("Arial", 40, "bold"))
        self.display.place(x = 0, y = 40)

        roundlabel = tk.Label(self.root, text = "Round to                      decimal points")
        roundlabel.place(x = 150, y = 120)

        roundchoice = tk.StringVar(self.root)
        roundchoice.set(10)

        roundnumbers = tk.OptionMenu(self.root, roundchoice, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        roundnumbers.place(x = 205, y = 110)

        equal = tk.Button(self.root, text="=", anchor='center', bg='DarkSlateGray2', command=self.calculate)
        equal.configure(font=("Arial", 20, "bold"))
        equal.place(x = 175, y = 530, height = 60, width = 350, anchor='center')

        # addition button
        plus = tk.Button(self.root, text="+", anchor='center', bg='gainsboro', command=self.add)
        plus.configure(font=("Arial", 20, "bold"))
        plus.place(x = 262.5, y = 440, height = 60, width = 87.5)

        # subtraction button
        minus = tk.Button(self.root, text="-", anchor='center', bg='gainsboro', command=self.subtract)
        minus.configure(font=("Arial", 20, "bold"))
        minus.place(x = 262.5, y = 380, height = 60, width = 87.5)

        # multiplication button
        multiply = tk.Button(self.root, text="x", anchor='center', bg='gainsboro', command=self.multiply)
        multiply.configure(font=("Arial", 20, "bold"))
        multiply.place(x = 262.5, y = 320, height = 60, width = 87.5)

        # divide button
        divide = tk.Button(self.root, text="/", anchor='center', bg='gainsboro', command=self.divide)
        divide.configure(font=("Arial", 20, "bold"))
        divide.place(x = 262.5, y = 260, height = 60, width = 87.5)
    
        # decimal button
        decimal = tk.Button(self.root, text=".", anchor='center', bg='white', command=self.assign_decimal)
        decimal.configure(font=("Arial", 20, "bold"))
        decimal.place(x = 175, y = 440, height = 60, width = 87.5)

        # integer button
        integer = tk.Button(self.root, text="+/-", anchor='center', bg='white', command=self.assign_integer)
        integer.configure(font=("Arial", 20, "bold"))
        integer.place(x = 0, y = 440, height = 60, width = 87.5)

        # zero button
        num0 = tk.Button(self.root, text="0", anchor='center', bg='white', command=lambda:self.assign(0))
        num0.configure(font=("Arial", 20, "bold"))
        num0.place(x = 87.5, y = 440, height = 60, width = 87.5)
            
        # one button
        num1 = tk.Button(self.root, text="1", anchor='center', bg='white', command=lambda:self.assign(1))
        num1.configure(font=("Arial", 20, "bold"))
        num1.place(x = 0, y = 380, height = 60, width = 87.5)

        # two button
        num2 = tk.Button(self.root, text="2", anchor='center', bg='white', command=lambda:self.assign(2))
        num2.configure(font=("Arial", 20, "bold"))
        num2.place(x = 87.5, y = 380, height = 60, width = 87.5)

        # three button
        num3 = tk.Button(self.root, text="3", anchor='center', bg='white', command=lambda:self.assign(3))
        num3.configure(font=("Arial", 20, "bold"))
        num3.place(x = 175, y = 380, height = 60, width = 87.5)

        # four button
        num4 = tk.Button(self.root, text="4", anchor='center', bg='white', command=lambda:self.assign(4))
        num4.configure(font=("Arial", 20, "bold"))
        num4.place(x = 0, y = 320, height = 60, width = 87.5)

        # five button
        num5 = tk.Button(self.root, text="5", anchor='center', bg='white', command=lambda:self.assign(5))
        num5.configure(font=("Arial", 20, "bold"))
        num5.place(x = 87.5, y = 320, height = 60, width = 87.5)

        # six button
        num6 = tk.Button(self.root, text="6", anchor='center', bg='white', command=lambda:self.assign(6))
        num6.configure(font=("Arial", 20, "bold"))
        num6.place(x = 175, y = 320, height = 60, width = 87.5)

        # seven button
        num7 = tk.Button(self.root, text="7", anchor='center', bg='white', command=lambda:self.assign(7))
        num7.configure(font=("Arial", 20, "bold"))
        num7.place(x = 0, y = 260, height = 60, width = 87.5)

        # eight button
        num8 = tk.Button(self.root, text="8", anchor='center', bg='white', command=lambda:self.assign(8))
        num8.configure(font=("Arial", 20, "bold"))
        num8.place(x = 87.5, y = 260, height = 60, width = 87.5)
        
        # nine button
        num9 = tk.Button(self.root, text="9", anchor='center', bg='white', command=lambda:self.assign(9))
        num9.configure(font=("Arial", 20, "bold"))
        num9.place(x = 175, y = 260, height = 60, width = 87.5)

        # backspace button
        backspace = tk.Button(self.root, text="<--", anchor='center', bg='lightcoral')
        backspace.configure(font=("Arial", 20, "bold"))
        backspace.place(x = 262.5, y = 200, height = 60, width = 87.5)

        # square root button
        squareroot = tk.Button(self.root, text="sqr", anchor='center', bg='gainsboro', command=lambda:self.exponent(0.5))
        squareroot.configure(font=("Arial", 20, "bold"))
        squareroot.place(x = 175, y = 200, height = 60, width = 87.5)

        # square exponent button
        squared = tk.Button(self.root, text="x" + get_super("2"), anchor='center', bg='gainsboro', command=lambda:self.exponent(2))
        squared.configure(font=("Arial", 20, "bold"))
        squared.place(x = 0, y = 200, height = 60, width = 87.5)

        # exponent button
        exponente = tk.Button(self.root, text="x" + get_super('y'), anchor='center', bg='gainsboro', command=self.exponent)
        exponente.configure(font=("Arial", 20, "bold"))
        exponente.place(x = 87.5, y = 200, height = 60, width = 87.5)

        # clear equation button
        clear = tk.Button(self.root, text="CE", anchor='center', bg='lightcoral', command=self.clear_all)
        clear.configure(font=("Arial", 20, "bold"))
        clear.place(x = 262.5, y = 140, height = 60, width = 87.5)

        # memory clear button
        mem_clear = tk.Button(self.root, text="MC", anchor='center', bg='gainsboro', command=self.clear_memory)
        mem_clear.configure(font=("Arial", 20, "bold"))
        mem_clear.place(x = 0, y = 140, height = 60, width = 87.5)
        
        # memory add button
        mem_add  = tk.Button(self.root, text="MS", anchor='center', bg='gainsboro', command=self.add_memory)
        mem_add.configure(font=("Arial", 20, "bold"))
        mem_add.place(x = 87.5, y = 140, height = 60, width = 87.5)

        # init instance variables 
        self.clear_all()

        self.root.bind("<Key>", self.keydown)
        self.root.title("Calculator")
        self.root.geometry('350x560')
        self.root.resizable(False, False)

    def clear_all(self):
        self.memory = 0
        self.ctrlexp = -1
        self.exponent_number = 0

        self.output = 0
        self.input1 = 0
        self.input2 = 0
        
        self.is_addition       = False
        self.is_subtraction    = False
        self.is_multiplication = False
        self.is_division       = False
        self.is_exponent       = False
        self.is_square_root    = False
        self.is_decimal        = False
        self.decimal_place     = 1
        self.is_firstnum       = True

        self.display.configure(text="display")

        self.equation.configure(text="") 

    def clear_memory(self):
        self.memory = 0

    def add_memory(self):
        print('memory added')

    def keydown(self, key):

        print(key)

    def assign_decimal(self):
        
        if self.is_decimal:
            return 

        self.is_decimal = True 
        self.input1 = float(self.input1)
        self.input2 = float(self.input2)

    def assign_integer(self):
        print(f"assigning integer")

        if self.is_exponent:

            self.exponent_number *= -1

            if self.is_firstnum:
                self.display.configure(text= str(self.input1) + get_super(str(self.exponent_number)))
                self.equation.configure(text= str(self.input1) + get_super(str(self.exponent_number)))
            else:
                self.display.configure(text= str(self.input2) + get_super(str(self.exponent_number)))

            return 

        if self.is_firstnum:

            self.input1 *= -1

            self.equation.configure(text= self.equation.cget("text"))
            self.display.configure(text= str(self.input1))
            return
        
        self.input2 *= -1
        self.display.configure(text=str(self.input2))

    def assign(self, value):
        print(f"assigning {value}")

        if self.is_exponent:

            if self.is_decimal:
                self.decimal_place /= 10

                if self.exponent_number == 0 : self.exponent_number = value*self.decimal_place
                elif self.exponent_number < 0: self.exponent_number = self.exponent_number - value*self.decimal_place
                else:                          self.exponent_number = self.exponent_number + value*self.decimal_place

            else:
                if self.exponent_number == 0 : self.exponent_number = value
                elif self.exponent_number < 0: self.exponent_number = self.exponent_number*10 - value
                else:                          self.exponent_number = self.exponent_number*10 + value


            if self.is_firstnum:

                self.display.configure(text= str(self.input1) + get_super(str(self.exponent_number)))
                self.equation.configure(text= str(self.input1) + get_super(str(self.exponent_number)))
                return 

            self.display.configure(text= str(self.input2) + get_super(str(self.exponent_number)))
            self.equation.configure(text= self.equation.cget("text") + get_super(str(self.exponent_number)))
            return 

        
        if self.is_firstnum:
            
            if self.is_decimal:
                self.decimal_place /= 10
                if self.input1 == 0 : self.input1 = value*self.decimal_place
                elif self.input1 < 0: self.input1 = self.input1 - value*self.decimal_place
                else:                 self.input1 = self.input1 + value*self.decimal_place
                
            else:
                if self.input1 == 0 : self.input1 = value
                elif self.input1 < 0: self.input1 = self.input1*10 - value
                else:                 self.input1 = self.input1*10 + value
            
            self.display.configure(text=self.input1)
            self.equation.configure(text=self.equation.cget("text") + str(value))
            return 

        if self.is_decimal:
            self.decimal_place /= 10
            if self.input2 == 0 : self.input2 = value*self.decimal_place
            elif self.input2 < 0: self.input2 = self.input2 - value*self.decimal_place
            else:                 self.input2 = self.input2 + value*self.decimal_place
                
        else:
            if self.input2 == 0 : self.input2 = value
            elif self.input2 < 0: self.input2 = self.input2*10 - value
            else:                 self.input2 = self.input2*10 + value

        self.display.configure(text=self.input2)
        self.equation.configure(text= self.equation.cget("text") + str(value))

    def exponent(self, exponent = None):

        if exponent is not None:

            self.exponent_number = exponent

        self.is_exponent = True

        if self.is_firstnum:
            self.equation.configure(text= str(self.input1) + get_super(str(self.exponent_number)))
            self.display.configure(text= str(self.input1) + get_super(str(self.exponent_number)))
        else:
            self.display.configure(text= str(self.input2) + get_super(str(self.exponent_number)))

    def is_modifier(self):

        return self.is_division or self.is_addition or self.is_subtraction or self.is_multiplication

    def calc_input1(self):

        self.is_decimal = False 
        self.decimal_place = 1

        if self.is_exponent:

            self.is_exponent = False 
            self.input1 = self.input1 ** self.exponent_number
            self.exponent_number = 0
            self.input2 = 0
            return 

        if self.is_division:

            self.is_division = False 
            self.input1 = self.input1 / self.input2 
            self.exponent_number = 0
            self.input2 = 0
            return 

        if self.is_multiplication:

            self.is_multiplication = False 
            self.input1 = self.input1 * self.input2 
            self.exponent_number = 0
            self.input2 = 0
            return 

        if self.is_addition:

            self.is_addition = False 
            self.input1 = self.input1 + self.input2 
            self.exponent_number = 0
            self.input2 = 0
            return 

        if self.is_subtraction:

            self.is_subtraction = False 
            self.input1 = self.input1 - self.input2 
            self.exponent_number = 0
            self.input2 = 0
            return 

    def divide(self):
        self.calc_input1()

        if self.is_division:
            return 

        self.is_division = True
        self.is_addition = False 
        self.is_subtraction = False 
        self.is_multiplication = False 
        self.is_firstnum = False 

        self.equation.configure(text= str(self.input1) + " / ")

    def multiply(self):
        self.calc_input1()

        if self.is_multiplication:
            return 

        self.is_division = False
        self.is_addition = False 
        self.is_subtraction = False 
        self.is_multiplication = True 
        self.is_firstnum = False 

        self.equation.configure(text= str(self.input1) + " x ")

    def add(self):
        self.calc_input1()

        if self.is_addition:
            return 

        self.is_division = False
        self.is_addition = True 
        self.is_subtraction = False 
        self.is_multiplication = False 
        self.is_firstnum = False 

        self.equation.configure(text= str(self.input1) + " + ")

    def subtract(self):
        self.calc_input1()

        if self.is_subtraction:
            return 

        self.is_division = False
        self.is_addition = False 
        self.is_subtraction = True 
        self.is_multiplication = False 
        self.is_firstnum = False 

        self.equation.configure(text= str(self.input1) + " - ")

    def calculate(self):
        
        print(self.input1)
        print(self.input2)
        print(self.exponent_number)




def main(args):

    calc = Calculator(ROOT)

    ROOT.mainloop()


if __name__ == "__main__":

    main(sys.argv[1:])