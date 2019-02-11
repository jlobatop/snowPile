# Package importation
import numpy as np
import sys
from problemSetup import *

################################################################################
#                                    INPUTS                                    #
################################################################################
# Get the inputs from the terminal line
gen = int(sys.argv[1])

################################################################################
#                                   MAIN BODY                                  #
################################################################################
# Get the values of the search space
var = np.genfromtxt('./gen%i/pop' %(gen))

# Loop over all individuals
for ind in range(Nind):
	# Get the variables for each individual
    f1 = var[ind,0]**2
    f2 = (var[ind,0]-2)**2
    # Save the values of the search space and the function value toghether in a file
    with open('./data/gen%i.txt' %gen, 'a') as file:
        for i in range(Nvar):
            file.write("%.6f, " %(var[ind,i]))
        file.write("%.6f, " %(f1))
        file.write("%.6f \n" %(f2))
