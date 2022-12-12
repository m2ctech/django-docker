import json
from django.http import HttpResponse
import requests
#from .dashboard_menu import Dashboard_menu

from django.core.cache import cache



class Menu(object):

    
    def __init__(self, session_id, session,user_response, phone_number=None, level=None):
        self.session = session
        self.session_id = session_id
        self.user_response = user_response
        self.phone_number = phone_number
        self.level = level
        

    def execute(self):
        raise NotImplementedError

    def ussd_proceed(self, menu_text):
        cache.set(self.session_id, self.session)
        menu_text = "CON {}".format(menu_text)
        response = HttpResponse(menu_text, 200)
        response.headers['Content-Type'] = "text/plain"
        return response

    def ussd_end(self, menu_text):
        cache.delete(self.session_id)
        menu_text = "END {}".format(menu_text)
        response = HttpResponse(menu_text, 200)
        response.headers['Content-Type'] = "text/plain"
        return response

    def invalid_input(self):
        menu_text = "Invalid Input"
        return self.ussd_end(menu_text)

    """def go_back(self,back_function,level_number = 461,function_name=""):

        #menu = Dashboard_menu(session_id = self.session_id, session = self.session, phone_number = self.phone_number,
                      #user_response = self.user_response,level = self.level)

        self.session['level'] = level_number

        if function_name == "manage_account":
            return back_function()

        elif function_name == "set_primary_contact":
            return back_function()

        elif function_name == "change_password":
            return back_function()
        elif function_name == "":
            return back_function"""

        
    def home(self):
        """serves the home menu"""
        menu_text = "Welcome to 1Gov,\n Choose an option\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. Citizen Registration\n"
        menu_text += " 2. Non-Citizen Registration\n"
        menu_text += " 3. Login\n"
        
        self.session['level'] = 1
        
        # print the response on to the page so that our gateway can read it
        return self.ussd_proceed(menu_text)


    def __str__(self):
        return "Base Menu (blueprint)"