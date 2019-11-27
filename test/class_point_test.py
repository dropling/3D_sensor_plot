import unittest

from src.windows.data_and_plotting.data_management.objects.class_point import Point

class TestPoint(unittest.TestCase):

    point_1 = None
    point_2 = None
    point_3 = None
    point_4 = None
    
    def test_settin_points(self):
        
        # creating points
        self.point_1 = Point(ID='1', x=1, y=1, z=1)
        self.point_2 = Point(ID='2', x=2.0, y=2.0, z=2.0)
        self.point_3 = Point(ID='3', x=3.00, y=3.00, z=3.00)
        self.point_4 = Point(ID='4', x=1.49, y=7.16, z=8.151)
        
        # check IDs and coordinates
        self.assertEqual(self.point_1.ID, '1', "Error in point_1.ID")
        self.assertEqual(self.point_1.x, 1, "Error in point_1.x")
        self.assertEqual(self.point_1.y, 1, "Error in point_1.y")
        self.assertEqual(self.point_1.z, 1, "Error in point_1.z")
        
        self.assertEqual(self.point_2.ID, '2', "Error in point_2.ID")
        self.assertEqual(self.point_2.x, 2, "Error in point_2.x")
        self.assertEqual(self.point_2.y, 2, "Error in point_2.y")
        self.assertEqual(self.point_2.z, 2, "Error in point_2.z")
        
        self.assertEqual(self.point_3.ID, '3', "Error in point_3.ID")
        self.assertEqual(self.point_3.x, 3, "Error in point_3.x")
        self.assertEqual(self.point_3.y, 3, "Error in point_3.y")
        self.assertEqual(self.point_3.z, 3, "Error in point_3.z")
        
        self.assertEqual(self.point_4.ID, '4', "Error in point_4.ID")
        self.assertEqual(self.point_4.x, 1.49, "Error in point_4.x")
        self.assertEqual(self.point_4.y, 7.16, "Error in point_4.y")
        self.assertEqual(self.point_4.z, 8.151, "Error in point_4.z")
        
        self.assertEqual(self.point_1.adjacent_points_add([self.point_2, self.point_3, self.point_4]), True, "Error in point_1.adjacent_points_add")
        self.assertEqual(self.point_2.adjacent_points_add([self.point_1.ID, self.point_3.ID, self.point_4.ID]), True, "Error in point_2.adjacent_points_add")
        self.assertEqual(self.point_3.adjacent_points_add([self.point_1, self.point_2.ID, self.point_4]), True, "Error in point_3.adjacent_points_add")
        
        self.assertEqual(self.point_1.return_adjacent_points().difference({'2','3','4'}), set(), "Difference between is and should int point_1_set")
        self.assertEqual(self.point_2.return_adjacent_points().difference({'1','3','4'}), set(), "Difference between is and should int point_2_set")
        self.assertEqual(self.point_3.return_adjacent_points().difference({'1','2','4'}), set(), "Difference between is and should int point_2_set")
            

if __name__ == '__main__':
    unittest.main()
