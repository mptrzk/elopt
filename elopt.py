import numpy as np
import math


def genE(lo_mag, hi_mag):
  return np.concatenate([*[np.array([1, 1.5, 2.2, 3.3, 4.7, 6.8]) * 10**n
                           for n in range(lo_mag, hi_mag)], 
                         np.array([10**hi_mag])])



def lowpass(R1, R2, C1, C2):
  f = 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))
  Q = math.sqrt(R1 * R2 * C1 * C2) / ((R1 + R2) * C1)
  return f, Q

resistors = {'unit':'Ω', 'series':genE(0, 6)}
capacitors = {'unit':'F', 'series':genE(-12, -6)}

def cost(f_ref, Q_ref, components):
  R1, R2, C1, C2 = components
  f, Q = lowpass(R1.val(), R2.val(), C1.val(), C2.val())
  mse = ((f - f_ref)/f_ref)**2 + ((Q - Q_ref)/f_ref)**2
  return mse, f, Q

#proper impl would also handle exponential notation, but here it's not needed
#for this case, the digits don't even have to be significant
#we get no leading zeros, right?
#noo, FP hazard

def pidx(arr, p, miss=None):
  for i, el in enumerate(arr):
    if el == p: 
      return el
  return miss
pidx([1, 2, 3], 4, 'nudtid')
pidx([1, 2, 3], 2, 'nudtid')

def digits(x):
  s = str(x)
  significant = False
  ret = ''
  for i, c in enumerate(s):
    if c  == '.':
      continue
    if c == '0' and not significant:
      continue
    if c == 'e':
      break
    ret += c
    significant = True
  return ret

digits(1234)
digits(0.1234e-12)
digits(012.34e-12)


def sigfloor(x, n):
  s = str(x)
  l = 0
  for l, c in enumerate(s):
    if c != 0:
      break
  for i, c in enumerate(s):
    if n == 0 or c == 'e':
      return s[l:i]
    if c != '.':
      n -= 1
  return s

def dtrunc(x, n):
  s = str(x)
  i = 0
  for j, c in enumerate(s):
    if i == n:
      return s[:j]
    if c == '.':
      continue
    i += 1
  return s
dtrunc(1.23456, 3)
dtrunc(13323456, 3)



def si_repr(x):
  suffixes = ['p', 'n', 'μ', 'm', '', 'k', 'M', 'G', 'T', 'P']
  suffix_offset = suffixes.index('')
  e = math.floor(math.log(x, 1000))
  sfx = suffixes[suffix_offset+e]
  return str(dtrunc(x / 1000 ** e, 3)) + sfx
si_repr(12323.123)
si_repr(132.3123)
si_repr(1e-10)
si_repr(1.2e10)
si_repr(1e-12)


class Component:
  def __init__(self, ctype, i):
    self.ctype = ctype
    self.i = i
  def val(self):
    return self.ctype['series'][self.i]
  def inc(self):
    if self.i + 1 < len(self.ctype['series']):
      self.i += 1
    return self
  def dec(self):
    if self.i - 1 >= 0:
      self.i -= 1
    return self
  def __repr__(self):
    return si_repr(self.val()) + self.ctype['unit']
#stop writing classes?

    
def optimize(f_ref, Q_ref):
  changed = True
  '''
  while changed:
    changed = False
    R
  '''
  R1 = Component(resistors, len(resistors) - 1)
  R2 = Component(resistors, len(resistors) - 1)
  C1 = Component(capacitors, 0)
  C2 = Component(capacitors, 0)
  components = [R1, R2, C1, C2]
  mse, f, Q = cost(f_ref, Q_ref, components) 
  print(mse, f, Q, components)
optimize(10e3, 0.5)

