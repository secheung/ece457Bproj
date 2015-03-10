
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

def generateDocs(FuzzyController):
    system = FuzzyController.getFuzzySystem()
    from fuzzy.doc.plot.gnuplot import doc
    doc = doc.Doc("doc")
    doc.createDoc(system)
    doc.create2DPlot(system,"input_pay","happiness")
    doc.create2DPlot(system,"input_rep","happiness")
    doc.create2DPlot(system,"input_employees","happiness")

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hp",["plot"])
    except getopt.GetoptError:
        print 'main.py -p'
        sys.exit(2)

    controller = Controller();

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
