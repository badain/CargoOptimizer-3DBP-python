#########################################################################
# Description: 3D Bin Packing optimization algorithm: given a set of packages, optimize their transport in a set of vehicles.
# Dependencies: argparse, csv, collections
# Usage: transport.py [-h] [--v V] [--p P] [--d] [--l]
# Optional arguments:
#     -h, --help    shows help message and exit
#    --v V          path to the .csv file of vehicles ["Platform", "Name", "Width", "Height", "Thickness", "Weight"]
#    --p P          path to the .csv file of packages  ["Name", "Width", "Height", "Thickness", "Weight"]
#    --d, --dist    distributes the packages among vehicles
#    --l, --list    lists the packed packages in a .txt file
#
# Ref: Dube & Kanavathy. "Optimizing Three-Dimensional Bin Packing Through Simulation." Sixth IASTED International Conference Modelling, Simulation, and Optimization. 2006.
##########################################################################

# Dependencies
from collections import defaultdict
import argparse
import csv

# Argument Parsing
def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='3D Bin Packing optimization algorithm')
    parser.add_argument('--v', metavar='V', help='path to the .csv file of vehicles', required=False)
    parser.add_argument('--p', metavar='P', help='path to the .csv file of packages', required=False)
    parser.add_argument('--d', '--dist', default=False, action='store_true', help='distributes the packages among vehicles')
    parser.add_argument('--l', '--list', default=False, action='store_true', help='lists the packed packages in a .txt file')
    return parser.parse_args()

# Classes
class Package:
    """
    Class representing a package with dimensions and weight.
    """
    def __init__(self, name, w, t, h, weight):
        self.__name = name
        self.__weight = weight
        self.__height = h
        self.__width = w
        self.__thickness = t
        self.__volume  = w * h * t
        self.__currentRotation = 0
        self.__coordinate = [0, 0, 0] # vertex position (Bottom Rear Left) of the Package in 3D space [width, thickness, height]

    def get_name(self):
        return self.__name

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_thickness(self):
        return self.__thickness

    def get_weight(self):
        return self.__weight

    def get_volume(self):
        return self.__volume

    def get_rotation(self, type):
        if   type == 0: return [self.__width, self.__thickness, self.__height]
        elif type == 1: return [self.__width, self.__height, self.__thickness]
        elif type == 2: return [self.__thickness, self.__height, self.__width]
        elif type == 3: return [self.__thickness, self.__width, self.__height]
        elif type == 4: return [self.__height, self.__width, self.__thickness]
        elif type == 5: return [self.__height, self.__thickness, self.__width]

    def set_rotation_type(self, type):
        self.__currentRotation = type

    def get_rotation_type(self):
        return self.__currentRotation

    def get_size(self):
        return self.get_rotation(self.__currentRotation)

    def set_coordinate(self, coordinate):
        self.__coordinate = coordinate

    def get_coordinate(self):
        return self.__coordinate

    def get_max_width(self):
        return self.__coordinate[0] + self.__width

    def get_max_thickness(self):
        return self.__coordinate[1] + self.__thickness

    def get_max_height(self):
        return self.__coordinate[2] + self.__height

class Vehicle(Package):
    """
    Class representing a vehicle with specific platform and weight limits.
    Inherits from Package.
    """
    def __init__(self, platform, name, w, t, h, weight):
        self._Package__name = name
        self._Package__height = h
        self._Package__width = w
        self._Package__thickness = t
        self._Package__volume  = w * h * t 
        self.__weightLimit = weight        
        self.__loadedWeight = 0
        self.__packagesInside = []
        self.__packagesOutside = []
        self.__occupiedPivots = []
        self.__platform = platform

    def get_platform(self):
        return self.__platform

    def get_packed_packages(self):
        return self.__packagesInside

    def get_unpacked_packages(self):
        return self.__packagesOutside

    def get_occupied_pivots(self):
        return self.__occupiedPivots

    def set_occupied_pivot(self, pivot):
        self.__occupiedPivots.append(pivot)

    def add_packed_package(self, package):
        self.__packagesInside.append(package)

    def add_unpacked_package(self, package):
        self.__packagesOutside.append(package)

    def add_loaded_weight(self, weight):
        self.__loadedWeight += weight

    def get_loaded_weight(self):
        return self.__loadedWeight

    def get_weight_limit(self):
        return self.__weightLimit

    def get_available_weight(self):
        return self.__weightLimit - self.__loadedWeight

    def get_packed_volume(self):
        volume = 0
        for package in self.__packagesInside:
            volume += package.get_volume()
        return volume

    def get_available_volume(self):
        return self._Package__volume - self.get_packed_volume()

    def clear(self):
        self.__loadedWeight = 0
        self.__packagesInside = []
        self.__packagesOutside = []

    def pack(self, package, pivot):
        """
        Attempt to pack a package into the vehicle at the given pivot.
        """
        for rotation in range(6):
            packageSize = package.get_rotation(rotation)
            if (self._Package__width - pivot[0]) < packageSize[0]:
                continue
            if (self._Package__thickness - pivot[1]) < packageSize[1]:
                continue
            if (self._Package__height - pivot[2]) < packageSize[2]:
                continue
            collided = False
            for packed in self.__packagesInside:
                packedCoordinate = packed.get_coordinate()
                if ((packedCoordinate[0] < (pivot[0] + packageSize[0]) and packed.get_max_width() > pivot[0]) and
                    (packedCoordinate[1] < (pivot[1] + packageSize[1]) and packed.get_max_thickness() > pivot[1]) and
                    (packedCoordinate[2] < (pivot[2] + packageSize[2]) and packed.get_max_height() > pivot[2])):
                    collided = True
                    break
            if not collided:
                package.set_rotation_type(rotation)          # success: change current package rotation
                package.set_coordinate(pivot)                # success: position the package at the pivot (Bottom Rear Left)
                self.set_occupied_pivot(pivot)               # success: position the package at the pivot
                self.add_packed_package(package)             # success: insert package into vehicle's packed packages
                self.add_loaded_weight(package.get_weight()) # success: add the package weight to the load
                return True # if all checks are passed, the package is <= the available space
        return False # if no rotation returns True, then no rotation fits the package

# Packer
def packer(vehicle, packages):
    """
    Attempt to pack all packages into the given vehicle.
    """
    sorted_packages = sorted(packages, key=lambda p: (p.get_volume(), p.get_weight()), reverse=True)  # Sort packages by volume and weight
    for package in sorted_packages:
        packageFit = False

        if (vehicle.get_available_weight() < package.get_weight()) or (vehicle.get_available_volume() < package.get_volume()):
            vehicle.add_unpacked_package(package)
            continue

        if len(vehicle.get_packed_packages()) == 0:
            packageFit = vehicle.pack(package, [0, 0, 0])
            if not packageFit:
                vehicle.add_unpacked_package(package)  # if the package didn't fit in the empty vehicle,
                continue                               # it is larger or heavier than the vehicle
        
        # Pivot Selection: vehicle loaded with at least one package
        else:
            pivots = get_pivots(vehicle)
            for pivot in pivots:
                if pivot in vehicle.get_occupied_pivots():
                    continue
                    
                packageFit = vehicle.pack(package, pivot)  # if the package fits, its information is added to the vehicle
                if packageFit:
                    break # if the package was packed, there's no need to check other pivots

        # If no attempt fit the package, it remains outside
        if not packageFit:
            vehicle.add_unpacked_package(package)

def get_pivots(vehicle):
    """
    Generate potential pivot points for placing new packages.
    """
    pivots = set()
    for packed in vehicle.get_packed_packages():
        packedCoordinate = packed.get_coordinate()
        packedSize = packed.get_size()
        pivots.add((packedCoordinate[0] + packedSize[0], packedCoordinate[1], packedCoordinate[2]))  # [Bottom Rear Right]
        pivots.add((packedCoordinate[0], packedCoordinate[1] + packedSize[1], packedCoordinate[2]))  # [Bottom Front Left]
        pivots.add((packedCoordinate[0], packedCoordinate[1], packedCoordinate[2] + packedSize[2]))  # [Top Rear Left]
    return list(pivots)

# Classifier
def classifier(platforms, packages):
    """
    Classify the best vehicle or combination of vehicles to pack the packages.
    """
    if not args.d:
        print("Smallest vehicle that accommodates the maximum load:")
    else:
        print("Best combination of vehicles that accommodates the maximum load:")
    
    for platform in platforms.keys():
        packagePercentage = {}
        packageCount = {}
        packageNames = {}

        vehicles = platforms.get(platform)
        vehicles.sort(key=lambda vehicle: vehicle.get_volume())  # Sort vehicles by volume
        unpackedPackages = packages

        for vehicle in vehicles:
            packer(vehicle, unpackedPackages)
            packagePercentage[vehicle.get_name()] = (len(vehicle.get_packed_packages()) / len(packages))  # Store the % of load carried for each vehicle
            packageCount[vehicle.get_name()] = (len(vehicle.get_packed_packages()))                       # Store the raw count of load carried for each vehicle
            packageNames[vehicle.get_name()] = (vehicle.get_packed_packages())                            # Store the packages loaded in each vehicle
            
            if len(vehicle.get_packed_packages()) == len(packages):  # Early termination if all packages are packed
                break
            if args.d:  # Only unpacked packages will be sent
                unpackedPackages = vehicle.get_unpacked_packages()
            if args.d and len(unpackedPackages) == 0:  # End the loop if there are no more packages to load
                break
        
        # Output
        if not args.d:
            bestOption = max(packagePercentage, key=packagePercentage.get)
            print(f"{platform} | {bestOption} | Packages accommodated: {(packagePercentage[bestOption]*100)}%")
            if args.l:
                with open(f"best_individual_vehicle_{platform}.txt", "w") as packageList:
                    packageList.write(f"{platform} = {bestOption}\n")
                    for package in packageNames[bestOption]:
                        packageList.write(f"{package.get_name()}\n")
        else:
            print(f"{platform}: {sum(packageCount.values())} packages occupied")
            if args.l:
                with open(f"best_combination_{platform}.txt", "w") as packageList:
                    packageList.write(f"{platform}:\n")
                for vehicle in packageCount:
                    print(f"{vehicle} | Packages Occupied: {(packageCount[vehicle])}")
                    if args.l:
                        with open(f"best_combination_{platform}.txt", "a") as packageList:
                            packageList.write(f"{vehicle}\n")
                            for package in packageNames[vehicle]:
                                packageList.write(f"{package.get_name()}\n")

# Input
def read_vehicles(file_path):
    """
    Read vehicles from the CSV file.
    """
    platforms = defaultdict(list)
    with open(file_path, 'rt') as f:
        csv_vehicles = csv.reader(f, skipinitialspace=True)
        next(csv_vehicles)
        for row in csv_vehicles:
            platforms[row[0]].append(Vehicle(row[0], row[1], int(row[2]), int(row[3]), int(row[4]), int(row[5])))
    return platforms

def read_packages(file_path):
    """
    Read packages from the CSV file.
    """
    packages = []
    with open(file_path, 'rt') as f:
        csv_packages = csv.reader(f, skipinitialspace=True)
        next(csv_packages)
        for row in csv_packages:
            packages.append(Package(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4])))
    return packages

# Main
if __name__ == "__main__":
    args = parse_arguments()

    # Default vehicles and packages if no CSV paths are provided
    if args.v:
        platforms = read_vehicles(args.v)
    else:
        platforms = {
            'Platform1': [Vehicle('Platform1', 'Vehicle1', 10, 10, 10, 50),
                          Vehicle('Platform1', 'Vehicle2', 15, 15, 15, 75)]
        }

    if args.p:
        packages = read_packages(args.p)
    else:
        packages = [Package(f"Package{i}", 1, 1, 1, 1) for i in range(10)]

    classifier(platforms, packages)