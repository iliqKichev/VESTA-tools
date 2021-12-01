import math
import argparse
import numpy as np

from typing import List, Tuple, Dict


class Vector3:
    def __init__(self, x: float = 0., y: float = 0., z: float = 0.):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "{0:.6f}\t{1:.6f}\t{2:.6f}".format(self.x, self.y, self.z)

    def dist(self, other: 'Vector3'):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def __mul__(self, other: float):
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __add__(self, other: 'Vector3'):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)


WORLD_POS = [(-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
             (-1, 0, -1), (-1, 0, 0), (-1, 0, 1),
             (-1, 1, -1), (-1, 1, 0), (-1, 1, 1),
             (0, -1, -1), (0, -1, 0), (0, -1, 1),
             (0, 0, -1), (0, 0, 0), (0, 0, 1),
             (0, 1, -1), (0, 1, 0), (0, 1, 1),
             (1, -1, -1), (1, -1, 0), (1, -1, 1),
             (1, 0, -1), (1, 0, 0), (1, 0, 1),
             (1, 1, -1), (1, 1, 0), (1, 1, 1)]


class Atom(Vector3):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, symbol: str = "", index: int = 0):
        Vector3.__init__(self, x, y, z)
        self.symbol: str = symbol
        self.index: int = index

    def periodic_dist(self, other: 'Atom', brave_v: List[Vector3]) -> float:
        min_dist = 10000000000.0
        for wp in WORLD_POS:
            min_dist = min(min_dist, self.dist(other + brave_v[0] * wp[0] + brave_v[1] * wp[1] + brave_v[2] * wp[2]))
        return min_dist

    def __str__(self):
        return f"{self.symbol}\t{Vector3.__str__(self)}"


# def load_xyz_file(file_name: str) -> List[Atom]:
#     if file_name.split(".")[-1] == "xyz":
#         atoms: list[Atom] = []
#         with open(file_name) as file:
#             content = file.readlines()
#             for line in content[2:]:
#                 atoms.append(Atom(line))
#             for ind in range(len(atoms)):
#                 atoms[ind].index = ind
#
#             return atoms.copy()
#     else:
#         raise FileNotFoundError("Not supported another but xyz format!")


def load_contcar(file_name: str) -> (Dict[str, Atom], List[Vector3]):
    if file_name.endswith("CONTCAR"):
        with open(file_name) as file:
            content = file.readlines()
            # Everything has to be multiplied by that constant. (It is usually 1)
            lattice_constant: float = float(content[1].strip())
            # Bravais Unit Cell (once stored in np coordinates and once in internal class) -> is this necessary?
            bravais_v: List[Vector3] = [Vector3(float(d.split()[0]), float(d.split()[1]), float(d.split()[2]))
                                        for d in content[2:5]]
            bravais_np = np.array([[bravais_v[0].x, bravais_v[0].y, bravais_v[0].z],
                                   [bravais_v[1].x, bravais_v[1].y, bravais_v[1].z],
                                   [bravais_v[2].x, bravais_v[2].y, bravais_v[2].z]])
            symbols = [s.strip() for s in content[5].split()]
            symbol_count = [int(s.strip()) for s in content[6].split()]

            coord_np = np.array([[float(_) for _ in line.split()] for line in content[8:sum(symbol_count) + 8]])
            coord_np = coord_np.dot(bravais_np)

            sc = 1
            si = 0
            atoms: Dict[str, Atom] = dict()
            for ind, v in enumerate(coord_np):
                if sc > symbol_count[si]:
                    sc = 1
                    si += 1
                atoms[f"{symbols[si]}{sc}"] = (Atom(float(v[0]) * lattice_constant, float(v[1]) * lattice_constant,
                                                    float(v[2]) * lattice_constant, symbols[si]))
                sc += 1
            bravais_v = [_ * lattice_constant for _ in bravais_v]

            return atoms.copy(), [_ * lattice_constant for _ in bravais_v]


def print_in_xyz_format(atoms: Dict[str, Atom], comment: str = "") -> None:
    print(len(atoms), f"\n{comment}")
    for a in atoms:
        print(atoms[a])


def iterate_over_bonds(file_name: str) -> List[Tuple[str, str, float]]:
    with open(file_name) as file:
        # Load the atoms
        atoms, bravais = load_contcar(args.filename)

        # print_in_xyz_format(atoms)

        pairs = file.readlines()
        output: List[Tuple[str, str, float]] = list()
        for d in pairs:
            ind_1 = d.split()[0]
            ind_2 = d.split()[1]
            length = atoms[ind_1].periodic_dist(atoms[ind_2], bravais)
            output.append((ind_1, ind_2, length))
        return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("atoms_numbers_file")
    parser.add_argument("-o")
    args = parser.parse_args()

    output: List[Tuple[str, str, float]] = iterate_over_bonds(args.atoms_numbers_file)

    if args.o is not None:
        with open(args.o, "w") as f:
            f.writelines([f"{d[0]}\t{d[1]}\t{d[2]}\n" for d in output])
    else:
        with open("{}_output.txt".format(args.atoms_numbers_file.split(".")[0]), "w") as f:
            f.writelines([f"{d[0]}\t{d[1]}\t{d[2]}\n" for d in output])


