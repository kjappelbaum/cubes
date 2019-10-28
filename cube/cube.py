import os
import numpy as np
from numba import jit

class Cube:
    """Tiny cube class that uses some jit for efficiency"""

    def __init__(self, cubefile0):
        if os.path.isfile(cubefile0):
            self.read_cube(cubefile0)

    def read_cube(self, fname):
        """
        Method to read cube file. Just needs the filename. 
        Stolen from https://github.com/funkymunkycool/Cube-Toolz/blob/master/cube_tools.py
        """

        with open(fname, "r") as fin:
            self.filename = fname
            self.comment1 = fin.readline()  # Save 1st comment
            self.comment2 = fin.readline()  # Save 2nd comment
            nOrigin = fin.readline().split()  # Number of Atoms and Origin
            self.natoms = int(nOrigin[0])  # Number of Atoms
            self.origin = np.array(
                [float(nOrigin[1]), float(nOrigin[2]), float(nOrigin[3])]
            )  # Position of Origin
            nVoxel = fin.readline().split()  # Number of Voxels
            self.NX = int(nVoxel[0])
            self.X = np.array([float(nVoxel[1]), float(nVoxel[2]), float(nVoxel[3])])
            nVoxel = fin.readline().split()  #
            self.NY = int(nVoxel[0])
            self.Y = np.array([float(nVoxel[1]), float(nVoxel[2]), float(nVoxel[3])])
            nVoxel = fin.readline().split()  #
            self.NZ = int(nVoxel[0])
            self.Z = np.array([float(nVoxel[1]), float(nVoxel[2]), float(nVoxel[3])])
            self.atoms = []
            self.atomsXYZ = []
            for atom in range(self.natoms):
                line = fin.readline().split()
                self.atoms.append(line[0])
                self.atomsXYZ.append(list(map(float, [line[2], line[3], line[4]])))
            self.data = np.zeros((self.NX, self.NY, self.NZ))
            i = int(0)
            for s in fin:
                for v in s.split():
                    self.data[
                        int(i / (self.NY * self.NZ)),
                        int((i / self.NZ) % self.NY),
                        int(i % self.NZ),
                    ] = float(v)
                    i += 1
            # if i != self.NX*self.NY*self.NZ: raise NameError, "FSCK!"
        return None

    def _checks(self, other):
        """Can only perform arithmetics if the cube is for the same structure"""
        assert self.NX == other.NX, "Number of grid points in x must be the same"
        assert self.NY == other.NY, "Number of grid points in y must be the same"
        assert self.NZ == other.NZ, "Number of grid points in z must be the same"

        assert self.natoms == other.natoms, "Number of atoms must be the same"

        assert self.X == other.X, "X dimension must be the same"
        assert self.Y == other.Y, "Y dimension must be the same"
        assert self.Z == other.Z, "Z dimension must be the same"

    def __add__(self, other):
        self._checks(self, other)
        return np.add(self.data, other.data)

    def __sub__(self, other):
        self._checks(self, other)
        return np.sub(self.data, other.data)

    @staticmethod
    @jit(float32(float32, float32, float32))
    def _volume(x, y, z):
        return np.linalg.det(np.array([x, y, z]))

    @property
    def volume(self):
        return Cube._volume(self.X, self.Y.self.Z)

    @staticmethod
    @jit(float32(float32[:, :, :], float32[:, :, :], float32))
    def _multiply(data0, data1, volume):
        """Calculate overlap integral between two cube arrays"""
        return np.prod(np.sum(np.prod(data0, data1)), np.square(volume))

    def __mul__(self, other):
        """Return overlap integral"""
        self._checks(self, other)

        vol = self.volume

        return Cube._multiply(self.data, other.data, vol)

