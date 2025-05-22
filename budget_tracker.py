import json
import datetime
import os

fileName = "budget_log.json"
#checks if file exists or not to avoid errors
if not os.path.exists(fileName) or os.path.getsize(fileName) == 0:
    with open(fileName, 'w') as f:
        json.dump([], f)

print("\n\033[4mSimple Budget Tracker\033[0m")
print("\nEnter 0 at any time to exit.\n")

def addTransaction():
    currentDate = datetime.datetime.today()
    formattedDate = currentDate.strftime("%a %m/%d/%y %I:%M%p")
    transactionType = None
    
    #Get income or expense prefix from user
    while transactionType not in (1, 2):
        try:
            transactionType = int(input("\nEnter 1 if your transaction is income, or enter 2 if it is an expense: "))
        except ValueError:
            print("\nPlease enter 1 for income, or 2 for expense. ")
    if transactionType == 1:
        prefix = "Income: +$"
        tType = "income"
    else:
        prefix = "Expense: -$"
        tType = "expense"

    #Get transaction amount
    while True:
        try:
            userAmount = float(input("\nHow much is this transaction: "))
            break
        except ValueError:
                    print("\nPlease enter a number.")

    #Transaction confirmation
    userConf = input(f"You want to add \033[4m{prefix}{userAmount}\033[0m to your account?. Type YES to confirm: ").upper()
    if userConf != "YES" and userConf != "Y":
        return None
    
    
    #File writing
    entry = {
        "date": formattedDate,
        "type": tType,
        "amount": userAmount
    }


    if not os.path.exists(fileName):
        with open(fileName, 'w') as file:
            json.dump([entry], file, indent=2)
    else:
        with open(fileName, 'r+') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.append(entry)
            file.seek(0)
            json.dump(data, file, indent=2)

    print(f"\nAdded \033[4m{prefix}{userAmount}\033[0m to your account.\n")
            
            
def viewBalance():
    balance = 0

    with open(fileName, 'r') as file:
        try:
           data = json.load(file)
        except json.JSONDecodeError:
            data = []

        for entry in data:
            if entry['type'] == 'income':
                balance += entry['amount']
            else:
                balance -= entry['amount']
    print(f"Your total balance is ${balance:.2f}")

def viewHistory():
    with open(fileName, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

        for entry in data:
            print(f"{entry['date']} | {entry['type'].capitalize()} | ${entry['amount']:.2f}")

def deleteTransactions():
    confirm = input("You are about to \033[4mDELETE ALL TRANSACTIONS!\033[0m Type \033[4mYES\033[0m to continue: ").upper()
    if confirm == "YES" or confirm == 'Y':
        with open(fileName, 'w') as file:
                json.dump([], file)
        print("\nAll transactions have been deleted.")
    else:
        print("\nDeletion cancelled.")
    
    
def main():
    #Establish main menu choice loop
    menuChoice = None
    #If the user enters 0 the loop will end and program will exit.
    while menuChoice != 0:
        #Error Handling
        try:
            menuChoice = int(input("\n1 to add transaction, 2 to view balance, 3 to view transaction history, 4 to delete all transactions: "))
            print("\n")
        except ValueError:
            print("\nPlease enter a number 1-4.\n")
            continue

        match menuChoice:
            #Add Transaction
            case 1:
                addTransaction()
            #View Balance
            case 2:
                viewBalance()
            #Transaction History
            case 3:
                viewHistory()
            #Delete Transactions
            case 4:
                deleteTransactions()
            #Exit Program
            case 0:
                print("Goodbye!")
            #Edge case catching
            case _:
                print("That is not a valid choice.")
        print("\n")

main()