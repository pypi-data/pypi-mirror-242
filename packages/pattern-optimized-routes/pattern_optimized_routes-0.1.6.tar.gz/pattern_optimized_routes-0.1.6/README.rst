Multilevel Expected Road Usage
==============================

This library was developed during the research of my master's degree thesis. 
It consists of an alternative routing strategy based on road usage patterns. 
I called it MERU, it is designed to avoid popular roads, increase path diversity, 
and reduce CO2 emissions in urban mobility through the application of a multilevel penalization schema. 
The package includes also ways to test, simulate, and reproduce results on a mobility demand with all the available state-of-the-art algorithms.

Getting started
---------------

This library makes extensive use of
`SUMO <https://sumo.dlr.de/docs/Installing/index.html>`__, 
`iGraph <https://python.igraph.org/en/stable/>`__, and another
library I worked to develop called `routing_lib <https://github.com/lwdovico/routing-lib>`__.

Pypi
~~~~

To install this framework you can just open a terminal and then you can input a pip command:

::

   pip install pattern-optimized-routes

Import the library
~~~~~~~~~~~~~~~~~~

On Python, you can import the library by doing:

::

   import meru

There are 5 modules available:

-  multilevel.py contains the code of the algorithm and various utilities to
   make it work
-  baselines.py contains a class to run other algorithms from
   `routing_lib <https://github.com/lwdovico/routing-lib>`__
-  extract_measures.py allows the extraction of a set of useful
   quantitative and qualitative measures out of the raw paths
-  simulate.py contains a few functions to start a
   `SUMO <https://sumo.dlr.de/docs/Installing/index.html>`__ simulation
-  testing.py contains the function to run the simulation with
   customizable settings (the default parameters are those of my
   research)

Loading a Road Network
~~~~~~~~~~~~~~~~~~~~~~

The network files that are meant to work with this library must have been downloaded through OSMWebWizard
Once a city road network like "road_network.net.xml" file is available you can load it this way:

::

   from routing_lib import from_sumo_to_igraph_network
   road_network = sumolib.net.readNet("road_network.net.xml")
   G = from_sumo_to_igraph_network(road_network)

What these lines do is basically importing a network through the SUMO library and translate it to an iGraph network.

Multilevel Module
-----------------

It is easy to instantiate our model. The first step is to declare how many k layers (or output paths) should be produced.
Then we must tell the model which are our weights, traveltime is generally used as weight in this context, 
but also edge "length" is avaialable.

::

   from meru.multilevel import MultiLevelModel

   meru_model = MultiLevelModel(G, k = 3, attribute = "traveltime")

Then you must tune the model. It is possible to provide specific values to test during the instantiation, 
otherwise the values I used in my thesis are going to be tested.

::

   meru_model.parameter_selection(random_state = 42)

It should be noted that it is possible to specify a random state, so that during the generation of a temporary mobility demand 
a seed is applied to make the parameter selection reproducible. It is also possible to provide a specific number of vehicles to use
by using the parameter "n_vehicles" which is defaulted to allow the automatic selection.

After tuning it is necessary to fit the model since the tuning makes available only the first layer for testing the log-normality distribution of values. 
During the fitting process are generated k levels of "expected road usage" values that were cumulatively computed to get a set of values that indicates precisely the expected popularity of the roads, 
without making secondary roads more popular during the process. For reproducibility purposes it is again suggested to use a random state. The weights of the model become available after the fitting process.

::

   meru_model.fit(random_state = 42)
   model_weights = meru_model.weights

By providing an origin and destination pair of edges, it is then easy to compute a path through:

::

   output_paths = meru_model.predict(origin, destination)

The output_paths are a list of dictionaries, each containing the "edges" ID, the iGraph indexes and some simple metrics.

The module contains also the following relevant utilities:

-   get_map_shape(igraph.Graph): allows for the extraction of the bounding box of the road network to a GeoDataFrame
-   get_edges_to_tile(igraph.Graph, tile_shape, tile_side_meters): make use of scikitmobility to compute a tesselation and assigning each edge to a tile of the tesselation
-   get_source_kroad_dist(igraph.Graph, list_of_paths, edges_to_tile, mds_threshold = 0.8): extract the distribution of k-road values from a list of paths by providing an edges to tile map and a threshold to define the major driver sources.
-   get_kroad_levels(igraph.Graph, n_layers, attribute, edges_to_tile, n_expected_vehicles): compute the kroad levels by using a custom defined number of layers and number of expected vehicles
-   get_kroad_maps(G, edges_weight_layers, color = 'blue', tiles='cartodbpositron', zoom_start=13): generate a list of maps to visualize the popularity of the edges for each layer (edges_weight_layers is a dictionary having the layer number mapped to the edge weights, it is the output of the previous function)
-   multilevel_edge_penalization(igraph.Graph, from_edge, to_edge, k, attribute, kroad_levels): it is possible to run the algorithm by giving the kroad_levels (a dictionary mapping layers to edge weights)
-   balance_test(kroad_levels, lvl = 1, threshold = 0.0): function used to test the distribution log-normality according to the principle of distance threshold between Q1 and the minimum value of the distribution (threshold should be 0 or at most 0.2, going over allows for unsuitable distribution to be chosen)

Baselines Module
----------------

This module implement only the class that makes the baselines available, it is required the knowled of the parameters to be provided to the class, but if not known the error message would tell the missing parameter.
It can be instantiated as it follows:

::
   
   from meru.baselines import BaselineModel
   baseline_model = BaselineModel(algorithm_tag, G, k = 3, attribute = 'traveltime', **parameters)

The algorithm available to be input as algorithm_tag are:

-   NR: It provides the shortest path according to Dijkstra
-   KSP: It provides k-shortest path using Yen's algorithm
-   KD: It provides k-disjoint paths
-   KML: It provides k-shortest paths with minimum collective length. Parameter "theta" is the maximum similarity allowed.
-   KMO: It provides k-shortest paths with minimum overlapping. Parameter "theta" is the maximum similarity allowed.
-   PLAT: It provides the result of the plateau algorithm. Parameter "epsilon" is the maximum length allowed for a path.
-   PP: It provides the results of a constant penalization algorithm (IPM). Parameter "p" is the constant penalization value to apply to the weights.
-   GR: It provides the results of a random graph weight update at each iteration. Parameter "delta" is the standard deviation to move the weights from their original value, "tau" is the minimum value in case of negative weights.
-   PR: It provides the results of a random path weight update at each iteration. Parameter "delta" is the standard deviation to move the weights from their original value, "tau" is the minimum value in case of negative weights.
-   DR: It provides the result of a noise factor applied on the path at each iteration. Parameter "w" indicates the noise.
-   KMD: It provides the result of the k-most diverse nearest shortest paths. Parameter "epsilon" stands for the maximum length allowed for a path.

Extract Measure Module
----------------------

It contains various functions to extract measures, the main function is "get_resulting_paths_and_measures" which by providing:

- The road network
- A mobility demand
- The list of suggested paths for each OD-pair of the mobility demand 
- The edge_weights of MERU
- Optionally the traffic assignment criterion function (defaulted to random assignment (using numpy.random.choice), hence also a random_state parameter can be set)

Computes all the measures used in our study. It can be easily invoked this way:

::
   from meru.extract_measures import get_resulting_paths_and_measures

   get_resulting_paths_and_measures(road_network, 
                                    mobility_demand, 
                                    suggested_paths,
                                    meru_weights)

The output is a dictionary mapping the assigned paths in "paths", and the measures in "measures".


Simulate Module
---------------

This module contains two fundamental functions, one is "save_sumo_routes" which just store away the routes in a format readable by SUMO.

The most important function is "simulate_sumo_paths", which launches a simulation and store the resulting measure into the input dictionary.

To run a simulation one just need to:

::

   from meru.simulate import simulate_sumo_paths

   simulate_sumo_paths(dictionary_of_measures, road_network_path, routes_file_path)

The dictionary of measures contains the place to store the simulation measures (CO2, simulation time and number of collisions). 
The main intent of this function is to update a dictionary of theoretical measures generated through the extract measure module.

Testing Module
--------------

This module is expected to be used only to reproduce results for a research framework. There are two core functions, which basically provide a wrapper for the entire pipeline of testing the proposal parameters, by running "pipeline_test_reproducible_kdistributions", and the pipeline to test against a set of baseline algorithms and parameters. It follows a brief discussion of the most ambigous parameters.

::

   from meru.testing import pipeline_test_reproducible_kdistributions

   pipeline_test_reproducible_kdistributions(road_network_path, results_output_folder, 
                                             mobility_demand_path, distributions_to_test,
                                             k = 3, attribute = 'traveltime', 
                                             experiment_per_rs = 10, 
                                             random_state = 42,
                                             sample = None)

This function launches a number of simulations equal to the number present in experiment_per_rs, it tests only meru, the main parameter to set is "distributions_to_test" which is a list of the number of vehicles to test, in our study we tested the following parameters:

::
   
   [200, 500, 1000, 2000, 3500, 5000, 7000, 12000, 15000, 17000, 20000, 30000, 50000, 75000, 100000, 200000]

Once the function ends it will store a csv file containing the resulting measures in the results_output_folder. It can be noticed also a sample of the mobility demand can be provided by inputting the value of OD pairs to be tested.

Similarly we have a corresponding function that tests for the algorithms. It can be invoked throguh:

::

   from meru.testing import pipeline_test_reproducible_kdistributions

   pipeline_test_reproducible_baselines(road_network_path, results_output_folder, 
                                        mobility_demand_path, algorithm_parameters,
                                        k = 3, attribute = 'traveltime', 
                                        experiment_per_rs = 10, 
                                        random_state = 42,
                                        sample = None)

The inner working of most parameters is identical to the previous function except for algorithm_parameters, that should be a dictionary containing the "algorithm_tag" mapped to a dictionary of parameters to test. Since the randomization algorithms require two parameters (even though one of them is ininfluential) we test all the possible combination provided. If in the future new parameters will be added with multiple parameters, the number of parameters to test should be provided carefully to avoid a combinatorial explosion.

The structure of algorithm_parameters is the following.

::

   algorithm_parameters = { 'NR': {},
                            'KSP': {},
                            'KD': {},
                            'PP': {'p': [0.05, 0.2, 0.3, 0.4, 0.5]},
                            'KMD': {'epsilon': [0.2, 0.3]},
                            'GR': {'delta': [0.2, 0.3, 0.4, 0.5], 'tau': [0.2]},
                            'KML': {'theta': [0.6, 0.7, 0.8]},
                            'PLAT': {'epsilon': [1.3, 2, 5, 15]}
                          }

If an algorithm is omitted it won't be tested, the same fo the parameters. An error would be raised if an algorithm requiring one of the parameters is provided without the parameter key in this dictionary.