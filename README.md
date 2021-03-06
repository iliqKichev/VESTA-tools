# VESTA-tools
A collection of simple tools that proved to be needed for handling large periodic calculations with the VASP software package.

---
## distTotCalc.py
This is a simple script that gets the number of metal atoms (hardcoded for now) form an xyz file.
### Usage
Create an in directory in the folder of the script and then run it with plain python3.
### Requirements
- python 3.6+

---
## distPairCalc.py
This is a simple script that gets the distance between two atoms in a periodic structure. It uses the format of CONTCAR file, used by VASP.
### Usage
`python3 distTPairCalc.py <input_CONTCAR> <atoms_list.txt>`
- **optional** `-o output file` specifies the output file; default: atoms_list_output.txt
- atoms_list.txt need to have the following format: 
> A1 A2
> Where A1 and A2 are atoms from the VESTA labeling system.
### Requirements
- python 3.6+
- numpy

---
## distList.py
This is a simple script that lists all the distances between atoms from one element bellow a certain counting length.
### Usage
`python3 distList.py <input_CONTCAR> -at <atoms_type> -cl <counting_length> -o <output_file>`
- **optional** `-at <atom_type>` specifies the atomic type. The default is Li.
- **optional** `-cl <counting_length>` specifies the maximum distance. The default is 5.0 Angstroms.
- `-o <output_file>` is mandatory; in it the format is 
> A1 A2 L
> Where A1 and A2 are atoms from the VESTA labeling system and L is the distance in Angstroms
### Requirements
- python 3.6+
- numpy
