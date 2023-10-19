import pkmodel as pk


model = pk.ThreeCellModel()
sol = pk.Solution(model)
model.name = 'Test Model '
sol.solve()
sol.plot()
sol.plotDose()