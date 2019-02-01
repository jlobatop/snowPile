# Package importation
import numpy as np
from problemSetup import *

################################################################################
#                              FUNCTION DEFINITION                             #
################################################################################
def initialization():
    """
    Initialization the population

    INPUTS:
    (Nind):           number of individuals
    (var_low):        lower limits of the search domain variables
    (var_high):       upper limits of the search domain variables
    (constrainedPts): function that returns a masked array for constrained points

    OUTPUTS:
    initialPop:       numpy.ndarray with the initial N individuals

    This function computes the initial population for a Nvar variable problem
    with an equally-spaced point distribution of Nind individuals
    """
    # preallocate space for a population of size Nind and Nvar
    initialPop = np.zeros((Nind,Nvar))

    # for each variable
    for i in range(Nvar):
        # compute the location of the division within the variables
        div = int(Nind/round(Nind**((i+1)/Nvar)))
        # crate a boolean array to be filled per variable
        bool = round(Nind**((Nvar-1)/Nvar)/div)* \
               [div*[j] for j in range(round(Nind**(1/Nvar)))]
        # flatten the boolean array
        bool = np.array(bool).flatten()
        # get a linspace for the current vairable
        var = np.linspace(var_low[i],var_high[i],int(Nind**(1/Nvar)))
        # apply the boolean (repeated values for different individuals)
        initialPop[:,i] = var[bool]
    # return the initial population array
    return initialPop

################################################################################
#                                   MAIN BODY                                  #
################################################################################
# initialize the population
population = initialization()

# save the population in the file
np.savetxt('./gen0/pop', population, fmt='%.6f', delimiter=' ')
