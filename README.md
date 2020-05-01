# PREPV
PREPV reinforcment learning (Probabilistic Regional Epsilon Proportional Vector)

***[CURRENTLY UNDER DEVELOPMENT]***

PREPV hyperparameters:

l: Number of steps to take, epsilon gradually decreases through this from 1 to 0. 

k: Used to control how sure the agent is of its area, if the graph shows it is too spread out, reduce k, if it is too clustered by a local min, increase k

{l, k}={20, 0.65} was used. It worked well with l > 15 and 0.25<k<2

PREPV algorithm:

First calculate epsilon s.t. it is linearly dicreasing from (0, 1) to (l, 0)

Calculate a list of all points in the Q-table ranked by performance. 

Working upwards the system has an epsilon / 2 probability of swapping two adjacent elements. 

The top one is the selected region point. 

Then, select a random point closer to this region point than all other previous region points. 

This is the initial selected point.

Next, calculate the vector from the initial selected point to the selected region point. 

Multiply this vector by the scalar epsilon^k.

Sum the vector of the initial selected point with this new vector. 

This new vector corresponds to the point in policy space that the agent is selecting. 
