# mdshare
Get access to our MD data files.

[![CircleCI](https://circleci.com/gh/markovmodel/mdshare/tree/master.svg?style=svg)](https://circleci.com/gh/markovmodel/mdshare/tree/master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b9a86155b4e84bf3b397bad0c04e42a9)](https://www.codacy.com/app/cwehmeyer/mdshare?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=markovmodel/mdshare&amp;utm_campaign=Badge_Grade)

This is a downloader for molecular dynamics (MD) data from a public FTP server at FU Berlin. See [here](https://markovmodel.github.io/mdshare/) for a full list of available datasets and terms of use.

## Example
This code will download a file (if it does not already exist locally) with a featurized set of three alanine dipeptide MD trajectories and store its content of three `numpy.ndarray` objects (each of `shape=[250000, 2], dtype=numpy.float32`) in the list `trajs`:

```python
import mdshare
import numpy as np

local_filename = mdshare.fetch('alanine-dipeptide-3x250ns-backbone-dihedrals.npz')
with np.load(local_filename) as fh:
    trajs = [fh[key] for key in sorted(fh.keys())]
```

By default, the `mdshare.fetch()` function will look in and download to the current directory (function parameter `working_directory='.'`). If you instead set this parameter to `None` ...

```python
local_filename = mdshare.fetch(
    'alanine-dipeptide-3x250ns-backbone-dihedrals.npz',
    working_directory=None)
```

... the file will be downloaded to a temporary directory. In both cases, the function will return the path to the downloaded file.

Should the requested file already be present in the `working_directory`, the download is skipped.

Using `mdshare.catalogue()` to view the files and filesizes of the available trajectories ...

```python
mdshare.catalogue()
```

... produces the output:

```text
Repository: http://ftp.imp.fu-berlin.de/pub/cmb-data/
Files:
alanine-dipeptide-0-250ns-nowater.xtc                  42.9 MB
alanine-dipeptide-1-250ns-nowater.xtc                  42.9 MB
alanine-dipeptide-2-250ns-nowater.xtc                  42.9 MB
alanine-dipeptide-3x250ns-backbone-dihedrals.npz        6.0 MB
alanine-dipeptide-3x250ns-heavy-atom-distances.npz    135.0 MB
[...]
Containers:
mdshare-test.tar.gz                                   193.0 bytes
pyemma-tutorial-livecoms.tar.gz                       123.9 MB
```

Using `mdshare.search(filename_pattern)` to select for a given group of files ...

```python
pentapeptide_xtcs = mdshare.search('penta*xtc')
print(pentapeptide_xtcs)
```

... produces the output:

```python
['pentapeptide-00-500ns-impl-solv.xtc',
 'pentapeptide-01-500ns-impl-solv.xtc',
 'pentapeptide-02-500ns-impl-solv.xtc',
...
 'pentapeptide-22-500ns-impl-solv.xtc',
 'pentapeptide-23-500ns-impl-solv.xtc',
 'pentapeptide-24-500ns-impl-solv.xtc']
```
