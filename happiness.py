
from fuzzy.set.Polygon import Polygon
from fuzzy.set.SFunction import SFunction
from fuzzy.set.ZFunction import ZFunction
from fuzzy.set.operations import merge
from fuzzy.norm.AlgebraicProduct import AlgebraicProduct

from passfilter import max_extend
from TrapezPiFunction import TrapezPiFunction

low_high = 35.0
med_low = 50.0
med_high = 70.0
high_low = 80.0

low_high_delta = (med_low - low_high) / 2.0
Happiness_bad = ZFunction(low_high + low_high_delta, low_high_delta)
Happiness_bad = max_extend(Happiness_bad, 0.0, low_high)
fixstart = Polygon([(0.0,0.0),(0.1,1.0),(med_low,1.0)])
Happiness_bad = merge(AlgebraicProduct(), Happiness_bad, fixstart)

Happiness_med = TrapezPiFunction(med_low, med_high,
                                 med_low - low_high, high_low - med_high)

high_low_delta = (high_low - med_high) / 2.0
Happiness_high = SFunction(high_low - high_low_delta, high_low_delta)
Happiness_high = max_extend(Happiness_high, high_low, 100.0)
fixend = Polygon([(med_high,1.0),(99.9,1.0),(100.0,0.0)])
Happiness_high = merge(AlgebraicProduct(), Happiness_high, fixend)
