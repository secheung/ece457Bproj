
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
    doc.create3DPlot(system,"input_employees","input_pay","happiness")

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
        opts, args = getopt.getopt(argv,"hpdei",["plot","dot"])
    except getopt.GetoptError:
        print 'main.py -p'
        sys.exit(2)

    users = employee_data.getEmployeeData()
    companies = company_data.getCompanyData()
    default_user = users[5]

    exit = False
    e = False
    userinput = False
    joke = False
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -p'
            exit = True
        elif opt in ("-p", "--plot"):
            generateDocs(Controller(default_user))
            exit = True
        elif opt in ("-d", "--dot"):
            generateDot(Controller(default_user))
            exit = True
        elif opt == "-e":
            e = True
        elif opt == "-i":
            userinput = True
    if exit: sys.exit(0)

    if e:
        controller = Controller(default_user, useGraphSystem=True)
        for company in companies[:]:
            res = controller.calculate(name=company["name"],
                                       salary=company["salary"],
                                       employees=company["employees"],
                                       reputation=company["reputation"],
                                       distance=company["distance"])
            print company["name"] + ": " + str(res)
        sys.exit(0)
    elif userinput:
        inputUser(companies)
        sys.exit(0)

    testSystem()

def inputUser(companies):
    print "Hi, "
    name = raw_input("Name: ")

    print
    print "Salary (0-200) [x $1000] - low, medium_low, medium_high, high" 
    salary_low_high = float(raw_input("Salary.Low: "))
    salary_med_low = float(raw_input("Salary.Med.Low: "))
    salary_med_high = float(raw_input("Salary.Med.High: "))
    salary_high_low = float(raw_input("Salary.High: "))
    salary = {
                "bad_low": 0,     # dummy pointless
                "good_high": 200, # dummy, pointless
                "bad_high": salary_low_high,
                "ok_low": salary_med_low,
                "ok_high": salary_med_high,
                "good_low": salary_high_low
             }

    print
    print "Number of employees (1-1000) - low, medium_low, medium_high, high"
    employees_low_high = float(raw_input("Employees.Low: "))
    employees_med_low = float(raw_input("Employees.Med.Low: "))
    employees_med_high = float(raw_input("Employees.Med.High: "))
    employees_high_low = float(raw_input("Employees.High: "))
    employees = {
                    "small_low": 1,     # dummy, pointless
                    "large_high": 1000, # dummy, pointless
                    "small_high": employees_low_high,
                    "med_low": employees_med_low,
                    "med_high": employees_med_high,
                    "large_low": employees_high_low
                }

    print
    print "Reputation (0-10) - low, high"
    rep_low = float(raw_input("Reputation.Low: "))
    rep_high = float(raw_input("Reputation.High: "))
    rep = {
                "low": rep_low,
                "high": rep_high
          }

    print
    print "Commute (0-150) [minutes] - close, medium, far"
    distance_low = float(raw_input("Commute.Close: "))
    distance_medium = float(raw_input("Commute.Medium: "))
    distance_far = float(raw_input("Commute.Far: "))
    commute = {
                    "close": distance_low,
                    "medium": distance_medium,
                    "far": distance_far
              }

    print
    graph = raw_input("Graphs? (typing anything means yes): ")

    user = { "name": name, "salary": salary, "employees": employees, \
             "rep": rep, "commute": commute }

    new_user_controller = Controller(user, useGraphSystem = True if graph else False)

    print
    for company in companies[:]:
        res = new_user_controller.calculate(name=company["name"],
                                   salary=company["salary"],
                                   employees=company["employees"],
                                   reputation=company["reputation"],
                                   distance=company["distance"])
        print company["name"] + ": " + str(res)


def testSystem():
    print "\n"
    users = employee_data.getEmployeeData()
    companies = company_data.getCompanyData()
    correct = 0
    
    resultsTotal = {}
  
    for user in users:
        print user["name"]
        controller = Controller(user)
        results = 0
        results_company = []
        get = ""
        for company in companies:
            res = controller.calculate(name=company["name"], salary=company["salary"], 
                                       employees=company["employees"], reputation=company["reputation"],
                                       distance=company["distance"])
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

        #print "got:",get, ", expected:",user["expected"]
        print "---- highest happiness: " + get
        if get == user["expected"]:
            correct = correct + 1
        print "\n"

        if get not in resultsTotal:
            resultsTotal[get] = 1
        else:
            resultsTotal[get] += 1

    print resultsTotal
    #print (100.0*correct/len(users)),"% correct"

if __name__ == "__main__":
    main(sys.argv[1:])
