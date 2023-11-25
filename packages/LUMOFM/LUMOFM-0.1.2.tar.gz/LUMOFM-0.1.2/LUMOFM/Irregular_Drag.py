import math as m

def Marayikkottu(arg1, arg2, Ma):
    """
    Marayikkottu(1 or 2, 1 or 2)
    Computes the drag and lift parameters for irregular 
    fractal aggregates in slip and transitional regimes
    
    param arg1 = 1 for slip, 2 for transitional
    param arg2 = 1 for open, 2 for dense aggregate
    param Ma : particle Mach number
    returns (p,q) 
    NOTE: the parameters have to be multiplied with the sphere
    drag formulation of Loth(2008) to get CD for the fractal aggregate
    
    Reference(s):
    """

    A1os = 1.3966; B1os = 45.108; A2os = 0.1412; B2os = 27.44; C2os = 0.0359
    A1ds = 1.2415; B1ds = 38.547; A2ds = 0.1683; B2ds = 9.624; C2ds = 0.0362
    A1ot = 2.2049; B1ot = 4.8792; A2ot = 0.4220; B2ot = 1.493; C2ot = 0.1137
    A1dt = 1.2113; B1dt = 19.358; A2dt = 0.4330; B2dt = 1.137; C2dt = 0.0816

    if(arg1 == 1 and arg2 == 1):
        A1=A1os; B1=B1os; A2=A2os; B2=B2os; C2=C2os
    if(arg1 == 1 and arg2 == 2):
        A1=A1ds; B1=B1ds; A2=A2ds; B2=B2ds; C2=C2ds 
    if(arg1 == 2 and arg2 == 1):
        A1=A1ot; B1=B1ot; A2=A2ot; B2=B2os; C2=C2ot
    if(arg1 == 2 and arg2 == 2):
        A1=A1dt; B1=B1dt; A2=A2dt; B2=B2ds; C2=C2dt

    p = A1*m.log(1+B1*Ma)
    q = A2*m.log(1+B2*Ma)/(1+C2*Ma*Ma)
    
    return(p,q)                                   
