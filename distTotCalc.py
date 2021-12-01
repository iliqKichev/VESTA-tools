import os
import math
import argparse

IN_FOLDER = os.path.join(os.getcwd(), "in")
CRITICAL_LENGTH = 2.7
COUNTING_LENGTH = 5


class Atom:
    def __init__(self, line: str, index: int = 0):
        self.x: float = float(line.split()[1])
        self.y: float = float(line.split()[2])
        self.z: float = float(line.split()[3])
        self.symbol: str = line.split()[0]
        self.index: int = index

    def dist(self, other: 'Atom'):
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2

    def __str__(self):
        return f"{self.x}\t{self.y}\t{self.z}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    if args.filename.endswith(".xyz"):
        cont = open(args.filename)
        nlines = int(cont.readline())
        cont.readline()

        sodium: list[Atom] = []
        for i in range(nlines):
            new_line = cont.readline()
            if new_line.startswith("Li"):
                sodium.append(Atom(new_line, i+1))

        size: int = len(sodium)
        counter: float = 0
        total: float = 0
        atom_counter: set[int] = set()
        print("Atoms that have a neighbour at under {}A:".format(CRITICAL_LENGTH))
        for i in range(size):
            for j in range(i+1, size):
                if math.sqrt(sodium[i].dist(sodium[j])) < COUNTING_LENGTH:
                    total += 1
                if math.sqrt(sodium[i].dist(sodium[j])) < CRITICAL_LENGTH:
                    counter += 1
                    atom_counter.add(sodium[i].index)
                    atom_counter.add(sodium[j].index)
                    print(sodium[i].index, sodium[j].index, sodium[i].dist(sodium[j]))
        if not atom_counter:
            print("No such atoms.")
        else:
            print("Number of atoms that have a neighbour at under {}A: {}".format(CRITICAL_LENGTH, len(atom_counter)))
            print("Percentage of atoms that have a neighbour at under {}A: {}".format(CRITICAL_LENGTH, len(atom_counter)/size))
            print("Percentage of distances between two atoms under {}A that are under {}A: {}".format(COUNTING_LENGTH, CRITICAL_LENGTH, counter / total * 100))

