from PLPlaneSweep import PersistantLandscape

bd_pairs = [(1, 3)]
pl = PersistantLandscape(bd_pairs, 2)
landscapes = pl.generate_landscapes()
print(landscapes)
