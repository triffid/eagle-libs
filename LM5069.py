#!/usr/bin/python3
#-*- coding: utf8 -*-

# low voltage turn-on threshold
Vuvh = 44

# low voltage turn-off threshold
Vuvl = 41

# high voltage turn-off threshold
Vovh = 62

# MOSFET Power limit, watts
Plim = 30

# current limit, amps
Imax = 2

# capacitance downstream of the controller
Cout = 100e-6 * 3

import sys
from pprint import pprint, pformat
import argparse
from operator import itemgetter
from math import log10, ceil, floor, inf, fabs

def siprefix(val):
	gr = min(max(int(floor(log10(val) / 3)), -8), 8)
	return "%1.2f%s"%(val / (10 ** (3 * gr)), (gr != 0 and "yzafpnum_kMGTPEZY"[gr + 8]) or "")

eseries = {
	 3: [100, 220, 470],
	 6: [100, 150, 220, 330, 470, 680],
	12: [100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820],
	24: [100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910],
	48: [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301, 316, 332, 248, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909, 953],
	96: [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309, 316, 324, 332,340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976],
	192: [100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 113, 114, 115, 117, 118, 120, 121, 123, 124, 126, 127, 129, 130, 132, 133, 135, 137, 138, 140, 142, 143, 145, 147, 149, 150, 152, 154, 156, 158, 160, 162, 164, 165, 167, 169, 172, 174, 176, 178, 180, 182,184, 187, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213, 215, 218, 221, 223, 226, 229, 232, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 271, 274, 277, 280, 284, 287, 291, 294, 298, 301, 305, 309, 312, 316, 320, 324, 328, 332, 336, 340, 344, 348, 352, 357, 361, 365, 370, 374, 379, 383, 388, 392, 397, 402, 407, 412, 417, 422, 427, 432, 437, 442, 448, 453, 459, 464, 470, 475, 481, 487, 493, 499, 505, 511, 517, 523, 530, 536, 542, 549, 556, 562, 569, 576, 583, 590, 597, 604, 612, 619, 626, 634, 642, 649, 657, 665, 673, 681, 690, 698, 706, 715, 723, 732, 741, 750, 759, 768, 777, 787, 796, 806, 816, 825, 835, 845, 856, 866, 876, 887, 898, 909, 920, 931, 942, 953, 965, 976, 988]
}

def closest(val, eser = eseries[24]):
	mul1 = 10 ** (ceil(log10(val)) - 2)
	mul2 = 10 ** (floor(log10(val)) - 2)
	best = 0
	besterror = inf
	for r in eser:
		if (fabs((r * mul1) - val) < fabs(besterror)):
			best = r * mul1
			besterror = (r * mul1) - val
		if (fabs((r * mul2) - val) < fabs(besterror)):
			best = r * mul2
			besterror = (r * mul2) - val
	return [best, besterror]

def higher(val, eser = eseries[24]):
	mul1 = 10 ** (ceil(log10(val)) - 2)
	mul2 = 10 ** (floor(log10(val)) - 2)
	best = 0
	besterror = inf
	for r in eser:
		if  (((r * mul1) - val) > 0) and \
			(((r * mul1) - val) < (besterror)):
			best = r * mul1
			besterror = (r * mul1) - val
		if  (((r * mul2) - val) > 0) and \
			(((r * mul2) - val) < (besterror)):
			best = r * mul2
			besterror = (r * mul2) - val
	return [best, besterror]

R1 = (Vuvh - Vuvl) / 0.000021

res = closest(R1)

print("R1 = %sΩ -> %sΩ (%+1.2f%%)" % (siprefix(R1), siprefix(res[0]), res[1]  / res[0] * 100))

R1 = res[0]

R3 = 2.5 * R1 * Vuvl / Vovh / (Vuvl - 2.5)

res = closest(R3)

print("R3 = %sΩ -> %sΩ (%+1.2f%%)" % (siprefix(R3), siprefix(res[0]), res[1]  / res[0] * 100))

R3 = res[0]

R2 = (2.5 * R1 / (Vuvl - 2.5)) - R3

res = closest(R2)

print("R2 = %sΩ -> %sΩ (%+1.2f%%)" % (siprefix(R2), siprefix(res[0]), res[1]  / res[0] * 100))

R2 = res[0]

Vuvh = 2.5 + (R1 * (0.000021 + 2.5 / (R2 + R3)))
Vuvl = 2.5 * (R1 + R2 + R3) / (R2 + R3)
Vovh = 2.5 * (R1 + R2 + R3) / R3
Vovl = (R1 + R2) * (2.5 / R3 - 0.000021) + 2.5

print("Vuvh = %sv (rising turn-on)" % siprefix(Vuvh))
print("Vuvl = %sv (falling turn-off)" % siprefix(Vuvl))
print("Vovh = %sv (rising turn-off)" % siprefix(Vovh))
print("Vovl = %sv (falling turn-on)" % siprefix(Vovl))

Rsns = 0.0485 / Imax

#Rsns = 0.005

res = closest(Rsns, [200, 250, 300, 400, 500, 600, 800, 900] + eseries[12])

#res = [ 0.005, 0 ]

print("Rsns = %sΩ -> %sΩ (%+1.2f%%), %sW -> %sA" % (siprefix(Rsns), siprefix(res[0]), res[1] / res[0] * 100, siprefix(Imax * Imax * res[0]), siprefix(0.0485 / Rsns)))

Rsns = res[0]
Imax = 0.0485 / Rsns

Plimmin = 0.005 * Vovh / Rsns

if (Plim < Plimmin):
	print("Power limit will be inaccurate! Minimum is %sW, requested is %sW" % (siprefix(Plimmin), siprefix(Plim)))

Rpwr = 1.3e5 * Rsns * (Plim - 0.00118 * Vovh / Rsns)

try:
	res = closest(Rpwr)
	Plim = res[0] / 1.3e5 / Rsns + 0.00118 * Vovh / Rsns
	print("Rpwr = %sΩ -> %sΩ (%+1.2f%%) -> %sW" % (siprefix(Rpwr), siprefix(res[0]), res[1] / res[0] * 100, siprefix(Plim)))
except:
	print("Rpwr value %gΩ is nonsense, lowest power is %sW @ Rpwr = 0" % (Rpwr, siprefix(0.00118 * Vovh / Rsns)))
	Plim = 0.00118 * Vovh / Rsns


tStart = Cout / 2 * ((Vovh ** 2) / Plim + Plim / (Imax ** 2))

Ctimer = tStart * 85e-6 / 4 * 1.5

res = higher(Ctimer, eseries[3])

print("tStart = %ss, Ctimer = %sF -> %sF (%+1.2f%%)" % (siprefix(tStart), siprefix(Ctimer), siprefix(res[0]), res[1] / res[0] * 100))

print("tFault = %ss" % (siprefix(res[0] * 4 / 85e-6)))
