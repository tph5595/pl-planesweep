""" test: used to test the other files in this project """
from pl_planesweep import PersistantLandscape
from barcode import BarcodeFilter

def pl_test_1():
    """ Basic test with 3 bd_pairs """
    bd_pairs = [(0, 6), (1, 3), (2, 7)]
    pl_obj = PersistantLandscape(bd_pairs, 4)
    landscapes = pl_obj.generate_landscapes()
    pl_obj.plot()
    print(landscapes)

def barcode_test_1():
    bd_pairs = [(0, 6), (1, 3), (2, 7)]
    barcode_filter = BarcodeFilter(bd_pairs, 1)
    filtered = barcode_filter.filter()
    print(filtered)

barcode_test_1()
