
from fuzzy.set.Polygon import Polygon
from fuzzy.set.Trapez import Trapez
from fuzzy.set.ZFunction import ZFunction
from fuzzy.set.SFunction import SFunction
from fuzzy.set.PiFunction import PiFunction

from passfilter import bandpass
from passfilter import max_extend
from passfilter import reduce_certainty

# Deprecated bad_low, good_high
def generate_pay(bad_low, bad_high, ok_low, ok_high, good_low, good_high ):
    pay_bad = Polygon()
    pay_bad.add(x = 0.0, y = 0.0)
    pay_bad.add(x = 0.0, y = 1.0)
    pay_bad.add(x = bad_high, y= 1.0)
    pay_bad.add(x = ok_low, y = 0.0)
   
    # just trying this
    pay_ok = Trapez(ok_low, ok_high, abs(ok_low - bad_high), abs(good_low - ok_high))

    pay_high = Polygon()
    pay_high.add(x =  ok_high, y= 0.0)
    pay_high.add(x =  good_low, y= 1.0)
    pay_high.add(x =  200.0, y= 1.0) # dummy
    # everything over good_high is still good... may need to add an extension

    return {
        "bad": pay_bad,
        "ok": pay_ok,
        "high": pay_high
    }

def generate_rep(low, high):
    low_delta = (high - low)/2.0
    low_rep = ZFunction(low + low_delta, low_delta)
    low_rep = max_extend(low_rep, 0.0, low)

    high_delta = low_delta
    high_rep = SFunction(high - high_delta, high_delta)
    high_rep = max_extend(high_rep, high, 10.0)

    return {
        "low": low_rep,
        "high": high_rep
    }

# Deprecated small_low, large_high
def generate_employee(small_low, small_high, med_low, med_high, large_low, large_high):
    employee_small = Polygon()
    employee_small.add(x=0.0, y=0.0)
    employee_small.add(x=0.0, y=1.0)
    employee_small.add(x=small_high, y=1.0)
    employee_small.add(x=med_low, y=0.0)

    employee_med = Trapez(med_low, med_high,
                          abs(med_low - small_high),
                          abs(large_low - med_high))

    employee_large = Polygon()
    employee_large.add(x=med_high, y = 0.0 )
    employee_large.add(x=large_low, y = 1.0 )
    employee_large.add(x=1000.0, y=1.0) #dummy

    return {
        "small": employee_small,
        "med":employee_med,
        "large":employee_large
    }

def generate_commute(close, medium, far):
    # fake medium low and high... should be fine
    medium_low = medium - 5
    medium_high = medium + 5

    close_delta = (medium_low - close)/2.0
    close_commute = ZFunction(close + close_delta, close_delta)
    close_commute = max_extend(close_commute, 0.0, close)

    medium_commute = Trapez(medium_low, medium_high,
                            abs(medium_low - close),
                            abs(far - medium_high))

    far_delta = (far - medium_high)/2.0
    far_commute = SFunction(far - far_delta, far_delta)
    far_commute = max_extend(far_commute, far, 150.0)

    return {
        "close": close_commute,
        "medium": medium_commute,
        "far": far_commute
    }
