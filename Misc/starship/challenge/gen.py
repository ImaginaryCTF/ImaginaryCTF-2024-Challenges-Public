#!/usr/bin/env python3

import random
import math

def distance(p1, p2):
  p1 = list(map(int, p1.split(",")[:-1]))
  p2 = list(map(int, p2.split(",")[:-1]))
  return math.sqrt(sum([(i1-i2)**2 for i1, i2 in zip(p1, p2)]))

def classify(pt):
  return pt.split(",")[-1]

def explode(pt):
  return list(map(int, pt.split(",")[:-1]))

def gen_hypersphere_pt(dim, radius, pt):
  random_coords = [random.randint(-radius, radius) for _ in range(dim)]
  magnitude_squared = sum(x**2 for x in random_coords)
  scaling_factor = radius / math.sqrt(magnitude_squared)
  scaled_coords = [round(scaling_factor * x) for x in random_coords]
  random_point = [scaled_coords[i] + pt[i] for i in range(dim)]
  return random_point

def gen_targets(l):
  while True:
    pt = ",".join(map(str, [random.randint(0, 100) for n in range(10)]))
    dists = [(n,distance(pt, n)) for n in l]
    dists.sort(key=lambda x: x[1])
    if classify(dists[0][0]) == "friendly" and classify(dists[1][0]) == "enemy" and classify(dists[2][0]) == "enemy":
      break
  odists = dists
  while True:
    pt2 = ",".join(map(str, gen_hypersphere_pt(9, 80, explode(pt))))
    dists = [(n,distance(pt2, n)) for n in l]
    dists.sort(key=lambda x: x[1])
    if distance(pt2, pt) < dists[2][1] or distance(pt2, pt) > (dists[2][1]+odists[2][1]):
      continue
    if classify(dists[0][0]) == "friendly" and classify(dists[1][0]) == "enemy" and classify(dists[2][0]) == "enemy":
      break
  pt = ",".join(pt.split(",")[:-1])
  pt2 = ",".join(pt2.split(","))
#  print(pt, odists[0:3])
#  print(pt2, dists[0:3])
  return [pt, pt2]

def gen_data():
  header = "x,y,velocity,rotation,price,rizz,anger,patience,aura,classification"
  l = []
  avg1 = [random.randint(0, 100) for n in range(9)]
  avg2 = [random.randint(0, 100) for n in range(9)]
  for n in range(30):
    o = ""
    for _ in range(9):
      o += str(avg1[_] + random.randint(-35, 35)) + ","
    o += "enemy"
    l.append(o)
  for n in range(30):
    o = ""
    for _ in range(9):
      o += str(avg2[_] + random.randint(-35, 35)) + ","
    o += "friendly"
    l.append(o)
  random.shuffle(l)
  csv = header + "\n" + "\n".join(l)
  targets = gen_targets(l)
  return csv, targets
