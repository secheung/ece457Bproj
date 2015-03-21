'''
Band pass filter to keep fuzzy sets within a x range
Low extend
High extend
'''

from fuzzy.set.Polygon import Polygon
from fuzzy.norm.AlgebraicProduct import AlgebraicProduct
from fuzzy.norm.Max import Max
from fuzzy.set.operations import merge

import copy

def bandpass(fuzzy_set, x_start, x_end):
    band = Polygon()
    band.add(x = x_start, y = 0)
    band.add(x = x_start, y = 1)
    band.add(x = x_end, y = 1)
    band.add(x = x_end, y = 0)
    return merge(AlgebraicProduct(), fuzzy_set, band)

def max_extend(fuzzy_set, x_start, x_end):
    band = Polygon()
    band.add(x = x_start, y = 0)
    band.add(x = x_start, y = 1)
    band.add(x = x_end, y = 1)
    band.add(x = x_end, y = 0)
    return merge(Max(), fuzzy_set, band)

def reduce_certainty(fuzzy_set, times, segment_size=None):
    new_fuzzy_set = fuzzy_set
    for _ in range(times):
        new_fuzzy_set = merge(AlgebraicProduct(), new_fuzzy_set, new_fuzzy_set,
                              segment_size=segment_size)
    return new_fuzzy_set
