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

problem_pairs_4 = [(3, float("inf")),
                   (3, 7)]

torus_bd_pairs = prep_torus(0)
# print(torus_bd_pairs)
# print("#############################")
# print(pl_runner(torus_bd_pairs, 3, debug=False))

# barcode_table_tests()
barcode_bdtest_1 = [(0.8998820185661316, 1.0887004137039185),
                    (0.8431480526924133, 0.8592690825462341),
                    (0.8322747945785522, 0.8514002561569214),
                    (0.7880150675773621, 0.8393602967262268),
                    (0.743628203868866, 0.7473208904266357),
                    (0.7204825282096863, 0.7382306456565857),
                    (0.7204036116600037, 0.8006560802459717),
                    (0.6939055919647217, 0.7553191781044006),
                    (0.679487407207489, 0.8503829836845398),
                    (0.6593510508537292, 0.7170162796974182),
                    (0.6545075178146362, 0.8717374801635742),
                    (0.6497418880462646, 0.6717594265937805),
                    (0.6354684233665466, 0.7172889113426208),
                    (0.622560441493988, 0.6439796686172485),
                    (0.6196547150611877, 0.687408447265625),
                    (0.603175699710846, 0.7162836194038391),
                    (0.5877352952957153, 0.6829168796539307),
                    (0.5837560296058655, 0.6654344797134399),
                    (0.5736892223358154, 0.6740358471870422),
                    (0.5725956559181213, 0.6844267845153809),
                    (0.5666984915733337, 0.6001288294792175),
                    (0.5663051605224609, 0.7018839716911316),
                    (0.5634450912475586, 0.5892950296401978),
                    (0.5629109144210815, 0.5884401202201843),
                    (0.5623810291290283, 0.6192795634269714),
                    (0.5578960180282593, 0.5956233739852905),
                    (0.5496746897697449, 0.6456038355827332),
                    (0.5495465993881226, float("inf")),
                    (0.5419073104858398, 0.5517745018005371),
                    (0.53703773021698, 0.5762943029403687),
                    (0.5252540111541748, 0.5378221273422241),
                    (0.5214066505432129, 0.6484578251838684),
                    (0.5145647525787354, 0.5971382260322571),
                    (0.5107016563415527, 0.619568943977356),
                    (0.5062195658683777, 0.7367080450057983),
                    (0.4884960353374481, 0.5712498426437378),
                    (0.48335686326026917, 0.5671738982200623),
                    (0.48206597566604614, 0.7143527865409851),
                    (0.475940078496933, 0.4777391850948334),
                    (0.47272005677223206, 0.555039644241333),
                    (0.4682125151157379, 0.6573713421821594),
                    (0.4595029056072235, 0.47380006313323975),
                    (0.4509623944759369, 0.4830169379711151),
                    (0.4485805034637451, 0.5019347071647644),
                    (0.44425326585769653, 0.5640609264373779),
                    (0.4410913288593292, 0.468575119972229),
                    (0.43909093737602234, 0.5425354838371277),
                    (0.4379830062389374, 0.6354851722717285),
                    (0.4376507103443146, 0.46338996291160583),
                    (0.4360906481742859, 0.46878087520599365),
                    (0.4323119521141052, 0.6424628496170044),
                    (0.42453137040138245, 0.4422511160373688),
                    (0.4208298623561859, 0.44243013858795166),
                    (0.42026299238204956, 0.49537867307662964),
                    (0.4183376133441925, 0.572892427444458),
                    (0.4179627299308777, 0.4602329134941101),
                    (0.4091794788837433, 0.4383660554885864),
                    (0.39888033270835876, 0.44565948843955994),
                    (0.397603303194046, 0.4229426085948944),
                    (0.3920821249485016, 0.47968342900276184),
                    (0.3860357999801636, 0.46284201741218567),
                    (0.38361144065856934, 0.5208412408828735),
                    (0.3834861218929291, 0.38799354434013367),
                    (0.3821530342102051, 0.4476892352104187),
                    (0.3755461275577545, 0.4324246346950531),
                    (0.3735635578632355, 0.38328301906585693),
                    (0.370235800743103, 0.4596685767173767),
                    (0.36855754256248474, 0.5733824968338013),
                    (0.3682868778705597, 0.3902391493320465),
                    (0.3623531758785248, 0.42082446813583374),
                    (0.3605818450450897, 0.4480241537094116),
                    (0.35938429832458496, 0.4621211588382721),
                    (0.35531294345855713, 0.36811622977256775),
                    (0.35498183965682983, 0.41742467880249023),
                    (0.3545284867286682, 0.44881564378738403),
                    (0.33910009264945984, 0.40551334619522095),
                    (0.3325440585613251, 0.34740105271339417),
                    (0.3238995373249054, 0.5257483720779419),
                    (0.3221982419490814, 0.34686362743377686),
                    (0.31718379259109497, 0.3199167847633362),
                    (0.3165828287601471, 0.41897714138031006),
                    (0.31171298027038574, 0.3309594392776489),
                    (0.3073737919330597, 0.31598368287086487),
                    (0.30543139576911926, 0.3438115417957306),
                    (0.3042530119419098, 0.3803316056728363),
                    (0.3038560152053833, 0.3167882263660431),
                    (0.30332133173942566, 1.1276997327804565),
                    (0.301599383354187, 0.35251644253730774),
                    (0.30147168040275574, 0.30441221594810486),
                    (0.29764825105667114, 0.40765073895454407),
                    (0.29578542709350586, 0.31696125864982605),
                    (0.28721341490745544, 0.2888384163379669),
                    (0.2620401084423065, 0.2699930965900421),
                    (0.25899991393089294, 0.28616535663604736),
                    (0.25174883008003235, 0.28099286556243896),
                    (0.2500452399253845, 0.2701255679130554),
                    (0.24170352518558502, 0.2870234549045563),
                    (0.24006398022174835, 0.2609170079231262),
                    (0.205924391746521, 0.2070665806531906),
                    (0.19936572015285492, 0.2079983502626419),
                    (0.19454821944236755, 0.21990838646888733),
                    (0.19133752584457397, 0.20684555172920227),
                    (0.18672098219394684, 0.1995505392551422),
                    (0.17697729170322418, 0.2106212079524994),
                    (0.1550106704235077, 0.22144968807697296),
                    (0.15023969113826752, 0.15087532997131348),
                    (0.12529709935188293, 0.13184352219104767)]

k_1 = 4
original_length_1 = len(barcode_bdtest_1)
original_1 = pl_runner(barcode_bdtest_1, k_1)
barcodes_1 = barcode_runner(barcode_bdtest_1, k_1)
print("Removed " + str(original_length_1 - len(barcodes_1)) + " pairs. " +
      str(original_length_1/float(len(barcodes_1))) + "%")

filtered_1 = pl_runner(barcodes_1, k_1)
# https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
# print(list(set(original_1).symmetric_difference(set(filtered_1))))

# k_2 = 2
# original_2 = pl_runner(problem_pairs_3, k_2)
# barcodes_2 = barcode_runner(problem_pairs_3, k_2)
# filtered_2 = pl_runner(problem_pairs_3, k_2)
