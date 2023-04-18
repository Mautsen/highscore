import unittest
from validation import *


class TestValidation(unittest.TestCase):

    def test_validate_username(self):
        self.assertTrue(validate_username("Pimu"))
        self.assertFalse(validate_username("pimu"))
        self.assertFalse(validate_username("P imu"))  
        self.assertFalse(validate_username("P+mu")) 
        self.assertFalse(validate_username("P*imu"))
        self.assertFalse(validate_username(" Pimu")) 
        self.assertFalse(validate_username("Pimu ")) 
        self.assertFalse(validate_username("P1mu"))
        self.assertFalse(validate_username("Pimupimupimu"))
        self.assertFalse(validate_username("Kakka"))