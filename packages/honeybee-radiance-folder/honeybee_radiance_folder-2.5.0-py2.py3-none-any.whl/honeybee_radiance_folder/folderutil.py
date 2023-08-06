# -*- coding: utf-8 -*-
"""Utilities for Radiance folder structure."""
import os
import json


def _as_posix(path):
    return path.replace('\\', '/')


class SceneState(object):
    """A state for a dynamic non-aperture geometry.

    This object is parallels the ``ShadeState`` class in ``honeybee-radiance``.

    Args:
        identifier (str): Human-readable identifier for the state.
        default (str): Path to file to be used for normal representation of the geometry.
        direct (str): Path to file to be used for direct studies.

    Properties:
        * identifier
        * default
        * direct
    """
    def __init__(self, identifier, default, direct):
        self.identifier = identifier
        self.default = _as_posix(default)
        self.direct = _as_posix(direct)

    @classmethod
    def from_dict(cls, input_dict):
        """Create a state from an input dictionary.

        .. code-block:: python

            {
            "identifier": "grass_covered",
            "default": "ground..summer..000.rad",
            "direct": "ground..direct..000.rad",
            }
        """
        for key in ['identifier', 'default', 'direct']:
            assert key in input_dict, 'State is missing required key: %s' % key
        identifier = input_dict['identifier']
        default = _as_posix(os.path.normpath(input_dict['default']))
        direct = _as_posix(os.path.normpath(input_dict['direct']))
        return cls(identifier, default, direct)

    def validate(self, folder):
        """Validate files in this state.

        Args:
            folder: Path to state folder.
        """
        assert os.path.isfile(os.path.join(folder, self.default)), \
            'Failed to find default file for %s' % self.identifier
        assert os.path.isfile(os.path.join(folder, self.direct)), \
            'Failed to find direct file for %s' % self.identifier

    def __repr__(self):
        return 'SceneState: {}'.format(self.identifier)


class ApertureState(SceneState):
    """A state for a dynamic aperture from Radiance files.

    This object parallels the honeybee-radiance ``SubFaceState`` in
    ``honeybee-radiance``.

    Args:
        identifier (str): Optional human-readable identifier for the state. Can be None.
        default (str): Path to file to be used for normal representation of the geometry.
        direct (str): Path to file to be used for direct studies.
        black (str): Path to file for blacking out the window.
        tmtx (str): Path to file for transmittance matrix.
        vmtx (str): Path to file for transmittance matrix.
        dmtx (str): Path to file for transmittance matrix.

    Properties:
        * identifier
        * default
        * direct
        * black
        * tmtx
        * vmtx
        * dmtx
    """

    def __init__(
        self, identifier, default, direct, black=None, tmtx=None, vmtx=None,
            dmtx=None):
        SceneState.__init__(self, identifier, default, direct)
        self.black = _as_posix(black)
        self.tmtx = _as_posix(tmtx)
        self.vmtx = _as_posix(vmtx)
        self.dmtx = _as_posix(dmtx)

    @classmethod
    def from_dict(cls, input_dict):
        """Create a state from an input dictionary.

        .. code-block:: python

            {
                "identifier": "clear",
                "default": "./south_window..default..000.rad",
                "direct": "./south_window..direct..000.rad",
                "black": "./south_window..black.rad",
                "tmtx": "clear.xml",
                "vmtx": "./south_window..mtx.rad",
                "dmtx": "./south_window..mtx.rad"
            }

        """
        for key in ['identifier', 'default', 'direct']:
            assert key in input_dict, 'State is missing required key: %s' % key
        identifier = input_dict['identifier']
        default = _as_posix(os.path.normpath(input_dict['default']))
        direct = _as_posix(os.path.normpath(input_dict['direct']))
        try:
            black = input_dict['black']
        except KeyError:
            black = None
        try:
            tmtx = input_dict['tmtx']
        except KeyError:
            tmtx = None
        try:
            vmtx = _as_posix(os.path.normpath(input_dict['vmtx']))
        except KeyError:
            vmtx = None
        try:
            dmtx = _as_posix(os.path.normpath(input_dict['dmtx']))
        except KeyError:
            dmtx = None
        return cls(identifier, default, direct, black, tmtx, vmtx, dmtx)

    def validate(self, folder, bsdf_folder):
        """Validate files in this state.

        Args:
            folder: Path to dynamic scene folder.
            bsdf_folder: Path to BSDF folder.
        """
        assert os.path.isfile(os.path.join(folder, self.default)), \
            'Failed to find default file for %s' % self.identifier
        assert os.path.isfile(os.path.join(folder, self.direct)), \
            'Failed to find direct file for %s' % self.identifier
        if self.black is not None:
            assert os.path.isfile(os.path.join(folder, self.black)), \
                'Failed to find black file for %s' % self.identifier
        if self.tmtx is not None:
            assert os.path.isfile(os.path.join(bsdf_folder, self.tmtx)), \
                'Failed to find tmtx file for %s' % self.identifier
        if self.vmtx is not None:
            assert os.path.isfile(os.path.join(folder, self.vmtx)), \
                'Failed to find vmtx file for %s' % self.identifier
        if self.dmtx is not None:
            assert os.path.isfile(os.path.join(folder, self.dmtx)), \
                'Failed to find dmtx file for %s' % self.identifier

    def __repr__(self):
        return 'ApertureState: {}'.format(self.identifier)


class DynamicScene(object):
    """Representation of a Dynamic scene geometry in Radiance folder.

    Args:
        identifier (str): Text string for a unique dynamic scene group identifier.
            This is required and cannot be None.
        states(list[SceneState]): A list of scene states.

    Properties:
        * identifier
        * states
        * state_count
    """

    def __init__(self, identifier, states):
        self.identifier = identifier
        self.states = states

    @property
    def state_count(self):
        """Number of states."""
        return len(self.states)

    @classmethod
    def from_dict(cls, input_dict):
        """Create a dynamic scene from a dictionary.

        Args:
            input_dict: An input dictionary.

            .. code-block:: python

                {
                    "ground": [
                        {
                        "identifier": "grass_covered",
                        "default": "ground..summer..000.rad",
                        "direct": "ground..direct..000.rad",
                        },
                        {
                        "identifier": "snow_covered",
                        "default": "ground..winter..001.rad",
                        "direct": "ground..direct..000.rad"
                        }
                    ]
                }

        """
        keys = list(input_dict.keys())
        assert len(keys) == 1, \
            'There must be only one dynamic group in input dictionary.'
        identifier = keys[0]

        states_dict = input_dict[identifier]
        states = [SceneState.from_dict(state) for state in states_dict]
        return cls(identifier, states)

    def validate(self, folder):
        """Validate this dynamic geometry.

        Args:
            folder: Path to dynamic scene folder.
        """
        for state in self.states:
            state.validate(folder)

    def __repr__(self):
        return 'DynamicScene: {}'.format(self.identifier)


class ApertureGroup(DynamicScene):
    """Representation of a Dynamic aperture in Radiance folder.

    Args:
        identifier (str): Text string for a unique dynamic aperture group identifier.
            This is required and cannot be None.
        states: A list of aperture states.

    Properties:
        * identifier
        * states
    """

    @classmethod
    def from_dict(cls, input_dict):
        """Create a dynamic aperture from a dictionary.

        .. code-block:: python

            {
                "south_window": [
                    {
                    "identifier": "clear",
                    "default": "./south_window..default..000.rad",
                    "direct": "./south_window..direct..000.rad",
                    "black": "./south_window..black.rad",
                    "tmtx": "clear.xml",
                    "vmtx": "./south_window..mtx.rad",
                    "dmtx": "./south_window..mtx.rad"
                    },
                    {
                    "identifier": "diffuse",
                    "default": "./south_window..default..001.rad",
                    "direct": "./south_window..direct..001.rad",
                    "black": "./south_window..black.rad",
                    "tmtx": "diffuse50.xml",
                    "vmtx": "./south_window..mtx.rad",
                    "dmtx": "./south_window..mtx.rad"
                    }
                ]
            }

        """
        keys = list(input_dict.keys())
        assert len(keys) == 1, \
            'There must be only one dynamic group in input dictionary.'
        identifier = keys[0]

        states_dict = input_dict[identifier]
        states = [ApertureState.from_dict(state) for state in states_dict]
        return cls(identifier, states)

    def validate(self, folder, bsdf_folder):
        """Validate aperture group.

        Args:
            folder: Path to dynamic scene folder.
            bsdf_folder: Path to BSDF folder.
        """
        for state in self.states:
            state.validate(folder, bsdf_folder)

    def __repr__(self):
        return 'ApertureGroup: {} (#{})'.format(self.identifier, len(self.states))


def parse_aperture_groups(states_file, validate=True, bsdf_folder=None):
    """Parse dynamic apertures from a states.json file.

    Args:
        states_file: Path to states JSON file.
        validate: Validate the files in states files exist in the folder.
        bsdf_folder: Required for validation of tmtx. Not required if validate is set to
            False.

    Returns:
        A list of dynamic apertures
    """
    if not os.path.isfile(states_file):
        return []

    with open(states_file) as inf:
        data = json.load(inf)

    apertures = [ApertureGroup.from_dict({key: value}) for key, value in data.items()]

    if validate:
        # check for the files to exist
        folder = os.path.dirname(states_file)
        for aperture in apertures:
            aperture.validate(folder, bsdf_folder)

    return apertures


def parse_dynamic_scene(states_file, validate=True):
    """Parse dynamic nonaperture geometries from a state file.

    Args:
        states_file: Path to states JSON file.

    Returns:
        A list of dynamic nonaperture geometries
    """
    if not os.path.isfile(states_file):
        return []

    with open(states_file) as inf:
        data = json.load(inf)

    geometries = [
        DynamicScene.from_dict({key: value})
        for key, value in data.items()
    ]

    if validate:
        # check for the files to exist
        folder = os.path.dirname(states_file)
        for geometry in geometries:
            geometry.validate(folder)

    return geometries


def _nukedir(target_dir, rmdir=True):
    """Delete all the files inside target_dir.
    Usage:
        nukedir("c:/ladybug/libs", True)
    """
    d = os.path.normpath(target_dir)

    if not os.path.isdir(d):
        return

    files = os.listdir(d)

    for f in files:
        if f == '.' or f == '..':
            continue
        path = os.path.join(d, f)

        if os.path.isdir(path):
            _nukedir(path)
        else:
            try:
                os.remove(path)
            except Exception:
                print("Failed to remove %s" % path)

    if rmdir:
        try:
            os.rmdir(d)
        except Exception:
            print("Failed to remove %s" % d)
