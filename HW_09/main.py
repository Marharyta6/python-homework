def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)

    return wrapper


contacts = {}


@input_error
def add_contact(name, phone):
    contacts[name] = phone
    return f"Contact '{name}' with phone number '{phone}' has been added."


@input_error
def change_phone(name, phone):
    if name in contacts:
        contacts[name] = phone
        return f"Phone number for contact '{name}' has been updated to '{phone}'."
    else:
        raise KeyError(f"Contact '{name}' not found.")


@input_error
def get_phone(name):
    if name in contacts:
        return f"The phone number for '{name}' is '{contacts[name]}'."
    else:
        raise KeyError(f"Contact '{name}' not found.")


def show_all_contacts():
    if not contacts:
        return "There are no contacts saved."
    result = ""
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return result


def main():
    #print("How can I help you?")
    while True:
        user_input = input(">>>").strip().lower()

        if user_input in ("good bye", "close", "exit"):
            print("Good bye!")
            break

        if user_input == "hello":
            print("How can I help you?")

        elif user_input.startswith("add "):
            data = user_input[4:].split(" ")
            if len(data) != 2:
                print("Give me name and phone please")
            else:
                name, phone = data
                print(add_contact(name, phone))

        elif user_input.startswith("change "):
            data = user_input[7:].split(" ")
            if len(data) != 2:
                print("Give me name and phone please")
            else:
                name, phone = data
                print(change_phone(name, phone))

        elif user_input.startswith("phone "):
            name = user_input[6:].strip()
            print(get_phone(name))

        elif user_input == "show all":
            print(show_all_contacts())

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
