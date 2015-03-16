
import fuzzy.System
import math
import sys, getopt
from Controller import Controller
try:
    import Gnuplot
    have_Gnuplot = 1
except:
    have_Gnuplot = 0

companies = [
    {"name": "Acme Inc",
     "salary": 55,
     "employees": 150,
     "reputation": 7.5},
    {"name": "Smith Consulting",
     "salary": 90,
     "employees": 150,
     "reputation": 2.3},
    {"name": "John Engineering",
     "employees": 4,
     "salary": 35,
     "reputation": 9}]

users = [{#0
	    "salary": {
		"bad_low": 0,
		"bad_high": 10,
		"ok_low": 30,
		"ok_high": 50,
		"good_low": 90,
		"good_high": 100
	    },
	    "employees": {
		"small_low": 1,
		"small_high": 20,
		"med_low": 35,
		"med_high": 40,
		"large_low": 50,
		"large_high": 100
	    },
	    "rep": {
		"low": 3,
		"high": 4
	    }
    	},
	{#1
	    "salary": {
		"bad_low": 25,
		"bad_high": 35,
		"ok_low": 40,
		"ok_high": 50,
		"good_low": 75,
		"good_high": 100
	    },
	    "employees": {
		"small_low": 1,
		"small_high": 20,
		"med_low": 50,
		"med_high": 100,
		"large_low": 200,
		"large_high": 500
	    },
	    "rep": {
		"low": 3,
		"high": 8
	    }
    }]

def generateDocs(FuzzyController):
    system = FuzzyController.getFuzzySystem()
    from fuzzy.doc.plot.gnuplot import doc
    doc = doc.Doc("doc")    
    doc.createDoc(system)
    #doc.create2DPlot(system,"input_employees","happiness")
    #doc.create2DPlot(system,"input_rep","happiness")
    #doc.create2DPlot(system,"input_pay","happiness")
    
    #doc.create3DPlot(system,"input_pay","input_employees","happiness")
    #doc.create3DPlot(system,"input_rep","input_pay","happiness")
    doc.create3DPlot(system,"input_rep","input_employees","happiness")

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hp",["plot"])
    except getopt.GetoptError:
        print 'main.py -p'
        sys.exit(2)

    controller = Controller(users[0]);

    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -p'
            sys.exit()
        elif opt in ("-p", "--plot"):
            generateDocs(controller)
            sys.exit(0)

    for company in companies:
        res = controller.calculate(company["employees"], company["salary"], company["reputation"])
        print company["name"] + ": " + str(res)




if __name__ == "__main__":
    main(sys.argv[1:])
