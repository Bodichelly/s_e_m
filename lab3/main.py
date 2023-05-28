from util import MetricsCalculator
from libs import tmp
from tests.mhf import a as mhf
from tests.inheritance_depth import a as dit
from tests.mif import a as mif
from tests.ahf import a as ahf
from tests.aif import a as aif
from tests.pof import a as pof


metric_calc = MetricsCalculator()
metric_calc.calculate(pof)

