import random as rnd, math as math, functools as ft
class PREPV_agent:
  def __init__(self, dims):
    self.dims = dims
    self.accdata = []
    self.old_accdata = []
    self.usedregions = []
    self.nsteps = 0
    self.old_epsilon = None
  def updateQTable(self, policy, performance):
    self.old_accdata = self.accdata[:]
    self.accdata.append([policy, performance])
  def selectPolicy(self):
    print("I (Agent) am selecting a policy. ")
    #print("My Q-Table is this: ")
    #print(self.accdata)
    self.nsteps += 1
    epsilon = self.calculateEpsilon()
    print("Epsilon is {}. ".format(epsilon))
    selectedregion = self.selectRegion(epsilon)
    print("I chose region {}. ".format(selectedregion))
    selectedpoint = self.randomWithinRegion(selectedregion)
    print("I selected point {} initially. ".format(selectedpoint))
    initialvector = self.calculateRectVector(selectedpoint, selectedregion)
    print("Local max is {} relative to my inital point. ".format(initialvector))
    newvector = self.epsilonModifyMagnitude(initialvector, epsilon)
    print("Modified vector is {}. ".format(newvector))
    respoint = self.vectorSum(newvector, selectedpoint)
    return respoint
  def calculateEpsilon(self):
    try: 
      qtablemax = ft.reduce(
        lambda a,x : x[1] if x[1] > a else a,
        self.accdata,
        float("-inf")
      )
      old_qtablemax = ft.reduce(
        lambda a,x : x[1] if x[1] > a else a,
        self.old_accdata,
        float("-inf")
      )
    except IndexError:
      pass
    if len(self.old_accdata) > 1:
      limit = abs(1 - ((qtablemax / old_qtablemax) * (1 - self.prev_epsilon)))
      res = limit - ((1/2) ** self.nsteps)
    else:
      if len(self.accdata) == 0:
        res = 0
      elif (len(self.accdata) == 1) or (len(self.accdata) == 2):
        res = 1 / 3
      else:
        res = (old_qtablemax / qtablemax) * 2
    self.prev_epsilon = res
    return res
  def selectRegion(self, epsilon):
    e2 = epsilon / 2
    ls = self.accdata[:]
    ranking = sorted(ls, key = lambda x : x[1])[:]
    #print("[selectRegion] ranking is: ")
    #print(ranking)
    r = list(reversed(ranking))[:]
    for i in range(len(ranking)-1):
      if rnd.random() < e2:
        tmp = r[i+1][:]
        r[i+1] = r[i][:]
        r[i] = tmp[:]
    newranking = r[:] #list(reversed(r))[:]
    #print("[selectRegion] newranking is: ")
    #print(newranking)
    newtop = newranking[0]
    self.usedregions.append(newtop)
    return newtop
  def randomWithinRegion(self, region):
    while True:
      rndpt = [ rnd.random() for _ in range(self.dims) ]
      usabledata = list([ i[0] for i in (self.usedregions) ] + [region[0]])
      #print("[randomWithinRegion] usabledata is: ")
      #print(list(usabledata))
      dists = list(map(lambda x : self.getL2NDist(x, rndpt), usabledata))
      #print("[randomWithinRegion] dists are: ")
      #print(dists)
      mindistpt = usabledata[dists.index(min(dists))]
      #print("[randomWithinRegion] mindistpt is: ")
      #print(mindistpt)
      #print("Region Point is: ")
      #print(region[0])
      if mindistpt == region[0]:
        break
    return rndpt
  def calculateRectVector(self, point, region):
    regionpt = region[0]
    r = [ i for i in range(self.dims) ][:]
    deltas = list(map(lambda i : (regionpt[i] - point[i]), r))
    return deltas
  def epsilonModifyMagnitude(self, oldvector, epsilon):
    beta = epsilon #1-epsilon
    newvector = list(map(lambda x : x * beta, oldvector))
    return newvector
  def vectorSum(self, a, b):
    r = [ i for i in range(self.dims) ][:]
    return list(map(lambda i : (a[i] + b[i]), r))
  def getL2NDist(self, a, b):
    sumd = 0
    for i in range(len(a)):
      sumd += (a[i] - b[i]) ** 2
    return math.sqrt(sumd)