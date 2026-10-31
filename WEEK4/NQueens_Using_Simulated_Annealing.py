import math
import random


def solve_nqueens(n, s):

  def conflicts(st):
    return sum(
        st[i] == st[j] or abs(st[i] - st[j]) == abs(i - j)
        for i in range(n)
        for j in range(i + 1, n)
    )

  t = 100.0
  curr_c = conflicts(s)

  while curr_c > 0 and t > 0.001:
    i, j = random.sample(range(n), 2)
    ns = list(s)
    ns[i], ns[j] = ns[j], ns[i]

    next_c = conflicts(ns)
    delta = next_c - curr_c

    if delta < 0 or random.random() < math.exp(-delta / t):
      s, curr_c = ns, next_c

    t *= 0.99

  return s


if __name__ == "__main__":
  n = int(input("Enter n: "))
  print("Enter queen positions:")
  s = []
  for i in range(n):
    s.append(int(input()))

  final_s = solve_nqueens(n, s)

  print(f"\nFinal List: {final_s}")
  print("Final Matrix:")
  for r in range(n):
    row_str = ""
    for c in range(n):
      row_str += "Q " if final_s[c] == r else ". "
    print(row_str)
