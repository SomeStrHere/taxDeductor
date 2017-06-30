#Program to take in input from the user and calculate how much tax and NI contributions a 
#self employed user would have to pay for that years, based on the users input.
#
#Version 1.1.2
#Versioning: a.b.c
#a = major change, b = smaller change, c = minor changes (bug fixes, etc)

#import required libraries
import sys
import re

#Initialize variables and CONSTANTS
TAXPERSONALALLOWANCE = 11500 #The standard personal allowance
taxAdditionalAllowance = 0 #i.e "tax write-offs"
totalTaxAllowance = (TAXPERSONALALLOWANCE + taxAdditionalAllowance) #The amount you don't have to pay tax on
taxPayable = 0.00

#Values for tax bands...
#1 = basic rate, 2 = higher rate, 3 = additional rate
# see; https://www.gov.uk/income-tax-rates/current-rates-and-allowances
TAXBAND1MIN = 11501.00
TAXBAND1MAX = 45000.00
TAXBAND1PERCENT = 0.20 #The value as a percentage which will be used to calc tax based on income

TAXBAND2MIN = 45001.00
TAXBAND2MAX = 150000.00
TAXBAND2PERCENT = 0.40 #The value as a percentage which will be used to calc tax based on income

TAXBAND3MIN = 150000.01
TAXBAND3PERCENT = 0.45 #The value as a percentage which will be used to calc tax based on income

grossIncome = 0.00 #The users income before deducting tax and NI contributions
businessCosts = 0.00
preTaxProfits = 0.00 
netIncome = 0.00 #The value to be returned to the user after tax and NI is deducted 
niPayable = 0.00 #total of all National Insurance contributions to be paid, calculated based on 
#user  input and constants.

#NI contributions variables and CONSTANTS
#see; https://www.gov.uk/self-employed-national-insurance-rates
CLASS2NITHRESHOLD = 6025.00
CLASS2NIRATE = 2.85 # Amount to be charged in £ per week
class2NI = 0.00 #amount of class 2 due to pay based on pre-tax profits
class4NI = 0.00 #amount of class 4 due to pay based on pre-tax profits
CLASS4NITHRESHOLD = 8164.00
CLASS4FIRSTRATE = 0.09 #The value as a percentage which will be used to calc class 4 contributions
CLASS4SSECONDRATETHRESHOLD = 45000.01
CLASS4SECONDRATE = 0.02 #The value as a percentage which will be used to cal class contributions on pre-tax profits above CLASS4SSECONDRATETHRESHOLD

def menu() : #declare the menu function
    """Displays a menu and accepts user input."""
    print('\nTax & NI Deductor')
    print('##################')
    print('A program to calculate the tax and NI contributions per year, for a \nself employed person\
 in the UK.')
    print('\nMenu')
    print('------')
    print('Please enter a number to choose from the following menu options.\n')
    print('(1) Declare an addition to your "Personal Standard Allowance".')
    print('(2) Declare business costs; for NI insurance calculations.')
    print('(3) Calculate tax and NI deductions based on monthly values.')
    print('(4) Calculate tax and NI deductions based on yearly value.')
    print('(5) Exit program.\n')
    menuChoice = input() #obtain input from the user

    if not re.match("^[1-5]*$", menuChoice) or (int(menuChoice) > 5):
        print("Error! Only numbers 1-5 are allowed.")
        clearConsole(3)
        menu()
    else :
        if menuChoice == "1" :
            additionalTaxAllowance()

        if menuChoice == "2" :
            declareBusinessCosts()

        if menuChoice == "3" :
            monthlyPreTax()

        if menuChoice == "4" :
            yearlyPreTax()                        

        if menuChoice == "5" :
            sys.exit()

def additionalTaxAllowance() : #function to increase users personal tax free allowance
    """Ask's the user to enter how much additional tax free allowance they wish to declare."""

    global taxAdditionalAllowance

    try :
        taxAdditionalAllowance = float(input('\nHow much do you want to add\
 to your tax free allowance?\n\n£'))
    except :
        print('Sorry, there was an error... please try again.')
        additionalTaxAllowance()

    clearConsole(0)
    print('\nOperation complete')
    print('Returning you to the menu...')
    menu()

def declareBusinessCosts() : #Take in business costs value from user
   """Asks the user to enter the total costs of business costs they wish to declare.."""

   try :
       businessCosts = float(input("\nWhat is the total cost of the business costs you wish to declare?\n\n£"))
   except :
       print('Sorry, there was an error... please try again.')
       declareBusinessCosts()

   clearConsole(0)
   print('\nOperation complete')
   print('Returning you to the menu...')
   menu()

def yearlyPreTax() : #function for user to input total pre-tax income for the year
    """Asks the user to enter their total pre-tax income for the year."""
    
    global grossIncome

    try :
        grossIncome = float(input('\nWhat was your pre-tax income for the year?\n\n£'))
    except :
        print('Sorry, there was an error... please try again.')
        yearlyPreTax()

    print('\nThank you...')
    clearConsole(3)

    calculateTax()
    calculateNI()
    #netIncome returned by takeHomePay()
    #taxPayable returned by calculateTax()
    #niPayable returned by calculateNI()
    programOutput(calculateTax(), calculateNI(), takeHomePay())

def monthlyPreTax() : #function for user to input monthly pre-tax income figures
    """Prompts the user to enter their pre-tax income for each month of the year.\
    User input is stored in array preTaxMonthlyIncome[] with a range of 0-12."""

    preTaxMonthlyIncome = []
    print('') #To create a line of empty space before the loop

    monthlyIncomeContainer = 0
    print('Please enter your pre-tax income for each month, and press enter:\n')

    for x in range(0,12):

        try :
            monthlyIncomeContainer = float(input('£'))
        except :
            print('Sorry, there was an error... please try again.')
            monthlyPreTax()

        preTaxMonthlyIncome.append(monthlyIncomeContainer)

    #Following code creates a total for all the values in the above array
        preTaxMonthlyArrayTotal = 0.0 
    for i in range(len(preTaxMonthlyIncome)):
        preTaxMonthlyArrayTotal += preTaxMonthlyIncome[i]

    #The array is used to increase the functionality of later versions of the program.

    global grossIncome

    grossIncome = preTaxMonthlyArrayTotal

    print('\nThank you...')
    clearConsole(3)
    #print(preTaxMonthlyArrayTotal) #Uncomment to test the contents of the array

    calculateTax()
    calculateNI()
    #netIncome returned by takeHomePay()
    #taxPayable returned by calculateTax()
    #niPayable returned by calculateNI()
    programOutput(calculateTax(), calculateNI(), takeHomePay())

def calculateTax() : 
     """Calculates the total tax due to be paid by user (taxPayable)."""

     global TAXBAND3MIN
     global TAXBAND2MIN
     global TAXBAND1MIN

     global TAXBAND3PERCENT
     global TAXBAND2PERCENT
     global TAXBAND1PERCENT

     global TAXBAND2MAX
     global TAXBAND1MAX

     global grossIncome
     global totalTaxAllowance

     if grossIncome >= TAXBAND3MIN :
         taxPayable = (grossIncome - totalTaxAllowance ) * TAXBAND3PERCENT
     elif grossIncome >= TAXBAND2MIN and grossIncome <= TAXBAND2MAX :
         taxPayable = (grossIncome - totalTaxAllowance)  * TAXBAND2PERCENT
     elif grossIncome >= TAXBAND1MIN and grossIncome <= TAXBAND1MAX :
         taxPayable = (grossIncome - totalTaxAllowance) * TAXBAND1PERCENT
     else :
         taxPayable = 0.00

     return(taxPayable)

def calculateNI() : #Calculatte Class 2 contributions
   """Calculates the total NI contributions to be paid, returns (niPayable)."""
    
   global grossIncome
   global businessCosts
   global preTaxProfits

   global CLASS2NITHRESHOLD
   global CLASS2NIRATE
   global CLASS4NITHRESHOLD
   global CLASS4SSECONDRATETHRESHOLD
   global CLASS4FIRSTRATE
   global CLASS4SECONDRATE
   global class2NI
   global class4NI

   preTaxProfits = (grossIncome - businessCosts)

   if preTaxProfits > CLASS2NITHRESHOLD :
        class2NI = (CLASS2NIRATE * 52)

   #Calculate Class 4 contributions using first rate
   if preTaxProfits > CLASS4NITHRESHOLD and preTaxProfits < CLASS4SSECONDRATETHRESHOLD :
        class4NI = (preTaxProfits * CLASS4FIRSTRATE) #calculates first rate of class 4

   #Calculate remaining Class 4 using second rate
   if preTaxProfits > CLASS4NITHRESHOLD :
        class4NI = class4NI + ((preTaxProfits - CLASS4SSECONDRATETHRESHOLD) * CLASS4SECONDRATE)

   #Total NI contribution
   niPayable = (class2NI + class4NI)

   return(niPayable)

def takeHomePay() : #Calculate take home pay
   """Calculates the users take home pay after deducing tax and NI contributions, returns\
   (netIncome)."""

   #taxPayable returned from calculateTax()
   #niPayable returned from calculateNI()
   #netIncome = (grossIncome - calculateTax()) + (grossIncome - calculateNI()) #initial attempt, bug
   netIncome = grossIncome - (calculateTax() + calculateNI())

   return(netIncome)

def clearConsole(wait) : #function to clear console on Linux or Windows
   """Accepts an integer argument and produces a delay for the number of seconds passed as an argument\
    the program will then attempt to clear the console for Windows, and if that fails will try to clear\
     the console for Linux."""

   import time
   time.sleep(wait) # produces a delay based on the argument given to clearConsole()
    
   import os

   try :
       os.system('cls') #clears console on Windows
   except :
       os.system('clear') #clears console on Linux

def programOutput(taxPayable, niPayable, netIncome) : #print output to the user
   """Prints information to the screen."""

   print('\nDetails of your "take home pay", net income, will be shown bellow: \n')
   print('Total tax: £%.2f' %(taxPayable))
   print('Total NI: £%.2f' %(niPayable))
   print('\nYour "take home pay" after deducting tax and NI contributions will be:\n\
\n£%.2f\n' %(netIncome))
       
menu() #call the menu function