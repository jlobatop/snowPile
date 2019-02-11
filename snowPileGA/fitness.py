# Package importation
import numpy as np
import sys
import scipy.optimize
from problemSetup import *

################################################################################
#                                    INPUTS                                    #
################################################################################
# Get the inputs from the terminal line
gen = int(sys.argv[1])

# Notebook variables (copied here to avoid expensive recomputations of the
# same values each generation evaluation)
# Fixed ice temperature
Tice = -10+273.15
# Fixed volume of the snow pile
fixedVol = 10000
# Surface heat conductive coefficient
k_soil = 3.0
# Ground temperature from the probes data
Tgnd = 282.4788753177849
# Ground probe depth
d = 1
# Average air convective heat transfer coefficient
h = 9.813040255272988
# Infinite temperature for the convective heat
Tinf = 279.63818897637805
# Solar incidence value from NOAA data
Gsolar = 144.61805555555554
# Sky temperature for the radiative heat
Tsky = 263.3815936815641
# Stephan Boltzmann constant in SI units
sigma = 5.67036713e-8

################################################################################
#                                  FUNCTION                                    #
################################################################################

# Function to compute the volume of the pile
def vol(alpha, b, H, l):
    # Get the upper side of the trapezoid
    b2 = b - 2*H*np.tan(np.deg2rad(90-alpha))
    # Get the trapezoidal area
    frontArea = H*(b+b2)/2
    # Get the volume with the length
    volume = frontArea*l
    return volume

# Lambda function for the solution of the equation
fVol = lambda l, b, H, alpha, fixedVol : vol(alpha, b, H, l)-fixedVol

# Function for surface temperature optimization
def Tsurf_fun(Tsurf, *data):
    h, Tinf, Ains, Gsolar, Eins, sigma, Tsky, Kins, Tice, Tins = data
    # convective heat
    qconv = h*(Tinf-Tsurf)
    # radiative heat
    qrad = Ains*Gsolar + Eins*sigma*(Tsky**4-Tsurf**4)
    # conductive heat
    qins = Kins*(Tsurf-Tice)/Tins
    return qconv + qrad - qins

################################################################################
#                                   MAIN BODY                                  #
################################################################################
# Get the values of the search space
var = np.genfromtxt('./gen%i/pop' %(gen))

# Loop over all individuals
for ind in range(Nind):
	# Get the variables for each individual
    alpha = var[ind,0]
    b = var[ind,1]
    H = var[ind,2]
    Tins = var[ind,3]
    Kins = var[ind,4]
    Eins = var[ind,5]
    Ains = var[ind,6]

    # each individual will require the solution of two equations with fsolve
    # length of the snow pile
    l = scipy.optimize.fsolve(fVol, 1e3, args=(b, H, alpha, fixedVol))
    # surface temperature of the snow pile outer insulator
    Tsurf = scipy.optimize.fsolve(Tsurf_fun, Tice,
                              args=(h, Tinf, Ains, Gsolar, Eins, sigma, Tsky,
                                    Kins, Tice, Tins))

    # AIR SURFACES
    # Conductive heat through the insulation
    qins = Kins*(Tsurf-Tice)/Tins
    # Upper base width
    b2 = b - 2*H*np.tan(np.deg2rad(90-alpha))
    # Lateral size
    ls = H/np.cos(np.deg2rad(90-alpha))
    # Air surface is 2*(trapezoidal front) + (upper rectangle) + 2*(side rectangles)
    air_surf = 2*(H*(b+b2)/2) + (b2*l) + 2*(ls*l)
    # Air surface heat is
    qair = qins*air_surf

    # SOIL SURFACES
    # Conductive heat of the ground
    qgnd = k_soil*(Tgnd-Tice)/d
    # Soil surface is simply the rectangle given by
    soil_surf = b*l
    # Soil surface heat is
    qsoil = qgnd*soil_surf

    # avoid upside down trapezoidal prisms
    if 2*H*np.tan(np.deg2rad(90-alpha)) > b:
    # put extremely large values as fitness values
        qair = 1e15
        qsoil = 1e15
        air_surf = 1e15
        soil_surf = 1e15

    # Save the values of the search space and the function value toghether in a file
    with open('./data/gen%i.txt' %gen, 'a') as file:
        for i in range(Nvar):
            file.write("%.6f, " %(var[ind,i]))
        file.write("%.6f, " %(np.abs(qsoil)+np.abs(qair)))
        file.write("%.6f \n" %air_surf)
