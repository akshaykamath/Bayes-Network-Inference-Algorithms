from subprocess import Popen, PIPE
import random

# **NOTE**
# This script will invoke your program, provide input and test output. This is why
# you have to tell this script where your program is. You'd do this by editing the
# "cmd" variable below.
#
# Edit the cmd variable in this file that appears below this comment section,
# type in the command to run your program from the command line, and run *this*
# script as you would run any python program.
#
# Examples (that line below should look like):
#   cmd = "python /absolute/path/to/your/program"
#   cmd = "java com.package.program.Main"
#   cmd = "/location/to/executable-binary"
#   cmd = "python C:\Users\Me\Desktop\program.py" etc.
# Basically, put in the string that you can start from program from a terminal/command line.
#
# How you would run this script:
#   python validate.py 
#
# where *this* file is named validate.py.

cmd = "python C:\Users\Anuj\Documents\github\BayesNetworkInference\Bayes-Network-Inference-Methods\Main.py r 10"


def valid(m, n, x):
    node_names = "A B E J M".split()
    random.shuffle(node_names)

    inp = "%d %d\n"%(m,n) + \
            "".join("%s %s\n"%(name, random.sample(["t", "f"], 1)[0]) for name in node_names[:m]) + \
            "".join("%s\n"%name for name in node_names[m:m+n])
    
    print "Invoking program for testing"
    print "INPUT"
    print inp
    child = Popen(cmd + " " + x, shell=True, stdin=PIPE, stderr=PIPE, stdout=PIPE)
    stdout, stderr = child.communicate(inp)
    child.stdin.close()

    print "STDOUT"
    print stdout
    print "STDERR"
    print stderr

    if len(stderr):
        print "Child program printed something on stderr. Invalid input."
        return False
    
    output = [(x[0], float(x[1])) for x in (y.split() for y in stdout.splitlines())]
    assert [x[0] for x in output] == node_names[m:m+n]		
    for prob in (x[1] for x in output):		
        assert 0 <= prob <= 1
    return True

def main():
    try:
        for x in ["e 0", "r 1000", "p 100", "l 10"]:
            assert valid(2,1, x)
            assert valid(3,1, x)
        print "Format looks okay!"
    except:
        print "Please ensure that your program prints exactly one floating point number and nothing else."
        print "Please see updated doc: https://docs.google.com/document/d/1-GLH7yVTD7FoeaymQLi_fk_3OYU-86fbH2d5MSv6Cfs/edit"
        print "Failed to validate the format produced by the code."


if __name__ == '__main__':
    main()