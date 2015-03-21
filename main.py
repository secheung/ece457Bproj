
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

users = [{
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
    # doc.create2DPlot(system,"input_pay","happiness")
    # doc.create2DPlot(system,"input_rep","happiness")
    # doc.create2DPlot(system,"input_employees","happiness")
    doc.create3DPlot(system,"input_rep","input_employees","happiness")
    # doc.create3DPlot(system,"input_rep","input_pay","happiness")
    # doc.create3DPlot(system,"input_employees","input_pay","happiness")

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

    controller = Controller(users[0]);

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

    for company in companies:
        res = controller.calculate(company["employees"], company["salary"], company["reputation"])
        print company["name"] + ": " + str(res)

if __name__ == "__main__":
    main(sys.argv[1:])
