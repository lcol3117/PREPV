# PREPV
PREPV reinforcment learning (Probabilistic Regional Epsilon Proportional Vector)

***[CURRENTLY UNDER DEVELOPMENT]***

**PREPV hyperparameters: MIP only. This is because of the IPL2 algorithm which makes me happy. **

**Use: **

`PREPV_agent(dims, mip)`

MIP = Maximum Impossible Performance

**PREPV algorithm: **

First calculate epsilon per the IPL2 algorithm, it is mostly math so see the code for how it works. It is in `PREPV_agent.calculateEpsilon`.

Calculate a list of all points in the Q-table ranked by performance. 

Working upwards the system has an epsilon / 2 probability of swapping two adjacent elements. 

The top one is the selected region point. 

Then, select a random point. This is the initial selected point.

Next, calculate the vector from the initial selected point to the selected region point. 

Multiply this vector by the scalar epsilon^3.

Sum the vector of the initial selected point with this new vector. 

This new vector corresponds to the point in policy space that the agent is selecting. 

**PREPV example: **

In the example from *rlearn_tst.py*, the reward is a function of policy s.t. there is a local max at \[0.2,0.2\] in policy space, and a global maximum at \[0.7,0.7\]. 

When the agent initially believes that the local max is ideal, it eventually selects a different point to use as its region, and discovers the global max, which it stays nearby. 
