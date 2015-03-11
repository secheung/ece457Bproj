
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
        input_pay.adjectives["Ok"] = Adjective(pay["ok"])
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
        input_employees.adjectives["Medium"] = Adjective(employee["med"])
        input_employees.adjectives["Large"] = Adjective(employee["large"])

        # Input: Reputation
        user_rep = user["rep"]
        rep = inputs.generate_rep(user_rep["low"], user_rep["high"])
        input_rep = InputVariable(fuzzify=Plain(),
                                  description="Reputation",
                                  min=0, max=10)
        self.system.variables["input_rep"] = input_rep
        input_rep.adjectives["Unnoticed"] = Adjective(rep["low"])
        input_rep.adjectives["Recognized"] = Adjective(rep["high"])

        Happiness = OutputVariable(defuzzify=MaxLeft(),
                                   description="Happiness",
                                   min=0.0, max=100.0)
        self.system.variables["happiness"] = Happiness

        Happiness.adjectives["Bad"] = Adjective(happiness.Happiness_bad)
        Happiness.adjectives["Med"] = Adjective(happiness.Happiness_med)
        Happiness.adjectives["Good"] = Adjective(happiness.Happiness_good)
        Happiness.failsafe = 0.0 # let it output 0.0 if no COG available

        s = self.system

        rule1 = Rule(
            adjective=s.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
                              Input(s.variables['input_pay'].adjectives["Ok"]),
                              Input(s.variables['input_rep'].adjectives["Recognized"])),
            )

        rule2 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Good"],
            operator=Compound(Input(input_pay.adjectives["Good"])),
            CER=fuzzy.norm.Min.Min())

        rule3 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Med"],
            operator=Compound(FuzzyAnd(),
                              Input(input_employees.adjectives["Small"]),
                              Input(input_pay.adjectives["Bad"])),
            CER=fuzzy.norm.Min.Min())

        rule4 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Bad"],
            operator=Compound(FuzzyAnd(),
                              Input(input_rep.adjectives["Unnoticed"]),
                              Input(input_pay.adjectives["Bad"])),
            CER=fuzzy.norm.Min.Min())

        rule5 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Med"],
            operator=Compound(FuzzyAnd(),
                              Input(input_employees.adjectives["Large"]),
                              Input(input_pay.adjectives["Ok"])),
            CER=fuzzy.norm.Min.Min())

        rule6 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Good"],
            operator=Compound(FuzzyAnd(),
                              Input(input_rep.adjectives["Recognized"]),
                              Input(input_employees.adjectives["Small"])),
            CER=fuzzy.norm.Min.Min())

        self.system.rules["rule1"] = rule1
        self.system.rules["rule2"] = rule2
        self.system.rules["rule3"] = rule3
        self.system.rules["rule4"] = rule4
        self.system.rules["rule5"] = rule5
        self.system.rules["rule6"] = rule6

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
