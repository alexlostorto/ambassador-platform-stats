def yesNo(question):
    userInput = input(question)

    while True:
        # Check input is acceptable
        if userInput == '':
            print(f"Don't leave me empty!")
        elif userInput.lower() in ['y', 'ye', 'yes', 'yeah']:
            return True
        elif userInput.lower() in ['n', 'no', 'nop', 'nope']:
            return False
        else:
            print(f"Write yes or no.")

        userInput = input(question)


def chooseOptions(countOptions):
    options = list(countOptions.keys())
    parameters = []

    print("---OPTIONS---")

    for i in range(len(options)):
        userInput = yesNo(f"Do you want to use {options[i]}: ")
        parameters.append(userInput)
        countOptions[options[i]] = userInput

    return parameters
