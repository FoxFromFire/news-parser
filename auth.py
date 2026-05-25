from users import USERS

current_user = None

def login():

    global current_user

    username = input("Логин: ")
    password = input("Пароль: ")

    for user in USERS:

        if (
            user["username"] == username
            and
            user["password"] == password
        ):

            current_user = user

            print("Успешный вход")

            return True

    print("Неверный логин или пароль")

    return False