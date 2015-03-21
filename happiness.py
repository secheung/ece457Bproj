
from fuzzy.set.Polygon import Polygon
from fuzzy.set.SFunction import SFunction
from fuzzy.set.ZFunction import ZFunction

from passfilter import max_extend
from TrapezPiFunction import TrapezPiFunction

low_high = 35
med_low = 50
med_high = 70
high_low = 80

def get_deltas(low, high):
    return abs(high - low) / 2.0

low_high_delta = (med_low - low_high) / 2.0
Happiness_bad = ZFunction(low_high + low_high_delta, low_high_delta)
Happiness_bad = max_extend(Happiness_bad, 0, low_high)

Happiness_med = TrapezPiFunction(med_low, med_high,
                                 med_low - low_high, high_low - med_high)

high_low_delta = (high_low - med_high) / 2.0
Happiness_good = SFunction(high_low - high_low_delta, high_low_delta)
Happiness_good = max_extend(Happiness_good, high_low, 100)
