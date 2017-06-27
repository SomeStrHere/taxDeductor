#Program to accept user input (monthly pay or anticipated monthly pay) and will return
#an estimation of UK self employment tax and NI deductions/contributions and what the 
#users take home pay will be.

#import libraries

#Variable and constant declarations
TAXPERSONALALLOWANCE = 11500 # Don't pay tax on earnings up to this amount
taxAdditionalAllowance = 0
totalTaxAllowance = (TAXPERSONALALLOWANCE + taxAdditionalAllowance)
taxPayable = 0.00

#Values for tax band...
PERSONALALLOWANCERATE = 0

#1 = basic rate, 2 = higher rate, 3 = additional rate
# see; https://www.gov.uk/income-tax-rates/current-rates-and-allowances
TAXBAND1MIN = 11501.00
TAXBAND1MAX = 45000.00
TAXBAND1PERCENT = 0.20 #The value as a percentage which will be used to calc tax based on income

TAXBAND2MIN = 45001.00
TAXBAND2MAX = 150000.00
TAXBANDPERCENT = 0.40 #The value as a percentage which will be used to calc tax based on income

TAXBAND3MIN = 150000.01
TAXBANDPERCENT = 0.45 #The value as a percentage which will be used to calc tax based on income

grossIncome = 0.00
businessCosts = 0.00
preTaxProfits = 0.00

#NI contributions variables and constants
#see; https://www.gov.uk/self-employed-national-insurance-rates
#CLASS2NITHRESHOLD = 6025.00
#CLASS4MAX = 45000.00
#class4contribution


#The purpose of this code block is to allow the user ti input either an annual pre-tax earnings
# figure or to allow the user to enter the amounts for each month.
yearlyOrMonthly = input("If you know your pre-tax income for the year press 'Y', to enter values \
for each month, please press 'M' ").upper()

if yearlyOrMonthly == "Y" :
    try :
        grossIncome = float(input('Please enter your annual pre tax income £'))
    except :
        print('Sorry, there was an error')
elif yearlyOrMonthly == "M" :
    preTaxMonthlyIncome =[]
    for x in range(0,12):
        try :
            float(input('Please enter your pre-text value for each month; one at a time: '))
        except :
            print('Sorry, there was an error')
            break # break is here to exit the loop in the case of an error
        preTaxMonthlyIncome.append(float(x))
    #First method for summing the array
    #grossIncome = sum(preTaxMonthlyIncome)
    #print('this is a test %.2f' %(grossIncome) ) #this line is just to test the code

    #New method to print the total of all of the monthly pre tax incomes in the array
    preTaxMonthlyArrayTotal = 0.0 
    for i in range(len(preTaxMonthlyIncome)):
        preTaxMonthlyArrayTotal += preTaxMonthlyIncome[i]
    print(preTaxMonthlyArrayTotal)
else :
    yearlyOrMonthly = input("Error; please enter 'Y' or 'M'...")

#Calculate tax payable
if grossIncome >= TAXBAND3MIN :
    print() #calculate tax payable
elif grossIncome >= TAXBAND2MIN and grossIncome <= TAXBAND2MAX :
    print() #calculate tax payable
elif grossIncome >= TAXBAND1MIN and grossIncome <= TAXBAND1MAX :
    print() #calculate tax payable
else :
    taxPayable = 0.00

#Calculate NI based on user input

#Calculate take home pay

#Print out tax and NI contributions and the take home pay to the user
