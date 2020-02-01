#!/usr/bin/env python3

R1 = 1e5
R2 = 68e2
R3 = 10e3

# R1 = 287000
# R2 = 47000
# R3 = 13000

print("R1 = %2.1fk"  % (R1 / 1000));
print("R2 = %2.1fk"  % (R2 / 1000));
print("R3 = %2.1fk"  % (R3 / 1000));
print("Vuvh: %2.2fv" % (2.5 + (R1 * (21e-6 + 2.5 / (R2 + R3)))))
print("Vuvl: %2.2fv" % (2.5 * (R1 + R2 + R3) / (R2 + R3)))
print("Vovh: %2.2fv" % (2.5 * (R1 + R2 + R3) / R3))
print("Vovl: %2.2fv" % (((R1 + R2) * ((2.5 / R3) - 21e-6)) + 2.5))
