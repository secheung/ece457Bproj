
from fuzzy.InputVariable import InputVariable
from fuzzy.OutputVariable import OutputVariable
from fuzzy.Adjective import Adjective
from fuzzy.set.Polygon import Polygon
from fuzzy.fuzzify.Plain import Plain


Happiness_bad = Polygon()
Happiness_bad.add(x =  0.0, y= 0.0)
Happiness_bad.add(x =  1.0, y= 1.0)
Happiness_bad.add(x =  25.0, y= 1.0)
Happiness_bad.add(x =  30.0, y= 0.0)

Happiness_med = Polygon()
Happiness_med.add(x =  30.0, y= 0.0)
Happiness_med.add(x =  35.0, y= 1.0)
Happiness_med.add(x =  70.0, y= 1.0)
Happiness_med.add(x =  75.0, y= 0.0)

Happiness_good = Polygon()
Happiness_good.add(x =  70.0, y= 0.0)
Happiness_good.add(x =  72.0, y= 1.0)
Happiness_good.add(x =  99.0, y= 1.0)
Happiness_good.add(x =  100.0, y= 0.0)
