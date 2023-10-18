import pkmodel as pk

model = pk.Model()
sol = pk.Solution(model)
model.name = 'Test Model '
sol.solve()
sol.plot()
