'''Design a Python program that helps users keep track of their expenses and manage their budgets.
Requirements:
The program should allow users to input their expenses, including the item name and its cost.
Provide options for the user to add, view, update, or delete expenses.
Implement error handling to handle invalid inputs or actions gracefully.
Calculate and display the total expenses incurred.
Allow users to set a budget and display their remaining budget after deducting their expenses.
Optionally, provide visualizations such as charts or graphs to represent expense categories or spending trends.'''

import json
import pandas

categories = {1: 'Utilities', 2: 'Entertainment', 3: 'Meals', 4: 'Transportation', 5: 'Office Supplies', 6: 'Travel',
              7: 'Other'}

def userOptionSelection(options, needValue=False):
    userMessage = ''
    for option in options:
        userMessage += (str(option) + '. ' + options[option]) + '\n'

    try:
        userResponse = int(input(userMessage))

        if options[userResponse] != '':
            if needValue:
                return options[userResponse]
            else:
                return userResponse
    except:
        print("Please provide a valid option")
        return userOptionSelection(options)

def handleShowExpanse():
    file = open("expanseTracker.json", "r")
    existingData = file.read()
    print('============= Expenses =============')

    if existingData != '':
        jsondata = json.loads(existingData)
        data = pandas.DataFrame(jsondata)
        print(data)
        print('====================================')

        print('What you want to do next?')
        userOptionsMod = {1: "Add Expenses", 2: "Edit", 3: "Delete"}
        UserInput = userOptionSelection(userOptionsMod)
        if UserInput == 1:
            handleAddExpanse()
        if UserInput == 2 or UserInput == 3:
            string = 'Which row would you like to {}? '
            message = string.format(userOptionsMod[UserInput])

            userResponse = int(input(message))

            if 0 <= userResponse < len(data):
                if UserInput == 2:
                    return handleEditExpanse(userResponse)
                if UserInput == 3:
                    return handleDeleteExpanse(userResponse)
            else:
                print('Please provide valid row key.')
                return handleShowExpanse()
    else:
        print('No records found.')
        print('====================================')
        print('What you want to do next?')
        UserInput = userOptionSelection({1: "Add Expenses"})
        if UserInput == 1:
            handleAddExpanse()

def handleAddExpanse():
    name = amount = category = ''

    try:
        name = input('What did you spent on?\n')
        amount = float(input('Amount\n'))
        print("Select category")
        category = userOptionSelection(categories, True)
    except:
        print("Please provide a valid data.")
        handleAddExpanse()

    try:
        file = open("expanseTracker.json", "r")
        existingData = file.read()
        data = json.loads(existingData)
    except:
        data = []

    try:
        data.append({'name': name, 'amount': amount, 'category': category})

        fileA = open("expanseTracker.json", "w")
        fileA.write(json.dumps(data))
        fileA.close()

        print('New expanse added.')
        handleShowExpanse()
    except:
        print('Something went wrong, try again.')
        handleShowExpanse()

def handleEditExpanse(rowKey):
    jsonData = pandas.read_json("expanseTracker.json")
    data = pandas.DataFrame(jsonData)
    name = amount = category = ''
    try:
        name = input('What did you spent on? -> ' + data.loc[rowKey, 'name'] + '\n')
        amount = float(input('Amount ' + str(data.loc[rowKey, 'amount']) + '\n'))
        print("Select category -> " + data.loc[rowKey, 'category'] + '\n')
        category = userOptionSelection(categories, True)
    except:
        print("Please provide a valid data.")
        handleEditExpanse(rowKey)

    try:
        data.loc[rowKey, 'name'] = name
        data.loc[rowKey, 'amount'] = amount
        data.loc[rowKey, 'category'] = category

        fileA = open("expanseTracker.json", "w")
        fileA.write(data.to_json(orient='records'))
        fileA.close()

        print('New expanse added.')
        handleShowExpanse()
    except:
        print('Something went wrong, try again.')
        handleShowExpanse()

def handleDeleteExpanse(rowKey):
    try:
        jsonData = pandas.read_json("expanseTracker.json")
        data = pandas.DataFrame(jsonData)

        data.drop(rowKey, inplace=True)

        fileA = open("expanseTracker.json", "w")
        fileA.write(data.to_json(orient='records'))
        fileA.close()

        print('Expanse deleted.')
        handleShowExpanse()
    except:
        print('Something went wrong, try again.')
        handleShowExpanse()

print("===== WELCOME =====")
print("Keep track of your expenses and manage budgets.")

handleShowExpanse()