import sys

doubles = {
}
for i in range(10):
  r = i * 2
  if r <= 9:
    doubles[i] = [r]
  else:
    doubles[i] = [r/10, r % 10]

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in n if d >= '0' and d <= '9']
    digits = digits_of(card_number)
    if len(digits) > 16 or len(digits) < 14:
      return 1 # ie fail
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    d_even = [doubles[i] for i in even_digits]
    unfold = [item for sublist in d_even for item in sublist]
    checksum += sum(unfold)
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
    if d == ' ' or d == '-':
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
  for i in range(len(s)):
    r = s[i:]
    for size in range(16, 13, -1):
      check = checkReplace(r, size)
      if check:
        results.append(s[:i] + check)
  for r in results:
    for i in range(len(r)):
      if r[i] == "X":
        s[i] = "X"
  return mixback(mix_back, s)

a = sys.stdin.readlines()
for l in a:
  sys.stdout.write(luhn(l))
