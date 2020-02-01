#!/usr/bin/python3

import sys
from pprint import pprint, pformat
import argparse
from operator import itemgetter
from math import log10, ceil, floor

def getg(r1, r2):
	return 1 + (r2 / r1)

def getbest(es, r1dec, r2dec):
	r = []
	for r1 in es:
		for r2 in es:
			r.append([r1 * r1dec, r2 * r2dec, getg(r1 * r1dec, r2 * r2dec)])
	return r

def sisuf(val):
	gr = min(max(int(floor(log10(val) / 3)), -8), 8)
	return "%0.2f%s"%(val / (10 ** (3 * gr)), "yzafpnum kMGTPEZY"[gr + 8])

eseries = {
	 3: [100, 220, 470],
	 6: [100, 150, 220, 330, 470, 680],
	12: [100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820],
	24: [100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910],
	48: [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301, 316, 332, 248, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909, 953],
	96: [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309, 316, 324, 332,340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976],
	192: [100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 113, 114, 115, 117, 118, 120, 121, 123, 124, 126, 127, 129, 130, 132, 133, 135, 137, 138, 140, 142, 143, 145, 147, 149, 150, 152, 154, 156, 158, 160, 162, 164, 165, 167, 169, 172, 174, 176, 178, 180, 182,184, 187, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213, 215, 218, 221, 223, 226, 229, 232, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 271, 274, 277, 280, 284, 287, 291, 294, 298, 301, 305, 309, 312, 316, 320, 324, 328, 332, 336, 340, 344, 348, 352, 357, 361, 365, 370, 374, 379, 383, 388, 392, 397, 402, 407, 412, 417, 422, 427, 432, 437, 442, 448, 453, 459, 464, 470, 475, 481, 487, 493, 499, 505, 511, 517, 523, 530, 536, 542, 549, 556, 562, 569, 576, 583, 590, 597, 604, 612, 619, 626, 634, 642, 649, 657, 665, 673, 681, 690, 698, 706, 715, 723, 732, 741, 750, 759, 768, 777, 787, 796, 806, 816, 825, 835, 845, 856, 866, 876, 887, 898, 909, 920, 931, 942, 953, 965, 976, 988]
}

parser = argparse.ArgumentParser(description='AD8237 Gain Resistor Finder')

parser.add_argument('G', metavar='Gain', type=float, help='Gain')
parser.add_argument('-e', '--series', help='E-series to use', type=int, choices=[3,6,12,24,48,96,192], default=12)
parser.add_argument('-r', '--results', help='Results to show', type=int, default=1)

args = parser.parse_args()

#pprint(args.Vin)
#pprint(args.Vout)
#pprint(eseries[args.series])

gain = args.G
es   = eseries[args.series]
rat  = gain - 1

b = getbest(es, 1, 10 ** ceil(log10(gain))) + getbest(es, 1, 10 ** floor(log10(gain))) + getbest(es, 1, 10 ** ceil(log10(gain) + 1))

#pprint(b)

best = list(map(lambda z: [z[0], z[1], abs(z[2] - gain)], b))

#pprint(best)

best.sort(key=itemgetter(2))

print()
print("Best results:")
for i in range(args.results):
	r1 = best[i][0]
	r2 = best[i][1]
	gac = getg(r1, r2)
	err = (gac - gain) * 100 / gain

	# get r1||r2 below 30k
	rp = 1 / ((1 / r1) + (1 / r2))
	print(rp)
	r1 *= 10 ** floor(log10(30000) - log10(rp))
	r2 *= 10 ** floor(log10(30000) - log10(rp))
	rp = 1 / ((1 / r1) + (1 / r2))

	print("\tR1 %sΩ R2 %sΩ G %g (%g %+4.1f%%)\tR1 || R2 = %sΩ\tR1 + R2 = %sΩ"%(sisuf(r1), sisuf(r2), gac, gain, err, sisuf(rp), sisuf(r1 + r2)))
