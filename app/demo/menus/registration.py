from urllib import request
from .base_menu import Menu
from ..utils import verify_username,verify_id, verify_omang_expiry, validate_password, unique_lastname, generate_password, check_expiry_date, send_message
from ..send_sms import send_sms
import requests
import json
import os

from appwrite.client import Client, AppwriteException
from appwrite.services.account import Account
from appwrite.services.users import Users


from appwrite.services.databases import Databases
from appwrite.id import ID

validate_omang_details = "https://crm.gov.bw/v1/functions/62fcb3f7a138ce17d8f1/executions"
get_user = "http://crmportal.gov.bw:4000/profile/get"
#create_profile_url = "https://crmportal.gov.bw/v1/functions/634e8d215dac82d053ce/executions"
create_user_profile = "http://crmportal.gov.bw:4000/profile/create"

project = os.environ.get('APPWRITE_PROJECT')
key = os.environ.get('APPWRITE_KEY')
head = {'X-Appwrite-Project': project, 'X-Appwrite-key':key}



class RegistrationMenu(Menu):
    """Serves registration callbacks"""

    def get_omang_expiry(self):
        # insert user's phone number
        self.session["level"] = 501

        if verify_id(self.user_response):
            self.session["id"] = self.user_response


            payload = {
                "username": f"{self.user_response}"
            }
            try:
                response = requests.post(get_user, headers=head, json=payload)
                r = response.json()

            except requests.exceptions.HTTPError as e:
                menu_text = "We are having technical difficulties, please try again later."
                return self.ussd_end(menu_text)
            
            if r["payload"]:
                menu_text = "Already registered"
                return self.ussd_end(menu_text)
            else:
                menu_text = "Enter your omang expiry date: dd-mm-yyyy"
                return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)

        
        

    def get_firstname(self):
        #if username or not User.by_username(username):  # check if user entered an option or username exists
            #self.user = User.create(username=username, phone_number=self.phone_number)
            
            #validate user id first
        #menu_text = verify_id(self.user_response)

        self.session["level"] = 502

        if verify_omang_expiry(self.user_response):
            self.session["idexp"] = self.user_response

            if check_expiry_date(self.user_response):

                menu_text = "Your Omang(ID) has expired"
                return self.ussd_end(menu_text)
            else:

                menu_text = "Enter your first name:"

                return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)
        

    def get_lastname(self):
        # insert user's phone number
        self.session["level"] = 503


        if verify_username(self.user_response):
            self.session["fname"] = self.user_response
            menu_text = "Enter your last name:"
            return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)

    """
    def get_password(self):
        self.session["level"] = 54

        if verify_username(self.user_response) or unique_lastname(self.user_response):
            self.session["lname"] = self.user_response
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
            self.session["level"] = 55
            self.session["password"] = self.user_response
            return self.ussd_proceed(menu_text)
    """

    def create_user_profile(self, first_name, last_name, date_of_birth, gender, marital_status, place_of_birth):

        pass
    
    def create_profile(self, first_name, last_name, id, date_of_birth, gender):
        
        payload = {
            "async":False,
            "data":f"{{\"first_name\":\"{first_name.capitalize()}\",\"middle_name\": \"\",\"surname\": \"{last_name.capitalize()}\",\"username\": \"{id}\",\"date_of_birth\" : \"{date_of_birth}\",\"gender\" : \"{gender.capitalize()}\",\"avatar\" : \"https://ui-avatars.com/api/?name={first_name.upper()}+{last_name.upper()}&background=fff&color=69c5ec&rounded=true&bold=true&size=128\",\"country_of_birth\":\"Botswana\",\"nationality\":\"Botswana\",\"citizenship\":\"Citizen\",\"registration\":\"Passport\"}}"
        }
        
        try:
            response = requests.post(create_user_profile, headers=head, json=payload)
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:

            menu_text = f"{response} {e.message}"

            return self.ussd_end(menu_text)



    def send_message(self):
        # insert user's phone number
        #user_password = self.session.get("password")
        user_password = generate_password()


        #if self.user_response == user_password:
        if verify_username(self.user_response) or unique_lastname(self.user_response):

            self.session["lname"] = self.user_response
            id = self.session.get("id")
            id_exp = self.session.get("idexp")
            first_name = self.session.get("fname")
            first_name = first_name.capitalize()
            lastname = self.session.get("lname")

            payload = {
                "async": False,
                "data": f"{{\"user_id\":\"{id}\",\"expiry_date\":\"{id_exp}\",\"surname\":\"{lastname}\",\"firstname\":\"{first_name}\"}}"
            }
            ###try response
            try:
                response = requests.post(validate_omang_details, headers=head, json=payload)
                response.raise_for_status()
                
                r = response.json()

                data = r["response"]
                response = json.loads(data)

            except requests.exceptions.HTTPError as e:

                menu_text = f"{response} {e}"

                return self.ussd_end(menu_text)



            if response["message"]:
                #CREATE PROFILE CODE GOES HERE
                profile_payload = response["payload"]['data']
                #profile_data = json.loads(profile_payload)
                
                #Extract data
                date_of_birth = profile_payload['BIRTH_DTE']
                gender_data = profile_payload["SEX"]
                gender = "Male" if gender_data == "M" else "Female"
                marital_status = profile_payload["MARITAL_STATUS_DESCR"]
                place_of_birth = profile_payload["BIRTH_PLACE_NME"]

                try:
                    result = users.create(f'{id}', f'{id}@1gov.bw', None, user_password, f'{first_name}')
                    
                    #second_result = self.create_user_profile(first_name,lastname, date_of_birth, gender, marital_status, place_of_birth)
                    second_result = self.create_profile(first_name, lastname, id, date_of_birth, gender)
                    print(result)
                    print(second_result)
                    

                    message_body = "Thank you for registering for a 1Gov account with the Government of Botswana. You will recieve your username and temporary password once your details have been verified."
                    subject = "Non-Citizen Registration"
                    #send_sms().sending(self.phone_number,first_name,id,user_password)
                    response = send_message(self.phone_number, message_body, subject)

                    if response:
                        menu_text = "You have successfully registered, thank you."
                    else:
                        menu_text = "We are having technical difficulties, please try again later."


                    return self.ussd_end(menu_text)

                except AppwriteException as e:
                    print(e.message)
                    menu_text = e.message
                    return self.ussd_end(menu_text)
                    

                
            else:
                menu_text = "Invalid Credentials"
                return self.ussd_end(menu_text)


        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)
        #else:
            #menu_text = "Passwords do not Match"
            #return self.ussd_end(menu_text)
            # go to home
            #return self.home()
        #else:  # Request again for name - level has not changed...
           # menu_text = "Username is already in use. Please enter your username \n"
            #return self.ussd_proceed(menu_text)

    def execute(self):
        if self.session["level"] == 500:
            return self.get_omang_expiry()

        if self.session["level"] == 501:
            return self.get_firstname()

        if self.session["level"] == 502:
            return self.get_lastname()

        if self.session["level"] == 503:
            return self.send_message()

            """

            if self.session["level"] == 54:
                return self.get_verify_password()

            if self.session["level"] == 55:
                return self.send_message()
            """
        else:
            return self.get_username()

    def __str__(self):
        return "Citizen Registration"