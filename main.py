
import fuzzy.System
import math
import sys, getopt
from Controller import Controller
import employee_data
import company_data
import random

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
    # doc.create2DPlot(system,"input_pay","happiness")
    # doc.create2DPlot(system,"input_rep","happiness")
    # doc.create2DPlot(system,"input_employees","happiness")
    doc.create3DPlot(system,"input_rep","input_employees","happiness")
    doc.create3DPlot(system,"input_rep","input_pay","happiness")
    doc.create3DPlot(system,"input_pay","input_employees","happiness")

def generateDot(FuzzyController):
    system = FuzzyController.getFuzzySystem()
    from fuzzy.doc.structure.dot import dot
    import subprocess
    # expects dot directory
    directory = "dot"
    for name,rule in system.rules.items():
        cmd = "dot -T png -o '%s/Rule %s.png'" % (directory,name)
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        dot.print_header(proc.stdin)
        dot.print_dot(rule, proc.stdin, system, "")
        dot.print_footer(proc.stdin)
        proc.communicate()
    cmd = "dot -Tpng -o '%s/System.png'" % directory
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    dot.printDot(system, proc.stdin)
    proc.communicate()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hpd",["plot","dot"])
    except getopt.GetoptError:
        print 'main.py -p'
        sys.exit(2)

    users = employee_data.getEmployeeData()
    companies = company_data.getCompanyData()
    controller = Controller(users[5])

    exit = False
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -p'
            exit = True
        elif opt in ("-p", "--plot"):
            generateDocs(controller)
            exit = True
        elif opt in ("-d", "--dot"):
            generateDot(controller)
            exit = True
    if exit: sys.exit(0)

    for company in companies[1:1]:
        res = controller.calculate(name=company["name"],
                                   salary=company["salary"],
                                   employees=company["employees"],
                                   reputation=company["reputation"],
                                   distance=company["distance"])
        print company["name"] + ": " + str(res)

    testSystem()

def testSystem():
    print "\n"
    users = employee_data.getEmployeeData()
    companies = company_data.getCompanyData()
    correct = 0
    correct2 = 0

    for user in users:
        print user["name"]
        controller = Controller(user)
        results = 0
        results_company = []
        get = ""
        for company in companies:
            res = controller.calculate(salary=company["salary"],
                                       employees=company["employees"],
                                       reputation=company["reputation"])
            if res == results:
                  results_company.append(company["name"])
            elif res > results:
                results = res
                del results_company[:]
                results_company.append(company["name"])
            print company["name"] + ": " + str(res)
        if len(results_company) > 1:
            get = random.choice(results_company)
        else:
            get = results_company[0]

        print "got:",get, ", expected:",user["expected"]
        if get == user["expected"]:
            correct = correct + 1
        #print "\n"
        for answer in results_company:
            if answer == user["expected"]:
                correct2 = correct2 + 1
        #print "\n"

    print (100.0*correct/len(users)),"% correct"
    print (100.0*correct2/len(users)),"% correct contains"

if __name__ == "__main__":
    main(sys.argv[1:])
