"""
This program generates a unique password, sends it to an email, and
the person inputs the number sent to the email.  If successful, the
person can proceed with the program.  There's another file that
contains emails and passwords.  If the email and passwords are
correct, it proceeds to generate the otp and asks the user to input
the sent code.

"""

import random
import smtplib
import string


import re

user_name = re.compile(r"[A-Za-z]+")  # first name
username = re.compile(r"[A-Za-z0-9@_-]+")  # The unique one
email_format = re.compile(r"[A-Za-z0-9\.-_~]+@[A-Za-z]+\.(com|edu|org|net)")

capital = re.compile(r"[A-Z]")
numerical = re.compile(r"[0-9]")
small_letter = re.compile(r"[a-z]")


def Verify(user_passwd):  # This verifies that the password is safe
    capital_count = 0
    numerical_count = 0
    small_letter_count = 0
    user_passwd = list(user_passwd)
    for letter in user_passwd:
        if capital.search(letter) is not None:
            capital_count = capital_count + 1
        if numerical.search(letter) is not None:
            numerical_count = numerical_count + 1
        if small_letter.search(letter) is not None:
            small_letter_count = small_letter_count + 1
    if capital_count > 0 and numerical_count > 0 and small_letter_count > 0:
        return True
    elif len(user_passwd) > 12 and small_letter_count > 0:
        return True
    elif len(user_passwd) > 12 and capital_count > 0:
        return True
    else:
        return False


def GenerateCode():
    """Generate a unique code"""
    numerals = string.digits
    letters = string.ascii_lowercase
    capitals = string.ascii_uppercase
    escape = ["!", "@", "$", "#", "^", "&", "*", "(", ")", "-", "="]
    first_list = []
    start = 0
    while start < 3:
        first_list.append(random.choice(numerals))
        first_list.append(random.choice(letters))
        first_list.append(random.choice(capitals))
        first_list.append(random.choice(escape))
        start = start + 1
    random.shuffle(first_list)
    return "".join(first_list)


def Signup():
    """
    Just providing details which are then stored in a .txt
    file. Username and email should be unique.
    """
    details = {}

    user = input("Enter your name: ")
    bad_letter = False
    for letter in user:
        if user_name.search(letter) is None:
            bad_letter = True
    if bad_letter:
        print("wrong format")
    if len(user) > 20:
        print("Too long")
    else:
        details["firstname"] = user

    second = input("Enter your username: ")
    wrongformat = False
    for letter in second:
        if username.search(letter) is None:
            wrongformat = True
    if wrongformat:
        print("Wrong username format")
    else:
        # Open the file with usernames and check whether the
        #  name exists, if so, invalidate
        with open("usernames.txt", "r") as file:
            if second in file.read():
                print("Name already exists")
            else:
                # add the given username to the details dictionary
                details["username"] = second

    password = input("Enter a safe password: ")
    if Verify(password):
        details["password"] = password
    else:
        print(
            """Unsafe. Make sure the password has small and capital
            letters and some characters, or just a long password
            that's above 13 characters"""
        )

    email = input("Enter your email: ")
    correct_email = email_format.search(email)
    with open("emailfile.txt", "r") as file:
        names = file.read()
    if email in names:
        print("This email already exists")
    elif correct_email is not None and email not in names:
        correct_email = correct_email.group()
        if len(email) == len(correct_email):
            details["email"] = correct_email
        else:
            print("Wrong email format")
    else:
        print("Wrong email format")

    if (
        len(details.items()) == 4
    ):  # If all details are saved in the details, meaning all are
        # correct. Here now I can proceed with sending emails and
        # verification. If failed, repeat Signup
        print("Wait for a code to be sent to your email")
        the_code = GenerateCode()
        to_send = smtplib.SMTP("smtp.gmail.com", 587)
        to_send.ehlo()
        to_send.starttls()
        to_send.login("$EMAIL_ADDRESS", "£EMAIL_PASSWORD")
        to_send.sendmail("$EMAIL_ADDRESS",
                         details["email"],
                         str(the_code))
        to_send.quit()
        returned = input("Enter the code that has been sent to your email: ")
        if returned == the_code:
            details["status"] = "verified"
            print("You are now verified")
            # Now that the user is verified, add the email and username to
            # the files so that no other users can have the
            # same email or usernames
            with open("usernames.txt", "a") as file:
                file.write(details["username"] + "\n")
            with open("emailfile.txt", "a") as file:
                file.write(details["email"])
                file.write("\n")
            with open("verified_details.txt", "a") as file:
                file.write(str(details) + "\n")
        else:
            print("Wrong code: Try signing up again")
    else:
        print("Some details you entered are not correct, try again")

Signup()
