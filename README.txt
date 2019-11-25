README for Term Project 2 Graph Solver
---------------------------------------------------------

Contributors:
Keiser Ruiz
Taleen Sarkissian
----------------------------------------------------------

Summary:
This is the source code for a graph problem solver from
the EECS 118 class of UCI. The graph problem is as stated.

find s where is_path(s, A, B) and 
no_nodes(s, t) and 
total_weight(s, u) and 
t=C and u>D.

When starting to execute the program, the user will pass
the name of an input csv file. Each row in the csv file 
will contain node 1, node 2, weight, and color. For example:

1, 2, 0.5, green
3, 4, 0.7, green
1, 4, 0.5, red

Based on the input csv filve, the graph solver program will
find all path solutions fulfilling the predicates where the 
set of edges, s, is a path between node A and node B and the 
number of nodes in s is equal to C and the total weight of
s is greater than D. A, B, C, and D are all defined by a user.

Once all paths that fulfill the predicates are found, the set 
of edges of these paths are written into an output csv file 
like so:

path_1
1, 2
3, 4
path_2
2, 3
3, 4
----------------------------------------------------------------

Requirements:
Python3.6 or greater
networkx
----------------------------------------------------------------

How To Execute:
Open a terminal and redirect to the directory for this project.
Execute the following line:

$python main.py input.csv

You can substitute "input.csv" with the name of you own input csv
file that you want to red from. Next, the program will ask you to 
enter a set of input for the starting node, ending node, the exact
number of nodes a path solution shoudld have, the minimum (exclusive) 
weight a path should have, and the name of the output csv file.  

