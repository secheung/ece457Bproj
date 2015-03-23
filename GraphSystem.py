from fuzzy.doc.plot.gnuplot import doc
from fuzzy.System import System
from fuzzy.set.Set import Set, norm, merge
from fuzzy.set.Polygon import Polygon
from fuzzy.norm.Min import Min
from fuzzy.norm.Max import Max
from fuzzy import Rule
from fuzzy.operator.Compound import Compound
from fuzzy.operator.Input import Input
from fuzzy.operator.Not import Not
from fuzzy.operator.Const import Const

import os
import shutil

class GraphSystem(System):
    def __init__(self,description="",rules=None,directory="graphsystem"):
        super(GraphSystem, self).__init__(description=description)
        self.directory = directory
        self.fuzzified_sets = {}
        self.inf_input_sets = {}
        self.inf_output_all_sets = {}
        self.inf_output_merged_sets = {}
        self.inf_output_cer_sets = {}
        self.activated_sets = {}
        self.final_sets = {}

    def reset(self):
        super(GraphSystem, self).reset()
        self.fuzzified_sets = {}
        self.inf_input_sets = {}
        self.inf_output_all_sets = {}
        self.inf_output_merged_sets = {}
        self.inf_output_cer_sets = {}
        self.activated_sets = {}
        self.final_sets = {}

    def calculate(self, input, output, input_name):
        # hope that the input_name has valid filename characters...
        self.input_name = input_name.replace(' ', '_')
        self.output_location = self.directory + "/" + self.input_name
        self.saveLocation = self.output_location + "/plots"
        if not os.path.exists(self.saveLocation):
            os.makedirs(self.saveLocation)
        self.plotDoc = doc.Doc(self.saveLocation)
        self.plotDoc.createDoc(self)
        
        super(GraphSystem, self).calculate(input, output)

        shutil.copy("graphsystem_viewer.html", self.output_location)

    def fuzzify(self, input):
        super(GraphSystem, self).fuzzify(input)
       
        # make graphs to plot
        for var_name in input:
            var = self.variables[var_name]
            fuzzified_set = {}
            for adj_name, adj in var.adjectives.items():
                intersection = adj.getMembership() # may be None
                if intersection:
                    # maybe incorporate segment_size... but from where?
                    # Min should be fine
                    fuzzified_adj = norm(Min(), adj.set, intersection)
                else:
                    # create zero line at y=0 to preserve x range (for graphing)
                    x_min, x_max = doc.getMinMax(adj.set)
                    fuzzified_adj = Polygon([(x_min, 0.0),(x_max, 0.0)])
                fuzzified_set[adj_name] = fuzzified_adj
           
            self.fuzzified_sets[var_name] = fuzzified_set

            # try to plot
            title = "fuzzified_" + var_name
            xlabel = var.description
            unit = var.unit
            self.plotDoc.createDocSets(fuzzified_set,title,description=xlabel,units=unit)

    def inference(self):
        super(GraphSystem, self).inference()
        
        for rule_name, rule in self.rules.items():
            output_adj_name, output_input_name = rule.adjective.getName(self)
            inf_output_all_set = {}
            inf_output_merged_set = {}
            inf_output_cer_set = {}
           
            inputs = []
            if type(rule.operator) is Compound:
                inputs = rule.operator.inputs
            elif type(rule.operator) is Input:
                inputs = [rule.operator]
            elif type(rule.operator) is Not:
                inputs = [rule.operator.input]
            elif type(rule.operator) is Const: 
                pass # ignored... not coded

            # get plot for each input (e.x. input_pay.low, input_rep.unnoticed) in a rule
            for rule_input in inputs:
                adj = rule_input.adjective 
                adj_name, input_name = adj.getName(self)
                if input_name in self.inf_input_sets and adj_name in self.inf_input_sets[input_name]:
                    # reuse
                    input_set = self.inf_input_sets[input_name][adj_name]
                else:
                    # copy sets
                    input_set = {}
                    for key_adj_name, value_set in self.fuzzified_sets[input_name].items():
                        if key_adj_name == adj_name:
                            input_set[key_adj_name] = value_set
                        else:
                            # may be a bug here
                            x_min, x_max = doc.getMinMax(value_set)
                            input_set[key_adj_name] = Polygon([(x_min, 0.0),(x_max, 0.0)])

                    if input_name not in self.inf_input_sets:
                        self.inf_input_sets[input_name] = {}
                    self.inf_input_sets[input_name][adj_name] = input_set

                # try to plot
                title = "rule_" + rule_name + "_" + input_name
                xlabel = self.variables[input_name].description 
                unit = self.variables[input_name].unit
                self.plotDoc.createDocSets(input_set,title,description=xlabel,units=unit)

                # get inferenced output
                l = input_name + "." + adj_name
                out_x_min, out_x_max = doc.getGlobalMinMax(doc.getSets(self.variables[output_input_name]))
                # Inputs norm'd via operator specified in rule.operator
                norm_to_use = Min()
                if type(rule.operator) is Compound:
                    norm_to_use = rule.operator.norm
                inf_output_all = norm(norm_to_use, rule.adjective.set, adj.getMembership())
                # Max is fine, this is for graphing purposes
                inf_output_all = merge(Max(), inf_output_all, Polygon([(out_x_min,0.0),(out_x_max,0.0)]))
                inf_output_all_set[l] = inf_output_all

                # merged
                if output_input_name not in inf_output_merged_set:
                    inf_output_merged_set[output_input_name] = inf_output_all
                else:
                    # Outputs joined using norm specified by Rule
                    inf_output_merged_set[output_input_name] = merge(Min(), 
                                                                     inf_output_merged_set[output_input_name], 
                                                                     inf_output_all)
            
            inf_output_cer_set[output_input_name] = norm(rule.CER or rule.__CER,
                                                         inf_output_merged_set[output_input_name],
                                                         rule.certainty)
            
            self.inf_output_all_sets[rule_name] = inf_output_all_set
            self.inf_output_merged_sets[rule_name] = inf_output_merged_set
            self.inf_output_cer_sets[rule_name] = inf_output_cer_set

            # try to plot
            title = "rule_" + rule_name + "_output_all_" + output_input_name + "_" + output_adj_name
            xlabel = output_input_name
            unit = self.variables[output_input_name].unit
            self.plotDoc.createDocSets(inf_output_all_set,title,description=xlabel,units=unit)
            
            # try to plot merged
            title = "rule_" + rule_name + "_output_merged_" + output_input_name + "_" + output_adj_name
            xlabel = output_input_name
            unit = self.variables[output_input_name].unit
            self.plotDoc.createDocSets(inf_output_merged_set,title,description=xlabel,units=unit)

            # try to plot certainty
            title = "rule_" + rule_name + "_output_cer_" + output_input_name + "_" + output_adj_name
            xlabel = output_input_name
            unit = self.variables[output_input_name].unit
            self.plotDoc.createDocSets(inf_output_cer_set,title,description=xlabel,units=unit)

    def defuzzify(self, output):
        super(GraphSystem, self).defuzzify(output)

        for var_name in output.keys():
            var = self.variables[var_name]
            # shows the adjectives, prior to combining
            activated_sets = var.defuzzify.activated_sets
            # shows the final combined set, used defuzzify (e.x. COG)
            final_sets = {var_name : var.defuzzify.accumulated_set}

            self.activated_sets[var_name] = activated_sets
            self.final_sets[var_name] = final_sets

            # try to plot
            title = "activated_sets"
            xlabel = var.description
            unit = var.unit
            self.plotDoc.createDocSets(activated_sets,title,description=xlabel,units=unit)
            
            title = "final_inference"
            self.plotDoc.createDocSets(final_sets,title,description=xlabel,units=unit)
