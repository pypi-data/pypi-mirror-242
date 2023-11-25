import math as m

def Kn_to_Re (Kn,Ma,gamma):
    """
    Kn_to_Re (Kn,Ma,gamma)
    Function to convert Knudsen number to Reynolds number
    
    param Kn : Knudsen number
    param Ka : Mach number
    param gamma : cp/cv ratio for the gas
    """

    temp = (0.5*gamma*m.pi)**0.5
    Re = Ma*temp/Kn
    return(Re)

def Kn_to_Ma (Kn,Re,gamma):
    """
    Kn_to_Ma (Kn,Re,gamma)
    Function to convert Knudsen number to Reynolds number
    
    param Kn : Knudsen number
    param Re : Reynolds number
    param gamma : cp/cv ratio for the gas
    """

    temp = (0.5*gamma*m.pi)**0.5
    Ma = Kn*Re/temp
    return(Ma)

def Re_to_Kn(Re,Ma,gamma):
    """
    Re_to_Kn (Re,Ma,gamma)
    Function to convert Knudsen number to Reynolds number
    
    param Re : Reynolds number
    param Ma : Mach number
    param gamma : cp/cv ratio for the gas
    """

    temp = (0.5*gamma*m.pi)**0.5
    Kn = Ma*temp/Re
    return(Kn)

def Re_to_Ma(Re,Kn,gamma):
    """
    Re_to_Ma (Re,Kn,gamma)
    Function to convert Reynolds number to Mach number
    
    param Kn : Knudsen number
    param Re : Reynolds number
    param gamma : cp/cv ratio for the gas
    """

    temp = (0.5*gamma*m.pi)**0.5
    Ma = Kn*Re/temp
    return(Ma)

def Ma_to_Kn(Ma,Re,gamma):
    """
    Ma_to_Kn (Ma,Re,gamma)
    Function to convert Knudsen number to Reynolds number
    
    param Kn : Knudsen number
    param Ka : Mach number
    param gamma : cp/cv ratio for the gas
    """

    temp = (0.5*gamma*m.pi)**0.5
    Kn = Ma*temp/Re
    return(Kn)

def Ma_to_Re(Ma,Kn,gamma):
    """
    Ma_to_Re (Kn,Ma,gamma)
    Function to convert Knudsen number to Reynolds number
    
    param Kn : Knudsen number
    param Ka : Mach number
    param gamma : cp/cv ratio for the gas
    """

    temp = (0.5*gamma*m.pi)**0.5
    Re = Ma*temp/Kn
    return(Re)
