
import fuzzy.System
import math

from fuzzy.InputVariable import InputVariable
from fuzzy.OutputVariable import OutputVariable
from fuzzy.fuzzify.Plain import Plain
from fuzzy.defuzzify.COG import COG
from fuzzy.defuzzify.MaxLeft import MaxLeft
from fuzzy.defuzzify.MaxRight import MaxRight
from fuzzy.Adjective import Adjective
from fuzzy.set.Polygon import Polygon

system = fuzzy.System.System()

#input--------------------------------------

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

input_pay = InputVariable(fuzzify=Plain())
system.variables["Pay"] = input_pay
input_pay.adjectives["Bad"] = Adjective(pay_bad)
input_pay.adjectives["Ok"] = Adjective(pay_ok)
input_pay.adjectives["Good"] = Adjective(pay_good)


input_job_pay = InputVariable(fuzzify=Plain())
system.variables["JobPay"] = input_job_pay
input_job_pay.adjectives["Bad"] = Adjective(pay_bad)
input_job_pay.adjectives["Ok"] = Adjective(pay_ok)
input_job_pay.adjectives["Good"] = Adjective(pay_good)



#consequences/output-------------------------
Happiness = OutputVariable(defuzzify=MaxLeft())

system.variables["Happiness"] = Happiness
Happiness.failsafe = 0.0 # let it output 0.0 if no COG available

Happiness_bad = Polygon()
Happiness_bad.add(x =  0.0, y= 0.0)
Happiness_bad.add(x =  1.0, y= 1.0)
Happiness_bad.add(x =  25.0, y= 1.0)
Happiness_bad.add(x =  30.0, y= 0.0)
Happiness.adjectives["Bad"] = Adjective(Happiness_bad)

Happiness_med = Polygon()
Happiness_med.add(x =  30.0, y= 0.0)
Happiness_med.add(x =  35.0, y= 1.0)
Happiness_med.add(x =  70.0, y= 1.0)
Happiness_med.add(x =  75.0, y= 0.0)
Happiness.adjectives["Med"] = Adjective(Happiness_med)

Happiness_good = Polygon()
Happiness_good.add(x =  70.0, y= 0.0)
Happiness_good.add(x =  72.0, y= 1.0)
Happiness_good.add(x =  99.0, y= 1.0)
Happiness_good.add(x =  100.0, y= 0.0)
Happiness.adjectives["Good"] = Adjective(Happiness_good)

#rules--------------------------------------
from fuzzy.Rule import Rule
from fuzzy.norm.Min import Min
from fuzzy.operator.Input import Input
from fuzzy.operator.Compound import Compound

#if Pay is Bad and JobPay is Bad then Happiness is Good
rule1 = Rule(   adjective=system.variables["Happiness"].adjectives["Good"],
                operator=Compound(
                                    Min(),
									Input(system.variables["Pay"].adjectives["Bad"]),
                                    Input(system.variables["JobPay"].adjectives["Bad"]),
				)
	    )

#if Pay is Good and JobPay is Bad then Happiness is Bad
rule2 = Rule(   adjective=system.variables["Happiness"].adjectives["Bad"],
                operator=Compound(
                                    Min(),
									Input(system.variables["Pay"].adjectives["Good"]),
                                    Input(system.variables["JobPay"].adjectives["Bad"]),
				)
	    )

#if Pay is Bad and JobPay is Ok then Happiness is Med
rule3 = Rule(   adjective=system.variables["Happiness"].adjectives["Med"],
                operator=Compound(
                                    Min(),
									Input(system.variables["Pay"].adjectives["Bad"]),
                                    Input(system.variables["JobPay"].adjectives["Ok"])
				)
	    )

system.rules["rule1"]=rule1
system.rules["rule2"]=rule2
system.rules["rule3"]=rule3


#execute-----------------------------------
data_in = {}
data_out = {'Happiness':0.0}
data_in["Pay"] = 35
data_in["JobPay"] = 25
system.calculate(data_in,data_out)

print data_out['Happiness']


