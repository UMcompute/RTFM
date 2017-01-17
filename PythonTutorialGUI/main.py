from tkinter import *

#  import tkinter as tk
#  from Tkinter import *

# Lesson 14: Images and Icons 01-10-17 day

# add images and icons to your GUI!

#root = Tk()

#photo = PhotoImage(file="fire.png")

# set the photo inside a label and then place the label anywhere
#label = Label(root, image=photo)
#label.pack()

#root.mainloop()

# Lesson 1: Introduction 01-03-17 night

# create a blank window and add some text
#root = Tk()
#theLabel = Label(root, text="this is my first label")
#theLabel.pack()
#root.mainloop()


# Lesson 2: Organizing the Layout 01-03-17 night

# how do we organize our screen?
root = Tk()

# make invisible container
topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

button1 = Button(topFrame, text="Button 1", fg="red")
button2 = Button(topFrame, text="Button 2", fg="blue")
button3 = Button(topFrame, text="Button 3", fg="green")
button4 = Button(bottomFrame, text="Button 4", fg="purple")

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)

#root.mainloop()

# Lesson 3: Fitting Widgets in Your Layout 01-08-17 night
root = Tk()

one = Label(root, text="One", bg="red", fg="white")
one.pack()
two = Label(root, text="Two", bg="green", fg="black")
two.pack(fill=X)
three = Label(root, text="Three", bg="blue", fg="white")
three.pack(side=LEFT, fill=Y)

#root.mainloop()

# Lesson 4: Grid Layout 01-08-17 night
root = Tk()

# two text prompts
label_1 = Label(root, text="Username")
label_2 = Label(root, text="Password")

# two entry boxes
entry_1 = Entry(root)
entry_2 = Entry(root)

# place them in a "grid"
label_1.grid(row=0, column=0, sticky=E)
label_2.grid(row=1, column=0, sticky=E)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

# Lesson 5: More on the Grid Layout 01-08-17 night

# make a checkbox, default is true or false basically
c = Checkbutton(root, text="Keep me logged in")
c.grid(columnspan=2)

# root.mainloop()

# Lesson 6: Binding a Function to Layouts 01-08-17 night
root = Tk()


def printName():
    print("hello my name is Paul")


def printName2(event):
    print("hello my name is Paul")


# button_1 = Button(root, text="Print my name", command=printName)
# button_1.pack()

button2 = Button(root, text="Print my name")
button2.bind("<Button-1>", printName2)
button2.pack()

# root.mainloop()



# Lesson 7: Mouse Click Events 01-10-17 day

root = Tk()

# different actions for different mouse clicks


def left_click(event):
    print("left")


def right_click(event):
    print("right")


def middle_click(event):
    print("middle")


frame = Frame(root, width=300, height=250)
frame.bind("<Button-1>", left_click)
frame.bind("<Button-2>", middle_click)
frame.bind("<Button-3>", right_click)
frame.pack()

# root.mainloop()


# Lesson 8: Using Classes 01-10-17 day
class MyClass:

    # master is the root or main window
    def __init__(self, master):
        # create a frame in the main window
        frame = Frame(master)
        frame.pack()

        self.printButton = Button(frame, text="Print Message", command=self.print_msg)
        self.printButton.pack(side=LEFT)

        # self.quit will break the main loop to quit it
        self.quitButton = Button(frame, text="Quit", command=frame.quit)
        self.quitButton.pack(side=LEFT)

    def print_msg(self):
        print("the button worked!")


root = Tk()
p = MyClass(root)
# root.mainloop()


# Lesson 9: Creating Drop-down Menus 01-10-17 day
# (first of a mini-series)

def do_nothing():
    print("ok I will do nothing")

root = Tk()

menu = Menu(root)  # object created from the Menu class
root.config(menu=menu)  # configure that menu for your code

subMenu = Menu(menu)  # create a sub-menu in the main menu
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New Project...", command=do_nothing)
subMenu.add_command(label="New ...", command=do_nothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=do_nothing)

# make another menu now
editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=do_nothing)

# Lesson 10: Creating a Toolbar 01-10-17 day

# create the toolbar
toolbar = Frame(root, bg="blue")

# put it in the toolbar frame
insertButton = Button(toolbar, text="Insert Image", command=do_nothing)
insertButton.pack(side=LEFT)
printButton = Button(toolbar, text="Print", command=do_nothing)
printButton.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

# Lesson 11: Adding the Status Bar 01-10-17 day

# bd is the border
status = Label(root, text="Preparing to do Nothing...", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

# root.mainloop()

# Lesson 12: Message Box 01-10-17 day
import tkinter.messagebox

root = Tk()

tkinter.messagebox.showinfo('Window Title', 'This is our test message for the box')

answer = tkinter.messagebox.askquestion('Question 1', 'Do you like this program interface?')

if answer == 'yes':
    print("good! =)")

# root.mainloop()

# Lesson 13: Shapes and Graphics 01-10-17 day

root = Tk()

canvas = Canvas(root, width=200, height=100)
canvas.pack()

# now we can create shapes on our new canvas space
blackLine = canvas.create_line(0, 0, 200, 50)
redLine = canvas.create_line(0, 100, 200, 50, fill="red")
greenBox = canvas.create_rectangle(25, 25, 130, 60, fill="green")

# hide and show different graphics
canvas.delete(redLine)
canvas.delete(ALL)  # clears the canvas back to its original clean self

root.mainloop()

# (moved Lesson 14 to the top in order to avoid the conflict with previous windows closing)

# FINISH THIS SET ON 01-10-17 AT 16:10 WHILE AT WORK

