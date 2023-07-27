# Simple password generator


# Yes, this uses os.system(). Not serious project anyway
import os
import string
import random


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def input_parameters():
    print(HELP_MESSAGE)
    allowed_parameters = set(ALLOWED_PARAMETERS.keys())
    while True:
        parameters = set(input("Enter parameters > ").strip())
        if not parameters <= allowed_parameters:
            incorrect_parameters = parameters - allowed_parameters
            print("Incorrect parameters found: %s" % str(incorrect_parameters))
        elif not parameters:
            print("No parameters have been specified")
        else:
            return parameters


def input_length():
    while True:
        try:
            length = int(input("Enter password length > "))
            if length < 8:
                print("Password must be 8 or more characters long")
            else:
                return length
        except ValueError:
            print("Password length must be a number")


def construct_alphabet(parameters):
    if "a" in parameters:
        return ALLOWED_PARAMETERS["a"]
    else:
        alphabet = str()
        for parameter in parameters:
            alphabet += ALLOWED_PARAMETERS[parameter]
        return alphabet


def generate_password(alphabet, length):
    return "".join(random.choices(alphabet, k=length))


if __name__ == "__main__":
    HELP_MESSAGE = (
        "Available parameters:\n"
        "* l | lowercase letters\n"
        "* u | uppercase letters\n"
        "* d | digits\n"
        "* p | punctuation\n"
        "* w | whitespace\n"
        "* a | all of the above"
    )
    ALLOWED_PARAMETERS = {
        "l": string.ascii_lowercase,
        "u": string.ascii_uppercase,
        "d": string.digits,
        "p": string.punctuation,
        "w": string.whitespace,
        "a": string.printable,
    }

    while True:
        try:
            clear_screen()
            parameters = input_parameters()
            length = input_length()
            alphabet = construct_alphabet(parameters)
            password = generate_password(alphabet, length)
            print("Generated password: %s" % password)
            input("\nPress 'Enter' to continue...")
        except KeyboardInterrupt:
            raise SystemExit
