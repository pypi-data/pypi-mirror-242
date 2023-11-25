def Stokes(Re):
    """
    Stokes (Re)
    Computes the coefficient of drag using Stokes relationship
    
    CD = 24/Re
    
    param Re : Reynolds number of the particle
    
    NOTE: The model is valid for very low Re (Re << 1), 
    Stokes regime
    """
    
    temp = 24/Re
    
    return(temp)

def Sternin(Re):
    """
    Sternin (Re)
    Computes the coefficient of drag using Sternin's formulation
    
    param Re : particle Reynolds number
    
    Reference :
    """
    
    temp = (24/Re)+4.4/(Re**0.5)+0.42
    return(temp) 


def Schiller_Neumann(Re):
    """
    Schiller_Neumann (Re)
    Computes the coefficient of drag using Schiller-Neumann relationship

    CD = (24/Re)*(1+0.15 Re^0.687)
    
    param Re: particle Reynolds number 
    """
     
    temp = 24*(1+0.15*Re**(.687))/Re
    return(temp)

def Clift_Gauvin(Re):
    """
    Clift_Gauvin (Re)
    Computes the coefficient of drag using Clift-Gauvin relation

    Ref: 

    param Re : particle Reynolds number
    """

    t1 = 1+0.15*Re**(.687)
    t2 = Re*(0.42/(1+42500*Re**(-1.16)))/24
    temp = 24*(t1+t2)/Re
    return(temp)
