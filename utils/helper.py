import numpy as np

def fractionRound(x, base):
    return base * round(x/base)

def fibonnaci(low, high, fraction, level, beta=[1, 0.786, 0.618, 0.5, 0.382, 0.236, 0]):
  selisih = high - low
  ratio = [1, 0.786, 0.618, 0.5, 0.382, 0.236, 0]
  levelOne = list(map(lambda x: fractionRound(low + (selisih * x), fraction), ratio))
  levelTwo = []
  if level == "alpha":
    return np.unique(levelOne)

  elif level == "beta":
    for i, label in enumerate(levelOne):
      if i < len(levelOne)-1:
        selisihLevelTwo = label - levelOne[i+1]
        x = list(map(lambda x: fractionRound(levelOne[i+1] + (selisihLevelTwo * x), fraction), beta))
        levelTwo.append(x)
    return np.unique(np.array(levelTwo).flatten()) 

def checking_fibo(data, vocab):
  low_pos = []
  high_pos = []
  for v in vocab:
    if data > v:
      low_pos.append(v)
    elif data < v:
      high_pos.append(v)
      break
  try:
    return [low_pos[-1], high_pos[0]]
  except:
    return [0, 0]

def HelperLine(value):
  if (value <= 200):
    return (1, 50, 200)
  elif (200 < value <= 500):
    return (2, 200, 500)
  elif(500 < value <= 2000):
    return (5, 500, 2000)
  elif(2000 < value <= 5000):
    return (10, 2000, 5000)
  else:
    return (25, 5000, 10000)

def Line(min, max):
  fmnMin, vmnMin, vmxMin = HelperLine(min)
  fmnMax, vmnMax, vmxMax = HelperLine(max)
  fiboMinAlpha = fibonnaci(vmnMin, vmxMin, fmnMin, "alpha")
  fiboMaxAlpha = fibonnaci(vmnMax, vmxMax, fmnMax, "alpha")
  fiboMinBeta = fibonnaci(vmnMin, vmxMin, fmnMin, "beta", beta=[0.618, 0.382])
  fiboMaxBeta = fibonnaci(vmnMax, vmxMax, fmnMax, "beta", beta=[0.618, 0.382])
  Alpha = np.unique(np.concatenate((fiboMinAlpha, fiboMaxAlpha), axis=0))
  Beta = np.unique(np.concatenate((fiboMinBeta, fiboMaxBeta), axis=0))
  return (Alpha, Beta)

fibo1 = fibonnaci(50, 200, 1, "alpha")
fibo2 = fibonnaci(200, 500, 2, "alpha")
fibo3 = fibonnaci(500, 2000, 5, "alpha")
fibo4 = fibonnaci(2000, 5000, 10, "alpha")
fibo5 = fibonnaci(5000, 10000, 25, "alpha")
fibo6 = fibonnaci(10000, 20000, 25, "alpha")
fibo7 = fibonnaci(20000, 40000, 25, "alpha")
Alpha = np.unique(np.concatenate((fibo1, fibo2, fibo3, fibo4, fibo5, fibo6, fibo7), axis=0))
  
fibo1 = fibonnaci(50, 200, 1, "beta", beta=[0.618, 0.382])
fibo2 = fibonnaci(200, 500, 2, "beta", beta=[0.618, 0.382])
fibo3 = fibonnaci(500, 2000, 5, "beta", beta=[0.618, 0.382])
fibo4 = fibonnaci(2000, 5000, 10, "beta", beta=[0.618, 0.382])
fibo5 = fibonnaci(5000, 10000, 25, "beta", beta=[0.618, 0.382])
fibo6 = fibonnaci(10000, 20000, 25, "beta", beta=[0.618, 0.382])
fibo7 = fibonnaci(20000, 40000, 25, "beta", beta=[0.618, 0.382])
Beta = np.unique(np.concatenate((fibo1, fibo2, fibo3, fibo4, fibo5, fibo6, fibo7), axis=0))

def standardeviation(data, span):
  return data.rolling(span).std()
  
def simplemovingavarage(data, span):
  return data.rolling(span).mean()
  
def exponentialmovingaverage(data, period):
  return data.ewm(span=period).mean()
  
def bollingerband(data, multiplier, spanma, spanstd):
  sma = simplemovingavarage(data, spanma)
  std = standardeviation(data, spanstd)
  up = sma + (std*multiplier)
  down = sma - (std*multiplier)
  return [up, down, sma]
  
def stochastic(data, kspan, dspan):
  H14 = data.rolling(kspan).max()
  L14 = data.rolling(dspan).min()
  k = 100 * (data - L14)/(H14 - L14)
  d = k.rolling(dspan).mean()
  return [k,d]
  
def volumeoscillator(data, shortspan, longspan):
  shortsma = simplemovingavarage(data, shortspan)
  longsma = simplemovingavarage(data, longspan)
  return ((shortsma-longsma)/longsma)*100
  
#===RSI====
  
def percentageprofit(data):
  profit = data
  profit['Diff'] = profit.loc[:,'Close'].diff()
  profit['profit'] = profit.loc[profit['Diff'].gt(0)
                            ,['Diff']].abs()
  profit.loc[:, 'profit'].fillna(0, inplace=True)
  percentageProfit = (profit.loc[:, 'profit'] / profit.loc[:, 'Close']) * 100
  return percentageProfit

def percentageloss(data):
  loss = data
  loss['Diff'] = loss.loc[:,'Close'].diff()
  loss['loss'] = loss.loc[loss['Diff'].lt(0)
                            ,['Diff']].abs()
  loss.loc[:, 'loss'].fillna(0, inplace=True)
  percentageLoss = (loss.loc[:, 'loss'] / loss.loc[:, 'Close']) * 100
  return percentageLoss
  
def relativeStrenghIndex(data, span):
  pro = percentageprofit(data)
  los = percentageloss(data)
  rsi = 100 - (100/(1 + (pro.rolling(span).mean()/los.rolling(span).mean())))
  return rsi.round(1)
