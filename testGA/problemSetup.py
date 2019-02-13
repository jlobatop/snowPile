# Package importation
import numpy as np

################################################################################
#                                    INPUTS                                    #
################################################################################

# number of variables of each individual
Nvar = 7
# number of indiiduals per generation (x^Nvar being x a real number)
Nind = 2**Nvar
# search spaces limits
var_low = np.array([-10,-1,-1,-1,-1,-1,-1])
var_high = np.array([10,1,1,1,1,1,1])
# comparison mode for search space limits (row per each one of the variables,
# first row is for the low limit and the second row in for the high limit)
compMode = [['leq', 'geq'],
            ['leq', 'geq'],
            ['leq', 'geq'],
            ['leq', 'geq'],
            ['leq', 'geq'],
            ['leq', 'geq'],
            ['leq', 'geq']]

################################################################################
#                                  FUNCTION                                    #
################################################################################
def constrainedPts(points, var_low, var_high, compMode):
    """Function that will constraint points out of bounds

    INPUTS:
    points:     points in the parameter search space as a numpy.ndarray
    (var_low):  limits of the search domain variables
    (var_high): limits of the search domain
    compMode:   comparison mode ('leq','geq','less','greater','equal') as list

    OUTPUTS:
    booleanMat: boolean matrix with 1 for the individuals out of bounds

    This function will evaluate the constraints for all points in the set
    returning a boolean masked matrix with the values that are constrained.
    """

    # preallocate a matrix to analyze out-of-bound points with 'points' shape
    # for the low limit
    boolMatLo = np.zeros((points.shape))
    # for the high limit
    boolMatHi = np.zeros((points.shape))

    # get the points that are valid under the constraints
    for i in range(Nvar):
        # upper limit comparison
        # lower or equal to the high limit
        if compMode[i][0] == 'leq':
            boolMatHi[:,i] = np.logical_or(points[:,i] < var_high[i],
                                         points[:,i] == var_high[i])
        # lower to the high specified limit
        elif compMode[i][0] == 'less':
            boolMatHi[:,i] = np.logical_or(points[:,i] < var_high[i])
        # strictly equal to the high specified limit (be careful!)
        elif compMode[i][0] == 'eq':
            boolMatHi[:,i] = np.logical_or(points[:,i] == var_low[i])
        # error if specified differently
        else:
            raise RuntimeError('Bad comparison mode matrix')

        # lower limit comparison
        # greater or equal to the lower limit
        if compMode[i][1] == 'geq':
            boolMatLo[:,i] = np.logical_or(points[:,i] > var_low[i],
                                         points[:,i] == var_low[i])
        # greater than the high limit
        elif compMode[i][1] == 'greater':
            boolMatLo[:,i] = np.logical_or(points[:,i] > var_low[i])
        # strictly equal to the high specified limit (be careful!)
        elif compMode[i][1] == 'eq':
            boolMatLo[:,i] = np.logical_or(points[:,i] == var_low[i])
        # error if specified differently
        else:
            raise RuntimeError('Bad comparison mode matrix')

    # combine both the low and high boolean matrices
    boolMat = np.logical_and(boolMatHi,boolMatLo)

    # once all the comparisons are made, the output should be an AND array where
    # all the conditions are met by each one of the individuals
    return np.logical_not(np.logical_and.reduce((boolMat.T)))
