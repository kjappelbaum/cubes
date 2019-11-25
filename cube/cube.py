# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import numpy as np
from numba import jit, float32
from six.moves import map
from six.moves import range


class Cube:
    """Tiny cube class that uses some jit for efficiency"""

    def __init__(self, cubefile0):
        if os.path.isfile(cubefile0):
            self.read_cube(cubefile0)
        else:
            raise FileNotFoundError('Did not find cube file')

    def read_cube(self, fname):
        """
        Method to read cube file. Just needs the filename.
        Stolen from https://github.com/funkymunkycool/Cube-Toolz/blob/master/cube_tools.py
        """

        with open(fname, 'r') as fin:
            self.filename = fname
            self.comment1 = fin.readline()  # Save 1st comment
            self.comment2 = fin.readline()  # Save 2nd comment
            nOrigin = fin.readline().split()  # Number of Atoms and Origin
            self.natoms = int(nOrigin[0])  # Number of Atoms
            self.origin = np.array(
                [np.float32(nOrigin[1]), np.float32(nOrigin[2]), np.float32(nOrigin[3])]
            )  # Position of Origin
            nVoxel = fin.readline().split()  # Number of Voxels
            self.NX = int(nVoxel[0])
            self.X = np.array(
                [np.float32(nVoxel[1]), np.float32(nVoxel[2]), np.float32(nVoxel[3])]
            )
            nVoxel = fin.readline().split()  #
            self.NY = int(nVoxel[0])
            self.Y = np.array(
                [np.float32(nVoxel[1]), np.float32(nVoxel[2]), np.float32(nVoxel[3])]
            )
            nVoxel = fin.readline().split()  #
            self.NZ = int(nVoxel[0])
            self.Z = np.array(
                [np.float32(nVoxel[1]), np.float32(nVoxel[2]), np.float32(nVoxel[3])]
            )
            self.atoms = []
            self.atomsXYZ = []
            for _ in range(self.natoms):
                line = fin.readline().split()
                self.atoms.append(line[0])
                self.atomsXYZ.append(list(map(np.float32, [line[2], line[3], line[4]])))
            self.data = np.zeros((self.NX, self.NY, self.NZ), dtype=np.float32)
            i = int(0)
            for s in fin:
                for v in s.split():
                    self.data[
                        int(i / (self.NY * self.NZ)),
                        int((i / self.NZ) % self.NY),
                        int(i % self.NZ),
                    ] = np.float32(v)
                    i += 1
            # if i != self.NX*self.NY*self.NZ: raise NameError, "FSCK!"

            self.dV = np.dot(self.X, np.cross(self.Y, self.Z))

    def _checks(self, other):
        """Can only perform arithmetics if the cube is for the same structure"""
        assert self.NX == other.NX, 'Number of grid points in x must be the same'
        assert self.NY == other.NY, 'Number of grid points in y must be the same'
        assert self.NZ == other.NZ, 'Number of grid points in z must be the same'

        assert self.natoms == other.natoms, 'Number of atoms must be the same'

        assert all(self.X == other.X), 'X dimension must be the same'
        assert all(self.Y == other.Y), 'Y dimension must be the same'
        assert all(self.Z == other.Z), 'Z dimension must be the same'

        assert self.data.shape == other.data.shape

    def __add__(self, other):
        self._checks(other)
        return np.add(self.data, other.data)

    def __sub__(self, other):
        self._checks(other)
        return np.sub(self.data, other.data)

    @staticmethod
    @jit(float32(float32[:, :]), nopython=True)
    def _volume(latticearray):
        return np.linalg.det(latticearray)

    @property
    def volume(self):
        return Cube._volume(np.array([self.X, self.Y, self.Z]))

    @staticmethod
    @jit(float32(float32[:, :, :], float32[:, :, :], float32), nopython=True)
    def _multiply(data0, data1, volume):
        """Calculate overlap integral between two cube arrays"""
        return np.multiply(np.sum(np.multiply(np.abs(data0), np.abs(data1))), volume)

    def __mul__(self, other):
        """Return overlap integral"""
        self._checks(other)
        vol = self.dV
        return Cube._multiply(self.data, other.data, vol)

    def spatial_overlap(self, other):
        """Return spatial overlap integral"""
        self._checks(other)
        vol = self.dV
        return Cube._multiply(np.abs(self.data), np.abs(other.data), vol)

    __rmul__ = __mul__
