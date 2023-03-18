import numpy as np
from math import *
from scipy.stats import norm
from tkinter.messagebox import showerror
from design import TableWidget

class Option_pricing:
    """
    Calculates the price of a barrier option using the Black-Scholes model.

    Parameters:
    S (float): The current underlying asset price.
    K (float): The option's strike price.
    H (float): The barrier level for the option.
    T (float): Time to expiration in years.
    sigma (float): The implied sigma of the underlying asset.
    r (float): The risk-free interest rate.
    q (float): The dividents yield.
    barrier_type (str): The type of barrier ('up-and-out', 'up-and-in', 'down-and-out', or 'down-and-in').
    option_type (str): The type of option ('call' or 'put').

    Returns:
    float: The price of the barrier option.
    """

    def call(self, S, K, H, T, sigma, r, q):
        d1 = (log(S/K)+(r-q+sigma*sigma/2)*T)/(sigma*sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        return S*exp(-q*T)*norm.cdf(d1) - K*exp(-r*T)*norm.cdf(d2)

    def call_down_and_in(self, S, K, H, T, sigma, r, q):
        if (S > H):
            if (H <= K):
                l = (r-q+sigma*sigma/2)/(sigma*sigma)
                y = log(H*H/(S*K))/(sigma*sqrt(T))+l*sigma*sqrt(T)
                return S*exp(-q*T)*(H/S)**(2*l)*norm.cdf(y)-K*exp(-r*T)*(H/S)**(2*l-2)*norm.cdf(y-sigma*sqrt(T))
            else:
                return self.call(S, K, H, T, sigma, r, q) - self.call_down_and_out(S, K, H, T, sigma, r, q)
        else:
            return self.call(S, K, H, T, sigma, r, q)

    def call_down_and_out(self, S, K, H, T, sigma, r, q):
        if (S > H):
            if (H <= K):
                return self.call(S, K, H, T, sigma, r, q) - self.call_down_and_in(S, K, H, T, sigma, r, q)
            else:
                l = (r-q+sigma*sigma/2)/(sigma*sigma)
                x1 = log(S/H)/(sigma*sqrt(T))+l*sigma*sqrt(T)
                y1 = log(H/S)/(sigma*sqrt(T))+l*sigma*sqrt(T)
                return S*norm.cdf(x1)*exp(-q*T)-K*exp(-r*T)*norm.cdf(x1 - sigma*sqrt(T))-S*exp(-q*T)*(H/S)**(2*l)*norm.cdf(y1)+K*exp(-r*T)*(H/S)**(2*l-2)*norm.cdf(y1-sigma*sqrt(T))
        else:
            return 0

    def call_up_and_in(self, S, K, H, T, sigma, r, q):
        if (S < H):
            if (H >= K):
                l = (r-q+sigma*sigma/2)/(sigma*sigma)
                x1 = log(S/H)/(sigma*sqrt(T))+l*sigma*sqrt(T)
                y1 = log(H/S)/(sigma*sqrt(T))+l*sigma*sqrt(T)
                y = log(H*H/(S*K))/(sigma*sqrt(T))+l*sigma*sqrt(T)
                return S*norm.cdf(x1)*exp(-q*T)-K*exp(-r*T)*norm.cdf(x1 - sigma*sqrt(T))-S*exp(-q*T)*(H/S)**(2*l)*(norm.cdf(-y)-norm.cdf(-y1))+K*exp(-r*T)*(H/S)**(2*l-2)*(norm.cdf(-y+sigma*sqrt(T))-norm.cdf(-y1+sigma*sqrt(T)))
            else:
                return self.call(S, K, H, T, sigma, r, q)
        else:
            return self.call(S, K, H, T, sigma, r, q)

    def call_up_and_out(self, S, K, H, T, sigma, r, q):
        if (H >= K):
            return self.call(S, K, H, T, sigma, r, q) - self.call_up_and_in(S, K, H, T, sigma, r, q)
        else:
            return 0

    def put(self, S, K, H, T, sigma, r, q):
        d1 = (log(S/K)+(r-q+sigma*sigma/2)*T)/(sigma*sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        return -S*exp(-q*T)*norm.cdf(-d1) + K*exp(-r*T)*norm.cdf(-d2)

    def put_down_and_out(self, S, K, H, T, sigma, r, q):
        if (S > H):
            if (H >= K):
                return 0
            else:
                return self.put(S, K, H, T, sigma, r, q) - self.put_down_and_in(S, K, H, T, sigma, r, q)
        else:
            return 0

    def put_down_and_in(self, S, K, H, T, sigma, r, q):
        if (S > H):
            if (H >= K):
                return self.put(S, K, H, T, sigma, r, q)
            else:
                l = (r-q+sigma*sigma/2)/(sigma*sigma)
                x1 = log(S/H)/(sigma*sqrt(T))+l*sigma*sqrt(T)
                y1 = log(H/S)/(sigma*sqrt(T))+l*sigma*sqrt(T)
                y = log(H*H/(S*K))/(sigma*sqrt(T))+l*sigma*sqrt(T)
                return -S*norm.cdf(-x1)*exp(-q*T)+K*exp(-r*T)*norm.cdf(-x1+sigma*sqrt(T))+S*exp(-q*T)*(H/S)**(2*l)*(norm.cdf(y)-norm.cdf(y1))-K*exp(-r*T)*(H/S)**(2*l-2)*(norm.cdf(y-sigma*sqrt(T))-norm.cdf(y1-sigma*sqrt(T)))
        else:
            return self.put(S, K, H, T, sigma, r, q)
            
    def put_up_and_in(self, S, K, H, T, sigma, r, q):
        if (S <= H):
            if (H >= K):
                l = (r-q+sigma*sigma/2)/(sigma*sigma)
                y = log(H*H/(S*K))/(sigma*sqrt(T))+l*sigma*sqrt(T)
                return -S*exp(-q*T)*(H/S)**(2*l)*norm.cdf(-y)+K*exp(-r*T)*(H/S)**(2*l-2)*norm.cdf(-y+sigma*sqrt(T))
            else:
                return self.put(S, K, H, T, sigma, r, q) - self.put_up_and_out(S, K, H, T, sigma, r, q)
        else:
       
            return self.put(S, K, H, T, sigma, r, q)

    def put_up_and_out(self, S, K, H, T, sigma, r, q):
        if (S <= H):
            if (H >= K):
                return self.put(S, K, H, T, sigma, r, q) - self.put_up_and_in(S, K, H, T, sigma, r, q)
            else:
                l = (r-q+sigma*sigma/2)/(sigma*sigma)
                x1 = log(S/H)/(sigma*sqrt(T))+l*sigma*sqrt(T)
                y1 = log(H/S)/(sigma*sqrt(T))+l*sigma*sqrt(T)
                return -S*norm.cdf(-x1)*exp(-q*T)+K*exp(-r*T)*norm.cdf(-x1+sigma*sqrt(T))+S*exp(-q*T)*(H/S)**(2*l)*norm.cdf(-y1)+K*exp(-r*T)*(H/S)**(2*l-2)*norm.cdf(-y1+sigma*sqrt(T))
        else:
            return 0


def logic_of_buttom(obj):
    try:
        S0 = float(obj.get_param("S0"))
        K = float(obj.get_param("K"))
        H = float(obj.get_param("H"))
        sigma = float(obj.get_param("sigma"))
        T = float(obj.get_param("T"))
        r = float(obj.get_param("r"))
        q = float(obj.get_param("q"))
        barrier_type = obj.get_param("barrier_type")
        option_type = obj.get_param("option_type")

        option = Option_pricing()
        if option_type=='all':
            option_type = ['call','put']
        elif option_type == 'call':
            option_type = ['call']
        elif option_type == 'put':
            option_type = ['put']
        else:
           raise ValueError("Such type of options does not exist") 

        while 'all' in barrier_type:
            barrier_type = barrier_type.replace('all', "down-and-out,down-and-in,up-and-out,up-and-in")

        list_of_barriers = barrier_type.split(',')
        for i in range(len(list_of_barriers)):
            list_of_barriers[i] = list_of_barriers[i].replace(' ', '')

        for i in list_of_barriers:
            if (i!='up-and-out') and (i!='up-and-in') and (i!='down-and-out') and (i!='down-and-in'):
               raise ValueError("Such type of barrier does not exist") 
        table = TableWidget(list_of_barriers)

        for opt in option_type:
            result=[]
            for barrier in list_of_barriers:
                temp = barrier.split("-")
                method_name = opt+"_"+temp[0]+'_'+temp[1]+'_'+temp[2]

                method = getattr(option, method_name)
                result += [round(method(S0, K, H, T, sigma, r, q),4)]

            table.add_raw(opt,result)
        table.pack()
        table.show_table()
        # else:
        #     raise ValueError("Such type of options does not exist")
    except ValueError as error:
        showerror(title='Error', message=error)