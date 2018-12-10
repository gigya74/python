"""
Term project by Will and Venkat.
application requirements:
1)python must be installed
2)run the below pip commands
pip install pandas
pip install matplotlib
pip install sqlite3
3)place the wamp.db in C:\\sqlite\\databases\\ path.


"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
LARGE_FONT = ("Verdana", 12)
import sqlite3
import pandas as pd
import logging
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pandas.tools.plotting import table

font = {'family' : 'monospace'}


matplotlib.rc('font', **font)
#------------------ CONFIGURATION -------------------------------
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
db_file = "C:\\sqlite\\databases\\wamp.db"


# ------------------	FUNCTION DEFINITIONS ------------------------




class __mainApp(tk.Tk):

    """Constructor"""
    def __init__(self):
        self.root = tk.Tk()

        ############################
        d = StartPage(self)
        d.showGraph()
        ############################
        self.root.mainloop()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="8715188.png")
        tk.Tk.wm_title(self, "WAMP project")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
    """shows the frames"""
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


"""the class which will be used to display the widgets"""
class StartPage(tk.Frame):

    """creates a connection object."""
    def create_connection(self):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Exception as e:
            print("Database error-probably ",db_file ," file not found:::",e)

        return None

    """ query to get results for chart1"""
    def getQ1(self):
        conn = self.create_connection()
        df_txn = pd.read_sql_query(
            "select fyear as Year,round(SUM(income_amount) + SUM(refund_amount),1) as NetAmount from transactions "
            " group by fyear", conn)
        conn.close()
        return df_txn

    """ query to get results for chart2"""
    def getQ2(self):
        conn = self.create_connection()
        df_txn = pd.read_sql_query(
            "SELECT fyear, perf_code, SUM(income_amount) + SUM(refund_amount) AS NetAmount FROM transactions  "
            "GROUP BY fyear,"
            " perf_code ", conn)
        conn.close()
        return df_txn

    """ query to get results for chart3"""
    def getQ3(self):
        conn = self.create_connection()
        df_txn = pd.read_sql_query(
            "SELECT fyear, price_category, round(SUM(income_amount) + SUM(refund_amount),0) AS Net_Income "
            "FROM transactions GROUP BY fyear, price_category", conn)
        conn.close()
        return df_txn

    """ query to get results for chart4"""
    def getQ4(self):
        conn = self.create_connection()
        df_txn = pd.read_sql_query(
            "SELECT fyear, price_type, round(SUM(income_amount) + SUM(refund_amount),0) AS Net_Income "
            "FROM transactions GROUP BY fyear, price_type having round(SUM(income_amount) + SUM(refund_amount),0)"
            " > 50000", conn)
        conn.close()
        return df_txn

    """ variable used by the radio buttons to update chart1"""
    colors = [
        ("Red", 'r'),
        ("Green", 'g'),
        ("Yellow", 'y')
    ]


    f = Figure(figsize=(5, 5), dpi=0)
    canvas = ''
    a = f.add_subplot(111)
    a1 = f.add_subplot(111)
    selectedYear = 2015

    """ paints chart1"""
    def q1(self):

        df_txn = self.getQ1()
        df_txn.plot(x='Year', y='NetAmount', color=self.var.get(), ax=self.a1, legend=False,fontsize=7)
        #self.a1.set_xlabel("Year")
        self.a1.set_ylabel("Net Amount")
        self.canvas._tkcanvas.pack()
        self.f1.canvas.draw()

        """ paints chart2"""
    def q2(self):
        df_txn = self.getQ2()
        self.f1.delaxes(self.a2)
        self.a2 = self.f1.add_subplot(233)
        ax1 = self.a2
        self.a2.set_title("Net income per show")
        index = set(df_txn["fyear"])
        print(self.selectedYear)
        res = df_txn[df_txn['fyear'] == self.selectedYear]  # make this dynamic
        labels = []
        sizes = []
        for index, row in res.iterrows():
            labels.append(row['perf_code'])
            sizes.append(row['NetAmount'])

        exp = [.15]
        for i in range(1, len(labels)):
            exp.append(0)
        plt = ax1.pie(sizes, explode=tuple(exp), labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 7})

        ax1.axis('equal')



        self.canvas._tkcanvas.pack()
        self.f1.canvas.draw()

    """ paints chart4"""
    def q4(self):
        style.use('ggplot')
        df_txn = self.getQ4()

        index = set(df_txn["fyear"])
        data = []
        index1 = []
        for i in sorted(index):
            index1.append(str(i))
            res = df_txn[df_txn['fyear'] == i]
            res = res.drop('fyear', 1)

            d = {}

            for index, row in res.iterrows():
                d[row['price_type']] = row['Net_Income']

            data.append(d)

        df = pd.DataFrame(data, index=sorted(index1))
        self.a4.set_xlabel("Year")
        self.a4.set_ylabel("Net Amount")
        df.plot(kind='bar', ax=self.a4, fontsize=7)

        self.f1.canvas.get_tk_widget().pack()
        self.f1.canvas.draw()

    """ paints chart3"""
    def q3(self):
        style.use('ggplot')
        # self.q3

        df_txn = self.getQ3()

        index = set(df_txn["fyear"])
        data = []
        index1 = []
        for i in sorted(index):
            index1.append(str(i))
            res = df_txn[df_txn['fyear'] == i]
            res = res.drop('fyear', 1)

            d = {}

            for index, row in res.iterrows():
                d[row['price_category']] = row['Net_Income']

            data.append(d)


        df = pd.DataFrame(data, index=sorted(index1))
        self.a3.set_xlabel("Year")
        self.a3.set_ylabel("Net Amount")
        df.plot(kind='bar', ax=self.a3,fontsize=7,figsize=(3,3))

        self.f1.canvas.get_tk_widget().pack()
        self.f1.canvas.draw()

    """ called by the slider"""
    def updateValue(self, event):
        print(self.slider.get())
        self.selectedYear = self.slider.get()
        self.q2()

    """ constructor of StartPage. Screen is prepared here. One figure and 4 subplots , a slider, three radio buttons are added to the screen"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        style.use('ggplot')
        selectedYear = 2015
        w = tk.Label(self, text="Slide to view \nchanges in \nnet income per concert")
        w.place(x=1200, y=160)
        self.slider = tk.Scale(self, from_=2015, to=2017,
                               orient="horizontal",
                               command=self.updateValue)
        self.slider.place(x=1200, y=210)

        self.f1 = Figure(figsize=(10, 10), dpi=100, facecolor='none')
        self.canvas = FigureCanvasTkAgg(self.f1, self)
        self.a1 = self.f1.add_subplot(231)
        self.a1.set_title("Net income by year")

        self.a2 = self.f1.add_subplot(233)

        self.a2.set_title("Net income per concert")

        self.a3 = self.f1.add_subplot(224)
        self.a3.set_title("Net income by price category")

        self.a4 = self.f1.add_subplot(223)
        self.a4.set_title("Net income by ticket price type")

        self.var = tk.StringVar()
        self.var.set('R')
        self._job = None

        w1 = tk.Label(self, text="Select a color!")
        w1.place(x=70, y=160)
        i = 0
        for key,color in self.colors:
            tk.Radiobutton(self,
                           text=key,
                           #padx=20,
                           variable=self.var,
                           command=self.q1,
                           value=color).place(x=70, y=185+i)
            i+=20

        self.q1()
        self.q2()
        self.q3()
        self.q4()


class PageThree(tk.Frame):

    def __init__(root, parent, controller):
        tk.Frame.__init__(root, parent)
        label = tk.Label(root, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(root, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, root)

        canvas.draw()

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

try:

    app = __mainApp()
    app.mainloop()

except Exception as e:
    print(e)