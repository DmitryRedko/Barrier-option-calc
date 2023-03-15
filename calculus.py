from math import exp, log,sqrt
from scipy.stats import norm
class Calc:
    @staticmethod
    def calc(S0=None,q=None,T=None,H=None,K=None,r=None,sigma=None,**_):

        print(S0,q,T)
        lam=(r-q+sigma*sigma/2)/sigma/sigma
        y=log(H*H/(S0*K))/(sigma*sqrt(T))+lam*sigma*sqrt(T)
        res = S0*exp(-q*T)*(H/S0)**(2*lam)*norm.cdf(y)-K*exp(-r*T)*(H/S0)**(2*lam-2)*norm.cdf(y-sigma*sqrt(T))
        return res
    
