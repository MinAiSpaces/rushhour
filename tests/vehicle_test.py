import unittest

from code.classes import Vehicle, VehicleMoveViolationError, Orientation


class TestVehicleClass(unittest.TestCase):
    def setUp(self):
        """
        Setup function for the Vehicle class tests

        Generates 3 vehicles
        - 1 vehicle with length 2 and Orientation.HORIZONTAL
        - 1 vehicle with length 3 and Orientation.VERTICAL
        - 1 vehicle with 'is_carter == True' vehicle with length 2 and Orientation.HORIZONTAL
        """
        self.test_values = {
            'names': ['A', 'B', 'X'],
            'orientations': [Orientation.HORIZONTAL, Orientation.VERTICAL, Orientation.HORIZONTAL],
            'start_cols': [1, 3, 4],
            'start_rows': [2, 3, 3],
            'lengths': [2, 3, 2],
        }

        self.vehicles = [
            Vehicle(
                name,
                orientation,
                start_col,
                start_row,
                length
            )
            for name, orientation, start_col, start_row, length in zip(
                self.test_values['names'],
                self.test_values['orientations'],
                self.test_values['start_cols'],
                self.test_values['start_rows'],
                self.test_values['lengths']
            )
        ]

    def test_vehicle_init(self):
        """
        Test if the Vehicle object is initialized properly
        """
        # Check if vehicles have the correct attributes and values
        for idx, vehicle in enumerate(self.vehicles):
            self.assertIsInstance(vehicle, Vehicle)
            self.assertEqual(vehicle.name, self.test_values['names'][idx])
            self.assertEqual(vehicle.start_col, self.test_values['start_cols'][idx])
            self.assertEqual(vehicle.start_row, self.test_values['start_rows'][idx])
            self.assertEqual(vehicle.is_carter, False if idx != 2 else True)
            self.assertEqual(len(vehicle.location), self.test_values['lengths'][idx])

        # Vehicle 1 should occupy 2 squares in horizontal direction
        self.assertEqual(self.vehicles[0].location, [
            (self.test_values['start_cols'][0], self.test_values['start_rows'][0]),
            (self.test_values['start_cols'][0] + 1, self.test_values['start_rows'][0]),
        ])

        # Vehicle 2 should occupy 3 squares in vertical direction
        self.assertEqual(self.vehicles[1].location, [
            (self.test_values['start_cols'][1], self.test_values['start_rows'][1]),
            (self.test_values['start_cols'][1], self.test_values['start_rows'][1] + 1),
            (self.test_values['start_cols'][1], self.test_values['start_rows'][1] + 2),
        ])

        # Vehicle 3 should occupy 2 squares in horizontal direction
        self.assertEqual(self.vehicles[2].location, [
            (self.test_values['start_cols'][2], self.test_values['start_rows'][2]),
            (self.test_values['start_cols'][2] + 1, self.test_values['start_rows'][2]),
        ])

    def test_vehicle_update_location(self):
        """
        Test if update_location method updates the vehicle location correctly

        Update location of a vehicle by passing a new start coordinate and:
        - check if we still have the same number of coordinates
        - if the front and the back of the vehicle have moved the expected number of steps
        """
        for idx, vehicle in enumerate(self.vehicles):
            vehicle_coords_old = vehicle.location
            col_vehicle_back_old, row_vehicle_back_old = vehicle_coords_old[0]
            col_vehicle_front_old, row_vehicle_front_old = vehicle_coords_old[-1]
            steps = 2

            if vehicle.orientation == Orientation.HORIZONTAL:
                vehicle.update_location(col_vehicle_back_old + steps, row_vehicle_back_old)

                self.assertEqual(len(vehicle_coords_old), len(vehicle.location))
                self.assertEqual(vehicle.location[0], (col_vehicle_back_old + steps, row_vehicle_back_old))
                self.assertEqual(vehicle.location[-1], (col_vehicle_front_old + steps, row_vehicle_front_old))
            else:
                vehicle.update_location(col_vehicle_back_old, row_vehicle_back_old + steps)

                self.assertEqual(len(vehicle_coords_old), len(vehicle.location))
                self.assertEqual(vehicle.location[0], (col_vehicle_back_old, row_vehicle_back_old + steps))
                self.assertEqual(vehicle.location[-1], (col_vehicle_front_old, row_vehicle_front_old + steps))

    def test_vehicle_update_location_violation(self):
        """
        Test if update_location method raises an error on an illegal update

        Depending on a vehicles orientation a vehicle cannot change row or column

        Try to update vehicle location by supplying an illegal new start coordinate and:
        - check if it correctly raises an error
        """
        for idx, vehicle in enumerate(self.vehicles):
            vehicle_coords_old = vehicle.location
            col_vehicle_back_old, row_vehicle_back_old = vehicle_coords_old[0]
            steps = 2

            if vehicle.orientation == Orientation.HORIZONTAL:
                # If vehicle orientation is HORIZONTAL a vehicle can't change rows
                with self.assertRaises(VehicleMoveViolationError) as cm:
                    vehicle.update_location(col_vehicle_back_old, row_vehicle_back_old + steps)
            else:
                # If vehicle orientation is VERTICAL a vehicle can't change columns
                with self.assertRaises(VehicleMoveViolationError) as cm:
                    vehicle.update_location(col_vehicle_back_old + steps, row_vehicle_back_old)
