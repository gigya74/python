import unittest
from GetCoordinates import get_coordinates

class GetCoordinatesTestCase(unittest.TestCase):
    def test_getCoordinates(self):

        latLong = [41.88147, -87.73380639999999]
        address = "4319 W. Washington Blvd. Chicago,IL 60624"
        self.assertEqual(get_coordinates(address),latLong)