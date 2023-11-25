from InquirerPy import inquirer
action = inquirer.select(
    message="Select your action",
    choices=['delete', 'mask']
).execute()

table = inquirer.text(message="What's your table name?").execute()

choices = ["Apple", "Orange", "Banana", "Grape", "Strawberry"]

selected_fruits = inquirer.checkbox(
    message="Select your favorite fruits:",
    choices=choices
).execute()

answers = {"table": table, "color": action}
print(answers)
