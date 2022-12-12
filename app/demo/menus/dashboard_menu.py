 
from .base_menu import Menu
 



class Dashboard_menu(Menu):

    def dashboard(self):
        """serves the dashboard menu"""

        stored_password = "default"

        #if self.user_response == stored_password:
        menu_text = "Manage Profile,\n Choose an option:\n"
        #menu_text += " 1. Manage Account\n"
        menu_text += " 1. Add Profile Information\n"
        menu_text += " 2. Set Primary Contact Method\n"
        menu_text += " 3. Change Password\n"
        
        # print the response on to the page so that our gateway can read it
        return self.ussd_proceed(menu_text)
        #else:
            #menu_text = "Invalid Credentials"
            #return self.ussd_end(menu_text)

    def invalid_password(self):
        menu_text = "Invalid Credentials"
        return self.ussd_end(menu_text)


    def manage_account(self):

        """serves the home menu"""
        self.session['level'] = 440
        menu_text = "Manage Profile\n Choose an option:\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. Add Phone Number\n"
        menu_text += " 2. Add Email Address\n"
        menu_text += " 3. Add Physical Address\n"
        menu_text += " 4. Add Postal Address\n"
        menu_text += " 5. Add Employment Status\n"
        menu_text += " 6. Add Education Level\n"
        menu_text += " 7. Add Marital Status\n"
        menu_text += " 0. Back\n"
        
        return self.ussd_proceed(menu_text)

    def change_password(self):
        self.session['level'] = 430
        pass

    def set_primary_contact(self):
        self.session['level'] = 420

        """serves the home menu"""
        menu_text = "Choose an option:\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. Set Primary Phone Number\n"
        menu_text += " 2. Set Primary Email Address\n"
        menu_text += " 0. Back\n"
        self.session['level'] = 420
        return self.ussd_proceed(menu_text)


    def execute(self):
        menus = {
            '1': self.manage_account,
            '2': self.set_primary_contact,
            '3': self.change_password,
        }

        stored_password = "default"

        if self.session["level"] == 460 and self.user_response == stored_password:
            self.session['level'] = 461
            return self.dashboard()

        elif self.session["level"] == 460 and self.user_response != stored_password:
            return self.invalid_password()

        elif self.session["level"] == 461 and self.user_response in ['1','2','3']:
            return menus.get(self.user_response)()
        else:
            return self.invalid_input()

    def __str__(self):
        return "Dashboard Menu)"


 
 
 
 
 
 
 
 
