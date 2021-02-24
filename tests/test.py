""" test: used to test the other files in this project """
# Ripser dataset creation
import random
import tadasets
from ripser import ripser
import numpy as np

# Testing framework
import pytest

# Files to be tested
from .context import pl_sweep

# with k = 3
PROBLEM_PAIRS_1 = [(0.9748720526695251, 0.9898090958595276),
                   (0.9600228071212769, 1.029630184173584),
                   (0.8873197436332703, 0.9408737421035767)]

PROBLEM_PAIRS_2 = [(0.9688469171524048, 1.1520495414733887),
                   (0.957465410232544, 1.002064824104309),
                   (0.8262945413589478, 0.9132182002067566)]

PROBLEM_PAIRS_3 = [(0.7875611782073975, 0.7921156287193298),
                   (0.7675137519836426, 0.8652346134185791),
                   (0.7498966455459595, 0.7622178196907043),
                   (0.7229699492454529, 0.7927138209342957),
                   (0.7065669894218445, 0.7505898475646973)]

TEST_2_BDS = [(1, 3), (3, 5)]
TEST_2_ANS = [[(1.0, 0), (2.0, 1.0), (3.0, 0), (3.0, 0), (4.0, 1.0), (5.0, 0)], []]
# Should remove infs
TEST_5_BDS = [(3, float("inf")),
              (0, 6)]
TEST_5_ANS = [[(0.0, 0), (3.0, 3.0), (6.0, 0)], []]

# Normal set of points
TEST_1_BDS = [(0, 6), (1, 3), (2, 7)]
TEST_1_ANS = [[(0.0, 0), (3.0, 3.0), (4.0, 2.0), (4.5, 2.5), (7.0, 0)], [(1.0,\
    0), (2.0, 1.0), (2.5, 0.5), (4.0, 2.0), (6.0, 0)], [(2.0, 0), (2.5, 0.5),\
        (3.0, 0)], []]
@pytest.mark.parametrize("bd_pairs,k,answer", [(TEST_1_BDS, 4, TEST_1_ANS),\
        (TEST_5_BDS, 2, TEST_5_ANS), (TEST_2_BDS, 2, TEST_2_ANS)])
def test_pl_runner(bd_pairs, k, answer, debug=False):
    """ Test runner far pl_planesweep """
    pl_obj = pl_sweep.pl_planesweep.PersistenceLandscape(bd_pairs, k)
    pl_obj.enable_debug(debug)
    landscapes = pl_obj.generate_landscapes()
    # pl_obj.plot()
    assert compare_landscapes(landscapes, answer)


def barcode_table_tests():
    """ Table driven testing for the barcode_filter """
    bd_pairs = [(0, 6), (1, 3), (2, 7)]
    print(barcode_runner(bd_pairs, 1))


def barcode_runner(bd_pairs, k):
    """ Test runner for barcode_filter """
    barcode_filter = pl_sweep.barcode.BarcodeFilter(bd_pairs, k)
    filtered = barcode_filter.filter()
    return filtered


def prep_torus(seed):
    """ Creates torus_bd_pairs for testing using tadasets and ripser"""
    random.seed(seed)
    data = np.concatenate([
        tadasets.dsphere(n=1000, d=1, r=10, noise=1.0),
        tadasets.dsphere(n=500, d=1, r=5, noise=0.5),
        tadasets.dsphere(n=100, d=1, r=1, noise=0.2)
    ])

    thresh = 1.5
    results0 = ripser(data, thresh=thresh, maxdim=1)

    diagrams = results0['dgms']
    return map(lambda x: (x[0], x[1]), diagrams[1])

def compare_landscapes(landscape1, landscape2):
    """ Compares two PersistenceLandscapes and returns True if they are the same """
    # Make sure they have the same k
    if len(landscape1) != len(landscape2):
        return False
    # Ensure they have the same pairs in eacb persistant landscape
    for i, _ in enumerate(landscape1, 0):
        # The len will be 0 when there are no differing pairs
        if len(set(landscape1[i]).symmetric_difference(set(landscape2[i]))) != 0:
            return False
    return True



# TORUS_BD_PAIRS = prep_torus(0)
# print(list(TORUS_BD_PAIRS))
# print("#############################")
# print(pl_runner(torus_bd_pairs, 3, debug=False))

BARCODE_BDTEST_2 = [(1.481631875038147, float("inf")),
                    (1.4144550561904907, float("inf")),
                    (1.4062637090682983, float("inf")),
                    (1.3770512342453003, float("inf")),
                    (1.3382128477096558, float("inf")),
                    (1.3249351978302002, 1.4105395078659058),
                    (1.3119128942489624, 1.4889532327651978),
                    (1.2456670999526978, 1.2640628814697266),
                    (1.232897400856018, 1.2429590225219727),
                    (1.2121959924697876, float("inf")),
                    (1.15329110622406, 1.2175172567367554),
                    (1.1373909711837769, 1.3003721237182617),
                    (1.1321552991867065, 1.3776209354400635),
                    (1.1243916749954224, 1.2062455415725708),
                    (1.0834310054779053, 1.3965675830841064),
                    (1.050351619720459, float("inf")),
                    (1.0092538595199585, 1.2520614862442017),
                    (0.9994320273399353, 1.035273790359497),
                    (0.9952770471572876, 1.2104796171188354),
                    (0.9830079674720764, 1.0581871271133423),
                    (0.9706149101257324, 1.0448448657989502),
                    (0.9633190035820007, 0.9768300652503967),
                    (0.9464677572250366, 1.0140705108642578),
                    (0.9297219514846802, 1.03699791431427),
                    (0.9256359338760376, 1.1982234716415405),
                    (0.9242291450500488, 1.0471967458724976),
                    (0.9177689552307129, 1.070784091949463),
                    (0.9161086678504944, 1.14002525806427),
                    (0.9129068851470947, 1.0044611692428589),
                    (0.9106112122535706, 0.9164996147155762),
                    (0.9006388783454895, 1.0411453247070312),
                    (0.8886387944221497, 1.1813955307006836),
                    (0.8830079436302185, 0.9522051215171814),
                    (0.8553048968315125, 0.9805757999420166),
                    (0.8487460017204285, 0.8722474575042725),
                    (0.8485161066055298, 1.1039115190505981),
                    (0.846491277217865, 0.9526726007461548),
                    (0.8450431227684021, 1.1482371091842651),
                    (0.8411774039268494, 0.8440901041030884),
                    (0.8409903049468994, 0.8795984983444214),
                    (0.8409115672111511, 0.8637188076972961),
                    (0.8314066529273987, 0.838056743144989),
                    (0.826688826084137, 0.8377659916877747),
                    (0.8227778673171997, 0.9258849620819092),
                    (0.8217761516571045, 1.1625670194625854),
                    (0.8205131888389587, 0.8303429484367371),
                    (0.8173962235450745, 0.902662456035614),
                    (0.8166961669921875, 0.9949051141738892),
                    (0.809103786945343, 1.0197639465332031),
                    (0.8089587688446045, 1.1676030158996582),
                    (0.8059825301170349, 1.1422145366668701),
                    (0.7989286184310913, 0.8499131798744202),
                    (0.7988312840461731, 0.8241064548492432),
                    (0.7892301082611084, 0.8258822560310364),
                    (0.7854287028312683, 0.8095000386238098),
                    (0.7833146452903748, 1.2511752843856812),
                    (0.7827491760253906, 1.1702667474746704),
                    (0.7805438041687012, 0.8463992476463318),
                    (0.7787849307060242, 1.1254445314407349),
                    (0.7746716141700745, 0.8316248655319214),
                    (0.7736115455627441, 0.8262039422988892),
                    (0.7729460597038269, 0.7739478945732117),
                    (0.7661694288253784, 0.8066154718399048),
                    (0.7619597911834717, 0.765904426574707),
                    (0.7601943016052246, 0.8852418661117554),
                    (0.7577259540557861, 1.0201863050460815),
                    (0.7540014982223511, 0.8000182509422302),
                    (0.7499094605445862, 1.19063401222229),
                    (0.7482446432113647, 0.7987059354782104),
                    (0.7449402213096619, 0.7860503792762756),
                    (0.7424613833427429, 0.7928765416145325),
                    (0.7418615221977234, 0.8824118971824646),
                    (0.7416989207267761, 0.9592906832695007),
                    (0.7335276007652283, 1.046741247177124),
                    (0.7285271883010864, 0.8027582168579102),
                    (0.7250372171401978, 0.8462553024291992),
                    (0.7232317328453064, 0.74974125623703),
                    (0.7222333550453186, 0.9108394384384155),
                    (0.7220621109008789, 0.8796037435531616),
                    (0.7153380513191223, 0.8463563323020935),
                    (0.7121539115905762, 0.7271350622177124),
                    (0.7064543962478638, 0.7506482005119324),
                    (0.7044801712036133, 0.7795663475990295),
                    (0.7020214796066284, 0.9202442169189453),
                    (0.7006472945213318, 0.7873549461364746),
                    (0.6939539313316345, 0.7289372086524963),
                    (0.6918390393257141, 0.745060920715332),
                    (0.6914541125297546, 0.9897555112838745),
                    (0.686971127986908, 0.8397865295410156),
                    (0.6845861077308655, 0.7215681672096252),
                    (0.6807985305786133, 0.7221785187721252),
                    (0.6795573234558105, 0.6835525631904602),
                    (0.679141640663147, 0.6983815431594849),
                    (0.6767559051513672, 0.6868113279342651),
                    (0.6745668649673462, 0.7161352634429932),
                    (0.6744533777236938, 0.8106876015663147),
                    (0.6740840077400208, 0.6940180063247681),
                    (0.671912431716919, 0.8891887068748474),
                    (0.6704688668251038, 0.6920487880706787),
                    (0.6703612208366394, float("inf")),
                    (0.6701758503913879, 0.6849068403244019),
                    (0.6657667756080627, 0.8290566205978394),
                    (0.6650967001914978, 0.6784605383872986),
                    (0.664659321308136, 0.7473794221878052),
                    (0.6640852689743042, 0.8008753061294556),
                    (0.6634785532951355, 0.7350871562957764),
                    (0.6627880334854126, 0.8983898758888245),
                    (0.659905731678009, 0.701255202293396),
                    (0.6589210629463196, 0.8839132785797119),
                    (0.6571162939071655, 0.7975335121154785),
                    (0.6536009907722473, 0.9748022556304932),
                    (0.651225209236145, 0.9511985778808594),
                    (0.6509765982627869, 0.9382463693618774),
                    (0.65053790807724, 0.6792913675308228),
                    (0.6504868865013123, 0.8807368278503418),
                    (0.6503118872642517, 1.0665146112442017),
                    (0.6430863738059998, 0.7372941374778748),
                    (0.6423664689064026, 0.6774399876594543),
                    (0.6393327116966248, 0.6691980361938477),
                    (0.6380499601364136, 0.6482954621315002),
                    (0.6376835703849792, 0.6840956807136536),
                    (0.6366122961044312, 0.7247949242591858),
                    (0.6355192065238953, 0.677711009979248),
                    (0.6329906582832336, 0.7220889925956726),
                    (0.629429280757904, 0.6992824673652649),
                    (0.6292639970779419, 0.8403111696243286),
                    (0.6263630986213684, 0.6616799235343933),
                    (0.6240965723991394, 0.77580726146698),
                    (0.6229950785636902, 0.9015716910362244),
                    (0.619798481464386, 0.6398169994354248),
                    (0.6174859404563904, 0.6466933488845825),
                    (0.611445426940918, 0.7511155605316162),
                    (0.610237717628479, 1.2525970935821533),
                    (0.6088447570800781, 0.9621044993400574),
                    (0.6080777645111084, 0.6666667461395264),
                    (0.6066958904266357, float("inf")),
                    (0.6055076718330383, 0.693598747253418),
                    (0.6054529547691345, 0.6232956647872925),
                    (0.6049930453300476, 0.7120577096939087),
                    (0.6045718789100647, 0.9507471323013306),
                    (0.6032463908195496, 0.6079991459846497),
                    (0.6027812957763672, 0.6348300576210022),
                    (0.5993397831916809, 0.6137608885765076),
                    (0.5989991426467896, 0.6450089812278748),
                    (0.598394513130188, 0.8460038304328918),
                    (0.5955779552459717, 0.6693125367164612),
                    (0.5953970551490784, 0.7432875037193298),
                    (0.5928097367286682, 0.7709223628044128),
                    (0.5927329659461975, 1.090397834777832),
                    (0.5904967188835144, 0.6709272265434265),
                    (0.5889416933059692, 0.6390506029129028),
                    (0.5870391130447388, 0.7059524059295654),
                    (0.5869517922401428, 1.1090947389602661),
                    (0.5858192443847656, 0.634588360786438),
                    (0.5842583179473877, 0.6357458829879761),
                    (0.5835880041122437, 0.6157607436180115),
                    (0.5828484892845154, 0.6206850409507751),
                    (0.5823701620101929, 0.6044929623603821),
                    (0.5823308229446411, 0.6341431140899658),
                    (0.5818325281143188, 0.8324937224388123),
                    (0.5802791118621826, 0.6006052494049072),
                    (0.5801320672035217, 1.0351170301437378),
                    (0.5797800421714783, 0.7217955589294434),
                    (0.5786688923835754, 0.7762054800987244),
                    (0.577835738658905, 1.0190012454986572),
                    (0.5775749087333679, 0.5950645208358765),
                    (0.5697754621505737, 0.5728341341018677),
                    (0.5683560371398926, 0.5735167264938354),
                    (0.5662610530853271, 0.5943789482116699),
                    (0.5601254105567932, 0.5969798564910889),
                    (0.5591826438903809, 0.7236485481262207),
                    (0.5591577887535095, 0.6513668298721313),
                    (0.5576199889183044, 0.6375749111175537),
                    (0.5546164512634277, 0.562654435634613),
                    (0.5537443161010742, 0.834680438041687),
                    (0.5531296133995056, 0.5774022936820984),
                    (0.5527563691139221, 0.5721720457077026),
                    (0.5440084338188171, 0.6126620769500732),
                    (0.5430779457092285, 0.5908530354499817),
                    (0.5411894917488098, 0.6623769402503967),
                    (0.5388427376747131, 0.7727528214454651),
                    (0.5383263826370239, 0.6463529467582703),
                    (0.5378576517105103, 0.5440163612365723),
                    (0.5361054539680481, 0.7368201613426208),
                    (0.5359145998954773, 0.673008918762207),
                    (0.5341739654541016, 0.7404593825340271),
                    (0.5323140621185303, 0.7873345017433167),
                    (0.5283307433128357, 0.5824089646339417),
                    (0.527509331703186, 0.7105690240859985),
                    (0.5237287282943726, 0.5466101765632629),
                    (0.5224566459655762, 0.5662746429443359),
                    (0.5213806629180908, 0.522926390171051),
                    (0.519740641117096, 0.5714864134788513),
                    (0.5190712213516235, 0.6206437945365906),
                    (0.5188747644424438, 0.6834644675254822),
                    (0.5182408690452576, 0.6446648836135864),
                    (0.5159358382225037, 0.5251471996307373),
                    (0.5135674476623535, 0.5392149686813354),
                    (0.5132052302360535, 0.5594580173492432),
                    (0.5126649737358093, 0.5135413408279419),
                    (0.5112890601158142, 0.6362955570220947),
                    (0.5103471875190735, 0.6378740668296814),
                    (0.5100218057632446, 0.7950718402862549),
                    (0.508346438407898, 0.5222676396369934),
                    (0.5072306990623474, 0.6027696132659912),
                    (0.5061385631561279, 0.5439258217811584),
                    (0.505460262298584, 0.523388683795929),
                    (0.5016008615493774, 0.6051018238067627),
                    (0.5007583498954773, 0.6892145872116089),
                    (0.4986569881439209, 0.49867093563079834),
                    (0.49730101227760315, 0.49844205379486084),
                    (0.49232399463653564, 0.6282255053520203),
                    (0.4911307096481323, 0.6371511816978455),
                    (0.48917341232299805, 0.5041730999946594),
                    (0.4853512942790985, 0.5037897825241089),
                    (0.48528966307640076, 0.6534183025360107),
                    (0.4817519187927246, 0.6473430395126343),
                    (0.47849470376968384, 0.6103792190551758),
                    (0.47842806577682495, 0.6315476894378662),
                    (0.47588708996772766, 0.6179797053337097),
                    (0.4718468189239502, 0.6924681067466736),
                    (0.4698081612586975, 0.5541027784347534),
                    (0.46582654118537903, 0.47091373801231384),
                    (0.46344029903411865, 0.517981767654419),
                    (0.46019119024276733, 0.48716604709625244),
                    (0.45901134610176086, 0.49793580174446106),
                    (0.45785993337631226, 0.4821133613586426),
                    (0.4573248624801636, 0.5394161343574524),
                    (0.4571272134780884, 0.4876660704612732),
                    (0.4571130573749542, 0.4680463373661041),
                    (0.4535447359085083, 0.48293912410736084),
                    (0.45347660779953003, 0.5509551763534546),
                    (0.45263850688934326, 0.4812355637550354),
                    (0.4523018002510071, 0.4575933814048767),
                    (0.4500240385532379, 0.4852781891822815),
                    (0.4498103857040405, 0.48080241680145264),
                    (0.4485081434249878, 0.4886663258075714),
                    (0.4464676082134247, 0.4476459324359894),
                    (0.4427518844604492, 0.46150898933410645),
                    (0.4405457675457001, 0.47828981280326843),
                    (0.43905261158943176, 0.6279465556144714),
                    (0.436135858297348, 0.5632307529449463),
                    (0.43472594022750854, 0.45656198263168335),
                    (0.43244749307632446, 0.537923276424408),
                    (0.4320847690105438, 0.4366479218006134),
                    (0.43146324157714844, 0.46071553230285645),
                    (0.43052881956100464, 0.4306296408176422),
                    (0.4293364882469177, 0.6929622888565063),
                    (0.4286726415157318, 0.5699349045753479),
                    (0.4279528260231018, 0.4395207166671753),
                    (0.42450016736984253, 0.5021734237670898),
                    (0.42387139797210693, 0.5287173390388489),
                    (0.4206458032131195, 0.7031878232955933),
                    (0.419978529214859, 0.5255144834518433),
                    (0.4199584126472473, 0.4539150595664978),
                    (0.4186234772205353, 0.4298841059207916),
                    (0.416860431432724, 0.43112027645111084),
                    (0.4159533381462097, 0.4176253080368042),
                    (0.4155365526676178, 0.46313387155532837),
                    (0.4149744212627411, 0.42975613474845886),
                    (0.41442427039146423, 0.4539644420146942),
                    (0.41436633467674255, 0.4157271087169647),
                    (0.41321519017219543, 0.5096892714500427),
                    (0.41255322098731995, 0.48333191871643066),
                    (0.4122515916824341, 0.6167746782302856),
                    (0.41184723377227783, 0.7303110957145691),
                    (0.40893352031707764, 0.44665998220443726),
                    (0.40851539373397827, 0.41385772824287415),
                    (0.40294089913368225, 0.45409029722213745),
                    (0.4027751684188843, 0.444316565990448),
                    (0.400320440530777, 0.5127819776535034),
                    (0.3991245627403259, 0.483447402715683),
                    (0.3979780077934265, 0.601361095905304),
                    (0.3978051543235779, 0.4119935631752014),
                    (0.39364033937454224, 0.45942503213882446),
                    (0.39335575699806213, 0.42769983410835266),
                    (0.393215537071228, 0.46079182624816895),
                    (0.3893350660800934, 0.45706313848495483),
                    (0.3881404399871826, 0.48434776067733765),
                    (0.3865682780742645, 0.4117366671562195),
                    (0.3850476145744324, 0.5088208317756653),
                    (0.38277488946914673, 0.47949084639549255),
                    (0.3823540210723877, 0.44439664483070374),
                    (0.3777044713497162, 0.3990843892097473),
                    (0.3775668144226074, 0.49923279881477356),
                    (0.37657037377357483, 0.44689032435417175),
                    (0.3753103017807007, 0.5327439308166504),
                    (0.3752804696559906, 0.46530136466026306),
                    (0.3745017349720001, 0.43027183413505554),
                    (0.37408462166786194, 0.4746931195259094),
                    (0.3733973503112793, 0.49304428696632385),
                    (0.37236806750297546, 0.5268123149871826),
                    (0.37065473198890686, 0.43093374371528625),
                    (0.3672820031642914, 0.41589251160621643),
                    (0.3660920262336731, 0.40569767355918884),
                    (0.355755478143692, 0.422402024269104),
                    (0.3542567789554596, 0.5182430744171143),
                    (0.35198724269866943, 0.3537302315235138),
                    (0.35187849402427673, 0.37499290704727173),
                    (0.35137978196144104, 0.35250601172447205),
                    (0.35096147656440735, 1.1059802770614624),
                    (0.34964773058891296, 0.354887992143631),
                    (0.3411686420440674, 0.39463719725608826),
                    (0.3409103751182556, 0.35127171874046326),
                    (0.3398619592189789, 0.34970590472221375),
                    (0.3365180492401123, 0.5133938193321228),
                    (0.326388418674469, 0.37379762530326843),
                    (0.3159005641937256, 0.3212797939777374),
                    (0.31509846448898315, 0.36788618564605713),
                    (0.31450995802879333, 0.4266972839832306),
                    (0.3118146061897278, 0.3268885314464569),
                    (0.3072877526283264, 0.35027241706848145),
                    (0.3062152564525604, 0.4038512408733368),
                    (0.3027048707008362, 0.4116564691066742),
                    (0.2986026704311371, 0.38306787610054016),
                    (0.29243406653404236, 0.31984400749206543),
                    (0.28893691301345825, 0.29304730892181396),
                    (0.2872058153152466, 0.36311545968055725),
                    (0.28121376037597656, 0.3079593777656555),
                    (0.2805631458759308, 0.33530500531196594),
                    (0.28048795461654663, 0.3866027593612671),
                    (0.2689947783946991, 0.27891770005226135),
                    (0.2669222056865692, 0.3552599549293518),
                    (0.26578986644744873, 0.35947176814079285),
                    (0.264553040266037, 0.3120937943458557),
                    (0.26244956254959106, 0.2895749807357788),
                    (0.25963711738586426, 0.2615290582180023),
                    (0.2520674467086792, 0.2630712389945984),
                    (0.24910610914230347, 0.28592783212661743),
                    (0.24440144002437592, 0.31692901253700256),
                    (0.23625588417053223, 0.27907779812812805),
                    (0.23359249532222748, 0.24949602782726288),
                    (0.23149652779102325, 0.24129268527030945),
                    (0.22226081788539886, 0.24002227187156677),
                    (0.19659288227558136, 0.19914129376411438),
                    (0.17456980049610138, 0.18322381377220154),
                    (0.16332241892814636, 0.20584480464458466),
                    (0.15968643128871918, 0.16814741492271423),
                    (0.06917203217744827, 0.07327581197023392)]

# barcode_table_tests()
BARCODE_BDTEST_1 = [(0.8998820185661316, 1.0887004137039185),
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

# K_1 = 4
# ORIGINAL_LENGTH_1 = len(BARCODE_BDTEST_1)
# ORIGINAL_1 = pl_runner(BARCODE_BDTEST_1, K_1)
# BARCODES_1 = barcode_runner(BARCODE_BDTEST_1, K_1)
# print("Removed " + str(ORIGINAL_LENGTH_1 - len(BARCODES_1)) + " pairs. " +
#       str(ORIGINAL_LENGTH_1 / float(len(BARCODES_1))) + "%")

# FILTERED_1 = pl_runner(BARCODES_1, K_1)
# # https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
# print(compare_landscapes(ORIGINAL_1, FILTERED_1))

# k_2 = 2
# original_2 = pl_runner(problem_pairs_3, k_2)
# barcodes_2 = barcode_runner(problem_pairs_3, k_2)
# filtered_2 = pl_runner(problem_pairs_3, k_2)

def find_problem_pairs(number_pairs, seed, k, minn, maxx):
    """ Do random search for problem pairs """
    # Set seed
    random.seed(a=seed, version=2)
    barcodes = []
    for _ in range(number_pairs):
        start = random.uniform(minn, maxx)
        length = random.uniform(minn, maxx)+1
        barcodes.append((int(start), int(start + length)))
    # Show the pairs
    print(barcodes)
    # Calculate
    filtered = barcode_runner(barcodes, k)
    landscapes = test_pl_runner(filtered, k, [])
    pl_obj_new = PersistenceLandscape([], 0)
    pl_obj_new.integrate(landscapes)

# I = 0
# MIN = 0
# MAX = 10
# PAIRS = 10
# K = (PAIRS*PAIRS)
# while True:
#     print(I)
#     find_problem_pairs(PAIRS, I, K, MIN, MAX)
#     I = I + 1

# K_2 = 3
# FILTERED_2 = barcode_runner(BARCODE_BDTEST_2, K_2)
# LANDSCAPES = test_pl_runner(FILTERED_2, K_2, [])
# PL_OBJ_NEW = PersistenceLandscape([], 0)
# INTS = pl_obj_new.integrate(landscapes)
