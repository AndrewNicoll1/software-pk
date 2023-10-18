import unittest
import pytest
import pkmodel
from pkmodel.model import Model


class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def test_create(self):
        """
        Tests Model creation.
        """
        model = pkmodel()
        self.assertEqual(model.value, 42)



class TestDoseFunction(unittest.TestCase):
    
    def test_valid_number_input(self):
        # Test with a valid numeric input
        model_args = {'X': 5.0}  # Replace with your actual model parameters
        model = Model(model_args=model_args)  
        result = model.dose(1.0)
        self.assertIsInstance(result, (int, float), "Input must be a number (int or float)")
    
    def test_invalid_string_input(self):
        # Test with an invalid string input
        model_args = {'X': "invalid"}  # Replace with your actual model parameters
        model = Model(model_args=model_args)  
        with self.assertRaises(AssertionError):
            result = model.dose(1.0)

if __name__ == '__main__':
    unittest.main()
