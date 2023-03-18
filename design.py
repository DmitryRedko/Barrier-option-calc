import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
# from calc import Option_pricing
from math import exp, log, sqrt
from scipy.stats import norm


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.tooltip_label = None

    def show_tooltip(self, event):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_label = tk.Toplevel(self.widget)
        self.tooltip_label.wm_overrideredirect(True)
        self.tooltip_label.wm_geometry("+%d+%d" % (x, y))
        self.tooltip_label.wm_attributes("-topmost", 1)
        label = tk.Label(self.tooltip_label, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip_label:
            self.tooltip_label.destroy()


class Window(ttk.Frame):

    def __init__(self, container, pdx, pdy):
        super().__init__(container)
        # field options
        self.options = {'padx': pdx, 'pady': pdy}

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def add_button(self, posx, posy, text, command, obj):
        self.button = ttk.Button(self, text=text)
        self.button['command'] = lambda: command(obj)
        self.button.grid(column=posx, row=posy, sticky=tk.W, **self.options)

    def input(self, posx, posy, input_name, default):
        setattr(self, input_name, tk.StringVar())
        self.entry = ttk.Entry(self, textvariable=getattr(self, input_name))
        if default!=None:
            self.entry.insert(0,default)
        self.entry.grid(column=posx, row=posy, **self.options)
        self.entry.focus()

    def add_label(self, text, posx, posy, info=None):
        self.label = ttk.Label(self, text=text)
        self.label.grid(column=posx, row=posy, sticky=tk.W, **self.options)
        if info != None:
            tooltip = Tooltip(self.label, info)

    def print_message(self, posx, posy, text):
        self.message_label = ttk.Label(self)
        self.message_label.config(text=text)
        self.message_label.grid(row=posx, columnspan=posy, **self.options)

    def get_param(self, name):
        """  Handle button click event
        """
        try:
            # x=getattr(self,name)
            value = getattr(self,name).get()
            return value
        except ValueError as error:
            showerror(title='Error', message=error)

class TableWidget:
    def __init__(self, args):
        self.root = tk.Tk()
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = args
        for values in args:
            self.tree.heading(values, text=values)
            
    
    def add_raw(self, raw_name, args):
        self.tree.insert("", tk.END, text=raw_name, values=tuple(args))
        for col in self.tree["columns"]:
            self.tree.column(col)

    
    def pack(self):
        self.tree.pack()

    def show_table(self):
        self.root.mainloop()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Barrier calculator')
        self.geometry('350x400')
        self.resizable(False, False)
