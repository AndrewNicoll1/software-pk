import unittest
import pytest
import pkmodel as pk


class TestDoseFunction(unittest.TestCase):

    def test_dose_returns_constant_value(self):
        # Define the expected constant value 'X'
        expected_constant_value = 100000.0  # Replace with your expected constant value

        # Define a list of time points to test
        time_points = [0.0, 1.0, 2.0, 3.0] 

        for t in time_points:
            result = pk.dose(t, expected_constant_value)
            self.assertEqual(result, expected_constant_value, f"dose({t}) should return {expected_constant_value}")
    

class TestRHSFunction(unittest.TestCase):

    def test_rhs_with_known_parameters(self):
        # Define known model parameters
        Q_p1 = 1.0
        V_c = 1.0
        V_p1 = 1.0
        CL = 1.0
        X = 1.0

        # Define the initial state variables
        initial_state = [0.0, 0.0]

        # Time point for testing
        t = 55555555555555555555.7  # Replace with the desired time point

        # Calculate the expected rate of change manually based on known parameters
        q_c, q_p1 = initial_state
        transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
        expected_dqc_dt = pk.dose(t, X) - q_c / V_c * CL - transition
        expected_dqp1_dt = transition

        # Calculate the rate of change using the rhs function
        result = pk.rhs(t, initial_state, Q_p1, V_c, V_p1, CL, X)

        # Assert that the calculated rates match the expected rates
        self.assertAlmostEqual(result[0], expected_dqc_dt, places=6, msg="Rate of change of q_c does not match expected value")
        self.assertAlmostEqual(result[1], expected_dqp1_dt, places=6, msg="Rate of change of q_p1 does not match expected value")

class TestModelSimulation(unittest.TestCase):

    def test_model_simulation_with_known_parameters(self):
        # Define known model parameters
        Q_p1 = 1.0
        V_c = 1.0
        V_p1 = 1.0
        CL = 1.0
        X = 1.0

        # Define the initial state variables
        initial_state = [0.0, 0.0]

        # Define the time points for testing
        time_points = [0.0, 0.1, 0.2, 0.3]  # Replace with desired time points

        # Create lists to store the expected values for q_c and q_p1
        expected_q_c_values = []
        expected_q_p1_values = []

        for t in time_points:
            # Calculate the expected rate of change manually based on known parameters
            q_c, q_p1 = initial_state
            transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
            expected_dqc_dt = X - q_c / V_c * CL - transition
            expected_dqp1_dt = transition

            # Update the state variables based on the calculated rates
            q_c += expected_dqc_dt * (t - time_points[0])
            q_p1 += expected_dqp1_dt * (t - time_points[0])

            # Append the expected values to the lists
            expected_q_c_values.append(q_c)
            expected_q_p1_values.append(q_p1)

        # Perform model simulation using the rhs function
        model_simulation = self.simulate_model(initial_state, Q_p1, V_c, V_p1, CL, X, time_points)

        # Assert that the model simulation matches the expected values
        self.assertListEqual(model_simulation[0], expected_q_c_values, "q_c values do not match expected values")
        self.assertListEqual(model_simulation[1], expected_q_p1_values, "q_p1 values do not match expected values")

    def simulate_model(self, initial_state, Q_p1, V_c, V_p1, CL, X, time_points):
        # Function to simulate the model and return q_c and q_p1 values at specified time points
        q_c, q_p1 = initial_state
        simulated_q_c = [q_c]
        simulated_q_p1 = [q_p1]

        for t in time_points[1:]:
            q_c, q_p1 = pk.rhs(t, [q_c, q_p1], Q_p1, V_c, V_p1, CL, X)
            simulated_q_c.append(q_c)
            simulated_q_p1.append(q_p1)

        return [simulated_q_c, simulated_q_p1]
    
class TestPharmacokineticModels(unittest.TestCase):

    def test_TwoCellModelInitialization(self):
        # Test the initialization of the TwoCellModel class
        model_args = {
            'name': 'model1',
            'Q_p1': 1.0,
            'V_c': 2.0,
            'V_p1': 3.0,
            'CL': 4.0,
            'X': 5.0,
        }
        model = pk.TwoCellModel(model_args)
        
        self.assertEqual(model.name, 'Two cell model')
        self.assertEqual(model.Q_p1, 1.0)
        self.assertEqual(model.V_c, 2.0)
        self.assertEqual(model.V_p1, 3.0)
        self.assertEqual(model.CL, 4.0)
        self.assertEqual(model.X, 5.0)
        self.assertEqual(model.dim, 2)

    def test_ThreeCellModelInitialization(self):
        # Test the initialization of the ThreeCellModel class
        model_args = {
            'name': 'model2',
            'Q_p1': 2.0,
            'V_c': 3.0,
            'V_p1': 4.0,
            'CL': 5.0,
            'X': 6.0,
            'k_a': 7.0,
            'q0': 8.0,
        }
        model = pk.ThreeCellModel(model_args)
        
        self.assertEqual(model.name, 'Three cell model')
        self.assertEqual(model.Q_p1, 2.0)
        self.assertEqual(model.V_c, 3.0)
        self.assertEqual(model.V_p1, 4.0)
        self.assertEqual(model.CL, 5.0)
        self.assertEqual(model.X, 6.0)
        self.assertEqual(model.k_a, 7.0)
        self.assertEqual(model.q0, 8.0)
        self.assertEqual(model.dim, 3)

    def test_TwoCellModelDoseFunction(self):
        # Test the dose function of the TwoCellModel
        model_args = {
            'name': 'model1',
            'Q_p1': 1.0,
            'V_c': 2.0,
            'V_p1': 3.0,
            'CL': 4.0,
            'X': 5.0,
        }
        model = pk.TwoCellModel(model_args)
        
        # Test the dose function at a specific time
        t = 0.5
        expected_dose = 5.0  # X is 5.0
        self.assertEqual(model.dose(t), expected_dose)

    def test_ThreeCellModelDoseFunction(self):
        # Test the dose function of the ThreeCellModel
        model_args = {
            'name': 'model2',
            'Q_p1': 2.0,
            'V_c': 3.0,
            'V_p1': 4.0,
            'CL': 5.0,
            'X': 6.0,
            'k_a': 7.0,
            'q0': 8.0,
        }
        model = pk.ThreeCellModel(model_args)
        
        # Test the dose function at a specific time
        t = 0.5
        expected_dose = 6.0  # X is 6.0
        self.assertEqual(model.dose(t), expected_dose)

if __name__ == '__main__':
    unittest.main()
