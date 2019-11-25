# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from cube import Cube

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def test_vol():
    cube_a = Cube(os.path.join(THIS_DIR, 'AlPMOF-homo.cube'))
    cube_b = Cube(os.path.join(THIS_DIR, 'AlPMOF-lumo.cube'))
    assert cube_a.volume > 0
    assert cube_a.volume == cube_b.volume


def test_mul():
    cube_a = Cube(os.path.join(THIS_DIR, 'AlPMOF-homo.cube'))
    cube_b = Cube(os.path.join(THIS_DIR, 'AlPMOF-lumo.cube'))
    assert cube_a * cube_b < 0.01

    cube_c = Cube(os.path.join(THIS_DIR, 'MOF74Zn-homo.cube'))
    cube_d = Cube(os.path.join(THIS_DIR, 'MOF74Zn-lumo.cube'))
    assert (
        cube_c * cube_c > 0.99 <= 1.001
    )  # Overlap with itself should be 1 within some noise
    assert cube_c * cube_d > 0.65  # Large overlap between HOMO and LUMO
    assert (
        cube_c * cube_d > cube_a * cube_b
    )  # and the overlap in MOF74 is larger than in AlPMOF


def test_spatial_overlap():
    cube_a = Cube(os.path.join(THIS_DIR, 'AlPMOF-homo.cube'))
    cube_b = Cube(os.path.join(THIS_DIR, 'AlPMOF-lumo.cube'))
    assert cube_a.spatial_overlap(cube_b) < 0.01

    cube_c = Cube(os.path.join(THIS_DIR, 'MOF74Zn-homo.cube'))
    cube_d = Cube(os.path.join(THIS_DIR, 'MOF74Zn-lumo.cube'))

    assert cube_c.spatial_overlap(cube_d) > cube_a.spatial_overlap(
        cube_b
    )  # and the overlap in MOF74 is larger than in AlPMOF
