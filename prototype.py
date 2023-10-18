# The code allows you to visualize how the drug concentrations in the
# central compartment (q_c) and the peripheral compartment (q_p1) 
# change over time for different sets of model parameters. 
# It provides a comparison between the two models.


# import the necessary libraries, including matplotlib.pylab for plotting, numpy for numerical operations, 
# and scipy.integrate for solving differential equations.
import matplotlib.pylab as plt
import numpy as np
import scipy.integrate

# define a function dose(t, X) that represents the drug dose as a function of time. 
# It's a simple function that returns a constant dose X at any given time t.
def dose(t, X):
    return X

# define the right-hand side (rhs) function
# rhs(t, y, Q_p1, V_c, V_p1, CL, X)
# This function represents the pharmacokinetic model, with q_c and q_p1 as state variables. 
# It calculates the rate of change of these variables based on the given parameters and drug dose function.
def rhs(t, y, Q_p1, V_c, V_p1, CL, X):
    q_c, q_p1 = y
    transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
    dqc_dt = dose(t, X) - q_c / V_c * CL - transition
    dqp1_dt = transition
    return [dqc_dt, dqp1_dt]

# define two sets of model parameters, model1_args and model2_args
# each represent different model scenarios with various parameter values.
model1_args = {
    'name': 'model1',
    'Q_p1': 1.0,
    'V_c': 1.0,
    'V_p1': 1.0,
    'CL': 1.0,
    'X': 1.0,
}

model2_args = {
    'name': 'model2',
    'Q_p1': 2.0,
    'V_c': 1.0,
    'V_p1': 1.0,
    'CL': 1.0,
    'X': 1.0,
}

# time array t_eval to evaluate the model over a range of time points.
t_eval = np.linspace(0, 1, 1000)

#initialize the initial conditions for the state variables in y0.
y0 = np.array([0.0, 0.0])

# create a Matplotlib figure for plotting.
fig = plt.figure()

# Loop through both models (model1_args and model2_args
# to solve the pharmacokinetic model for each. 
# For each model, you set the model parameters,solve the differential equations
# using scipy.integrate.solve_ivp, and then plot the results for both q_c and q_p1 over time.
for model in [model1_args, model2_args]:
    args = [
        model['Q_p1'], model['V_c'], model['V_p1'], model['CL'], model['X']
    ]
    sol = scipy.integrate.solve_ivp(
        fun=lambda t, y: rhs(t, y, *args),
        t_span=[t_eval[0], t_eval[-1]],
        y0=y0, t_eval=t_eval
    )
    plt.plot(sol.t, sol.y[0, :], label=model['name'] + '- q_c')
    plt.plot(sol.t, sol.y[1, :], label=model['name'] + '- q_p1')

# Add labels, legends, and axis labels to the plot.
plt.legend()
plt.ylabel('drug mass [ng]')
plt.xlabel('time [h]')
plt.show()
