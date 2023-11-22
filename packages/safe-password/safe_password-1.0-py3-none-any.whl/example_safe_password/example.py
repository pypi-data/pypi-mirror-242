# import 'safe_password' library
from safe_password import generate, verify

# import 'getpass' for secure password input: https://docs.python.org/3/library/getpass.html
import getpass

# getting user information
user_login = input("Login: ").lower()
user_password = getpass.getpass("Password: ")

# writing to 'data' variable
data = generate(user_password)

# Verify user data, and encrypted data
status = verify(salt=data['salt'], user_input=input("Password one more time: "), password=data['password'])

if status == True:
    print("Welcome!")
else:
    print("Sorry, wrong password!")