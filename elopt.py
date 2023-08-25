import math
from functools import partial

def genE(lo, hi):
  for i in range(lo, hi):
    for x in [1, 1.5, 2.2, 3.3, 4.7, 6.8]:
      yield x * 10**i
  yield 10**hi

e_series = list(genE(-12, 12))


def psi(s):  
  if s[-1].isdigit():
    return float(s)
  x = float(s[:-1])
  sx = s[-1:]
  if sx == 'u':
    sx = 'μ'
  suffixes = ['p', 'n', 'μ', 'm', '', 'k', 'M', 'G', 'T']
  suffix_offset = suffixes.index('')
  e = suffixes.index(sx) - suffix_offset
  return x * 1000 ** e
psi('1.5u')



def pidx(arr, p, reverse=False):
  ran = range(len(arr))
  for i in reversed(ran) if reverse else ran:
    if p(arr[i]):
      return i
  raise ValueError('no value satisfies predicate')
pidx([1, 2, 2, 2, 2, 3], lambda x: x == 2)
pidx([1, 2, 2, 2, 2, 3], lambda x: x == 2, True)



def bound(lo: str, hi: str) -> tuple[int, int]:
  lox = psi(lo)
  hix = psi(hi)
  lon = pidx(e_series, lambda x: x >= lox)
  hin = pidx(e_series, lambda x: x <= hix, True)
  return lon, hin
bound('1m', '1500u')


def detrail(s: str) -> str:
  s1 = str(float(s))
  if s1[-2:] == '.0':
    return s1[:-2]
  return s1

def dtrunc(x: float, n :int) -> str:
  s = str(x)
  i = 0
  for j, c in enumerate(s):
    if i == n:
      return detrail(s[:j])
    if c == '.':
      continue
    i += 1
  return detrail(s)
assert(dtrunc(1.23456, 3) == '1.23')
assert(dtrunc(13323456, 3) == '133')
assert(dtrunc(1.001, 3) == '1')
assert(dtrunc(1.0, 3) == '1')


def si(x):
  suffixes = ['p', 'n', 'μ', 'm', '', 'k', 'M', 'G', 'T']
  suffix_offset = suffixes.index('')
  e = math.floor(math.log(x, 1000))
  sfx = suffixes[suffix_offset+e]
  return str(dtrunc(round(x / 1000 ** e, 3), 3)) + sfx
assert(si(12323.123) == '12.3k')
assert(si(132.3123) == '132')
assert(si(1e-10) == '100p')
assert(si(1.2e10) == '12G')
assert(si(1e-12) == '1p')
assert(si(680e-9) == '680n')

class Component:
  def __init__(self, lo, hi, i, unit):
    self.lo, self.hi = bound(lo, hi)
    self.unit = unit
    self.i = self.lo + i % (self.hi - self.lo + 1)
  def val(self):
    return e_series[self.i]
  def inc(self):
    if self.i < self.hi:
      self.i += 1
    return self
  def dec(self):
    if self.i > self.lo:
      self.i -= 1
    return self
  def __repr__(self):
    return si(self.val()) + self.unit
Capacitor = partial(Component, unit='F')
Resistor = partial(Component, unit='Ω')
Resistor('1', '1M', -1)
Capacitor('1p', '1m', -2)




def cost(fn, f_ref, Q_ref, components):
  f, Q = fn(components)
  mse = (((f - f_ref) / f_ref)**2 +
         ((Q - Q_ref) / Q_ref)**2
         )
  return mse



def optimize(fn, f_ref, Q_ref):
  R1 = Resistor('1', '1M', 1)
  R2 = Resistor('1', '1M', 1)
  C1 = Capacitor('1p', '1u', 0)
  C2 = Capacitor('1p', '1u', 0)
  components = [R1, R2, C1, C2]
  cf = partial(cost, fn, f_ref, Q_ref)
  mse = cf(components) 
  changed = True
  while changed:
    changed = False
    for c in components:
      c.dec()
      mse2 = cf(components) 
      if mse2 < mse:
        mse = mse2
        changed = True
      else:
        c.inc()
    for c in components:
      c.inc()
      mse2 = cf(components) 
      if mse2 < mse:
        mse = mse2
        changed = True
      else:
        c.dec()
  print(*fn(components), components)
  return components


def lowpass(components):
  R1, R2, C1, C2 = map(lambda c: c.val(), components)
  f = 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))
  Q = math.sqrt(R1 * R2 * C1 * C2) / ((R1 + R2) * C2)
  return f, Q

def highpass(components):
  R1, R2, C1, C2 = map(lambda c: c.val(), components)
  f = 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))
  Q = math.sqrt(R1 * R2 * C1 * C2) / (R1 * (C1 + C2))
  return f, Q

optimize(lowpass, 350, 0.707)

optimize(highpass, 300, 0.707)

optimize(lowpass, 4000, 0.707)

optimize(highpass, 4000, 0.707)
