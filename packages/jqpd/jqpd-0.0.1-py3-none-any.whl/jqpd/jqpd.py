import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import norm
from scipy.stats import lognorm


#getting model equation parameters from given information
def get_params_s(lbound, alpha, low, base, high):
    assert low <= base <= high
    c = norm.ppf(1-alpha)
    L = np.log(low - lbound)
    B = np.log(base - lbound)
    H = np.log(high - lbound)
    n = np.sign(L + H - 2*B)
    if n == 1:
        theta = low - lbound
    elif n == 0:
        theta = base - lbound
    else:
        theta = high - lbound
    delta = (1/c)*np.sinh(np.arccosh((H-L)/(2*min(B-L, H-B))))
    lamb = (1/(delta*c))*min(H-B, B-L)
    return c, L, B, H, n, theta, delta, lamb

def get_params_b(lbound, ubound, alpha, low, base, high):
    assert low <= base <= high
    c = norm.ppf(1-alpha)
    L = norm.ppf((low - lbound)/(ubound - lbound))
    B = norm.ppf((base - lbound)/(ubound - lbound))
    H = norm.ppf((high - lbound)/(ubound - lbound))
    n = np.sign(L + H - 2*B)
    if n == 1.0:
        xi = L
    elif n == 0.0:
        xi = B
    else:
        xi = H
    delta = (1/c)*np.arccosh((H-L)/(2*min(B-L, H-B)))
    lamb = (H-L)/(np.sinh(2*delta*c))
    
    return c, L, B, H, n, xi, delta, lamb

#defining quantile functions
def qs(lbound, alpha, low, base, high, p):
    c, L, B, H, n, theta, delta, lamb = get_params_s(lbound, alpha, low, base, high)
    
    if n == 0:
        return lbound + theta*np.exp(lamb*delta(norm.ppf(p)))
    return lbound + theta*np.exp(lamb*np.sinh(np.arcsinh(delta*norm.ppf(p)) + np.arcsinh(n*c*delta))) 

def qb(lbound, ubound, alpha, low, base, high, p):
    c, L, B, H, n, xi, delta, lamb = get_params_b(lbound, ubound, alpha, low, base, high)
    
    if n == 0:
        return lbound + (ubound-lbound)*norm.cdf(B + (H-L)/((2*c))*norm.ppf(p))
    
    return lbound + (ubound-lbound)*norm.cdf(xi + lamb* (np.sinh(delta* (norm.ppf(p) + n*c))))

def quantile(p, alpha, low, base, high, lbound, ubound = None):
    if ubound:
        return qb(lbound, ubound, alpha, low, base, high, p)
    else:
        return qs(lbound, alpha, low, base, high, p)


#defining pdf
def qbpdf(lbound, ubound, alpha, low, base, high, x):
    c, L, B, H, n, xi, delta, lamb = get_params_b(lbound, ubound, alpha, low, base, high)
    
    if n == 0:
        return ((2*c/((H-L)*(ubound-lbound)))*(1/(norm.pdf(norm.ppf((x-lbound)/(ubound-lbound)))))*\
            norm.pdf((2*c/(H-L))*(-B+norm.ppf((x-lbound)/(ubound-lbound)))))
    
    
    return (1/delta)*(1/(ubound-lbound))*norm.pdf(-n*c + (1/delta)*np.arcsinh((1/lamb)*(-xi + norm.ppf((x-lbound)/\
        (ubound-lbound)))))*(1/(norm.pdf(norm.ppf((x - lbound)/(ubound - lbound)), 0)))*\
            (1/np.sqrt((lamb**2)+((-xi + norm.ppf((x-lbound)/(ubound-lbound)))**2)))

def qspdf(lbound, alpha, low, base, high, x):
    c, L, B, H, n, theta, delta, lamb = get_params_s(lbound, alpha, low, base, high)
    
    if n == 0:
        mu = np.log(theta)
        sigma = (H-B)/c
        return lognorm.pdf(x-lbound, mu, sigma)
    
    return norm.pdf(np.sinh(np.arcsinh(c*n*delta) - np.arcsinh((1/lamb)*np.log((x - lbound)/theta)))/delta)\
            *np.cosh(np.arcsinh(c*n*delta) - np.arcsinh((1/lamb)*np.log((x - lbound)/theta)))/\
            ((x - lbound)*delta*lamb*np.sqrt(1+(np.log((x - lbound)/theta)/lamb)**2))

def pdf(x, alpha, low, base, high, lbound, ubound = None):
    if ubound:
        return qbpdf(lbound, ubound, alpha, low, base, high, x)
    else:
        return qspdf(lbound, alpha, low, base, high, x)

#defining cdf
def qbcdf(lbound, ubound, alpha, low, base, high, x):
    c, L, B, H, n, xi, delta, lamb = get_params_b(lbound, ubound, alpha, low, base, high)
    
    if n == 0:
        norm.cdf((2*c/(H-L))*(-B+norm.ppf((x-lbound)/(ubound-lbound))))
    
    return norm.cdf((1/delta)*np.arcsinh((1/lamb)*(norm.ppf((x-lbound)/(ubound-lbound)) - xi)) - n*c)

def qscdf(lbound, alpha, low, base, high, x):
    c, L, B, H, n, theta, delta, lamb = get_params_s(lbound, alpha, low, base, high)
    
    if n == 0:
        mu = np.log(theta)
        sigma = (H-B)/c
        return lognorm.cdf(x-lbound, mu, sigma)
    
    return norm.cdf((1/delta)*np.sinh(np.arcsinh((1/lamb)*np.log((x-lbound)/theta)) - np.arcsinh(n*c*delta)))

def cdf(x, alpha, low, base, high, lbound, ubound = None):
    if ubound:
        return qbcdf(lbound, ubound, alpha, low, base, high, x)
    else:
        return qscdf(lbound, alpha, low, base, high, x)