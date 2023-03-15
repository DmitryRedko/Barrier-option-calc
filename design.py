import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from calculus import Calc
from math import exp, log,sqrt
from scipy.stats import norm

class Window(ttk.Frame):

    def __init__(self, container,pdx,pdy):
        super().__init__(container)
        # field options
        self.options = {'padx': pdx, 'pady': pdy}

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def add_button(self,posx,posy,text, command, *args):
        self.button = ttk.Button(self, text=text)
        self.button['command'] = lambda: command(*args)
        self.button.grid(column=posx, row=posy, sticky=tk.W, **self.options)

    def input(self,posx,posy,input_name):
        setattr(self,input_name, tk.StringVar())
        self.entry = ttk.Entry(self, textvariable=getattr(self,input_name))
        self.entry.grid(column=posx, row=posy, **self.options)
        self.entry.focus()
    
    def add_label(self,text,posx,posy):
        self.label = ttk.Label(self, text=text)
        self.label.grid(column=posx, row=posy, sticky=tk.W, **self.options)

    def print_message(self,posx,posy,text):
        self.message_label = ttk.Label(self)
        self.message_label.config(text=text)
        self.message_label.grid(row=posx, columnspan=posy, **self.options)

    def calculate(self,*args):
        """  Handle button click event
        """
        try:
            S0 = float(self.S0.get())
            q = float(self.q.get())
            K = float(self.K.get())
            H = float(self.H.get())
            sigma = float(self.sigma.get())
            T = float(self.T.get())
            r = float(self.r.get())
            lam=(r-q+sigma*sigma/2)/sigma/sigma
            y=log(H*H/(S0*K))/(sigma*sqrt(T))+lam*sigma*sqrt(T)
            result = S0*exp(-q*T)*(H/S0)**(2*lam)*norm.cdf(y)-K*exp(-r*T)*(H/S0)**(2*lam-2)*norm.cdf(y-sigma*sqrt(T))
            print(result)
            self.print_message(10,10,result)
        except ValueError as error:
            showerror(title='Error', message=error)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Barrier calculator')
        self.geometry('350x400')
        self.resizable(False, False)


