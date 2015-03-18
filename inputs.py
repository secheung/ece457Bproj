
from fuzzy.InputVariable import InputVariable
from fuzzy.Adjective import Adjective
from fuzzy.set.Polygon import Polygon
from fuzzy.fuzzify.Plain import Plain
from fuzzy.set.Trapez import Trapez


# PAy
def generate_pay(bad_low, bad_high, ok_low, ok_high, good_low, good_high ):
    pay_bad = Polygon()
    pay_bad.add(x = max(bad_low - 5, 0), y= 0.0)
    pay_bad.add(x = bad_low, y= 1.0)
    pay_bad.add(x = bad_high, y= 1.0)
    pay_bad.add(x = bad_high + 5, y= 0.0)

    pay_ok = Polygon()
    pay_ok.add(x =  ok_low - 5 , y= 0.0)
    pay_ok.add(x =  ok_low, y= 1.0)
    pay_ok.add(x =  ok_high, y= 1.0)
    pay_ok.add(x =  ok_high + 20, y= 0.0)

    pay_good = Polygon()
    pay_good.add(x =  good_low - 10, y= 0.0)
    pay_good.add(x =  good_low, y= 1.0)
    pay_good.add(x =  good_high, y= 1.0)
    # everything over good_high is still good
    # pay_good.add(x =  good_high + 50 , y= 1.0)

    return {
        "bad": pay_bad,
        "ok": pay_ok,
        "good": pay_good
    }

def generate_rep(low, high):
    low_rep = Polygon()
    low_rep.add(x = 0, y = 0.0)
    low_rep.add(x = 0, y = 1.0)
    low_rep.add(x = low, y = 1.0)
    low_rep.add(x = low + 1, y = 0.0)

    high_rep = Polygon()
    high_rep.add(x = high - 3, y= 0.0)
    high_rep.add(x = high, y = 1.0)
    high_rep.add(x = 10, y = 1.0)

    return {
        "low": low_rep,
        "high": high_rep
    }

def generate_employee(small_low, small_high, med_low, med_high, large_low, large_high):
    employee_small = Polygon()
    employee_small.add(x=0, y=0)
    small_slop = max(small_low - 5, 0)

    employee_small.add(x=small_low - small_slop , y = 1)
    employee_small.add(x=small_low, y = 1)
    employee_small.add(x=small_high, y = 1)
    employee_small.add(x=small_high + 2, y = 0)

    employee_med = Polygon()
    employee_med.add(x=med_low - 10, y = 0)
    employee_med.add(x=med_low, y = 1)
    employee_med.add(x=med_high, y = 1)
    employee_med.add(x=large_low + 10, y = 0)

    employee_large = Polygon()
    employee_large.add(x=large_low - 25, y = 0 )
    employee_large.add(x=large_low, y = 1 )
    employee_large.add(x=large_high, y = 1 )

    return {
        "small": employee_small,
        "med":employee_med,
        "large":employee_large
    }
