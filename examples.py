import pkmodel as pk
import matplotlib.pyplot as plt

doses = [pk.dosing.constant(0.5),
         pk.dosing.pulse(1, 0.1, 0.2),
         pk.dosing.sawtooth(1, 0.1),
         pk.dosing.sine(0.5, 0.25),
         pk.dosing.sawtooth(2, 1/3)]

models = [pk.TwoCellModel, pk.ThreeCellModel]

for model_type in models:
    fig, axs = plt.subplots(2, len(doses), sharex=True, figsize=(len(doses)*4, 6))

    for i, dose in enumerate(doses):
        model = model_type(dose=dose)
        sol = pk.Solution(model)
        sol.solve()
        sol.plot(axs.T[i])

    fig.tight_layout()
    fig.savefig('example ' + str(model))
    plt.show()