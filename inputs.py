
from fuzzy.InputVariable import InputVariable
from fuzzy.Adjective import Adjective
from fuzzy.set.Polygon import Polygon
from fuzzy.fuzzify.Plain import Plain
from fuzzy.set.Trapez import Trapez


# PAy
def generate_pay(bad_low, bad_high, ok_low, ok_high, good_low, good_high ):
    alright = (bad_high + ok_low)/2

    fine = (ok_high + good_low)/2

    pay_bad = Polygon()
    pay_bad.add(x = 0.0, y= 0.0)
    pay_bad.add(x = bad_low, y= 1.0)
    pay_bad.add(x = bad_high, y= 1.0)
    pay_bad.add(x = ok_low + 5, y= 0.0)

    pay_alright = Polygon()
    pay_alright.add(x =  alright - 10, y= 0.0)
    pay_alright.add(x =  alright, y= 1.0)
    pay_alright.add(x =  alright + 10, y= 0.0)

    pay_ok = Polygon()
    pay_ok.add(x =  ok_low - 5 , y= 0.0)
    pay_ok.add(x =  ok_low, y= 1.0)
    pay_ok.add(x =  ok_high, y= 1.0)
    pay_ok.add(x =  ok_high + 10, y= 0.0)

    pay_fine = Polygon()
    pay_fine.add(x =  fine - 10, y= 0.0)
    pay_fine.add(x =  fine, y= 1.0)
    pay_fine.add(x =  fine + 10, y= 0.0)

    pay_good = Polygon()
    pay_good.add(x =  ok_high, y= 0.0)
    pay_good.add(x =  good_low, y= 1.0)
    pay_good.add(x =  good_high, y= 1.0)
    # everything over good_high is still good
    pay_good.add(x =  good_high + 50 , y= 1.0)

    return {
        "bad": pay_bad,
	"alright":pay_alright,
        "ok": pay_ok,
	"fine" : pay_fine,
        "good": pay_good
    }

def generate_rep(low, high):
    med = (low + high)/2

    low_rep = Polygon()
    low_rep.add(x = 0, y = 1.0)
    low_rep.add(x = low, y = 1.0)
    low_rep.add(x = med, y = 0.0)

    med_rep = Polygon()
    med_rep.add(x = med - 3, y = 0.0)
    med_rep.add(x = med + 2, y = 1.0)
    med_rep.add(x = med + 3, y = 0.0)
    

    high_rep = Polygon()
    high_rep.add(x = med - 1, y= 0.0)
    high_rep.add(x = high, y = 1.0)
    high_rep.add(x = 10, y = 1.0)

    return {
        "low": low_rep,
	"med": med_rep,
        "high": high_rep
    }

def generate_employee(small_low, small_high, med_low, med_high, large_low, large_high):
    smallish = (small_high + med_low)/2
    largish = (med_high + large_low)/2

    employee_small = Polygon()
    employee_small.add(x=0, y=0)
    employee_small.add(x=small_low, y = 1)
    employee_small.add(x=small_high, y = 1)
    employee_small.add(x=smallish, y = 0)

    employee_smallish = Polygon()
    employee_smallish.add(x=smallish - 7, y=0)
    employee_smallish.add(x=smallish - 3, y = 1)
    employee_smallish.add(x=smallish + 3, y = 1)
    employee_smallish.add(x=smallish + 20, y = 0)

    employee_med = Polygon()
    employee_med.add(x=med_low - 10, y = 0)
    employee_med.add(x=med_low, y = 1)
    employee_med.add(x=med_high, y = 1)
    employee_med.add(x=largish + 10, y = 0)

    employee_largish = Polygon()
    employee_largish.add(x=largish - 15, y=0)
    employee_largish.add(x=largish - 5, y = 1)
    employee_largish.add(x=largish + 5, y = 1)
    employee_largish.add(x=largish + 45, y = 0)

    employee_large = Polygon()
    employee_large.add(x=large_low - 25, y = 0 )
    employee_large.add(x=large_low, y = 1 )
    employee_large.add(x=large_high, y = 1 )
    employee_large.add(x=large_high + 50, y = 0 )

    return {
        "small": employee_small,
	"smallish": employee_smallish,
        "med":employee_med,
	"largish": employee_largish,
        "large":employee_large
    }
