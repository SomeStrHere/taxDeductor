#Program to take in input from the user and calculate how much tax and NI contributions a 
#self employed user would have to pay for that years, based on the users input.

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

#Start user input
userInput = input("If you want to write something off against your tax, press 'Y', otherwise \
press the enter key to continue ").upper()

while userInput == "Y" :
    taxAdditionalAllowanc = float(input('Please enter the total in value of what you wish to write off against your tax; £'))
    break

#The purpose of this code block is to allow the user to input either an annual pre-tax earnings
#figure or to allow the user to enter the amounts for each month. So in future iterations the
#program can return individual values for each month and do more complex calculations.
yearlyOrMonthly = input("If you know your pre-tax income for the year press 'Y', to enter values \
for each month, please press 'M' ").upper()

if yearlyOrMonthly == "Y" :
    try :
        grossIncome = float(input('Please enter your annual pre tax income £'))
    except :
        print('Sorry, there was an error')
elif yearlyOrMonthly == "M" :
    preTaxMonthlyIncome = []
    for x in range(0,12):
        #monthlyIncomeContainer stores the user input and each time through the loop
        #adds that value to the array preTaxMonthlyIncome[]
        monthlyIncomeContainer = 0
        try :
            monthlyIncomeContainer = float(input('Please enter your pre-text value for each month; one at a time: '))
        except :
            print('Sorry, there was an error')
            break # break is here to exit the loop in the case of an error
        preTaxMonthlyIncome.append(monthlyIncomeContainer)

    #Following code creates a total for all the values in the above array
    preTaxMonthlyArrayTotal = 0.0 
    for i in range(len(preTaxMonthlyIncome)):
        preTaxMonthlyArrayTotal += preTaxMonthlyIncome[i]
else :
    yearlyOrMonthly = input("Error; please enter 'Y' or 'M'...")

#Calculate tax payable
if grossIncome >= TAXBAND3MIN :
    taxPayable = (grossIncome - totalTaxAllowance ) * TAXBAND3PERCENT
elif grossIncome >= TAXBAND2MIN and grossIncome <= TAXBAND2MAX :
    taxPayable = (grossIncome - totalTaxAllowance)  * TAXBAND2PERCENT
elif grossIncome >= TAXBAND1MIN and grossIncome <= TAXBAND1MAX :
    taxPayable = (grossIncome - totalTaxAllowance) * TAXBAND1PERCENT
else :
    taxPayable = 0.00

#Calculate NI based on user input
businessCosts = float(input("\nIf you need to declare any business costs/expenses for us to calculate your\
 NI contributions, please do so here.\nIf you don't have anything to declare just enter 0:\n\n£"))

preTaxProfits = (grossIncome - businessCosts)

#Calculatte Class 2 contributions
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

#Calculate take home pay
netIncome = (grossIncome - taxPayable) + (grossIncome - niPayable)

#Print output to user
print('\nDetails of your "take home pay", net income, will be shown bellow: \n')
print('Total tax: £%.2f' %(taxPayable))
print('Total NI: £%.2f' %(niPayable))
print('\nYour "take home pay" after deducting tax and NI contributions will be:\n\
\n£%.2f\n' %(netIncome))