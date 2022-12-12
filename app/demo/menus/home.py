from .base_menu import Menu


class LowerLevelMenu(Menu):
    """serves the home menu"""
    def citizen_registration(self):  # 1
        menu_text = "Enter your ID Number(Omang):\n"
        
        self.session['level'] = 500
        return self.ussd_proceed(menu_text)

    def noncitizen_registration(self):  # 2
        menu_text = "Enter your Passport Number:\n"
        self.session['level'] = 480
        return self.ussd_proceed(menu_text)

    def login(self):  # 3
        self.session['level'] = 470
        menu_text = "Enter your 1Gov ID:"
        
        # print the response on to the page so that our gateway can read it
        return self.ussd_proceed(menu_text)




    def execute(self):
        menus = {
            '1': self.citizen_registration,
            '2': self.noncitizen_registration,
            '3': self.login
        }

        if self.session['level'] == 0 or self.user_response in ['1','2','3']:

            return menus.get(self.user_response, self.home)()

        else:
            return self.invalid_input()


    def __str__(self):
        return "Entry level Menu"