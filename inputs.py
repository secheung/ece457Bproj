
from fuzzy.InputVariable import InputVariable
from fuzzy.Adjective import Adjective
from fuzzy.set.Polygon import Polygon
from fuzzy.fuzzify.Plain import Plain
from fuzzy.set.Trapez import Trapez


# PAy
def generate_pay(bad_low, bad_high, ok_low, ok_high, good_low, good_high ):
    alright = (bad_high + ok_low)/2
    fine = (ok_high + good_low)/2

    bad_slope = 5
    bad_low = bad_low if bad_low > 0 else 1    

    pay_bad = Polygon()
    pay_bad.add(x = 0.0, y= 0.0)
    pay_bad.add(x = bad_low, y= 1.0)
    pay_bad.add(x = bad_high, y= 1.0)
    pay_bad.add(x = bad_high+bad_slope, y= 0.0)
    #pay_bad.add(x = bad_slope+bad_slope, y= 0.0)


    alright_slope = 10 if bad_high > 10 else 0
    pay_alright = Polygon()
    pay_alright.add(x =  bad_high - alright_slope, y= 0.0)
    pay_alright.add(x =  alright, y= 1.0)
    pay_alright.add(x =  ok_low + alright_slope, y= 0.0)

    
    ok_slope = 5 if ok_low > 5 else 0
    pay_ok = Polygon()
    pay_ok.add(x =  ok_low - ok_slope , y= 0.0)
    pay_ok.add(x =  ok_low, y= 1.0)
    pay_ok.add(x =  ok_high, y= 1.0)
    pay_ok.add(x =  ok_high + 2*ok_slope, y= 0.0)

    fine_slope = 15 if ok_high > 15 else 0
    pay_fine = Polygon()
    pay_fine.add(x =  ok_high - fine_slope, y= 0.0)
    pay_fine.add(x =  fine, y= 1.0)
    pay_fine.add(x =  good_low + fine_slope, y= 0.0)

    good_slope = 20 if good_low > 20 else 0
    pay_good = Polygon()
    pay_good.add(x =  good_low - good_slope, y= 0.0)
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
    low_rep.add(x = 0, y = 0.0)
    low_rep.add(x = 0, y = 1.0)
    low_rep.add(x = low, y = 1.0)
    low_rep.add(x = med, y = 0.0)

    med_slope = 3 if med > 3 else 0
    med_rep = Polygon()
    med_rep.add(x = med - med_slope-1, y = 0.0)
    med_rep.add(x = med + med_slope-1, y = 1.0)
    med_rep.add(x = med + med_slope+1, y = 0.0)
    

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
    smallish = ((small_high + med_low)/2) if (small_high != med_low) else small_high
    largish = (med_high + large_low)/2 if (med_high != large_low) else large_low

    small_slope = 2 if small_low > 2 else 0

    employee_small = Polygon()
    employee_small.add(x=0, y=0)
    employee_small.add(x=small_low, y = 1)
    employee_small.add(x=small_high, y = 1)
    employee_small.add(x=small_high + small_slope, y = 0)

    smallish_slope = 10 if smallish > 10 else 0
    smallish_spread = 0 if smallish_slope > 0 else 0

    employee_smallish = Polygon()
    employee_smallish.add(x=smallish - smallish_slope, y=0)
    employee_smallish.add(x=smallish - smallish_spread, y = 1)
    employee_smallish.add(x=smallish + smallish_spread, y = 1)
    employee_smallish.add(x=smallish + 2*smallish_slope, y = 0)

    med_slope = 10 if med_low > 10 else 0
    med_spread = 0
    #print(med_low,largish,med_slope,med_spread)

    employee_med = Polygon()
    employee_med.add(x=med_low - med_slope, y = 0)
    employee_med.add(x=med_low, y = 1)
    employee_med.add(x=med_high, y = 1)
    employee_med.add(x=med_high + med_slope, y = 0)


    largish_slope = 15 if med_high > 15 else 0
    largish_spread = 0 if largish_slope > 0 else 0

    employee_largish = Polygon()
    employee_largish.add(x=med_high - largish_slope, y=0)
    employee_largish.add(x=largish - largish_spread, y = 1)
    employee_largish.add(x=largish + largish_spread, y = 1)
    employee_largish.add(x=large_low + 0.5*largish_slope, y = 0)



    large_slope = 25 if large_low > 25 else 0
    large_spread = 0

    employee_large = Polygon()
    employee_large.add(x=large_low - 0.25*large_slope, y = 0 )
    employee_large.add(x=large_low, y = 1 )
    employee_large.add(x=large_high, y = 1 )
    employee_large.add(x=large_high + 2*large_slope, y = 0 )

    return {
        "small": employee_small,
	"smallish": employee_smallish,
        "med":employee_med,
	"largish": employee_largish,
        "large":employee_large
    }
