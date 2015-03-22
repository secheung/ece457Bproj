
import fuzzy.System
import math
import sys, getopt
from Controller import Controller
import employee_data
import company_data

try:
    import Gnuplot
    have_Gnuplot = 1
except:
    have_Gnuplot = 0

def generateDocs(FuzzyController):
    system = FuzzyController.getFuzzySystem()
    from fuzzy.doc.plot.gnuplot import doc
    doc = doc.Doc("doc")    
    doc.createDoc(system)
    #doc.create2DPlot(system,"input_employees","happiness")
    #doc.create2DPlot(system,"input_rep","happiness")
    #doc.create2DPlot(system,"input_pay","happiness")
    
    #doc.create3DPlot(system,"input_employees","input_pay","happiness")
    doc.create3DPlot(system,"input_rep","input_pay","happiness")
    #doc.create3DPlot(system,"input_rep","input_employees","happiness")

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hp",["plot"])
    except getopt.GetoptError:
        print 'main.py -p'
        sys.exit(2)

    users = employee_data.getEmployeeData()
    companies = company_data.getCompanyData()
    controller = Controller(users[4]);

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


def testSystem(users, companies):
    for user in users:
        controller = Controller(user)
        print user["expected"]
        for company in companies:
            res = controller.calculate(company["employees"], company["salary"], company["reputation"])
            print company["name"] + ": " + str(res)
        print "\n"


if __name__ == "__main__":
    main(sys.argv[1:])
