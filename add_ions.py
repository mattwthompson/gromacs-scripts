from __future__ import print_function
import numpy as np
import pdb

#blueprint for adding two systems together, moved into [0, L] coordinates
carbon_file = open('dual-pores.gro', 'r')
carbon_lines = carbon_file.readlines()

carbon_natoms = int(carbon_lines[1].split()[0])
carbon_dims = [float(x) for x in carbon_lines[-1].split()]

carbon_coords = np.ndarray(shape=(carbon_natoms), dtype=('i4, a5, a5, i4, f4, f4, f4'))
for i in range(2, len(carbon_lines)-1):
    carbon_coords[i-2][0] = 1 ; int(carbon_lines[i][:5])  #resid
    carbon_coords[i-2][1] = str(carbon_lines[i][5:10]) #resname
    carbon_coords[i-2][2] = str(carbon_lines[i][10:15]) #atomname
    carbon_coords[i-2][3] = int(carbon_lines[i][15:20])  #atomid
    carbon_coords[i-2][4] = float(carbon_lines[i][20:28])# - carbon_dims[0]  #x, moved to origin
    carbon_coords[i-2][5] = float(carbon_lines[i][28:36])# - carbon_dims[1]  #y
    carbon_coords[i-2][6] = float(carbon_lines[i][36:44])# - carbon_dims[2]  #z
#carbon_coords = [carbon_lines[i].split()[-3:] for i in range(2, len(carbon_lines))]
#carbon_coords = np.array(carbon_coords)
#carbon_coords.astype(float)
base = np.zeros(3)

for q in range(3):
    base[q] = min([x[q+4] for x in carbon_coords])

for row in range(len(carbon_coords)):
    carbon_coords[row][4] -= base[0]
    carbon_coords[row][5] -= base[1]
    carbon_coords[row][6] -= base[2]

for q in range(3):
    carbon_dims[q] = max([x[q+4] for x in carbon_coords])

ion_file = open('il-bath.gro', 'r')
ion_lines = ion_file.readlines()

ion_natoms = int(ion_lines[1].split()[0])
ion_dims = map(int, [float(x) for x in ion_lines[-1].split()])

ion_coords = np.ndarray(shape=(ion_natoms), dtype=('i4, a5, a5, i4, f4, f4, f4'))
for i in range(2, len(ion_lines)-1):
    ion_coords[i-2][0] = int(ion_lines[i][:5])  #resid
    ion_coords[i-2][1] = str(ion_lines[i][5:10]) #resname
    ion_coords[i-2][2] = str(ion_lines[i][10:15]) #atomname
    ion_coords[i-2][3] = int(ion_lines[i][15:20])  #atomid
    ion_coords[i-2][4] = float(ion_lines[i][20:28])# - ion_dims[0]  #x, moved to origin
    ion_coords[i-2][5] = float(ion_lines[i][28:36])# - ion_dims[1]  #y
    ion_coords[i-2][6] = float(ion_lines[i][36:44])# - ion_dims[2]  #z
#carbon_coords = [carbon_lines[i].split()[-3:] for i in range(2, len(carbon_lines))]
#ion_coords = [ion_lines[i].split()[-3:] for i in range(2, len(ion_lines))]
#ion_coords = np.array(ion_coords)
#ion_coords.astype(float)

for q in range(3):
    base[q] = min([x[q+4] for x in ion_coords])

for row in range(len(ion_coords)):
    ion_coords[row][4] -= base[0]
    ion_coords[row][5] -= base[1]
    ion_coords[row][6] -= base[2]

for q in range(3):
    ion_dims[q] = max([x[q+4] for x in ion_coords])

box_natoms = carbon_natoms + ion_natoms

box_dims = np.zeros(3)

box_dims[0] = carbon_dims[0] + ion_dims[0] + 0.2
#box_dims[0] = carbon_dims[0] + ion_dims[0] + 0.2
box_dims[1] = max(carbon_dims[1], ion_dims[1])
#box_dims[1] = max(carbon_dims[1], ion_dims[1])
box_dims[2] = max(carbon_dims[2]+0.341, ion_dims[1])
#box_dims[2] = max(carbon_dims[2], ion_dims[2])

#trans_carbon_coords[:,0] = [trans_carbon_coords[i,0] + ion_dims[0] + 0.1 for i in range(len(trans_carbon_coords))]

for i in range(ion_natoms):
    ion_coords[i][0] += 1
    ion_coords[i][3] += carbon_natoms
    ion_coords[i][4] += carbon_dims[0] + 0.2

box_coords = np.hstack([carbon_coords, ion_coords])

print('slit pore, emimTf2N')
print(box_natoms)

for i,c in enumerate(box_coords):
    print("%5d%-5s%5s%5d%8.3f%8.3f%8.3f" % (c[0], c[1], c[2], c[3], c[4], c[5], c[6]))
print("    %6.3f %6.3f %6.3f" % (box_dims[0], box_dims[1], box_dims[2]))
