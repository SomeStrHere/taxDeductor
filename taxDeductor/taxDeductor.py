#Program to take in input from the user and calculate how much tax and NI contributions a 
#self employed user would have to pay for that years, based on the users input.
#
#Version 0.2.0 - Improved version of program with functions and menu system.

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
    print('\nTax & NI Deductor')
    print('##################')
    print('A program to calculate the tax and NI contributions per year, for a \nself employed person\
 in the UK.')
    print('\nMenu')
    print('------')
    print('Please enter a number to choose from the following menu options.\n')
    print('(1) To declare any additions to your "Personal Standard Allowance".')
    print('(2) To enter your total pre-tax income for the year.')
    print('(3) To enter your pre-tax income for each individual month.')
    print('(4) To declare any business costs; for NI insurance calculations.')
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
            yearlyPreTax()

        if menuChoice == "3" :
            monthlyPreTax()

        if menuChoice == "4" :
            declareBusinessCosts()

        if menuChoice == "5" :
            sys.exit()

def additionalTaxAllowance() : #function to increase users personal tax free allowance

    taxAdditionalAllowance = float(input('\nPlease enter the total in value, which you want to add\
to your tax free allowance; £')) 

    return(taxAdditionalAllowance)

def yearlyPreTax() : #function for user to input total pre-tax income for the year

    try :
        grossIncome = float(input('\nPlease enter your annual pre tax income £'))
    except :
        print('Sorry, there was an error')

    return(yearlyPreTax)

def monthlyPreTax() : #function for user to input monthly pre-tax income figures

    preTaxMonthlyIncome = []
    print('') #To create a line of empty space before the loop
    for x in range(0,12):
        #monthlyIncomeContainer stores the user input and each time through the loop
        #adds that value to the array preTaxMonthlyIncome[]
        monthlyIncomeContainer = 0
        try :
            monthlyIncomeContainer = float(input('Please enter your pre-tx income for each month; one at a time: '))
        except :
            print('Sorry, there was an error')
            break # break is here to exit the loop in the case of an error
        preTaxMonthlyIncome.append(monthlyIncomeContainer)

    #Following code creates a total for all the values in the above array
    preTaxMonthlyArrayTotal = 0.0 
    for i in range(len(preTaxMonthlyIncome)):
        preTaxMonthlyArrayTotal += preTaxMonthlyIncome[i]

    return(preTaxMonthlyArrayTotal) #returns the sum of the contents of the array
    #The array is used to increase the functionality of later versions of the program.

def calculateTax() :

    if grossIncome >= TAXBAND3MIN :
        taxPayable = (grossIncome - totalTaxAllowance ) * TAXBAND3PERCENT
    elif grossIncome >= TAXBAND2MIN and grossIncome <= TAXBAND2MAX :
      taxPayable = (grossIncome - totalTaxAllowance)  * TAXBAND2PERCENT
    elif grossIncome >= TAXBAND1MIN and grossIncome <= TAXBAND1MAX :
       taxPayable = (grossIncome - totalTaxAllowance) * TAXBAND1PERCENT
    else :
        taxPayable = 0.00

    return(taxPayable)

def declareBusinessCosts() : #Take in business costs value from user

    businessCosts = float(input("\nWhat is the total cost of the business costs you wish to declare?\n\n£"))

    return(businessCosts)

def calculateNI() : #Calculatte Class 2 contributions
    
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
   
   netIncome = (grossIncome - taxPayable) + (grossIncome - niPayable)

   return(netIncome)

def programOutput() : #print output to the user

    print('\nDetails of your "take home pay", net income, will be shown bellow: \n')
    print('Total tax: £%.2f' %(taxPayable))
    print('Total NI: £%.2f' %(niPayable))
    print('\nYour "take home pay" after deducting tax and NI contributions will be:\n\
\n£%.2f\n' %(netIncome))

def clearConsole(wait) : #function to clear console on Linux or Windows

    import time
    time.sleep(wait) # produces a delay based on the argument given to clearConsole()
    
    import os

    try :
        os.system('cls') #clears console on Windows
    except :
        os.system('clear') #clears console on Linux

menu() #call the menu function