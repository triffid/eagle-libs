#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import pi, floor, log10

def siprefix(val):
	if (val == 0):
		return "0"
	gr = min(max(int(floor(log10(val) / 3)), -10), 10)
	return "%1.2f%s"%(val / (10 ** (3 * gr)), (gr != 0 and "qryzafpnum_kMGTPEZYRQ"[gr + 10]) or "")

# Givens
VIN=24
VOUT=12
IOUT=12
VSENSE=5e-2
RSENSE=3e-3
CO=44e-6
L=4.7e-6
RESR=25e-3
RFREQ=33e3

# MP9928 intrinsics
VFB=0.8
GM=5e-4
AO=3000

# Calculated values
RLOAD=VOUT/IOUT
GCS=1/(12*RSENSE)
FSW=20000000/((RFREQ/1000)+1)
VRIPPLE=VOUT/FSW/L * (1 - (VOUT/VIN)) * (RESR + 1/8/FSW/CO)
AVDC=RLOAD*GCS*AO*VFB/VOUT
ΔIL = VOUT * (VIN-VOUT)/VIN/L/FSW
IRMS_CIN=IOUT*((VOUT/VIN * (1 - (VOUT/VIN)))**0.5)
# Compensation
FC=FSW/10
R5=2*pi*CO*FC/GM/GCS*VOUT/VFB
C6=4/2/pi/R5/FC
C7=0
if (RESR > 0):
	if (1/2/pi/CO/RESR < FSW/2):
		C7=CO*RESR/R5

print("Givens:\tVin:%sv Vout:%sv Iout:%sA Fsw:%sHz" % (siprefix(VIN), siprefix(VOUT), siprefix(IOUT), siprefix(FSW)))
print("Steady:\tIlim:%sA Ipk@Ioutnom:%sA Irms(Cin):%sA ΔVout (ripple): %sv" % (siprefix(VSENSE/RSENSE), siprefix(IOUT + ΔIL/2), siprefix(IRMS_CIN), siprefix(VRIPPLE)))

print("Comp:\tfC≤%sHz R5≈%sΩ C6≥%sF C7≈%sF" % (siprefix(FC), siprefix(R5), siprefix(C6), siprefix(C7)))

# select closest E-series values to suggestions above
R5=18000
C6=630e-12
C7=63e-12

FP1=GM/2/pi/C6/AO
FP2=1/2/pi/CO/RLOAD
FZ1=1/2/pi/C6/R5
FESR=0
if (RESR > 0):
	FESR=1/2/pi/CO/RESR
FP3=0
if (C7 > 0):
	FP3=1/2/pi/C7/R5

print("Comp:\t(given)     R5=%sΩ C6=%sF C7=%sF" % (siprefix(R5), siprefix(C6), siprefix(C7)))
print("Comp:\tfP1:%sHz fP2:%sHz fESR:%sHz ≈ fP3:%sHz fZ1:%sHz (≤ %sHz?)" % (siprefix(FP1), siprefix(FP2), siprefix(FESR), siprefix(FP3), siprefix(FZ1), siprefix(FC/4)))
