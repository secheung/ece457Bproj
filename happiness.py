
from fuzzy.InputVariable import InputVariable
from fuzzy.OutputVariable import OutputVariable
from fuzzy.Adjective import Adjective
from fuzzy.set.Polygon import Polygon
from fuzzy.fuzzify.Plain import Plain


Happiness_bad = Polygon()
Happiness_bad.add(x =  0.0, y= 0.0)
Happiness_bad.add(x =  1.0, y= 1.0)
Happiness_bad.add(x =  15.0, y= 1.0)
Happiness_bad.add(x =  25.0, y= 0.0)

Happiness_badish = Polygon()
Happiness_badish.add(x =  10.0, y= 0.0)
Happiness_badish.add(x =  20.0, y= 1.0)
Happiness_badish.add(x =  30.0, y= 1.0)
Happiness_badish.add(x =  40.0, y= 0.0)

Happiness_med = Polygon()
Happiness_med.add(x =  30.0, y= 0.0)
Happiness_med.add(x =  35.0, y= 1.0)
Happiness_med.add(x =  50.0, y= 1.0)
Happiness_med.add(x =  60.0, y= 0.0)

Happiness_goodish = Polygon()
Happiness_goodish.add(x =  50, y= 0.0)
Happiness_goodish.add(x =  55, y= 1.0)
Happiness_goodish.add(x =  75, y= 1.0)
Happiness_goodish.add(x =  85, y= 0.0)

Happiness_good = Polygon()
Happiness_good.add(x =  78.0, y= 0.0)
Happiness_good.add(x =  82.0, y= 1.0)
Happiness_good.add(x =  99.0, y= 1.0)
Happiness_good.add(x =  100.0, y= 0.0)
