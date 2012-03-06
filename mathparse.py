from __future__ import division
import random


def createMathProblemString( minL, maxL, minR, maxR, operators ):
    left = random.randint(minL, maxL)
    right = random.randint(minR, maxR)
    operator = operators[random.randint(0, len(operators)-1)]
    strList = [str(left), " ", operator, " ", str(right)]
    return ''.join(strList)

def solveMathProblemString( string ):
    return eval(string)


def run( minL, maxL, minR, maxR, operators ):
    while (True):
        string = createMathProblemString( minL, maxL, minR, maxR, operators )
        v = float(raw_input(''.join([string, " = "])))
        a = solveMathProblemString(string)
        print v
        if v == a:
            print "You're right!"
        else:
            print "Sorry, the answer was %f"%a
        
    