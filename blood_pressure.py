import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from sklearn import linear_model
from sklearn.metrics import r2_score

def load_data():
    return pd.read_csv("systolic.csv")

def show():
    for item in tree.get_children():
        tree.delete(item)
    data = load_data()
    for index, row in data.iterrows():
        tree.insert("", 'end', values=(row['id'], row['X1'], row['X2'], row['X3']))

def update():
    id_val = int(a.get())
    x1_val = float(b.get())
    x2_val = float(c.get())
    x3_val = float(d.get())
    data = load_data()
    data.loc[data['id'] == id_val, ['X1', 'X2', 'X3']] = [x1_val, x2_val, x3_val]
    data.to_csv("systolic.csv", index=False)
    la = Label(master=dolce, text="1 record was updated")
    la.place(x=20, y=680)

def delete():
    id_val = int(h.get())
    data = load_data()
    data = data[data['id'] != id_val]
    data.to_csv("systolic.csv", index=False)
    messagebox.showinfo("Result", "1 record was deleted")

def plot():
    data = load_data()
    mydata = data['X1'].values
    data2 = data['X2'].values
    data3 = data['X3'].values
    
    #----------X2 vs. Y graph
    regr = linear_model.LinearRegression()
    regr.fit(data[['X2']], mydata)
    pred_mydata = regr.predict(data[['X2']])
    
    fig = Figure(figsize=(3, 3), dpi=100)
    plot1 = fig.add_subplot(111)
    plot1.scatter(data2, mydata) #scatter() is a function to draw dots.
    
    plot1.plot(data2, pred_mydata, color='blue', linewidth=1) #plot() is a function to draw a line
    r2_value_X2 = r2_score(mydata, pred_mydata)
    plot1.text(min(data2), max(mydata), f'R2={r2_value_X2:.4f}', fontsize=10)
    
    canvas = FigureCanvasTkAgg(fig, master=dolce)
    canvas.draw()
    canvas.get_tk_widget().place(x=40, y=280)
    
    #-------X3 vs. Y graph
    regr2 = linear_model.LinearRegression()
    regr2.fit(data[['X3']], mydata)
    pred_mydata2 = regr2.predict(data[['X3']])
    
    fig2 = Figure(figsize=(3, 3), dpi=100)
    plot2 = fig2.add_subplot(111)
    plot2.scatter(data3, mydata)
    
    plot2.plot(data3, pred_mydata2, color='blue', linewidth=1) #plot() is a function to draw a line
    r2_value_X3 = r2_score(mydata, pred_mydata2)
    plot2.text(min(data3), max(mydata), 
               f'R2={r2_value_X3:.4f} \nEquation: y={regr2.coef_[0]:.4f}x + {regr2.intercept_:.4f}', fontsize=8)
        
    canvas2 = FigureCanvasTkAgg(fig2, master=dolce)
    canvas2.draw()
    canvas2.get_tk_widget().place(x=320, y=280)
    toolbar = NavigationToolbar2Tk(canvas, dolce)
    toolbar.update()

def forecast():
    data = load_data()
    X = data[["X2", "X3"]]
    y = data["X1"]
    regr = linear_model.LinearRegression()
    regr.fit(X, y)
    predicteddow = regr.predict([[float(f.get()), float(g.get())]])
    e10.delete(0, END)
    k.set(str(predicteddow))
    pearsonr = regr.score(X, y)
    la = Label(dolce, text="r = %.4f" % (pearsonr))
    la.place(x=350, y=600)
    lb = Label(dolce, text="y = %.4f *x1 + %.4f *x2 + %.4f" % (regr.coef_[0], regr.coef_[1], regr.intercept_))
    lb.place(x=350, y=630)

dolce = Tk()
dolce.geometry("740x700")
dolce.title("Input and Table")

a = StringVar()
e2 = Entry(master=dolce, textvar=a)
e2.place(x=420, y=60, width=60)
b = StringVar()
e3 = Entry(master=dolce, textvar=b)
e3.place(x=500, y=60, width=60)
c = StringVar()
e4 = Entry(master=dolce, textvar=c)
e4.place(x=580, y=60, width=60)
d = StringVar()
e44 = Entry(master=dolce, textvar=d)
e44.place(x=660, y=60, width=60)
f = StringVar()
e5 = Entry(master=dolce, textvar=f)
e5.place(x=200, y=600, width=60)
g= StringVar()
e5 = Entry(master=dolce, textvar=g)
e5.place(x=280, y=600, width=60)

h=StringVar()
e9 = Entry(master=dolce, textvar=h)
e9.place(x=580, y=140, width=60)

k=StringVar()
e10 = Entry(master=dolce, textvar=k)
e10.place(x=580, y=600, width=60, height=60)

tree = ttk.Treeview(dolce, selectmode='browse')
tree.place(x=10, y=10)

vsb = ttk.Scrollbar(dolce, orient="vertical", command=tree.yview)
vsb.place(x=360, y=10, height=230)

tree.configure(yscrollcommand=vsb.set)

tree["columns"] = ("1", "2", "3", "4")
tree['show'] = 'headings'
tree.column("1", width=90, anchor='c')
tree.column("2", width=90, anchor='c')
tree.column("3", width=90, anchor='c')
tree.column("4", width=90, anchor='c')

tree.heading("1", text="id")
tree.heading("2", text="systolic")
tree.heading("3", text="age")
tree.heading("4", text="weight")

b1 = Button(master=dolce, text="Show", command=show)
b1.place(x=420, y=20)

b3 = Button(master=dolce, text="Update", command=update)
b3.place(x=650, y=20)

b4 = Button(master=dolce, text="Delete", command=delete)
b4.place(x=650, y=140)

b5 = Button(master=dolce, text="Plot", command=plot)
b5.place(x=650, y=180)

b6 = Button(master=dolce, text="Forecast Systolic Blood Pressure", command=forecast)
b6.place(x=10, y=600)

dolce.mainloop()
