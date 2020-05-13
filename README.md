# PREPV
PREPV reinforcment learning (Probabilistic Regional Epsilon Proportional Vector)

***[CURRENTLY UNDER DEVELOPMENT]***

[![Run on Repl.it](https://repl.it/badge/github/lcol3117/PREPV)](https://repl.it/github/lcol3117/PREPV)

**PREPV hyperparameters: MIP and j. j = 4 should work fine. **

MIP is the maximum impossible performance

However, if something is really messed up change j to something other than 4. 

Higher j -> More spread out

Lower j -> Less spread out

**Use: **

`PREPV_agent(dims, mip, j = 4)`

MIP = Maximum Impossible Performance

**PREPV algorithm: **

First calculate epsilon as the max(Q) / MIP.

Calculate a list of all points in the Q-table ranked by performance. 

Working upwards the system has an epsilon / 2 probability of swapping two adjacent elements. 

The top one is the selected region point. 

Then, select a random point. This is the initial selected point.

Next, calculate the vector from the initial selected point to the selected region point. 

Multiply this vector by the scalar epsilon^j.

Sum the vector of the initial selected point with this new vector. 

This new vector corresponds to the point in policy space that the agent is selecting. 

**PREPV example: **

In the example from *rlearn_tst.py*, the reward is a function of policy s.t. there is a local max at \[0.2,0.2\] in policy space, and a global maximum at \[0.7,0.7\]. 

When the agent initially believes that the local max is ideal, it eventually selects a different point to use as its region, and discovers the global max, which it stays nearby. 
