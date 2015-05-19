import numpy as np
import pdb
import itertools as it
from copy import deepcopy

def read_pdb(lines):
    coords = list()
    j = 1
    for line in lines:
        data = line.split()
        if data[0] == 'ATOM':
            l = list(line)
            c = dict()
            c['atom_number'] = float(''.join(l[6:11]))
            c['atom_name'] = ''.join(l[12:16])
            c['res_name'] = ''.join(l[17:21])
            c['res_number'] = float(''.join(l[22:26]))
            c['x'] = float(''.join(l[30:38]))
            c['y'] = float(''.join(l[38:46]))
            c['z'] = float(''.join(l[46:54]))
            c['x'] /= 10
            c['y'] /= 10
            c['z'] /= 10
            if len(coords) > 1:
                if c['res_name'] == coords[-1]['res_name']:
                    c['res_number'] = coords[-1]['res_number']
                else:
                    c['res_number'] = coords[-1]['res_number']+1
            coords.append(c)
        j += 1
    box = lines[0].split()[1:4]
    return (box, coords)

pair_file = open('ion-pair.pdb', 'r')
pair_box, pair_proto = read_pdb(pair_file.readlines())

lattice_size = [10, 10, 10] #size of lattice in lattice units
lattice_spacing = [0.8, 0.8, 0.7] #units of nm
coordlist = list()

for j,n in enumerate(list(it.product(range(lattice_size[0]), range(lattice_size[1]), range(lattice_size[2])))):
    pair_copy = deepcopy(pair_proto)
    for atom in pair_copy:
        atom['x'] += float(lattice_spacing[0]*n[0])
        atom['y'] += float(lattice_spacing[1]*n[1])
        atom['z'] += float(lattice_spacing[2]*n[2])
        atom['res_number'] += j*2
        atom['atom_number'] += 34*j
        coordlist.append(atom)

print 'emim tf2n'
print len(coordlist)

for c in coordlist:
    print("%5d%5s%5s%5d%8.3f%8.3f%8.3f" % (c['res_number'], c['res_name'], c['atom_name'], c['atom_number'], c['x'], c['y'], c['z']))

print float(lattice_spacing[0]*lattice_size[0]), float(lattice_spacing[1]*lattice_size[1]), float(lattice_spacing[2]*lattice_size[2])
