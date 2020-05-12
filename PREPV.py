import random as rnd, math as math, functools as ft
class PREPV_agent:
  def __init__(self, dims, mip):
    self.dims = dims
    self.accdata = []
    self.old_accdata = []
    self.usedregions = []
    self.nsteps = 0
    self.prev_epsilon = None
    self.epsilonlimit = None
    self.mip = mip
    self.j = 3
  def updateQTable(self, policy, performance):
    self.old_accdata = self.accdata[:]
    self.accdata.append([policy, performance])
  def selectPolicy(self):
    print("I (Agent) am selecting a policy. ")
    self.nsteps += 1
    epsilon = self.calculateEpsilon()
    print("Epsilon is {}. ".format(epsilon))
    selectedregion = self.selectRegion(epsilon)
    print("I chose region {}. ".format(selectedregion))
    selectedpoint = self.randomPoint()
    print("I selected point {} initially. ".format(selectedpoint))
    initialvector = self.calculateRectVector(selectedpoint, selectedregion)
    print("Local max is {} relative to my inital point. ".format(initialvector))
    newvector = self.epsilonModifyMagnitude(initialvector, epsilon)
    print("Modified vector is {}. ".format(newvector))
    respoint = self.vectorSum(newvector, selectedpoint)
    return respoint
  def calculateEpsilon(self):
    k = 0.5
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
      if qtablemax > old_qtablemax:
        res = (qtablemax / self.mip) ** (1 / k)
      else:
        if self.prev_epsilon > (1 - (1 / 8)):
          self.epsilonlimit = 1
        res = (self.epsilonlimit * (self.nsteps + k)) / ((self.nsteps + k) + k)
    except IndexError:
      res = 0
    self.prev_epsilon = res
    self.epsilonlimit = 1 - ((1 - res) / 2)
    print("Set prev_epsilon to {}. ".format(self.prev_epsilon.__repr__()))
    return res
  def selectRegion(self, epsilon):
    e2 = epsilon / 2
    ls = self.accdata[:]
    ranking = sorted(ls, key = lambda x : x[1])[:]
    r = list(reversed(ranking))[:]
    for i in range(len(ranking)-1):
      if rnd.random() < e2:
        tmp = r[i+1][:]
        r[i+1] = r[i][:]
        r[i] = tmp[:]
    newranking = r[:]
    newtop = newranking[0]
    self.usedregions.append(newtop)
    return newtop
  def randomPoint(self):
    rndpt = map(
      lambda _ : rnd.random(),
      range(self.dims)
    )
    return list(rndpt)
  def calculateRectVector(self, point, region):
    regionpt = region[0]
    r = list(range(self.dims))[:]
    deltas = list(map(lambda i : (regionpt[i] - point[i]), r))
    return deltas
  def epsilonModifyMagnitude(self, oldvector, epsilon):
    newvector = list(map(lambda x : x * (epsilon ** self.j), oldvector))
    return newvector
  def vectorSum(self, a, b):
    r = list(range(self.dims))[:]
    return list(map(lambda i : (a[i] + b[i]), r))
  def getL2NDist(self, a, b):
    sumd = ft.reduce(
      lambda a,x : a + ((x[0] - x[1]) ** 2),
      list(zip(a, b)),
      0
    )
    return math.sqrt(sumd)
