![ions_logo](https://raw.githubusercontent.com/dembart/ions/main/ions_logo.png)


### About

ions is a small python library made as 

* a dataset with various features associated with ions in ionic crystals

* a tool for decoration of ase's Atoms objects with oxidation states

Note:
The decoration method is based on the pymatgen's implementaion for Structure object



### Installation

```pip install ions```

### Available data

* bv_data - bond valence parameters [1]

* bvse_data - bond valence site energy parameters[2]

* ionic_radii - Shannon ionic radii [3, 4]

* crystal_radii - Shannon crystal radii [3, 4]

* elneg_pauling - Pauling's elenctronegativities [5]



##### References

[1]. https://www.iucr.org/resources/data/datasets/bond-valence-parameters (bvparam2020.cif)

[2]. He, B., Chi, S., Ye, A. et al. High-throughput screening platform for solid electrolytes combining hierarchical ion-transport prediction algorithms. Sci Data 7, 151 (2020). https://doi.org/10.1038/s41597-020-0474-y

[3] http://abulafia.mt.ic.ac.uk/shannon/ptable.php

[4] https://github.com/prtkm/ionic-radii

[5] https://mendeleev.readthedocs.io/en/stable/



### How to work with datasets


```python
from ions.data import ionic_radii, crystal_radii, bv_data, bvse_data

#ionic radius
symbol, valence = 'V', 4
r_ionic = ionic_radii[symbol][valence]  


#crystal radius
symbol, valence = 'F', -1
r_crystal = crystal_radii[symbol][valence]


# bond valence parameters
source, source_valence = 'Li', 1
target, target_valence = 'O', -2
params = bv_data[source][source_valence][target][target_valence]
r0, b = params['r0'], params['b']


# bond valence site energy parameters
source, source_valence = 'Li', 1
target, target_valence = 'O', -2
params = bvse_data[source][source_valence][target][target_valence]
r0, r_min, alpha, d0  = params['r0'], params['r_min'], params['alpha'], params['d0']
```

### How to decorate ase's Atoms


```python
from ase.io import read
from ions import Decorator

file = '/Users/artemdembitskiy/Desktop/crystaldata/src/ions/data/Li2O_mp-1960.cif'
atoms = read(file)
calc = Decorator()
atoms = calc.decorate(atoms)
oxi_states = atoms.get_array('oxi_states')
list(zip(atoms.symbols, oxi_states))

```




    [('Li', 1),
     ('Li', 1),
     ('Li', 1),
     ('Li', 1),
     ('Li', 1),
     ('Li', 1),
     ('Li', 1),
     ('Li', 1),
     ('O', -2),
     ('O', -2),
     ('O', -2),
     ('O', -2)]



### Example


```python
import numpy as np
from ions import Decorator
from ase.io import read
from ase.neighborlist import neighbor_list
from ions.data import bv_data

file = '/Users/artemdembitskiy/Desktop/crystaldata/src/ions/data/Li2O_mp-1960.cif'
atoms = read(file)
calc = Decorator()
atoms = calc.decorate(atoms)
ii, jj, dd = neighbor_list('ijd', atoms, 5.0)  

symbols = atoms.symbols
valences = atoms.get_array('oxi_states')
for i in np.unique(ii):
    source = symbols[i]
    source_valence = valences[i]
    neighbors = jj[ii == i]
    distances = dd[ii == i]
    if source_valence > 0:
        bvs = 0
        for n, d in zip(neighbors, distances):
            target = symbols[n]
            target_valence = valences[n]
            if source_valence * target_valence < 0:
                params = bv_data[source][source_valence][target][target_valence]
                r0, b = params['r0'], params['b']
                bvs += np.exp((r0 - d) / b)
        print(f'Bond valence sum for {source} is {round(bvs, 4)}')

```

    Bond valence sum for Li is 0.9605
    Bond valence sum for Li is 0.9605
    Bond valence sum for Li is 0.9605
    Bond valence sum for Li is 0.9605
    Bond valence sum for Li is 0.9605
    Bond valence sum for Li is 0.9605
    Bond valence sum for Li is 0.9605
    Bond valence sum for Li is 0.9605

