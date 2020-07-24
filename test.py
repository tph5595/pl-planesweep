""" test: used to test the other files in this project """
from pl_planesweep import PersistantLandscape

bd_pairs = [(0, 6), (1, 3), (2, 7)]
pl = PersistantLandscape(bd_pairs, 4)
landscapes = pl.generate_landscapes()
pl.plot()
print(landscapes)
