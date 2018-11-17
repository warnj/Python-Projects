'''from tkinter import *

def show_entry_fields():
   print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
   e1.delete(0,END)
   e2.delete(0,END)

master = Tk()
Label(master, text="First Name").grid(row=0)
Label(master, text="Last Name").grid(row=1)

e1 = Entry(master)
e2 = Entry(master)
e1.insert(10,"Miller")
e2.insert(10,"Jill")

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Show', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

mainloop( )'''

from Tkinter import *
import tkMessageBox

def displayText():

     global entryWidget

     if entryWidget.get().strip() == "":
         tkMessageBox.showerror("Tkinter Entry Widget", "Enter a text value")
     else:
         tkMessageBox.showinfo("Tkinter Entry Widget", "Text value =" + entryWidget.get().strip())

if __name__ == "__main__":

     root = Tk()
     root.title("UW Auto Registration")
     root["padx"] = 100
     root["pady"] = 200

     # Create a text frame to hold the text Label and the Entry widget
     textFrame = Frame(root)

     #Create a Label in textFrame
     entryLabel = Label(textFrame)
     entryLabel["text"] = "UW NetID:"
     entryLabel.pack(side=LEFT)

     # Create an Entry Widget in textFrame
     entryWidget = Entry(textFrame)
     entryWidget["width"] = 50
     entryWidget.pack(side=LEFT)

     textFrame.pack()

     button = Button(root, text="Begin", command=displayText)
     button.pack()

     root.mainloop()