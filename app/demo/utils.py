
from ast import Return
import re
import random
import string
import datetime
from datetime import date
import requests
import os



project = os.environ.get('APPWRITE_PROJECT')  #""
key = os.environ.get('APPWRITE_KEY') #"
head = {'X-Appwrite-Project': project, 'X-Appwrite-key':key}

send_sms_url = "https://crm.gov.bw/v1/functions/62e8e5a101588529fd25/executions"


now = datetime.datetime.now()

def verify_id(user_id):
    """Validate ID/Omang number """
    if len(user_id) != 9 :
        return False
      
    elif user_id.isnumeric(): 
        return True

    else:
        return False
    
    

def verify_username(text):

    if text.isalpha():
        return True
    else:
        return False

def check_pin(user_pin):

    if len(user_pin) == 4 and user_pin.isnumeric() :
        return True
    else:
        return False

def verify_pin():
    pass



def verify_omang_expiry(date):
    check_value = 0
    if "-" in date:
        date_array = date.split("-")
        if len(date_array) == 3:
            if len(date_array[0])==2 and date_array[0].isnumeric():
                check_value += 1

            if len(date_array[1])==2 and date_array[1].isnumeric():
                check_value += 1
    
            if len(date_array[2])==4 and date_array[2].isnumeric():
                check_value += 1
            return True if check_value == 3 else False
        else:
            return False
    else:
        return False


def validate_password(password):

    pattern = re.compile(r'')

    menu_text = ""
    if (len(password)<8):
        menu_text = "NB: Your password must be eight characters long \n Enter your password:"
        
    elif re.search(r'[!@#$%&]', password) is None:
        menu_text = "NB: Your password must contain atleast one special symbol \n Enter your password:"
        
    elif re.search(r'\d', password) is None:
        menu_text = "NB: Your password must contain atleast one digit \n Enter your password:"
    
    elif re.search(r'[A-Z]', password) is None:
        menu_text = "NB: Your password must contain atleast one capital letter \n Enter your password:"
        
    elif re.search(r'[a-z]', password) is None:
        menu_text = "Your password must contain atleast one lowercase letter \n Enter your password:"
        
        
    elif re.match(r'[a-z A-Z 0-9 !@#$%&]{8}', password):
        pattern = re.compile(r'[a-z A-Z 0-9 !@#$%&]{8}')
        result = pattern.match(password)
        menu_text = "Verify your password:"
        
    else:
        menu_text= "Invalid password"

    return menu_text


def unique_lastname(lastname):
    
    if "." in lastname:
        new_array = lastname.split(".")
        for word in new_array:
            result = word.isalpha()
            if not result:
                return False
        return True
    
    
    elif "-"  or " " in lastname:
        new_array = lastname.split("-") if "-" in lastname else lastname.split(" ")
        if len(new_array) == 2 and new_array[0] and new_array[1]:
            result =  True if new_array[0].isalpha() and new_array[1].isalpha() else False
            return result
            
        else:
            result = False
            return result
            
    else:
        return False

def check_gender_input(text):
     
    gender = text.upper()

    if gender == "M" or gender == "MALE":
        gender = "M"
    elif gender == "F" or gender == "FEMALE":
        gender = "F"

    else:
        gender = "Invalid input"

    return gender


def generate_password():

    num_1 = random.randint(0,9)
    num_2 =  random.randint(0,9)
    upp_1 = random.choice(string.ascii_uppercase)
    upp_2 = random.choice(string.ascii_uppercase)
    low_1 = random.choice(string.ascii_lowercase)
    low_2 = random.choice(string.ascii_lowercase)
    low_3 = random.choice(string.ascii_uppercase)
    upp_3 = random.choice(string.ascii_uppercase)

    password = [num_1,num_2,upp_1,upp_2,upp_3,low_1,low_2,low_3]
    random.shuffle(password)
    password_2 = ""

    for i in password:
        password_2 +=f"{i}"

    return password_2



def check_expiry_date(date_input):
    
    date_array = date_input.split("-")
    
    date_1 = date(int(date_array[2]),int(date_array[1]),int(date_array[0]))
    date_2 = date(int(now.strftime("%Y")),int(now.strftime("%m")),int(now.strftime("%d")))
    
    return date_2 > date_1


def check_alpha(input):
    
    if re.match("^[A-Za-z0-9]+$", input):
        return True
    else:
        return False


def send_message(mobile_number, message_body, subject):


    mobile_number = mobile_number.replace('+', '')

    payload = {
            "async":False,
            "data":f"{{\"number\":\"{mobile_number}\",\"message\": \"{message_body}\",\"subject\" : \"{subject}\"}}"
        }
        
    try:
        response = requests.post(send_sms_url, headers=head, json=payload)
        response.raise_for_status()
        return True

    except requests.exceptions.HTTPError as e:

        menu_text = f"{response} {e.message}"

        return False







