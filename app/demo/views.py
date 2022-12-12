import json


from django.shortcuts import render
from django.core.cache import cache

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests

from .menus.base_menu import Menu
from .menus.home import LowerLevelMenu
from .menus.registration import RegistrationMenu
from .menus.noncitizen_registration import NonCitizenMenu
from .menus.login_menu import LoginMenu
from .menus.dashboard_menu import Dashboard_menu
from .menus.manage_account_menu import Manage_account
from .menus.primary_contacts_menu import PrimaryContacts
headers = {"Content-type": "application/json"}



@csrf_exempt
def index(request):

  """Handles post call back from AT"""

  if request.method == 'POST':
    session_id = request.POST.get('sessionId')
    service_code = request.POST.get('serviceCode')
    phone_number = request.POST.get('phoneNumber')
    text = request.POST.get('text')

    
    text_array = text.split("*")
    #reversed_text_array = text_array.reverse()
    text_array.reverse()
    user_response = text_array[0]

    if cache.get(session_id):
      session = cache.get(session_id)
    else:
      session = {"level":0, "session_id":session_id, "id": "default", "idexp": "default", "fname":"default", "lname":"default", "password":"default", "passport":"default", "passexp":"default", "gender":"default", "date_of_birth":"default", "place_of_birth":"default", "nationality":"default","country_of_birth":"default"}
      cache.set(session_id, session)

    level = session.get("level")

    if level < 2:
        menu = LowerLevelMenu(session_id=session_id, session=session, phone_number=phone_number,
                              user_response=user_response)
        return menu.execute()
      
    if level >= 500:
        menu = RegistrationMenu(session_id=session_id, session=session, phone_number=phone_number,
                       user_response=user_response,level=level)
        return menu.execute()

    if level >= 480:
        menu = NonCitizenMenu(session_id=session_id, session=session, phone_number=phone_number,
                       user_response=user_response,level=level)
        return menu.execute()

    if level >= 470:
        menu = LoginMenu(session_id=session_id, session=session, phone_number=phone_number,
                       user_response=user_response,level=level)
        return menu.execute()

    if level >= 460:
      menu = Dashboard_menu(session_id=session_id, session=session, phone_number=phone_number,
                      user_response=user_response,level=level)
      return menu.execute()
    
    if level >= 440:
      menu = Manage_account(session_id=session_id, session=session, phone_number=phone_number,
                      user_response=user_response,level=level)
      return menu.execute()

    if level >= 420:
      menu = PrimaryContacts(session_id=session_id, session=session, phone_number=phone_number,
                      user_response=user_response,level=level)
      return menu.execute_dash()




          
    response = ("END nothing here", 200)
      
    return HttpResponse(response, content_type='text/plain')
  
  elif request.method == 'GET':
    response = ("USSD LIVE ", 200)
    return HttpResponse(response, content_type='text/plain')

 