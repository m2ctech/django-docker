from .base_menu import Menu






class LoginMenu(Menu):

    def get_user_password(self):
        self.session["level"] = 460

        self.session["id"] = self.user_response

        menu_text = "Enter your password:"

        return self.ussd_proceed(menu_text)


    def authenticate(self):
        self.session["level"] = 60
        id = self.session.get("id")

        #get password--api call 
        stored_password = "default"

        if self.user_response == stored_password:

            menu_text = ""

            return

        else:
            menu_text = "Invalid Credentials"
            return self.ussd_end(menu_text)

    def execute(self):
        if self.session["level"] == 470:
            return self.get_user_password()

        if self.session["level"] == 71:
            return self.authenticate()



    def __str__(self):
        return "log in process menu"
            
            

        


