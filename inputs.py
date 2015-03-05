
from fuzzy.InputVariable import InputVariable
from fuzzy.Adjective import Adjective
from fuzzy.set.Polygon import Polygon
from fuzzy.fuzzify.Plain import Plain


        # PAy
pay_bad = Polygon()
pay_bad.add(x =     0, y= 0.0)
pay_bad.add(x =     1, y= 1.0)
pay_bad.add(x =  25.0, y= 1.0)
pay_bad.add(x =  35.5, y= 0.0)

pay_ok = Polygon()
pay_ok.add(x =  30.0, y= 0.0)
pay_ok.add(x =  35.0, y= 1.0)
pay_ok.add(x =  40.0, y= 1.0)
pay_ok.add(x =  50.0, y= 0.0)

pay_good = Polygon()
pay_good.add(x =  50.0, y= 0.0)
pay_good.add(x =  60.0, y= 1.0)
pay_good.add(x =  100.0, y= 1.0)
pay_good.add(x =  101.0, y= 0.0)

low_rep = Polygon()
low_rep.add(x = 0, y = 1.0)
low_rep.add(x = 2, y = 1.0)
low_rep.add(x = 4, y = 0.0)

high_rep = Polygon()
high_rep.add(x = 3, y= 0.0)
high_rep.add(x = 6, y = 1.0)
high_rep.add(x = 10, y = 1.0)
