# VSRstats ##
Sphygmogram VSR compute util

## Installation ##
The VSRstats package is completely pip-installable use: `$ pip install VSRstats`  
or install from github: `$ pip install git+https://github.com/semenovDA/VSRstats`  

## Usage ##
**You can use example that included in this repository**
```IRC log
$ git clone https://github.com/semenovDA/VSRstats
$ pyhton example.py
```

### Define required libraries: ###
```python
from struct import unpack
import numpy as np
from VSRstats import VSR
```

### Define loading signal function: ###
```python
def loadSignal(filepath):
    
    file = open(filepath, "rb").read()
    ufile = unpack('10000H', file)
    arr = np.array(ufile)
    
    return arr
```

### Usage for 1 signal: ###
```python
filepath = './data/d0001' # path to signal
signal = loadSignal(filepath)
stats = VSR(signal).stats
print(stats)
```
#### Output: ####
```
{'nni_counter': 125, 'nni_mean': 79.92, 'nni_min': 66.0, 'nni_max': 88.0, 'hr_mean': 752.1562922784314, 
'hr_min': 681.8181818181819, 'hr_max': 909.0909090909091, 'hr_std': 33.27091439584001, ..... 'tri_index': 1.6025641025641026}
```

### Usage example for signals: ###
```python
filepathes = ['./data/d0001', './data/d0002', './data/d0003'] # Signals
signals = np.array([loadSignal(f) for f in filepathes])
stats = VSR(signals).stats
print(len(stats))
```
#### Output: ####
```
3
```
