import africastalking

# TODO: Initialize Africa's Talking

africastalking.initialize(
    username='sandbox',
    api_key='0c476ef13cab0e15e6c1ee7c9905e7610feb7e23b8f49883a816988493e92b77'
)

sms = africastalking.SMS

class send_sms():

    def send(self):
        pass
        
        #TODO: Send message

    def sending(self, phone_number, first_name, id, password):
        # Set the numbers in international format
        recipients = [phone_number]
        # Set your message
        message = f"Hi {first_name.capitalize()} your 1Gov ID is: {id} and your temporary password is: {password}, please login to activate your account within the next 24 hrs.";
        # Set your shortCode or senderId
        sender = "1GOV"
        try:
            response = sms.send(message, recipients, sender)
            print (response)
        except Exception as e:
            print (f'Experiencing, technical difficulties: {e}')


class non_citizen_sms():


    def sending(self, phone_number):
        # Set the numbers in international format
        recipients = [phone_number]
        # Set your message
        message = f"Thank you for registering for a 1Gov account with the Government of Botswana. You will recieve your username and temporary password once your details have been verified.";
        # Set your shortCode or senderId
        sender = "1GOV"
        try:
            response = sms.send(message, recipients, sender)
            print (response)
        except Exception as e:
            print (f'Experiencing, technical difficulties: {e}')

