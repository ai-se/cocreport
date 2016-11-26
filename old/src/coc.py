
_  = None;  Coc2tunings = [[
#              vlow  low   nom   high  vhigh  xhigh   
# scale factors:
'Flex',        5.07, 4.05, 3.04, 2.03, 1.01,    _],[
'Pmat',        7.80, 6.24, 4.68, 3.12, 1.56,    _],[
'Prec',        6.20, 4.96, 3.72, 2.48, 1.24,    _],[
'Resl',        7.07, 5.65, 4.24, 2.83, 1.41,    _],[
'Team',        5.48, 4.38, 3.29, 2.19, 1.01,    _],[
# effort multipliers:        
'acap',        1.42, 1.19, 1.00, 0.85, 0.71,    _],[
'aexp',        1.22, 1.10, 1.00, 0.88, 0.81,    _],[
'cplx',        0.73, 0.87, 1.00, 1.17, 1.34, 1.74],[
'data',           _, 0.90, 1.00, 1.14, 1.28,    _],[
'docu',        0.81, 0.91, 1.00, 1.11, 1.23,    _],[
'ltex',        1.20, 1.09, 1.00, 0.91, 0.84,    _],[
'pcap',        1.34, 1.15, 1.00, 0.88, 0.76,    _],[ 
'pcon',        1.29, 1.12, 1.00, 0.90, 0.81,    _],[
'plex',        1.19, 1.09, 1.00, 0.91, 0.85,    _],[ 
'pvol',           _, 0.87, 1.00, 1.15, 1.30,    _],[
'rely',        0.82, 0.92, 1.00, 1.10, 1.26,    _],[
'ruse',           _, 0.95, 1.00, 1.07, 1.15, 1.24],[
'sced',        1.43, 1.14, 1.00, 1.00, 1.00,    _],[ 
'site',        1.22, 1.09, 1.00, 0.93, 0.86, 0.80],[ 
'stor',           _,    _, 1.00, 1.05, 1.17, 1.46],[
'time',           _,    _, 1.00, 1.11, 1.29, 1.63],[
'tool',        1.17, 1.09, 1.00, 0.90, 0.78,    _]]

def COCOMO2(project,  a = 2.94, b = 0.91, # defaults
                      tunes= Coc2tunings):# defaults 
  sfs,ems,kloc   = 0, 5 ,22        
  scaleFactors, effortMultipliers = 5, 17
  
  for i in range(scaleFactors):
    sfs += tunes[i][project[i]]
    
  for i in range(effortMultipliers):
    j = i + scaleFactors
    ems *= tunes[j][project[j]] 
    
  return a * ems * project[kloc] ** (b + 0.01*sfs) 


def COCONUT(training,          # list of projects
            a=10, b=1,         # initial  (a,b) guess
            deltaA    = 10,    # range of "a" guesses 
            deltaB    = 0.5,   # range of "b" guesses
            depth     = 10,    # max recursive calls
            constricting=0.66):# next time,guess less
            
  if depth > 0:
    useful,a1,b1= GUESSES(training,a,b,deltaA,deltaB)
    
    if useful: # only continue if something useful
      return COCONUT(training, 
                     a1, b1,  # our new next guess
                     deltaA * constricting,
                     deltaB * constricting,
                     depth - 1)
  return a,b

def GUESSES(training, a,b, deltaA, deltaB,
           repeats=20): # number of guesses
           
  useful, a1,b1,least,n = False, a,b, 10**32, 0
  
  while n < repeats:
    n += 1
    aGuess = a1 - deltaA + 2 * deltaA * rand()
    bGuess = b1 - deltaB + 2 * deltaB * rand()
    error  = ASSESS(training, aGuess, bGuess)
    
    if error < least: # found a new best guess
      useful,a1,b1,least = True,aGuess,bGuess,error
      
  return useful,a1,b1

def ASSESS(training, aGuess, bGuess):

   error = 0.0
   
   for project in training: # find error on training
     predicted = COCOMO2(project, aGuess, bGuess)
     actual    = effort(project)
     error    += abs(predicted - actual) / actual
     
   return error / len(training) # mean training error



def RIG():

 DATA = { COC81, NASA83, COC05, NASA10 }
 
 for data in DATA: # e.g. data = COC81
 
     mres= {}
     for learner in LEARNERS: # e.g. learner = COCONUT
       for n in range(10): #10 times repeat
       
         for project in DATA: #  e.g.  one project
           training = data - project # leave-one-out
           model    = learn(training)
           estimate = guess(model, project)
           actual   = effort(project)
           mre      = abs(actual - estimate)/actual
           mres[learner][n] = mre
           
     print rank(mres) # some statistical tests

def demo():
    most , least, mid = {},{},{}
    for i,x in enumerate(Coc2tunings):
        ranges = x[1:]
        hi, lo = -1, 10**32
        jhi, jlo= -1, 10
        for j,y in enumerate(ranges):
            k = j+1
            if y ==  _:
                continue
            if y > hi:
                jhi,hi = k,y
            if y < lo:
                jlo,lo = k,y
        most[i] =  jhi
        least[i] = jlo
        mid[i] = 4
    for k in range(10,1000,10):
        least[22] = most[22] = mid[22] = k
        print k,COCOMO2(least), COCOMO2(mid), COCOMO2(most)
    
demo()
