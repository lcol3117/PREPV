import PREPV as PREPV, random as rnd, math as math
import matplotlib.pyplot as plt
agentmodel = PREPV.PREPV_agent(2, 3)
def realLearnStep():
  policy = agentmodel.selectPolicy()
  performance = evaluatePolicy(policy)
  agentmodel.updateQTable(policy, performance)
  print("Agent tried policy {} with result {}. ".format(policy, performance))
  return [policy, performance]
def evaluatePolicy(policy):
  realmax = [0.7, 0.7]
  dist = getL2NDist(realmax, policy)
  initial = (2 - dist) + 1
  otherdist = getL2NDist([0.2,0.2], policy)
  otherinitial = 2 - dist
  if dist < otherdist:
    return initial
  else:
    return otherinitial
def getL2NDist(a,b):
  sumd = 0
  for i in range(len(a)):
    sumd += (a[i] - b[i]) ** 2
  return math.sqrt(sumd)
def pureExplorationStep():
  policy = [ rnd.random() for _ in range(2)]
  performance = evaluatePolicy(policy)
  agentmodel.updateQTable(policy, performance)
  print("Agent explored policy {} with result {}. ".format(policy, performance))
def realLearning():
  for _ in range(1):
    pureExplorationStep()
  notdone = True
  cnt = 1
  while notdone:
    result = realLearnStep()
    try:
      notdone = agentmodel.prev_epsilon < 0.95
      print("NOT DONE" if notdone else "DONE")
    except TypeError:
      notdone = True
    print("{} steps have passed. ".format(cnt))
    cnt += 1
  top = list(reversed(sorted(agentmodel.accdata, key = lambda x : x[1])))[0]
  [policy, performance] = top
  print("==============DONE==============")
  print("The agent decided on policy {}. ".format(policy))
  print("This policy had performance {}. ".format(performance))
  toplot = [ i[0] for i in agentmodel.accdata] + [[0,0],[0,1],[1,0],[1,1]]
  plt.scatter([ i[0] for i in toplot ],[ i[1] for i in toplot ])
  plt.show()
