import unittest
from cargoOptimizer_3DBP import Package, Vehicle, packer

class Test3DBinPacking(unittest.TestCase):

    def setUp(self):
        # Setting up Packages (packages) and vehicles for testing
        self.package1 = Package("Package1", 2, 2, 2, 1)
        self.package2 = Package("Package2", 3, 3, 3, 2)
        self.package3 = Package("Package3", 1, 1, 1, 1)
        self.vehicle = Vehicle("Platform1", "Vehicle1", 5, 5, 5, 10)

    def test_package_volume(self):
        self.assertEqual(self.package1.get_volume(), 8)
        self.assertEqual(self.package2.get_volume(), 27)
        self.assertEqual(self.package3.get_volume(), 1)

    def test_vehicle_capacity(self):
        self.assertEqual(self.vehicle.get_volume(), 125)
        self.assertEqual(self.vehicle.get_weight_limit(), 10)

    def test_packing_single_package(self):
        packed = self.vehicle.pack(self.package1, [0, 0, 0])
        self.assertTrue(packed)
        self.assertIn(self.package1, self.vehicle.get_packed_packages())

    def test_packing_multiple_packages(self):
        packer(self.vehicle, [self.package1, self.package2, self.package3])
        packed_packages = self.vehicle.get_packed_packages()
        self.assertIn(self.package1, packed_packages)
        self.assertIn(self.package3, packed_packages)
        self.assertIn(self.package2, packed_packages)
        self.assertEqual(len(packed_packages), 3)

    def test_unpacked_packages_due_to_weight(self):
        heavy_package = Package("HeavyPackage", 1, 1, 1, 11)
        packer(self.vehicle, [heavy_package])
        self.assertIn(heavy_package, self.vehicle.get_unpacked_packages())
        self.assertEqual(len(self.vehicle.get_unpacked_packages()), 1)

    def test_unpacked_packages_due_to_volume(self):
        large_package = Package("LargePackage", 6, 6, 6, 1)
        packer(self.vehicle, [large_package])
        self.assertIn(large_package, self.vehicle.get_unpacked_packages())
        self.assertEqual(len(self.vehicle.get_unpacked_packages()), 1)

    def test_large_number_of_small_packages(self):
        n = 1000
        vehicle = Vehicle("Platform1", "Vehicle1", 100, 100, 100, 10000)
        packages = [Package(f"Package{i}", 1, 1, 1, 1) for i in range(n)]
        packer(vehicle, packages)
        self.assertEqual(len(vehicle.get_packed_packages()), n)

    def test_exceeding_weight_limit(self):
        vehicle = Vehicle("Platform1", "Vehicle1", 10, 10, 10, 10)
        packages = [Package("HeavyPackage", 1, 1, 1, 11)]
        packer(vehicle, packages)
        self.assertEqual(len(vehicle.get_packed_packages()), 0)
        self.assertEqual(len(vehicle.get_unpacked_packages()), 1)
        self.assertEqual(vehicle.get_unpacked_packages()[0].get_name(), "HeavyPackage")

    def test_exact_fit_packages(self):
        vehicle = Vehicle("Platform1", "Vehicle1", 6, 6, 6, 50)
        packages = [
            Package("Package1", 3, 3, 3, 10),
            Package("Package2", 3, 3, 3, 10),
            Package("Package3", 3, 3, 3, 10),
            Package("Package4", 3, 3, 3, 10)
        ]
        packer(vehicle, packages)
        self.assertEqual(len(vehicle.get_packed_packages()), 4)
        self.assertEqual(len(vehicle.get_unpacked_packages()), 0)

    def test_rotated_fit_packages(self):
        vehicle = Vehicle("Platform1", "Vehicle1", 5, 5, 5, 50)
        packages = [
            Package("Package1", 5, 2, 2, 5),
            Package("Package2", 5, 2, 2, 5),
            Package("Package3", 2, 5, 2, 5)
        ]
        packer(vehicle, packages)
        self.assertEqual(len(vehicle.get_packed_packages()), 3)
        self.assertEqual(len(vehicle.get_unpacked_packages()), 0)

    def test_overlapping_packages(self):
        vehicle = Vehicle("Platform1", "Vehicle1", 6, 6, 6, 50)
        package1 = Package("Package1", 3, 3, 3, 5)
        package2 = Package("Package2", 3, 3, 3, 5)
        package3 = Package("Package3", 3, 3, 3, 5)
        
        self.assertTrue(vehicle.pack(package1, [0, 0, 0]))
        self.assertFalse(vehicle.pack(package2, [1, 1, 1]))  # This should fail due to overlap
        self.assertTrue(vehicle.pack(package3, [3, 3, 3]))   # This should succeed
        
        self.assertIn(package1, vehicle.get_packed_packages())
        self.assertIn(package3, vehicle.get_packed_packages())
        self.assertNotIn(package2, vehicle.get_packed_packages())

    def test_large_package_cannot_fit(self):
        vehicle = Vehicle("Platform1", "Vehicle1", 10, 10, 10, 100)
        large_package = Package("LargePackage", 15, 15, 15, 10)
        packer(vehicle, [large_package])
        self.assertIn(large_package, vehicle.get_unpacked_packages())
        self.assertEqual(len(vehicle.get_packed_packages()), 0)

if __name__ == '__main__':
    unittest.main()
