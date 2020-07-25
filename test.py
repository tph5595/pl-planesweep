""" test: used to test the other files in this project """
from pl_planesweep import PersistantLandscape
from barcode import BarcodeFilter

# Ripser dataset creation
import numpy as np

from ripser import ripser
import tadasets
import random


def pl_test_1():
    """ Basic test with 3 bd_pairs """
    bd_pairs = [(0, 6), (1, 3), (2, 7)]
    print(pl_runner(bd_pairs, 4))


def pl_runner(bd_pairs, k, debug=False):
    pl_obj = PersistantLandscape(bd_pairs, k)
    pl_obj.enable_debug(debug)
    landscapes = pl_obj.generate_landscapes()
    pl_obj.plot()
    return landscapes


def barcode_table_tests():
    bd_pairs = [(0, 6), (1, 3), (2, 7)]
    print(barcode_runner(bd_pairs, 1))


def barcode_runner(bd_pairs, k):
    barcode_filter = BarcodeFilter(bd_pairs, k)
    filtered = barcode_filter.filter()
    return filtered


def prep_torus(seed):
    random.seed(seed)
    data = np.concatenate([
        tadasets.dsphere(n=500, d=1, r=5, noise=0.5),
        tadasets.dsphere(n=100, d=1, r=1, noise=0.2)
    ])

    thresh = 1.5
    results0 = ripser(data, thresh=thresh, maxdim=1)

    diagrams = results0['dgms']
    return map(lambda x: (x[0], x[1]), diagrams[1])


# with k = 3
problem_pairs_1 = [(0.9748720526695251, 0.9898090958595276),
                   (0.9600228071212769, 1.029630184173584),
                   (0.8873197436332703, 0.9408737421035767)]

problem_pairs_2 = [(0.9688469171524048, 1.1520495414733887),
                   (0.957465410232544, 1.002064824104309),
                   (0.8262945413589478, 0.9132182002067566)]

problem_pairs_3 = [(0.7875611782073975, 0.7921156287193298),
                   (0.7675137519836426, 0.8652346134185791),
                   (0.7498966455459595, 0.7622178196907043),
                   (0.7229699492454529, 0.7927138209342957),
                   (0.7065669894218445, 0.7505898475646973)]

torus_bd_pairs = prep_torus(0)[:5]
print(torus_bd_pairs)
print("#############################")
print(pl_runner(torus_bd_pairs, 3, debug=True))

# barcode_table_tests()
