from .base_menu import Menu
from ..utils import verify_omang_expiry, verify_username, unique_lastname, check_gender_input, validate_password,generate_password,check_alpha
from ..send_sms import send_sms, non_citizen_sms
import requests
import os

from appwrite.client import Client, AppwriteException
from appwrite.services.account import Account
from appwrite.services.users import Users
from appwrite.services.databases import Databases
from appwrite.id import ID


create_profile_url = "https://crmportal.gov.bw/v1/functions/634e8d215dac82d053ce/executions"

project = os.environ.get('APPWRITE_PROJECT')
key = os.environ.get('APPWRITE_KEY')
head = {'X-Appwrite-Project': project, 'X-Appwrite-key':key}





class NonCitizenMenu(Menu):

    """Serves registration callbacks"""

    def get_passport_expiry(self):

        self.session["level"] = 481
        self.session["passport"] = self.user_response
        passport_number = self.user_response

        if check_alpha(passport_number):

            menu_text = "Enter your Passport Expiry Date\ndd-mm-yyyy:"

            return self.ussd_proceed(menu_text)

        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)


    def get_firstname(self):
        
        self.session["level"] = 482

        if verify_omang_expiry(self.user_response): #check passport numbers
            self.session["passexp"] = self.user_response

            menu_text = "Enter your first name:"

            return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)

    def get_lastname(self):
        
        self.session["level"] = 483

        if verify_username(self.user_response):
            self.session["fname"] = self.user_response
            menu_text = "Enter your last name:"
            return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)

    def get_gender(self):

        if verify_username(self.user_response) or unique_lastname(self.user_response):

            self.session["level"] = 484
            self.session["lname"] = self.user_response
            menu_text = "Enter your gender (M/F):"
            return self.ussd_proceed(menu_text)

        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)

    def get_date_of_birth(self):

        gender = check_gender_input(self.user_response)

        if gender == "F" or gender == "M":
            self.session["level"] = 485
            self.session["gender"] = gender
            menu_text = "Enter date of birth \n dd-mm-yyyy:"
            return self.ussd_proceed(menu_text)

        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)


    def get_place_of_birth(self):

        if verify_omang_expiry(self.user_response):
            self.session["level"] = 486
            self.session["date_of_birth"] = self.user_response

            menu_text = "Enter your place of birth:"
            return self.ussd_proceed(menu_text)


        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)


    def get_nationality(self):

        if self.user_response.isalnum():
            self.session["level"] = 487
            self.session["place_of_birth"] = self.user_response

            menu_text = "Enter your Nationality:"
            return self.ussd_proceed(menu_text)


        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)


    def get_country_of_birth(self):

        if self.user_response.isalpha():
            self.session["level"] = 488
            self.session["nationality"] = self.user_response

            menu_text = "Enter your Country of birth:"

            return self.ussd_proceed(menu_text)

        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)
    """
    def get_password(self):
        self.session["level"] = 39

        if self.user_response.isalpha():
            self.session["country_of_birth"] = self.user_response
            menu_text = "NB: Create a strong password \n Enter your password:"
            return self.ussd_proceed(menu_text)

        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)


    def get_verify_password(self):
        
        menu_text = validate_password(self.user_response)

        if "must" in menu_text:
            return self.ussd_proceed(menu_text)
        elif "Invalid" in menu_text:
            return self.ussd_end(menu_text)
        else:
            #session
            self.session["level"] = 40
            self.session["password"] = self.user_response
            return self.ussd_proceed(menu_text)
    """
    def create_profile(self, first_name, last_name, passport, date_of_birth, gender, country_of_birth, nationality):

        payload = {
            "async":False,
            "data":f"{{\"first_name\":\"{first_name.capitalize()}\",\"middle_name\": \"\",\"surname\": \"{last_name.capitalize()}\",\"username\": \"{passport}\",\"date_of_birth\" : \"{date_of_birth}\",\"gender\" : \"{gender}\",\"avatar\" : \"https://ui-avatars.com/api/?name={first_name.upper()}+{last_name.upper()}&background=fff&color=69c5ec&rounded=true&bold=true&size=128\",\"country_of_birth\":\"{country_of_birth.capitalize()}\",\"nationality\":\"{nationality.capitalize()}\",\"citizenship\":\"Non-Citizen\",\"registration\":\"Passport\"}}"
        }



        try:
            response = requests.post(create_profile_url, headers=head, json=payload)

        except requests.exceptions.HTTPError as e:

            menu_text = f"{response} {e.message}"

            return self.ussd_end(menu_text)


    def send_message(self):

        #user_password = self.session.get("password")
        user_password = generate_password()
        passport = self.session.get("passport")
        
        first_name = self.session.get("fname")
        lastname = self.session.get("lname")
        date_of_birth = self.session.get("date_of_birth")
        gender = self.session.get("gender")
        country_of_birth = self.session.get("country_of_birth")
        nationality = self.session.get("nationality")

        #if self.user_response == user_password:
        if self.user_response.isalpha():
            self.session["country_of_birth"] = self.user_response

            try:
                #result = users.create(f'{passport}', f'{passport}@1gov.bw', None, user_password, f'{first_name}')
                #second_result = self.create_user_profile(first_name,lastname, date_of_birth, gender, marital_status, place_of_birth)
                second_result = self.create_profile(first_name, lastname, passport, date_of_birth, gender, country_of_birth, nationality)
                #print(result)
                print(second_result)
                menu_text = "You have successfully registered, thank you"
                non_citizen_sms().sending(self.phone_number)
                return self.ussd_end(menu_text)
            except AppwriteException as e:
                print(e.message)
                menu_text = e.message
                return self.ussd_end(menu_text)

            menu_text = "You have successfully registered, thank you"
            send_sms().sending(self.phone_number,first_name,passport)
            return self.ussd_end(menu_text)

        else:
            #menu_text = "Passwords do not Match"
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)

    




    def execute(self):
        if self.session["level"] == 480:
            return self.get_passport_expiry()

        elif self.session["level"] == 481:
            return self.get_firstname()

        elif self.session["level"] == 482:
            return self.get_lastname()

        elif self.session["level"] == 483:
            return self.get_gender()

        elif self.session["level"] == 484:
            return self.get_date_of_birth()

        elif self.session["level"] == 485:
            return self.get_place_of_birth()

        elif self.session["level"] == 486:
            return self.get_nationality()

        elif self.session["level"] == 487:
            return self.get_country_of_birth()

        elif self.session["level"] == 488:
            return self.send_message()

    def __str__(self):
        return "Non-Citizen Registration Menu"



        
