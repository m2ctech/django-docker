from .base_menu import Menu
from .dashboard_menu import Dashboard_menu


class PrimaryContacts(Menu):
    """serves the home menu"""

    def set_primary_phone(self):  # 3

        self.session['level'] = 421
        """serves the choose primary phone menu"""
        menu_text = "\n Choose your primary mobile number:\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. +267 77654645\n"
        menu_text += " 2. +267 71234567\n"
        menu_text += " 0. Back\n"
        return self.ussd_proceed(menu_text)

    def set_primary_email(self):  # 3
        self.session['level'] = 422

        """serves the choose primary email menu"""
        menu_text = "\n Choose your primary email:\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. maemomothusi@gmail.com\n"
        menu_text += " 2. mothusi@pcgsoftware.co\n"
        menu_text += " 0. Back\n"
        return self.ussd_proceed(menu_text)

    def handle_set_primary_phone(self):

        menus = {
            #'1': function_1,
            #'2': function_2,
            '0': self.handlecontacts_go_back,
        }

        if self.session["level"] == 421 and self.user_response in ['0','1','2']:
            return menus.get(self.user_response)()
        else:
            return self.invalid_input()

    def handle_set_primary_email(self):

        menus = {
            #'1': function_1,
            #'2': function_2,
            '0': self.handlecontacts_go_back,
           # '0': self.go_back(self.set_primary_contact,"set_primary_contact"),
        }

        if self.session["level"] == 422 and self.user_response in ['0','1','2']:
            return menus.get(self.user_response)()
        else:
            return self.invalid_input()

    def handlecontacts_go_back(self):

        self.session['level'] = 461
        
        menu = Dashboard_menu(session_id = self.session_id, session = self.session, phone_number = self.phone_number,
                      user_response = self.user_response,level = self.level)

        return menu.set_primary_contact()
    
    def go_back(self):

        menu = Dashboard_menu(session_id = self.session_id, session = self.session, phone_number = self.phone_number,
                      user_response = self.user_response,level = self.level)
        
        self.session['level'] = 461
        
        return menu.dashboard()


    def execute_dash(self):

        
        menus = {
            '1': self.set_primary_phone,
            '2': self.set_primary_email,
            '0': self.go_back,
        }
        
        if self.session["level"] == 420 and self.user_response in ['1','2']:
            return menus.get(self.user_response)()

        elif self.session['level'] == 420 and self.user_response == "0":
            return menus.get(self.user_response)()

        elif self.session['level'] == 421:
            return self.handle_set_primary_phone()

        elif self.session['level'] == 422:
            return self.handle_set_primary_email()

        else:
            return self.invalid_input()

    def __str__(self):
        return "Manage Contact Menu"