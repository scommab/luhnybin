from multiprocessing import Pool
import sys

doubles = {
}
for i in range(10):
  r = i * 2
  if r <= 9:
    doubles[i] = r
  else:
    doubles[i] = sum([r/10, r % 10])

def luhn_checksum(card_number):
  # remove the non ints
  digits = [d for d in card_number if type(d) == int]

  # there are non-digits, skip it
  if len(digits) != len(card_number):
    return 1 # ie fail
  odd_digits = digits[-1::-2]
  even_digits = digits[-2::-2]
  checksum = 0
  checksum += sum(odd_digits)
  d_even = [doubles[i] for i in even_digits]
  checksum += sum(d_even)
  return checksum % 10

def checkReplace(s, size=14):
  for i in range(len(s) - size):
    r = s[i:i+size]
    if luhn_checksum(r) == 0:
      for j in range(i, i+size):
        s[j] = "X"
      return s
  return None

def removeSpacesAndDashes(s):
  d = {}
  r = []
  for i, c in zip(range(len(s)), s):
    if c == ' ' or c == '-':
      d[i] = c
    else:
      r.append(c)
  return d, r

def mixback(d, s):
  r = [i for i in s]
  for k in sorted(d.keys()):
    r.insert(k, d[k])
  return "".join(r)

def luhn(s):
  last = None
  mix_back, s = removeSpacesAndDashes(s)
  results = []
  w = []
  for c in s:
    if c >= '0' and c <= '9':
      w.append(int(c))
    else:
      w.append(c)
  for i in range(len(s) - 13):
    r = w[i:]
    for size in range(16, 13, -1):
      check = checkReplace(r, size)
      if check:
        results.append((i, check))
        break 
  # combine all the results
  for start, val in results:
    for i in range(len(val)):
      if val[i] == "X":
        s[start+i] = "X"
  return mixback(mix_back, s)


a = [l for l in sys.stdin.readlines()]
pool = Pool(10)
for l in pool.map(luhn, a):
  sys.stdout.write(l)
