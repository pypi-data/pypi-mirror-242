# safe_password

This is a simple library, i do in free time, when trying to understand, how websites store passwords, and how to do this as much secure, as possible. This is learning project, so you can use it for free in any software, you make.

# Examples

This module have only two functions - *generate(password)*, and *verify(salt, user_input)*. You can found more examples in **src/example_safe_password/**, but here is a short explanation:

1. *generate(password)* takes raw user password, and generate random hash and salt, that always unique.
2. *verify(salt, user_input, password)*, where salt and password is given by *generate()* function, and user_input is raw **user input**. This function return **True**, if it's correct input.