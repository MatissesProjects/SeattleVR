import re

####
# Math Section
####

#Calculates num!
def calculateFactorial(num):
    if num <= 1:
        return 1
    return num * calculateFactorial(num - 1)

#Calculates 1/num
def calculateReciprocal(num):
    if num == 0:
        return 0
    return 1.0/num

def test_calculateFactorial():
    print("testing prettyNum(calculateFactorial(2))  = %s" % (calculateFactorial(2))) #2
    print("testing prettyNum(calculateFactorial(3))  = %s" % (calculateFactorial(3))) #6
    print("testing prettyNum(calculateFactorial(5))  = %s" % (calculateFactorial(5))) #120
    print("testing prettyNum(calculateFactorial(7))  = %s" % (calculateFactorial(7))) #5040

def test_calculateReciprocal():
    print(prettyNum(calculateReciprocal(0)))
    print(prettyNum(calculateReciprocal(1)))
    print(prettyNum(calculateReciprocal(-1)))
    print(prettyNum(calculateReciprocal(2)))
    print(prettyNum(calculateReciprocal(1/2)))
    print(prettyNum(calculateReciprocal(-2)))
    print(prettyNum(calculateReciprocal(-1/2)))

####
# String manipulation
####

#takes in an equation string and puts spaces between all cared about operations
def tokenizeInput(equation):
    equation = equation.replace('+', ' + ').replace('-', ' - ')
    equation = equation.replace('*', ' * ').replace('/', ' / ')
    equation = equation.replace('(', ' ( ').replace(')', ' ) ')
    equation = equation.replace('^', ' ^ ').replace('1/x', ' 1/x ')
    equation = equation.replace('1 / X', ' 1/X ').replace('1/X', ' 1/X ').replace('1 / X', ' 1/X ')
    equation = equation.replace('!', '! ').replace('C', ' C ')
    equation = equation.replace('Q', ' Q ').replace('A', ' A ')
    equation = equation.split(' ')
    return equation

#takes the tokenized equation and truncates it down to just the parts
#involved in the equation, gets rid of extra spaces
#also tells us early if we have a Q in the string, which means quit
def truncateEquation(splitEquation):
    truncatedEquation = []
    for part in splitEquation:
        part = part.upper()
        #case splitEquation[i] is len = 0, noop
        if len(part) == 0:
            continue
        elif 'Q' in part:#case Q: quit
            return truncatedEquation, True # we need to quit the program
        elif 'C' in part:#case C: delete current number and previous operator
            truncatedEquation.pop()#pop-pop
            #in the case of first item deleting we must test
            if len(truncatedEquation) > 0:
                truncatedEquation.pop()
        elif 'A' in part:#case A: drop all
            truncatedEquation = []
        else:
            truncatedEquation.append(part)
    return truncatedEquation, False #continue execution

def test_tokenizeInput():
    print(tokenizeInput('3 + 2 -3'))
    print(tokenizeInput('6  + 3q  '))
    print(tokenizeInput('5+2 c+3'))
    print(tokenizeInput('7  +8 c+3'))

def test_truncatedEqucation():
    print(truncateEquation(tokenizeInput('3 + 2 -3')))
    print(truncateEquation(tokenizeInput('6  + 3q  ')))
    print(truncateEquation(tokenizeInput('5+2 c+3')))
    print(truncateEquation(tokenizeInput('7  +8 c+3')))

####
# Output Section
####

#get number in proper format, string version so we can print it later
def prettyNum(num):
    if float(num).is_integer(): #if we are dealing with an integer
        return str(int(num)) # force trailing 0's truncate, but return as string
    else: #floating point otherwise
        return str("%19.15f" % (num))

def test_prettyNum():
    print("testing prettyNum(1)                 = %s" % (prettyNum(1))) #1
    print("testing prettyNum(1.0)               = %s" % (prettyNum(1.0))) #1
    print("testing prettyNum(.5)                = %s" % (prettyNum(1/2))) #0.500000000000000
    print("testing prettyNum(3.141592653589793) = %s" % (prettyNum(3.141592653589793))) #3.141592653589793

####
# Test Cover section
####
def runAllTests():
    test_calculateFactorial()
    test_prettyNum()
    test_calculateReciprocal()
    test_tokenizeInput()
    test_truncatedEqucation()

runAllTests()
#9,223,372,036,854,775,807
    #2^64-1
        #on a x64 bit system this is python's max
        #on a x32 bit system we need to use a long
    #we can just cast to a long just to be sure!

#step 1 get input
print("enter an equation: ")
enteredEquation = input()
enteredEquation = str(enteredEquation).upper()

#step 2 clean input
splitEquation = tokenizeInput(enteredEquation)
#print(splitEquation)
truncatedEquation, quit = truncateEquation(splitEquation)
#print(truncatedEquation)
#step 3 do operations
  #switch on special operations
    #case 1/x in input: pop previous number, and 1/x it (^-1)
    #default: do normal operations

    #build a parse tree for the equation
    # 0:    starts null,
    #       given number
        #   number
    # 1:    given operator_1
        #number \
        #       |-operator_1
    # 2:    given number
        #number \
        #       |-operator_1
        #number /
    # 3     given operator_2
        #case operator_1 higher pressidense than operator_2
            #number \
            #       |-operator_1-|
            #number /            |
            #         operator_2-|
                #ex
                    # (3+2)-
#regex number finder,
  #negative optional, number, (with decimal number) optional
num_format = re.compile("-?\d+(?:\.\d+)?")

currValue = 0
firstItem = True
print(truncatedEquation)
for index in range(0,len(truncatedEquation)):
    part = truncatedEquation[index]
    isnumber = re.match(num_format, part)
    #case first item entered was a number
    if firstItem and '-' in part:
        print("firstItem is -")
        currValue = -1
    else:
        if index > 2:
            print(calculateReciprocal(float(truncatedEquation[index-2])))
        #rest of the numbers and symbols
        if '+' in part:
            currValue += float(truncatedEquation[index-1]) + float(truncatedEquation[index+1])
        elif '-' in part:
            currValue += float(truncatedEquation[index-1]) - float(truncatedEquation[index+1])
        elif '*' in part:
            currValue += float(truncatedEquation[index-1]) * float(truncatedEquation[index+1])
        elif '1/X' in part:
            truncatedEquation[index] = calculateReciprocal(float(truncatedEquation[index-1]))
        elif '/' in part:
            currValue += float(truncatedEquation[index-1]) / float(truncatedEquation[index+1])
        elif '!' in part:
        #else:
            #print(part)
    firstItem = False
        #

#step 4 display answer

if quit != True:
    print(truncatedEquation)
    print(prettyNum(currValue))
else:
    print("we exited the program")
