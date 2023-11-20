# CoefMod
from numpy import mod
from numpy.polynomial import Polynomial
def coefmod(x,m):
    v = mod(x.coef,m)
    return(Polynomial(v))

