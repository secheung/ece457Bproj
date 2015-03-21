
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
        input_pay.adjectives["Low"] = Adjective(pay["bad"])
        input_pay.adjectives["Medium"] = Adjective(pay["ok"])
        input_pay.adjectives["High"] = Adjective(pay["high"])

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

        Happiness.adjectives["Low"] = Adjective(happiness.Happiness_bad)
        Happiness.adjectives["Medium"] = Adjective(happiness.Happiness_med)
        Happiness.adjectives["High"] = Adjective(happiness.Happiness_high)
        Happiness.failsafe = 0.0 # let it output 0.0 if no COG available

        s = self.system

        rule1 = Rule(
            adjective=s.variables["happiness"].adjectives["High"],
            operator=Compound(FuzzyAnd(),
                              Input(s.variables['input_pay'].adjectives["High"]),
                              Input(s.variables['input_rep'].adjectives["Recognized"])),
            )

        rule2 = Rule(
            adjective=s.variables["happiness"].adjectives["Low"],
            operator=Compound(FuzzyAnd(),
                              Input(s.variables['input_pay'].adjectives["Low"]),
                              Input(s.variables['input_rep'].adjectives["Unnoticed"])),
            )

        rule3 = Rule(
            adjective=s.variables["happiness"].adjectives["High"],
            operator=Compound(FuzzyAnd(),
                              Input(s.variables['input_pay'].adjectives["Medium"]),
                              Input(s.variables['input_rep'].adjectives["Recognized"])),
            )

        rule4 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Low"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Low"]),
                              Input(input_employees.adjectives["Large"])),
            CER=fuzzy.norm.Min.Min())

        rule5 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Medium"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["Low"]),
                              Input(input_employees.adjectives["Small"])),
            CER=fuzzy.norm.Min.Min())

        rule6 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["High"]),
                              Input(input_employees.adjectives["Small"])),
            CER=fuzzy.norm.Min.Min())

        rule7 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["High"]),
                              Input(input_employees.adjectives["Medium"])),
            CER=fuzzy.norm.Min.Min())

        rule8 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(FuzzyAnd(),
                              Input(input_pay.adjectives["High"]),
                              Input(input_employees.adjectives["Large"])),
            CER=fuzzy.norm.Min.Min())

        rule9 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Low"],
            operator=Compound(FuzzyAnd(),
                              Input(input_rep.adjectives["Unnoticed"]),
                              Input(input_employees.adjectives["Small"])),
            CER=fuzzy.norm.Min.Min())

        rule10 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Low"],
            operator=Compound(FuzzyAnd(),
                              Input(input_rep.adjectives["Unnoticed"]),
                              Input(input_employees.adjectives["Large"])),
            CER=fuzzy.norm.Min.Min())

        rule11 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(FuzzyAnd(),
                              Input(input_rep.adjectives["Recognized"]),
                              Input(input_employees.adjectives["Small"])),
            CER=fuzzy.norm.Min.Min())

        rule12 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(FuzzyAnd(),
                              Input(input_rep.adjectives["Recognized"]),
                              Input(input_employees.adjectives["Large"])),
            CER=fuzzy.norm.Min.Min())

        self.system.rules["highpay_recognized"] = rule1 
        self.system.rules["lowpay_unnoticed"] = rule2 
        self.system.rules["medpay_recognized"] = rule3 
        self.system.rules["lowpay_large"] = rule4 
        self.system.rules["lowpay_small"] = rule5 
        self.system.rules["highpay_small"] = rule6 
        self.system.rules["highpay_med"] = rule7 
        self.system.rules["highpay_large"] = rule8 
        self.system.rules["unnoticed_small"] = rule9 
        self.system.rules["unnoticed_large"] = rule10 
        self.system.rules["recognized_small"] = rule11 
        self.system.rules["recognized_large"] = rule12 

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
