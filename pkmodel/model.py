#
# Model class
#
import pkmodel.dosing
class BaseModel:
    """A Pharmokinetic (PK) model

    Parameters
    ----------

    model_args: dict, optional
        Dictionary of model parameters.
        Defaults to all 1s if None is passed.
        Must include
    dose: func, optional
        The dosing function Dose(t).
        Defaults to constant concentration X.

    """
    def __init__(self, model_args=None, dose=None):
        
        if model_args is None:
            model_args = {
                'name': 'model',
                'Q_p1': 1.,
                'V_c': 1.,
                'V_p1': 1.,
                'CL': 1.,
                'X': 1.,
             }
        else:
            keys = ['name', 'Q_p1', 'V_c', 'V_p1', 'CL', 'X']
            assert set(keys) <= model_args.keys, "Invalid model arrguments"
        
        if dose is None:
            def dose(t):
                '''Define a function dose(t) that represents the drug dose as a function of time. 
                It's a simple function that returns a constant dose X at any given time t.'''
                return pkmodel.dosing.constant(model_args['X'])(t)
        
        self.model_args = model_args
        self.__dict__.update(model_args)  # Saves all params
        self.dose = dose
        self.dim = 0
    
    def __len__(self):
        return self.dim

    def __str__(self):
        return self.name

class TwoCellModel(BaseModel):
    def __init__(self, model_args=None, dose=None):
        super(TwoCellModel, self).__init__(model_args, dose)
        def rhs(t, y):
            '''Define the right-hand side (rhs) function
            This function represents the pharmacokinetic model, with q_c and q_p1 as state variables. 
            It calculates the rate of change of these variables based on the given parameters and drug dose function.'''
            q_c, q_p1 = y
            transition = self.Q_p1 * (q_c / self.V_c - q_p1 / self.V_p1)
            dqc_dt = self.dose(t) - q_c / self.V_c * self.CL - transition
            dqp1_dt = transition
            return [dqc_dt, dqp1_dt]
        
        self.rhs = rhs 
        self.dim = 2

        if self.name == 'model':
            self.name = "Two cell model"



Model = TwoCellModel


class ThreeCellModel(BaseModel):
    def __init__(self, model_args=None, dose=None):
        super(ThreeCellModel, self).__init__(model_args, dose)

        if 'k_a' not in self.model_args.keys():
            self.k_a = 1.
        if 'q0' not in self.model_args.keys():
            self.q0 = 1.

        def rhs(t, y):
            '''Define the right-hand side (rhs) function
            This function represents the pharmacokinetic model, with q_c and q_p1 as state variables. 
            It calculates the rate of change of these variables based on the given parameters and drug dose function.'''
            q_c, q0, q_p1 = y
            transition = self.Q_p1 * (q_c / self.V_c - q_p1 / self.V_p1)
            dq0_dt = self.dose(t) - self.k_a * self.q0
            dqc_dt = self.dose(t) - dq0_dt - q_c / self.V_c * self.CL - transition
            dqp1_dt = transition
            return [dqc_dt, dq0_dt, dqp1_dt]
        
        self.rhs = rhs 
        self.dim = 3

        if self.name == 'model':
            self.name = "Three cell model"
