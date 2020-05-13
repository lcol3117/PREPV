import random as rnd, math as math, functools as ft
class PREPV_agent:
  def __init__(self, dims, mip, j = 4):
    self.dims = dims
    self.accdata = []
    self.old_accdata = []
    self.usedregions = []
    self.nsteps = 0
    self.prev_epsilon = None
    self.mip = mip
    self.j = j
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
    newpoint = self.vectorSum(selectedpoint, newvector)
    print("New vector is {}. ".format(newvector))
    region_min = self.selectRegionMin(epsilon)
    print("I chose minimum region {}. ".format(region_min))
    vec_a = self.calculateRectVector(region_min, newpoint)
    vec_delta_b = self.calculateAvoidanceVector(vec_a, epsilon)
    print("Avoidance vector is {}.  ".format(vec_delta_b))
    chosenvector = self.vectorSum(region_min, vec_delta_b)
    return chosenvector
  def calculateEpsilon(self):
    try: 
      qtablemax = ft.reduce(
        lambda a,x : x[1] if x[1] > a else a,
        self.accdata,
        float("-inf")
      )
      res = (qtablemax / self.mip)
      print("Initial epsilon is {}. ".format(res))
      if res >= 0.8:
        res = 0.8 + (((5 * (res - 0.8)) ** self.j) / 5)
    except IndexError:
      res = 0
    self.prev_epsilon = res
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
    newtop = newranking[0][0]
    self.usedregions.append(newtop)
    return newtop
  def selectRegionMin(self, epsilon):
    e2 = epsilon / 2
    ls = self.accdata[:]
    ranking = sorted(ls, key = lambda x : 0 - x[1])[:]
    r = list(reversed(ranking))[:]
    for i in range(len(ranking)-1):
      if rnd.random() < e2:
        tmp = r[i+1][:]
        r[i+1] = r[i][:]
        r[i] = tmp[:]
    newranking = r[:]
    newtop = newranking[0][0]
    return newtop
  def randomPoint(self):
    rndpt = map(
      lambda _ : rnd.random(),
      range(self.dims)
    )
    return list(rndpt)
  def calculateRectVector(self, point, region):
    regionpt = region[:]
    r = list(range(self.dims))[:]
    deltas = list(map(lambda i : (regionpt[i] - point[i]), r))
    return deltas
  def epsilonModifyMagnitude(self, oldvector, epsilon):
    newvector = list(map(lambda x : x * (epsilon ** self.j), oldvector))
    return newvector
  def calculateAvoidanceVector(self, vec_a, epsilon):
    v_delta_b_0 = list(map(lambda x : x * ((epsilon ** (self.j)) / 4), vec_a))
    return self.vectorSum(vec_a, v_delta_b_0)
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
