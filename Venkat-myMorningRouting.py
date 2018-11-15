from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox


class Gui:
    # use tuple to store the days of the week and use this to populate the combobox.
    daysOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    activites_dict = {}  # initialize empty dict.
    activities = ['Exercise\nShower\n[Eat]',
                  'Exercise\nShower\n[Gardening]',
                  'Exercise\nShower\n[Read Online News]',
                  'Exercise\nShower\n[Trash Disposal]',
                  'Exercise\nShower\n[Organise days activities]',
                  'Exercise\nShower\n[Get grocery]',
                  'Exercise\nShower\n[Play with children]']  # list which is used to contruct the dictionary
    # construct the dictionary using the list and tuple to avoid typos.
    for x in daysOfWeek:
        act = activities[0]
        activites_dict[x] = act
        activities.remove(act)

    # init method called by default in a class
    def __init__(self):
        self.root = Tk()
        self.root.title("My Routine Activities")
        self.root.geometry("300x300")
        self.root.resizable(0, 0)  # Don't allow resizing in the x or y direction

        # the upper label frame where the user selects the day and clicks on the button
        upper_lf = Labelframe(self.root, text='Select a day of the week')
        upper_lf.grid(row=2, columnspan=7, sticky='WE', padx=15, pady=15, ipadx=135, ipady=35)

        # the combo box which has the days
        self.selections = C = Combobox(self.root)
        self.selections.bind("<<ComboboxSelected>>",
                             self.TextBoxUpdate)  # clear the label as the bombox value is changed
        self.selections['values'] = list(self.daysOfWeek)
        self.selections.place(x=40, y=40)
        # the button
        b = Button(self.root, text="Submit", command=self.checkSelection)
        b.place(x=200, y=35)

        # the lower label frame which displays the activities
        lower_lf = Labelframe(self.root, text='Routine for the day!!!')
        lower_lf.grid(row=3, columnspan=7, sticky='WE', padx=15, pady=25, ipadx=135, ipady=35)
        # the label which displays the activities
        self.labelText = ''
        self.actLabel = Label(lower_lf, text=self.labelText)
        self.actLabel.place(x=70, y=0)
        # the initial message as the window is shown to user.
        messagebox.showinfo("Select a value", "Select a value")
        self.selections.focus
        mainloop()


    # used to clear the label when value in combobox is changed
    def TextBoxUpdate(self, event):
        self.actLabel['text'] = ''
    # method called upon click of the button
    # checks if a value is selected.
    # if selected, gets the activites from dict and sets to the label
    def checkSelection(self):
        if self.selections.get() == '':
            messagebox.showinfo("Select a value", "Select a value")
            self.selections.focus
        else:
            act = self.activites_dict.get(self.selections.get())
            self.actLabel['text'] = act

app = Gui()
