from multiprocessing import Pool
import sys

doubles = {}

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
  s_and_d = {}
  r = []
  for i, c in zip(range(len(s)), s):
    if c == ' ' or c == '-':
      s_and_d[i] = c
    else:
      r.append(c)
  return s_and_d, r

def mixback(s_and_d, s):
  r = [i for i in s]
  for k in sorted(s_and_d.keys()):
    r.insert(k, s_and_d[k])
  return "".join(r)

def luhn(s):
  spaces_and_dashes, s = removeSpacesAndDashes(s)
  results = []
  parsed_s = []
  for c in s:
    if c >= '0' and c <= '9':
      parsed_s.append(int(c))
    else:
      parsed_s.append(c)
  for i in range(len(parsed_s) - 13):
    r = parsed_s[i:]
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
  return mixback(spaces_and_dashes, s)


if __name__ == "__main__":
  # read all the input
  a = [l for l in sys.stdin.readlines()]
  pool = Pool() # Spin up enough processes to saturate the CPUs
  # note this look will stall until all the input is processed
  for l in pool.map(luhn, a):
    sys.stdout.write(l)
