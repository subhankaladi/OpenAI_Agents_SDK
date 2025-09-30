
subject = input("Your Subject is :")

def prompt(ctx, agent):

    if subject.lower() == "python":
        return "You are python assistant always repond related to python"
    elif subject.lower() == "typescript":
        return "You are typescript assistant always respond related to typescript"
    else :
        return "You are helpfull assistant"
    