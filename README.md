# CargoOptimizer-3DBP-python

This repository contains a 3D Bin Packing optimization algorithm, which aims to optimize the transport of packages in a set of vehicles. The algorithm allows packages to be rotated in different orientations to achieve the best possible packing configuration. This implementation is based on the work of Dube, Kanavathy, and Woodview (2006) on optimizing three-dimensional bin packing through simulation.

## Table of Contents

- [Description](#description)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Algorithm Details](#algorithm-details)
- [How the Algorithm Works](#how-the-algorithm-works)
- [Next Steps](#next-steps)
- [References](#references)

## Description

The algorithm takes a set of packages and a set of vehicles, then determines the optimal way to pack the packages into the vehicles, considering possible rotations of the packages. It can either find the smallest vehicle that accommodates all packages or the best combination of vehicles to maximize load accommodation.

## Dependencies

- `argparse`
- `csv`
- `collections`

## Usage

```bash
python transport.py [-h] [--v V] [--p P] [--d] [--l]
```

### Optional Arguments

- `-h, --help`    : Shows the help message and exits.
- `--v V`         : Path to the .csv file of vehicles (columns: "Platform", "Name", "Width", "Height", "Thickness", "Weight").
- `--p P`         : Path to the .csv file of packages (columns: "Name", "Width", "Height", "Thickness", "Weight").
- `--d, --dist`   : Distributes the packages among vehicles.
- `--l, --list`   : Lists the packed packages in a .txt file.

### Example

```bash
python cargoOptimizer_3DBP.py --v vehicles.csv --p packages.csv --d --l
python -m unittest cargoOptimizer_3DBP_unittest.py
```

## Algorithm Details

### Classes

- **Package**: Represents a package with dimensions and weight.
- **Vehicle**: Represents a vehicle with specific platform and weight limits. Inherits from `Package`.

### Functions

- **parse_arguments()**: Parses command line arguments.
- **read_vehicles(file_path)**: Reads vehicles from a CSV file.
- **read_packages(file_path)**: Reads packages from a CSV file.
- **packer(vehicle, packages)**: Attempts to pack all packages into the given vehicle.
- **get_pivots(vehicle)**: Generates potential pivot points for placing new packages.
- **classifier(platforms, packages)**: Classifies the best vehicle or combination of vehicles to pack the packages.

## How the Algorithm Works

This 3D Bin Packing algorithm follows several key steps to optimize the packing of packages into vehicles:

1. **Input Parsing**:
   - The algorithm starts by parsing command line arguments to determine the input CSV files for vehicles and packages.

2. **Reading Input Files**:
   - `read_vehicles(file_path)`: Reads vehicle data from the provided CSV file and organizes them into a dictionary based on their platforms.
   - `read_packages(file_path)`: Reads package data from the provided CSV file and stores them in a list.

3. **Packing Logic**:
   - The main packing logic is handled by the `packer` function:
     - Packages are sorted by volume and weight in descending order to optimize packing efficiency.
     - For each package, the algorithm attempts to pack it into the vehicle by checking all six possible rotations.
     - If the package fits without colliding with already packed packages, it is placed at the specified pivot point.
     - If no rotation fits, the package is marked as unpacked.

4. **Pivot Point Generation**:
   - The `get_pivots` function generates potential pivot points for placing new packages based on the coordinates of already packed packages.

5. **Classification**:
   - The `classifier` function determines the best vehicle or combination of vehicles for packing the packages:
     - Vehicles are sorted by volume.
     - The `packer` function is called for each vehicle to attempt packing the packages.
     - If the `--dist` option is specified, the algorithm distributes packages across multiple vehicles to maximize load accommodation.
     - The results are printed and optionally saved to text files.

6. **Output**:
   - The algorithm outputs the results, including the percentage of packages accommodated by each vehicle or the best combination of vehicles.

## Next Steps

The current lower bound for the classical 3D Bin Packing Problem (3DBP) in the literature is defined by the work of Gzara, Elhedhli, and Yildiz (2020). Zhang, Yao, Kan, and Luo (2024) also proposes an interesting approach using a GAN-based genetic algorithm.

- Gzara, F., Elhedhli, S. & Yildiz, B. C. "The pallet loading problem: Three-dimensional bin packing with practical constraints." Eur. J. Oper. Res. 287, 1062–1074. (2020)
- Zhang, B., Yao, Y., Kan, H.K. et al. A GAN-based genetic algorithm for solving the 3D bin packing problem. Sci Rep 14, 7775 (2024).

## References

- Dube & Kanavathy. "Optimizing Three-Dimensional Bin Packing Through Simulation." Sixth IASTED International Conference Modelling, Simulation, and Optimization. 2006.