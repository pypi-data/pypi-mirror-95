# honeybee-radiance-folder
[![Build Status](https://travis-ci.com/ladybug-tools/honeybee-radiance-folder.svg?branch=master)](https://travis-ci.com/ladybug-tools/honeybee-radiance-folder)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/honeybee-radiance-folder/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/honeybee-radiance-folder)

[![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)

Honeybee Radiance Folder is a Python library to read, write and validate the
[Radiance folder structure](https://github.com/ladybug-tools/radiance-folder-structure).

# Installation

`pip install -U honeybee-radiance-folder`

# [API Documentation](https://www.ladybug.tools/honeybee-radiance-folder/docs/)

# Usage

```python
# create a Radiance Model folder
import os
from honeybee_radiance_folder import ModelFolder

rf = 'c:/ladybug/sample_folder'
folder = ModelFolder(rf)
folder.write(overwrite=True)

# check the folders and files created in model folder
for f in os.listdir(folder.model_folder(full=True)):
    print(f)
```

```shell
aperture
folder.cfg
grid
scene
```

```python
# load a Radiance folder

# in this case we are loading the folder from sample folder in radiance folder repository
# you can download it from here
# https://github.com/ladybug-tools/radiance-folder-structure/tree/master/project_folder
from honeybee_radiance_folder import ModelFolder

radiance_folder = r'./tests/assets/project_folder'
folder = ModelFolder(radiance_folder)

# get input files for scene
for f in folder.scene_files(black_out=False, rel_path=True):
    print(f)
```

```shell
model/scene/context.mat
model/scene/context.rad
model/scene/partition.mat
model/scene/partition.rad
model/scene/partition_glass.mat
model/scene/partition_glass.rad
model/scene/room_envelope.mat
model/scene/room_envelope.rad
```

```python
# and apertures
for f in folder.aperture_files(black_out=False, rel_path=True):
    print(f)
```

```shell
model\aperture\aperture.mat
model\aperture\aperture.rad
```

```python
# and finally get aperture groups - south window in this case
# and check each state
for count, ap in enumerate(folder.aperture_groups(interior=False)):
    print('Aperture group %d: %s' % (count + 1, ap.identifier))
    for state in ap.states:
        print('- %s: %s' % (state.identifier, state.default))
```

```shell
Aperture group 1: south_window
- 0_clear: south_window..default..000.rad
- 1_diffuse: south_window..default..001.rad
```
