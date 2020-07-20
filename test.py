from PLPlaneSweep import PersistantLandscape

bd_pairs = [(0, 6), (2, 7)]
pl = PersistantLandscape(bd_pairs, 4)
landscapes = pl.generate_landscapes()
print(landscapes)
