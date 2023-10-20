import pkmodel as pk
import matplotlib.pyplot as plt

doses = [pk.dosing.constant(0.5),
         pk.dosing.pulse(1, 0.1, 0.2),
         pk.dosing.sawtooth(1, 0.1),
        pk.dosing.sawtooth(2, 0.3)]

fig, axs = plt.subplots(2, len(doses), sharex=True, figsize=(len(doses)*4, 6))

for i, dose in enumerate(doses):
    model = pk.TwoCellModel(dose=dose)
    sol = pk.Solution(model)
    model.name = ''
    sol.solve()

    sol.plot(axs.T[i])

fig.tight_layout()
fig.savefig('example')
plt.show()