
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
from fuzzy.norm.Min import Min
from fuzzy.operator.Input import Input
from fuzzy.operator.Compound import Compound
from fuzzy.norm.AlgebraicProduct import AlgebraicProduct
from fuzzy.norm.AlgebraicSum import AlgebraicSum
from fuzzy.norm.GeometricMean import GeometricMean

import inputs
import happiness
from GraphSystem import GraphSystem

class Controller(object):
    def __init__(self, user, useGraphSystem=False):
        print "Creating system for " + user["name"]

        self.user = user

        # create system object
        if useGraphSystem:
            self.system = GraphSystem()
        else:
            self.system = fuzzy.System.System()

        # Input: Pay
        input_pay = InputVariable(fuzzify=Plain(),
                                  description="Pay",
                                  min=0.0, max=200.0, unit="x1000 ($)")
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

        salary_pref = float(user["salary_pref"]) if "salary_pref" in user else 1.0

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
                                        min=1.0, max=1000.0, unit=None)
        self.system.variables["input_employees"] = input_employees
        input_employees.adjectives["Small"] = Adjective(employee["small"])
        input_employees.adjectives["Medium"] = Adjective(employee["med"])
        input_employees.adjectives["Large"] = Adjective(employee["large"])

        employees_pref = float(user["employees_pref"]) if "employees_pref" in user else 1.0

        # Input: Reputation
        user_rep = user["rep"]
        rep = inputs.generate_rep(user_rep["low"], user_rep["high"])
        input_rep = InputVariable(fuzzify=Plain(),
                                  description="Reputation",
                                  min=0.0, max=10.0, unit="/10")
        self.system.variables["input_rep"] = input_rep
        input_rep.adjectives["Unnoticed"] = Adjective(rep["low"])
        input_rep.adjectives["Recognized"] = Adjective(rep["high"])
        
        rep_pref = float(user["rep_pref"]) if "rep_pref" in user else 1.0

        # Input: Distance/Commute
        user_distance = user["commute"]
        commute_pref = inputs.generate_commute(user_distance["close"],
                                               user_distance["medium"],
                                               user_distance["far"])
        input_commute = InputVariable(fuzzify=Plain(),
                                      description="Distance",
                                      min=0.0, max=150.0, unit="minutes")
        self.system.variables["input_commute"] = input_commute
        input_commute.adjectives["Close"] = Adjective(commute_pref["close"])
        input_commute.adjectives["Medium"] = Adjective(commute_pref["medium"])
        input_commute.adjectives["Far"] = Adjective(commute_pref["far"])
    
        # Output: Happiness
        Happiness = OutputVariable(defuzzify=COG(failsafe=0.0),
                                   description="Happiness",
                                   min=0.0, max=100.0, unit="/100")
        self.system.variables["happiness"] = Happiness

        Happiness.adjectives["Low"] = Adjective(happiness.Happiness_bad)
        Happiness.adjectives["Medium"] = Adjective(happiness.Happiness_med)
        Happiness.adjectives["High"] = Adjective(happiness.Happiness_high)

        s = self.system

        rule_inputs_norm = Min()
        CER_norm = Min()
        lowered_certainty = 0.7

        rule1 = Rule(
            adjective=s.variables["happiness"].adjectives["High"],
            operator=Compound(rule_inputs_norm,
                              Input(s.variables['input_pay'].adjectives["High"]),
                              Input(s.variables['input_rep'].adjectives["Recognized"])),
            certainty=1.0,
            CER=CER_norm)

        rule2 = Rule(
            adjective=s.variables["happiness"].adjectives["Low"],
            operator=Compound(rule_inputs_norm,
                              Input(s.variables['input_pay'].adjectives["Low"]),
                              Input(s.variables['input_rep'].adjectives["Unnoticed"])),
            certainty=1.0,
            CER=CER_norm)

        rule3 = Rule(
            adjective=s.variables["happiness"].adjectives["High"],
            operator=Compound(rule_inputs_norm,
                              Input(s.variables['input_pay'].adjectives["Medium"]),
                              Input(s.variables['input_rep'].adjectives["Recognized"])),
            certainty=lowered_certainty,
            CER=CER_norm)

        rule4 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Low"],
            operator=Compound(rule_inputs_norm,
                              Input(input_pay.adjectives["Low"]),
                              Input(input_employees.adjectives["Large"])),
            certainty=lowered_certainty,
            CER=CER_norm)

        rule5 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Medium"],
            operator=Compound(rule_inputs_norm,
                              Input(input_pay.adjectives["Low"]),
                              Input(input_employees.adjectives["Small"])),
            certainty=1.0,
            CER=CER_norm)

        rule6 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(rule_inputs_norm,
                              Input(input_pay.adjectives["High"]),
                              Input(input_employees.adjectives["Small"])),
            certainty=lowered_certainty,
            CER=CER_norm)

        rule7 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(rule_inputs_norm,
                              Input(input_pay.adjectives["High"]),
                              Input(input_employees.adjectives["Medium"])),
            certainty=lowered_certainty,
            CER=CER_norm)

        rule8 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(rule_inputs_norm,
                              Input(input_pay.adjectives["High"]),
                              Input(input_employees.adjectives["Large"])),
            certainty=1.0,
            CER=CER_norm)

        rule9 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Low"],
            operator=Compound(rule_inputs_norm,
                              Input(input_rep.adjectives["Unnoticed"]),
                              Input(input_employees.adjectives["Small"])),
            certainty=1.0,
            CER=CER_norm)

        rule10 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Low"],
            operator=Compound(rule_inputs_norm,
                              Input(input_rep.adjectives["Unnoticed"]),
                              Input(input_employees.adjectives["Large"])),
            certainty=1.0,
            CER=CER_norm)

        rule11 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(rule_inputs_norm,
                              Input(input_rep.adjectives["Recognized"]),
                              Input(input_employees.adjectives["Small"])),
            certainty=lowered_certainty,
            CER=CER_norm)

        rule12 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Compound(rule_inputs_norm,
                              Input(input_rep.adjectives["Recognized"]),
                              Input(input_employees.adjectives["Large"])),
            certainty=1.0,
            CER=CER_norm)

        # distance rules
        rule13 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Input(input_commute.adjectives["Close"]),
            certainty=1.0,
            CER=CER_norm)

        rule14 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Medium"],
            operator=Input(input_commute.adjectives["Medium"]),
            certainty=1.0,
            CER=CER_norm)

        rule15 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Low"],
            operator=Input(input_commute.adjectives["Far"]),
            certainty=1.0,
            CER=CER_norm)

        rule16 = Rule(
            adjective=self.system.variables["happiness"].adjectives["High"],
            operator=Input(input_rep.adjectives["Recognized"]),
            certainty=1.0,
            CER=CER_norm)
            
        rule17 = Rule(
            adjective=self.system.variables["happiness"].adjectives["Medium"],
            operator=Input(input_rep.adjectives["Unnoticed"]),
            certainty=lowered_certainty,
            CER=CER_norm)

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
        self.system.rules["closedist"] = rule13
        self.system.rules["mediumdist"] = rule14
        self.system.rules["fardist"] = rule15
        self.system.rules["recognized"] = rule16
        self.system.rules["unnoticed"] = rule17

    def calculate(self, name, salary, employees, reputation, distance):
        input_vals = {
            "input_pay": salary,
            "input_employees": employees,
            "input_rep": reputation,
            "input_commute": distance
        }
        output_vals = {"happiness": 0.0}
        if type(self.system) is GraphSystem:
            self.system.calculate(input=input_vals, output=output_vals, input_name=name, user_name=self.user["name"])
        else:
            self.system.calculate(input=input_vals, output=output_vals)

        r = output_vals["happiness"]
        return r

    def getFuzzySystem(self):
        return self.system;
