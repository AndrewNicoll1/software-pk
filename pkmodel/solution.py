#
# Solution class
#

class Solution:
    """A Pharmokinetic (PK) model solver

    Parameters
    ----------

    model: class
        Class from model.py describing the PK model
    T: float, optional
        End time, defaults to 1
    n: int, optional
        Number of timesteps, defaults to 1000
    y0: np.array (float), optional
        Two initial conditions for q_c and q_p1, 
        defaults to [0,0]
    """
    import pkmodel as pk
    import numpy as np
    import scipy.integrate

    def __init__(self, model, T=1., n=1000, y0=None):
        assert type(model)==pk.Model, "model is not a PK model type"
        self.model = model

        # time array t_eval to evaluate the model over a range of time points.
        t_eval = np.linspace(0, T, n)
        self.t_eval = t_eval

        #initialize the initial conditions for the state variables in y0.
        if y0 is None:
            y0 = np.array([0.0, 0.0])
        self.y0 = y0

    def solve(self):
        '''Solve the pharmacokinetic model using scipy.integrate.solve_ivp'''
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: self.model.rhs(t, y),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval
            ) 
        self.sol = sol

    def plot(self, show=True):
        '''plot the results for both q_c and q_p1 over time'''
        # create a Matplotlib figure for plotting.
        fig = plt.figure()

        sol = self.sol
        plt.plot(sol.t, sol.y[0, :], label=self.model.name + '- q_c')
        plt.plot(sol.t, sol.y[1, :], label=self.model.name + '- q_p1')
        # Add labels, legends, and axis labels to the plot.
        plt.legend()
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')
        if show:
            plt.show()












