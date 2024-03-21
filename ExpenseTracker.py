import json
import pandas as pd
import matplotlib.pyplot as plt

categories = {
    1: 'Utilities', 2: 'Entertainment', 3: 'Meals', 4: 'Transportation', 5: 'Office Supplies', 6: 'Travel',
    7: 'Other'
}


def user_option_selection(options, need_value=False):
    user_message = ''
    for option, description in options.items():
        user_message += f"{option}. {description}\n"

    try:
        user_response = int(input(user_message))

        if options.get(user_response):
            if need_value:
                return options[user_response]
            else:
                return user_response
    except ValueError:
        print("Please provide a valid option.")

    return user_option_selection(options, need_value)


def handle_expense_graph():
    file = open("expanseTracker.json", "r")
    existing_data = file.read()
    json_data = json.loads(existing_data)

    expenses = {}
    for expense in json_data:
        if expense['category'] in expenses:
            expenses[expense['category']] += float(expense['amount'])
        else:
            expenses[expense['category']] = float(expense['amount'])

    plt.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%')
    plt.show()
    handle_show_expense()


def handle_show_expense():
    file = open("expanseTracker.json", "r")
    existing_data = file.read()
    print('============= Expenses =============')

    if existing_data != '':
        json_data = json.loads(existing_data)
        data = pd.DataFrame(json_data)
        print(data)
        print('====================================')

        print('What do you want to do next?')
        user_options_mod = {1: "Add Expenses", 2: "Edit", 3: "Delete", 4: "Show Graph"}
        user_input = user_option_selection(user_options_mod)
        if user_input == 1:
            handle_add_expense()
        elif user_input == 2 or user_input == 3:
            string = 'Which row would you like to {}? '
            message = string.format(user_options_mod[user_input])

            user_response = int(input(message))

            if 0 <= user_response < len(data):
                if user_input == 2:
                    return handle_edit_expense(user_response)
                elif user_input == 3:
                    return handle_delete_expense(user_response)
            else:
                print('Please provide valid row key.')
                return handle_show_expense()
        elif user_input == 4:
            return handle_expense_graph()

    else:
        print('No records found.')
        print('====================================')
        print('What you want to do next?')
        user_input = user_option_selection({1: "Add Expenses"})
        if user_input == 1:
            handle_add_expense()


def handle_add_expense():
    name = amount = category = ''

    try:
        name = input('What did you spent on?\n')
        amount = float(input('Amount\n'))
        print("Select category")
        category = user_option_selection(categories, True)
    except ValueError:
        print("Please provide a valid data.")
        handle_add_expense()

    try:
        with open("expanseTracker.json", "r") as file:
            existing_data = file.read()
            data = json.loads(existing_data) if existing_data else []

        data.append({'name': name, 'amount': amount, 'category': category})

        with open("expanseTracker.json", "w") as file:
            file.write(json.dumps(data))

        print('New expense added.')
        handle_show_expense()
    except Exception as e:
        print(f'Something went wrong: {e}')
        handle_show_expense()


def handle_edit_expense(row_key):
    json_data = pd.read_json("expanseTracker.json")
    data = pd.DataFrame(json_data)
    name = amount = category = ''

    try:
        name = input('What did you spend on? -> ' + data.loc[row_key, 'name'] + '\n')
        amount = float(input('Amount ' + str(data.loc[row_key, 'amount']) + '\n'))
        print("Select category -> " + data.loc[row_key, 'category'] + '\n')
        category = user_option_selection(categories, True)
    except ValueError:
        print("Please provide a valid data.")
        handle_edit_expense(row_key)

    try:
        data.loc[row_key, 'name'] = name
        data.loc[row_key, 'amount'] = amount
        data.loc[row_key, 'category'] = category

        with open("expanseTracker.json", "w") as file:
            file.write(data.to_json(orient='records'))

        print('New expense added.')
        handle_show_expense()
    except Exception as e:
        print(f'Something went wrong: {e}')
        handle_show_expense()


def handle_delete_expense(row_key):
    try:
        json_data = pd.read_json("expanseTracker.json")
        data = pd.DataFrame(json_data)

        data.drop(row_key, inplace=True)

        with open("expanseTracker.json", "w") as file:
            file.write(data.to_json(orient='records'))

        print('Expense deleted.')
        handle_show_expense()
    except Exception as e:
        print(f'Something went wrong: {e}')
        handle_show_expense()


print("===== WELCOME =====")
print("Keep track of your expenses and manage budgets.")

handle_show_expense()
