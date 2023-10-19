#
# Solution class
#
import pkmodel as pk
import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt

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

    def __init__(self, model, T=1., n=1000, y0=None):
        assert issubclass(type(model), pk.BaseModel), "model is not a PK model type"
        self.model = model

        # time array t_eval to evaluate the model over a range of time points.
        t_eval = np.linspace(0, T, n)
        self.t_eval = t_eval

        #initialize the initial conditions for the state variables in y0.
        if y0 is None:
            y0 = np.zeros(len(model), dtype=np.float64)
        self.y0 = y0

    def solve(self):
        '''Solve the pharmacokinetic model using scipy.integrate.solve_ivp'''
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: self.model.rhs(t, y),
            t_span=[self.t_eval[0], self.t_eval[-1]],
            y0=self.y0, t_eval=self.t_eval
            ) 
        self.sol = sol

    def plot(self, ax=None):
        '''plot the results for both q_c and q_p1 over time'''

        try:
            sol = self.sol  # Ensure .solve has been run
        except:
            raise AttributeError('Run `.solve` method first')

        if ax is None:  # create a Matplotlib figure for plotting.
            fig = plt.figure()
            ax = plt
        ax.plot(sol.t, sol.y[0, :], label=self.model.name + '- q_c')
        if len(self.model) == 2:
            ax.plot(sol.t, sol.y[1, :], label=self.model.name + '- q_p1')
        elif len(self.model) == 3:
            ax.plot(sol.t, sol.y[1, :], label=self.model.name + '- q_p0')
            ax.plot(sol.t, sol.y[2, :], label=self.model.name + '- q_p1')

        # Add labels, legends, and axis labels to the plot.
        if ax == plt:
            ax.legend()
            ax.ylabel('drug mass [ng]')
            ax.xlabel('time [h]')
            plt.show()
    
    def plotDose(self, ax=None):
        if ax is None:  # create a Matplotlib figure for plotting.
            fig = plt.figure()
            ax = plt
        ax.plot(self.t_eval, self.model.dose(self.t_eval), label=self.model.name + 'dosing')

        # Add labels, legends, and axis labels to the plot.
        if ax == plt:
            ax.legend()
            ax.ylabel('drug mass [ng]')
            ax.xlabel('time [h]')
            plt.show()













