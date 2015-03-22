
import fuzzy
from fuzzy.InputVariable import InputVariable
from fuzzy.OutputVariable import OutputVariable
from fuzzy.Adjective import Adjective
from fuzzy.fuzzify.Plain import Plain
from fuzzy.defuzzify.COG import COG
from fuzzy.defuzzify.MaxLeft import MaxLeft
from fuzzy.defuzzify.MaxRight import MaxRight
from fuzzy.Rule import Rule
from fuzzy.norm.FuzzyAnd import FuzzyAnd
from fuzzy.norm.FuzzyOr import FuzzyOr
from fuzzy.operator.Not import Not
from fuzzy.operator.Input import Input
from fuzzy.operator.Compound import Compound

import inputs
import happiness


class Controller(object):
    def __init__(self, user):
        # create system object
        self.system = fuzzy.System.System()

        # Input: Pay
        input_pay = InputVariable(fuzzify=Plain(),
                                  description="Pay",
                                  min=0, max=101)
        self.system.variables["input_pay"] = input_pay

        user_pay = user["salary"]
        pay = inputs.generate_pay(user_pay["bad_low"],
                                        user_pay["bad_high"],
                                        user_pay["ok_low"],
                                        user_pay["ok_high"],
                                        user_pay["good_low"],
                                        user_pay["good_high"])
        input_pay.adjectives["Bad"] = Adjective(pay["bad"])
        input_pay.adjectives["Alright"] = Adjective(pay["alright"])
        input_pay.adjectives["Ok"] = Adjective(pay["ok"])
        input_pay.adjectives["Fine"] = Adjective(pay["fine"])
        input_pay.adjectives["Good"] = Adjective(pay["good"])

        # Input: Number of Employees
        user_size = user["employees"]
        employee = inputs.generate_employee(
            user_size["small_low"],
            user_size["small_high"],
            user_size["med_low"],
            user_size["med_high"],
            user_size["large_low"],
            user_size["large_high"]
        )
        input_employees = InputVariable(fuzzify=Plain(),
                                        description="Number of Employees",
                                        min=1, max=100)
        self.system.variables["input_employees"] = input_employees
        input_employees.adjectives["Small"] = Adjective(employee["small"])
	input_employees.adjectives["Smallish"] = Adjective(employee["smallish"])
        input_employees.adjectives["Medium"] = Adjective(employee["med"])
	input_employees.adjectives["Largish"] = Adjective(employee["largish"])
        input_employees.adjectives["Large"] = Adjective(employee["large"])

        # Input: Reputation
        user_rep = user["rep"]
        rep = inputs.generate_rep(user_rep["low"], user_rep["high"])
        input_rep = InputVariable(fuzzify=Plain(),
                                  description="Reputation",
                                  min=0, max=10)
        self.system.variables["input_rep"] = input_rep
        input_rep.adjectives["Unnoticed"] = Adjective(rep["low"])
	input_rep.adjectives["Upcoming"] = Adjective(rep["med"])
        input_rep.adjectives["Recognized"] = Adjective(rep["high"])

        Happiness = OutputVariable(defuzzify=MaxLeft(),
                                   description="Happiness",
                                   min=0.0, max=100.0)
        self.system.variables["happiness"] = Happiness

        Happiness.adjectives["Bad"] = Adjective(happiness.Happiness_bad)
	Happiness.adjectives["Badish"] = Adjective(happiness.Happiness_badish)
        Happiness.adjectives["Med"] = Adjective(happiness.Happiness_med)
	Happiness.adjectives["Goodish"] = Adjective(happiness.Happiness_goodish)
        Happiness.adjectives["Good"] = Adjective(happiness.Happiness_good)
        Happiness.failsafe = 0.0 # let it output 0.0 if no COG available

        s = self.system

	#Best - large companies with good pay and good reputation give good happiness i.e google
        #rule1 = Rule(
        #    adjective=s.variables["happiness"].adjectives["Good"],
        #    operator=Compound(FuzzyAnd(),
	#		      Compound(FuzzyAnd(),
	#	                       Input(input_employees.adjectives["Large"]),
	#	                       Input(input_pay.adjectives["Good"])),
	#		      Input(input_rep.adjectives["Recognized"])
	#		     ),
        #   CER=fuzzy.norm.Min.Min())

        rule1d1 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Large"]),
		              Input(input_pay.adjectives["Good"]),
			     ),
		     CER=fuzzy.norm.Min.Min())
        rule1d2 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Large"]),
		              Input(input_rep.adjectives["Recognized"]),
			     ),
		     CER=fuzzy.norm.Min.Min())

        rule1d3 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_rep.adjectives["Recognized"]),
		              Input(input_pay.adjectives["Good"]),
			     ),
		     CER=fuzzy.norm.Min.Min())

	#Worst - small companies with bad pay and bad reputation give bad happiness
        #rule2 = Rule(
        #    adjective=s.variables["happiness"].adjectives["Bad"],
        #    operator=Compound(FuzzyAnd(),
	#		      Compound(FuzzyAnd(),
	#	                       Input(input_employees.adjectives["Small"]),
	#	                       Input(input_pay.adjectives["Bad"])),
	#		      Input(input_rep.adjectives["Unnoticed"])
	#		     ),
        #    CER=fuzzy.norm.Min.Min())

        rule2d1 = Rule(
            adjective=s.variables["happiness"].adjectives["Bad"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Small"]),
		              Input(input_pay.adjectives["Bad"])
			     ),
            CER=fuzzy.norm.Min.Min())

        rule2d2 = Rule(
            adjective=s.variables["happiness"].adjectives["Bad"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Small"]),
			      Input(input_rep.adjectives["Unnoticed"])
			     ),
            CER=fuzzy.norm.Min.Min())

        rule2d3 = Rule(
            adjective=s.variables["happiness"].adjectives["Bad"],
            operator=Compound(FuzzyAnd(),
		              Input(input_pay.adjectives["Bad"]),
			      Input(input_rep.adjectives["Unnoticed"])
			     ),
            CER=fuzzy.norm.Min.Min())

	#Med - ok for ok pay and ok size company
        rule3 = Rule(
            adjective=s.variables["happiness"].adjectives["Med"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Ok"]),
                              Input(input_employees.adjectives["Medium"])),
            CER=fuzzy.norm.Min.Min())


	#street smart rules
	#small company with good pay and good rep
        #rule4 = Rule(
        #    adjective=s.variables["happiness"].adjectives["Good"],
        #    operator=Compound(FuzzyAnd(),
	#		      Compound(FuzzyAnd(),
	#	                       Input(input_employees.adjectives["Small"]),
	#	                       Input(input_pay.adjectives["Good"])),
	#		      Input(input_rep.adjectives["Recognized"])
	#		     ),
        #    CER=fuzzy.norm.Min.Min())
	
        rule4d1 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Small"]),
		              Input(input_pay.adjectives["Good"])
			     ),
            CER=fuzzy.norm.Min.Min())

        rule4d2 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Small"]),
                              Input(input_rep.adjectives["Recognized"])
			     ),
            CER=fuzzy.norm.Min.Min())

        rule4d3 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_pay.adjectives["Good"]),
                              Input(input_rep.adjectives["Recognized"])
			     ),
            CER=fuzzy.norm.Min.Min())

	#small company with no reputation is bad
        rule5 = Rule(
            adjective=s.variables["happiness"].adjectives["Bad"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Small"]),
			      Input(input_rep.adjectives["Unnoticed"])
			     ),
            CER=fuzzy.norm.Min.Min())

	#med companies with good rep get a bit better
        rule6 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Medium"]),
			      Input(input_rep.adjectives["Recognized"])
			     ),
            CER=fuzzy.norm.Min.Min())
	
	#med company with good pay is good
        rule7 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Medium"]),
			      Input(input_pay.adjectives["Good"])
			     ),
            CER=fuzzy.norm.Min.Min())

	#Granularity rules--------------------------------------------------------------------------
	#pay over certain amount eventually stops producing happiness
	rule20 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Goodish"],
            operator=Input(input_pay.adjectives["Fine"]),
            CER=fuzzy.norm.Min.Min())

	#pay less than a certain amount is desparaging
	rule21 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Badish"],
            operator=Compound(FuzzyOr(),
			 	  Input(input_pay.adjectives["Alright"]),
				  Input(input_pay.adjectives["Ok"])
				 ),
            CER=fuzzy.norm.Min.Min())
	
        #extension of rule 4 - good pay small/large company 
        rule22d1 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Smallish"]),
		              Input(input_pay.adjectives["Good"])
			     ),
            CER=fuzzy.norm.Min.Min())

        rule22d2 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
		              Input(input_employees.adjectives["Largish"]),
		              Input(input_pay.adjectives["Good"])
			     ),
            CER=fuzzy.norm.Min.Min())

	#extension of rule2 - bad pay small company
	rule23d1 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Bad"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Bad"]),
                              Input(input_employees.adjectives["Smallish"])),
            CER=fuzzy.norm.Min.Min())

	rule23d2 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Badish"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Alright"]),
                              Input(input_employees.adjectives["Smallish"])),
            CER=fuzzy.norm.Min.Min())

	#bad pay large company
	rule24d1 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Bad"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Bad"]),
                              Input(input_employees.adjectives["Large"])),
            CER=fuzzy.norm.Min.Min())

	rule24d2 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Badish"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Bad"]),
                              Input(input_employees.adjectives["Largish"])
                             ),
            CER=fuzzy.norm.Min.Min())

	#bad pay med company
	rule25d1 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Badish"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Bad"]),
                              Input(input_employees.adjectives["Medium"])
                             ),
            CER=fuzzy.norm.Min.Min())

	#ok pay any company size
	rule26d1 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Med"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Ok"]),
                              Compound(
                                      FuzzyOr(),
                                      Input(input_employees.adjectives["Small"]),
                                      Input(input_employees.adjectives["Smallish"])
                                  )),
            CER=fuzzy.norm.Min.Min())

	#rep vs pay
	rule27d1 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
                              Compound( FuzzyOr(),
					Input(input_pay.adjectives["Good"]),
					Input(input_pay.adjectives["Fine"])
                                      ),
                              Compound( FuzzyOr(),
					Input(input_rep.adjectives["Upcoming"]),
					Input(input_rep.adjectives["Recognized"])
                                      )),
            CER=fuzzy.norm.Min.Min())
	
	rule27d2 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Goodish"],
            operator=Compound(FuzzyAnd(),
                              Compound( FuzzyOr(),
					Input(input_pay.adjectives["Alright"]),
					Input(input_pay.adjectives["Ok"])
                                      ),
                              Compound( FuzzyOr(),
					Input(input_rep.adjectives["Upcoming"]),
					Input(input_rep.adjectives["Recognized"])
                                      )),
            CER=fuzzy.norm.Min.Min())

	rule27d3 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Goodish"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Fine"]),
                              Input(input_rep.adjectives["Upcoming"])),
            CER=fuzzy.norm.Min.Min())
	
	rule27d4 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Med"],
            operator=Compound(FuzzyAnd(),
			      Input(input_pay.adjectives["Fine"]),
                              Input(input_rep.adjectives["Unnoticed"])),
            CER=fuzzy.norm.Min.Min())

	rule27d5 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Med"],
            operator=Compound(FuzzyAnd(),
			      Input(input_pay.adjectives["Good"]),
                              Input(input_rep.adjectives["Unnoticed"])),
            CER=fuzzy.norm.Min.Min())

	rule27d6 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Badish"],
            operator=Compound(FuzzyAnd(),
                              Compound( FuzzyOr(),
					Input(input_pay.adjectives["Ok"]),
					Input(input_pay.adjectives["Alright"])
                                      ),
                              Input(input_rep.adjectives["Unnoticed"])),
            CER=fuzzy.norm.Min.Min())

        #rep vs employees
        #upcoming/recognized and small
        rule28d1 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Goodish"],
            operator=Compound(FuzzyAnd(),
                              Compound( FuzzyOr(),
					Input(input_employees.adjectives["Small"]),
					Input(input_employees.adjectives["Smallish"])
                                      ),
                              Compound( FuzzyOr(),
                                        Input(input_rep.adjectives["Upcoming"]),
                                        Input(input_rep.adjectives["Recognized"])
                                      )),
            CER=fuzzy.norm.Min.Min())

	#upcoming/recognized and med
        rule28d2 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Goodish"],
            operator=Compound(FuzzyAnd(),
                              Compound( FuzzyOr(),
					Input(input_employees.adjectives["Medium"]),
					Input(input_employees.adjectives["Largish"])
                                      ),
                              Compound( FuzzyOr(),
                                        Input(input_rep.adjectives["Upcoming"]),
                                        Input(input_rep.adjectives["Recognized"])
                                      )),
            CER=fuzzy.norm.Min.Min())

	#unnoticed and small
        rule28d3 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Bad"],
            operator=Compound(FuzzyAnd(),
                              Compound( FuzzyOr(),
					Input(input_employees.adjectives["Small"]),
					Input(input_employees.adjectives["Smallish"])
                                      ),
                              Input(input_rep.adjectives["Unnoticed"])),
            CER=fuzzy.norm.Min.Min())

	#unnoticed and med
        rule28d4 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Badish"],
            operator=Compound(FuzzyAnd(),
                              Compound( FuzzyOr(),
					Input(input_employees.adjectives["Medium"]),
					Input(input_employees.adjectives["Largish"])
                                      ),
                              Input(input_rep.adjectives["Unnoticed"])),
            CER=fuzzy.norm.Min.Min())

	#recognized and large - better to get into smaller upcoming company than large known company
        rule28d5 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Med"],
            operator=Compound(FuzzyAnd(),
                              Input(input_employees.adjectives["Large"]),
                              Input(input_rep.adjectives["Recognized"])
                             ),
            CER=fuzzy.norm.Min.Min())

	#upcoming large - sketch since large and upcoming
        rule28d6 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Badish"],
            operator=Compound(FuzzyAnd(),
                              Input(input_employees.adjectives["Large"]),
                              Input(input_rep.adjectives["Upcoming"])
                             ),
            CER=fuzzy.norm.Min.Min())

        self.system.rules["rule1d1"] = rule1d1
	self.system.rules["rule1d2"] = rule1d2
	self.system.rules["rule1d3"] = rule1d3
	self.system.rules["rule2d1"] = rule2d1
	self.system.rules["rule2d2"] = rule2d2
	self.system.rules["rule2d3"] = rule2d3
	self.system.rules["rule3"] = rule3
	self.system.rules["rule4d1"] = rule4d1
	self.system.rules["rule4d2"] = rule4d2
	self.system.rules["rule4d3"] = rule4d3
	self.system.rules["rule5"] = rule5
	self.system.rules["rule6"] = rule6
	self.system.rules["rule7"] = rule7

	#Granularity rules start at 20
        self.system.rules["rule20"] = rule20
        self.system.rules["rule21"] = rule21
	self.system.rules["rule22d1"] = rule22d1
	self.system.rules["rule22d2"] = rule22d2
	self.system.rules["rule23d1"] = rule23d1
	self.system.rules["rule23d2"] = rule23d2
	self.system.rules["rule24d1"] = rule24d1
	self.system.rules["rule24d2"] = rule24d2
	self.system.rules["rule25d1"] = rule25d1
	self.system.rules["rule26d1"] = rule26d1
	self.system.rules["rule27d1"] = rule27d1
	self.system.rules["rule27d2"] = rule27d2
	self.system.rules["rule27d3"] = rule27d3
	self.system.rules["rule27d4"] = rule27d4
	self.system.rules["rule27d5"] = rule27d5
	self.system.rules["rule27d6"] = rule27d6
	self.system.rules["rule28d1"] = rule28d1
	self.system.rules["rule28d2"] = rule28d2
	self.system.rules["rule28d3"] = rule28d3
	self.system.rules["rule28d4"] = rule28d4
	self.system.rules["rule28d5"] = rule28d5
	self.system.rules["rule28d6"] = rule28d6

    def calculate(self, salary, employees, reputation):
        input_vals = {
            "input_pay": salary,
            "input_employees": employees,
            "input_rep": reputation
        }
        output_vals = {"happiness": 0.0}
        self.system.calculate(input=input_vals, output=output_vals)

        r = output_vals["happiness"]
        return r

    def getFuzzySystem(self):
        return self.system;
