from fuzzy.doc.plot.gnuplot import doc
from fuzzy.System import System
from fuzzy.set.Set import Set, norm, merge
from fuzzy.set.Polygon import Polygon
from fuzzy.norm.Min import Min
from fuzzy.norm.Max import Max

import os

class GraphSystem(System):
    def __init__(self,description="",variables=None,rules=None,directory="graphsystem"):
        super(GraphSystem, self).__init__(description=description,variables=variables,rules=rules)
        self.directory = directory
        self.fuzzified_sets = {}
        self.inf_input_sets = {}
        self.inf_output_sets = {}
        self.activated_sets = {}
        self.final_sets = {}

    def reset(self):
        super(GraphSystem, self).reset()
        self.fuzzified_sets = {}
        self.inf_input_sets = {}
        self.inf_output_sets = {}
        self.activated_sets = {}
        self.final_sets = {}

    def calculate(self, input, output, input_name):
        # hope that the input_name has valid filename characters...
        self.input_name = input_name.replace(' ', '_')
        self.saveLocation = self.directory + "/" + self.input_name + "/plots"
        if not os.path.exists(self.saveLocation):
            os.makedirs(self.saveLocation)
        self.plotDoc = doc.Doc(self.saveLocation)
        self.plotDoc.createDoc(self)
        
        super(GraphSystem, self).calculate(input, output)

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
            inf_output_set = {}
            # get plot for each input (e.x. input_pay.low, input_rep.unnoticed) in a rule
            for rule_input in rule.operator.inputs:
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
                x_min,y_min = doc.getMinMax(rule.adjective.set)
                fix_range = norm(Min(), rule.adjective.set, adj.getMembership())
                fix_range = merge(Max(), fix_range, Polygon([(x_min,0.0),(x_max,0.0)]))
                inf_output_set[l] = fix_range
                
            self.inf_output_sets[rule_name] = inf_output_set
            
            # try to plot
            output_adj_name = rule.adjective.getName(self)[1]
            title = "rule_" + rule_name + "_output_" + output_adj_name
            xlabel = output_adj_name
            unit = self.variables[output_adj_name].unit
            self.plotDoc.createDocSets(inf_output_set,title,description=xlabel,units=unit)

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
