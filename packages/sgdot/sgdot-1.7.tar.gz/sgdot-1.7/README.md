### SG-DOT

§SGDOT is a Package created to help design and optimize the network
topology for swarm-grids. It uses satellite imagery of villages to be
electrified and enables designing and optimizing a grid with a tree-star
configuration. It has been created in 2020 by François Nzale for a
collaboration project with Power-Blox in the frame of his Master Thesis
at ETH Zurich.

The grids module containes the Grid class. A grid essentially contains two
DataFrames representing the nodes and the links composing the network.
The nodes represent houses to be connected to the grid and links represent
wires connecting pairs of houses together. There is a price associated with
each link and node. The price of a Grid is the sum of the prices of each
nodes and links.

The tools sub-package contains the **optimization, visualization, io** and **plot** modules.

- The **optimization** modules encapsulates functions that can be used to optimize the grid design to minimize the Grid's price.
- The **io** module contains the functions to be used to export and import a Grid.
- The **plot** module enables to display the grid object in a 2D plot as well as displaying the plot of the results of the optimizations
