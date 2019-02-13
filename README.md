# Optimization of a snow pile case with Genetic Algorithms
During my exchange last year at the University of Vermont, the assignment of the course *ME 144 - Heat Transfer* consisted on the design and analysis of a snow pile to preserve snow during the summer days. This is already being done in some places of the world, e.g.:
* Kathmandu surroundings, Nepal:
![Groomer working](https://www.lugaresdenieve.com/sites/default/files/snow-farming-ruka.jpg)
* Kitzbühel, Tyrol, Austria
![Snow insulation](https://media.skigebiete-test.de/images/ecu/content/c_blogarticle/snowfarming-recycled-heaven-for-skiing_n159699-43795-2_l.jpg)
![SnowPile size](https://media.skigebiete-test.de/images/ecu/content/c_blogarticle/snowfarming-recycled-heaven-for-skiing_n159699-43813-1_l.jpg)

Within these places, it can be seen that snow is piled up and covered with some insulation to prevent the snow from melting. This repository consists of three differentiated parts, that should be read in the following order for the explanation to be consistent:

## 1. [<tt> snowPile_notebook.ipynb</tt>](https://github.com/jlobatop/snowPile/blob/master/snowPile_notebook.ipynb)

In this notebook, the basic case is presented. The analysis is performed in a trapezoidal prism instead of a truncated pyramid as proposed in the original assignment for simplicity purposes as the optimization of a more complex case will require more computational power:

![truncatedVSprism](https://raw.githubusercontent.com/jlobatop/snowPile/master/images/truncatedVSprism.png)

In the left, the truncated pyramid can be seen, having in the right the trapezoidal prism. In the truncated pyramid the value of the angle β is another variable to the case. However, for simplicity, this value was chosen to be zero (having a perpendicular front and rear faces). Although all edges are labeled, the variables of the snow pile are:
* Length of the prism (L or l)
* Height of the trapezoid (H)
* Trapezoid base (b)
* Trapezoid angle (alpha), assuming that the trapezoid is symmetric

As described in the notebook, to have a fair comparison a robust optimization process, the value of the volume of snow was fixed. The other value that was assumed to be fixed is the snow inner temperature (-10ºC), having that the other parameters vary.

In the notebook, the heat circuit is shown as well as each one of the computations of temperature, heat or different coefficients required to have the heat loss per unit area of each one of the faces: the 5 surfaces that have direct contact with the air will have a heat transfer rate while the base of the prism which is in contact with the ground has another different heat transfer.

## 2. [<tt> testGA</tt> folder](https://github.com/jlobatop/snowPile/tree/master/testGA)

The code for the Genetic Algorithm optimization was extracted from my previous project dealing with [multiobjective optimization](https://github.com/jlobatop/GA-CFD-MO), which was based on the Non-dominated Sorting Genetic Algorithm II (NSGA-II) by K. Deb et al. The code was adapted to deal with 7 search space variables (instead of the 2 chosen for the CFD optimization, given that in this case, the evaluation of a generation is way cheaper than that of a CFD simulation). In order to check whether it was working properly and all necessary things had been modified.

To check that, the Schaffer function N.1 was taken from [here](https://en.wikipedia.org/wiki/Test_functions_for_optimization) and modified to adapt it to seven variables. Then the case was run with the required bash scripts and the results were stored in each corresponding generation folder. In the [<tt> testGA.ipynb</tt>](https://github.com/jlobatop/snowPile/blob/master/testGA/testGA.ipynb), the reading of the value of those individuals is performed, getting the function space with the well defined Pareto front.

In the notebook (**not available in the online render**) file, there is an animation that shows how the individuals evolve towards the Pareto front, proving that the algorithm is working. The final result can be seen below:

![testGAinAction](https://raw.githubusercontent.com/jlobatop/snowPile/master/images/testGA.png)

Now that the case has been defined and the optimization GA has been checked, it is time to combine both!

## 3. [<tt> snowPileGA</tt> folder](https://github.com/jlobatop/snowPile/tree/master/snowPileGA)
In the [<tt> snowPile_notebook</tt>](https://github.com/jlobatop/snowPile/blob/master/snowPile_notebook.ipynb) notebook, some of the optimization variables have been discussed, such as the angle, base length or height of the trapezoidal prism. However, when including the heat analysis, there are some variables that will depend on the choice of the insulator layer (such as the material properties and also its dimensions). Therefore, the whole search space is based in:
* trapezoid angle (alpha) in [20º ,60º]
* trapezoid base (b) in [0.2m, 10m]
* trapezoid height (H) in [0.5m, 5m]
* insulator thickness (tins) in [0.001m, 0.1m]
* insulator heat coefficient (kins) in [0.05W/(m·K), 0.2W/(m·K)]
* insulator emissivity (Eins) in [0, 1]
* insulator absorptivity (Ains) in [0, 1]

The ground conditions and weather conditions were fixed for all possible snow piles, given that those conditions can't be modified to achieve more efficient storage. The function space variables could be a wide variety of different outputs of the computations, but the selected ones were:
* Sum of total heat: the more heat loss, the more probabilities of snow melting
* Air surface of the snow pile: which is, indeed, similar to the cost of insulating the whole pile

These variables were included in the <tt> fitness.py</tt> file, modifying also the <tt> problemSetup.py</tt> with the ranges of the search space. The optimization process consisted on 200 generations with 128 individuals in each one (computing for each one all the temperatures and heats in the initial [<tt> snowPile_notebook</tt>](https://github.com/jlobatop/snowPile/blob/master/snowPile_notebook.ipynb), accounting for 25600 evaluations). As before, the results were stored in its generation folder and then analyzed with the [<tt> snowPileGA.ipynb</tt>](https://github.com/jlobatop/snowPile/blob/master/snowPileGA/snowPileGA.ipynb) notebook. Opposed to what was expected (as it can be denoted by the use of a multiobjective GA), there is not a clear Pareto front, which is good news! There is an optimum point that has both a small total heat transfer at the same time as a reduced surface in contact with the air (minimizing insulation costs).

![pileGAresults](https://raw.githubusercontent.com/jlobatop/snowPile/master/images/pileGA.png)

This solution may seem a little disapointing compared with the fancy function space of the Schaffer function N.1. Moreover, in real life situations, there is almost never a true only optimum point. Therefore, it can be stated that either the model has been oversimplified or the objective functions were not properly chosen.

## Possible upgrades
Some possible developments to solve the different issues encountered and mentioned above are listed:
* Include the computation of the Reynolds number for each individual separately, as some sample Reynolds number was selected (via the convective heat transfer coefficient) for all individuals, regardless their actual dimensions to reduce the computational time of the genetic algorithm
* Using a more realistic shape, such as a truncated pyramid with the use of the angle β as proposed in the original assignment
* Create a freezing model that reduces (or increases) the volume of the snow pile depending on the direction of the heat. This will increase the computation effort and complexity of the model
* Given that most of the information is available on a daily basis, a day-to-day analysis could be performed together with the freezing model to get an evolution of the snow pile volume
* Sides will generate shadows and sun will not hit all surfaces perpendicularly but with some angle that will vary the influence of the radiation heat transfer. High potential if combined with daily analysis and freezing model
