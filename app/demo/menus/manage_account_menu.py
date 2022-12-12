from .base_menu import Menu
from .dashboard_menu import Dashboard_menu


class Manage_account(Menu):
    """serves the home menu"""

   
    def add_phone_number(self):  # 1
        menu_text = "Enter your ID Number(Omang):\n"
        
        #self.session['level'] = 50
        return self.ussd_proceed(menu_text)

    def add_email_address(self):  # 2
        menu_text = "Enter your Passport Number:\n"
        #self.session['level'] = 30
        return self.ussd_proceed(menu_text)

    def add_physical_address(self):  # 3
        self.session['level'] = 20
        menu_text = "This service is not available yet\n"
        #self.session['level'] = 10
        return self.ussd_end(menu_text)

    def add_postal_address(self):  # 3
        self.session['level'] = 20
        menu_text = "This service is not available yet\n"
        #self.session['level'] = 10
        return self.ussd_end(menu_text)

    def add_employment_status(self):  # 3
        self.session['level'] = 441

        """serves the education level menu"""
        menu_text = "Choose Your Employment Status:\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. Employed\n"
        menu_text += " 2. Self-employed\n"
        menu_text += " 3. Unemployed\n"
        menu_text += " 0. Back\n"
        return self.ussd_proceed(menu_text)

    def add_education_level(self):  # 3
        self.session['level'] = 443

        """serves the education level menu"""
        menu_text = "Choose Your Education Level:\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. None (no formal education)\n"
        menu_text += " 2. Primary\n"
        menu_text += " 3. Secondary\n"
        menu_text += " 4. Certificate\n"
        menu_text += " 5. Diploma\n"
        menu_text += " 6. Undergraduate Degree\n"
        menu_text += " 7. Postgraduate Degree\n"
        menu_text += " 8. Doctoral\n"
        menu_text += " 9. Professor\n"
        menu_text += " 10. Other\n"
        menu_text += " 0. Back\n"
        return self.ussd_proceed(menu_text)

    def add_marital_status(self):  # 3
        self.session['level'] = 444

        """serves the education level menu"""
        menu_text = "Choose Your Marital Status:\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. Single\n"
        menu_text += " 2. Married\n"
        menu_text += " 3. Divorced\n"
        menu_text += " 4. Separated\n"
        menu_text += " 5. Widower\n"
        menu_text += " 0. Back\n"
        return self.ussd_proceed(menu_text)

    def handle_education_level(self):


        menus = {
            '1': "func",
            '2': "func",
            '3': "func",
            '4': "func",
            '5': "func",
            '6': "func",
            '7': "func",
            '8': "func",
            '9': "func",
            '10': "func",
            '0': self.manage_account_go_back,
        }

        if self.session["level"] == 443 and self.user_response in ['0','1','2','3','4','5','6','7','8','9','10']:
            return menus.get(self.user_response)()

        else:
            return self.invalid_input()
    
    def manage_account_go_back(self):

        self.session['level'] = 461
        
        menu = Dashboard_menu(session_id = self.session_id, session = self.session, phone_number = self.phone_number,
                      user_response = self.user_response,level = self.level)

        return menu.manage_account()

    """def go_back(self):

        self.session['level'] = 461
        
        menu = Dashboard_menu(session_id = self.session_id, session = self.session, phone_number = self.phone_number,
                      user_response = self.user_response,level = self.level)

        return menu.dashboard()"""
    def go_back(self):

        menu = Dashboard_menu(session_id = self.session_id, session = self.session, phone_number = self.phone_number,
                      user_response = self.user_response,level = self.level)
        
        self.session['level'] = 461
        
        return menu.dashboard()



    def execute(self):

        menus = {
            '1': self.add_phone_number,
            '2': self.add_email_address,
            '3': self.add_physical_address,
            '4': self.add_postal_address,
            '5': self.add_employment_status,
            '6': self.add_education_level,
            '7': self.add_marital_status,
            '0': self.go_back,
        }

        if self.session["level"] == 440 and self.user_response in ['0','1','2','3','4','5','6','7']:
            return menus.get(self.user_response)()

        elif self.session['level'] == 440 and self.user_response == "0":
            return menus.get(self.user_response)()

        elif self.session['level'] == 441:
            return self.handle_set_primary_phone()

        elif self.session['level'] == 443:
            return self.handle_education_level()

        else:
            return self.invalid_input()


    def __str__(self):
        return "Manage Account Menu"