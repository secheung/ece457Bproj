
from fuzzy.set.Polygon import Polygon
from fuzzy.set.Trapez import Trapez
from fuzzy.set.ZFunction import ZFunction
from fuzzy.set.SFunction import SFunction

from passfilter import bandpass
from passfilter import max_extend
from passfilter import reduce_certainty
from TrapezPiFunction import TrapezPiFunction

# Deprecated bad_low, good_high
def generate_pay(bad_low, bad_high, ok_low, ok_high, good_low, good_high ):
    pay_bad = Polygon()
    pay_bad.add(x = 0, y = 0)
    pay_bad.add(x = 0, y = 1)
    pay_bad.add(x = bad_high, y= 1.0)
    pay_bad.add(x = ok_low, y = 0.0)
   
    # just trying this
    pay_ok = Trapez(ok_low, ok_high, abs(ok_low - bad_high), abs(good_low - ok_high))

    pay_high = Polygon()
    pay_high.add(x =  ok_high, y= 0.0)
    pay_high.add(x =  good_low, y= 1.0)
    pay_high.add(x =  good_high, y= 1.0)
    pay_high.add(x =  good_high + 50, y= 1.0) # dummy
    # everything over good_high is still good... may need to add an extension

    return {
        "bad": pay_bad,
        "ok": pay_ok,
        "high": pay_high
    }

def generate_rep(low, high):
    low_delta = (high - low)/2.0
    low_rep = ZFunction(low + low_delta, low_delta)
    low_rep = max_extend(low_rep, 0, low)

    high_delta = low_delta
    high_rep = SFunction(high - high_delta, high_delta)
    high_rep = max_extend(high_rep, high, 10)

    return {
        "low": low_rep,
        "high": high_rep
    }

# Deprecated small_low, large_high
def generate_employee(small_low, small_high, med_low, med_high, large_low, large_high):
    employee_small = Polygon()
    employee_small.add(x=0, y=0)
    employee_small.add(x=0, y=1)
    employee_small.add(x=small_high, y=1)
    employee_small.add(x=med_low, y=0)

    employee_med = TrapezPiFunction(med_low, med_high, 
                                    abs(med_low - small_high),
                                    abs(large_low - med_high))

    employee_large = Polygon()
    employee_large.add(x=med_high, y = 0 )
    employee_large.add(x=large_low, y = 1 )
    employee_large.add(x=large_low + 100, y=1) #dummy

    return {
        "small": employee_small,
        "med":employee_med,
        "large":employee_large
    }
