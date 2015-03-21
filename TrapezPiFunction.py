from fuzzy.set.Polygon import Polygon
from fuzzy.set.SFunction import SFunction
from fuzzy.set.ZFunction import ZFunction
from fuzzy.norm.Max import Max
from fuzzy.set.operations import merge

from passfilter import bandpass

def TrapezPiFunction(trapez_start, trapez_end, start_delta, end_delta):
    trapez = Polygon()
    trapez.add(x=trapez_start, y=0)
    trapez.add(x=trapez_start, y=1)
    trapez.add(x=trapez_end, y=1)
    trapez.add(x=trapez_end, y=0)
    start = SFunction(trapez_start - start_delta/2.0, start_delta/2.0)
    start = bandpass(start, trapez_start - start_delta, trapez_start)
    end = ZFunction(trapez_end + end_delta/2.0, end_delta/2.0)
    end = bandpass(end, trapez_end, trapez_end + end_delta)
    return merge(Max(), merge(Max(),trapez, start), end)
