import numpy as np
import math


def genE(lo_mag, hi_mag):
  return np.concatenate([*[np.array([1, 1.5, 2.2, 3.3, 4.7, 6.8]) * 10**n
                           for n in range(lo_mag, hi_mag)], 
                         np.array([10**hi_mag])])

def genE(lo, hi):
  for i in range(lo, hi):
    for x in [1, 1.5, 2.2, 3.3, 4.7, 6.8]:
      yield x * 10**i
  yield 10**hi

e_series = list(genE(-12, 12))
list(map(si, e_series))

def psi(s):
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



def lowpass(components):
  R1, R2, C1, C2 = components
  f = 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))
  Q = math.sqrt(R1 * R2 * C1 * C2) / ((R1 + R2) * C1)
  return f, Q

def cost(f_ref, Q_ref, components):
  R1, R2, C1, C2 = components
  f, Q = lowpass(components)
  mse = (((f - f_ref) / f_ref)**2 +
         ((Q - Q_ref) / Q_ref)**2
         )
  return mse
cost(20e3, 0.707, [1, 1, 1, 1])


