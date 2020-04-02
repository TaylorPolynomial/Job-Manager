import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

### Global variables
base_url  = 'https://www.reed.co.uk/'
session = requests.session()
email = 'damienkharley@gmail.com'
password = 'Planck1034'          


def _get(url):
    return session.get(url)
    

def _token(url):
    site = _get(url)
    content = bs(site.content, 'html.parser')
    return content.find("input", {"name":"__RequestVerificationToken"})["value"]


def _post(url, data):
    return session.post(url, data)


login_reed = {
        
            '__RequestVerificationToken': _token(url='https://www.reed.co.uk/account/signin'),
            'Credentials.Email': email,
            'Credentials.Password': password,
            'Credentials.RememberMe': 'true',
            'Credentials.SignInAttempts': 0,
            'ReturnUrl': '/', 
        
            }

login_tj = {
            
            '__RequestVerificationToken': _token(url = 'https://www.totaljobs.com/account/signin'),
            'Form.Email': email,
            'Form.Password': password,
            'Form.RememberMe': 'true'
            
            }

_get(url = 'https://www.reed.co.uk/account/signin')
_token(url = 'https://www.reed.co.uk/account/signin')
_post(url = 'https://www.reed.co.uk/account/signin', data = login_reed)

_get(url = 'https://www.totaljobs.com/account/signin')
_token(url = 'https://www.totaljobs.com/account/signin')
_post(url = 'https://www.totaljobs.com/account/signin', data = login_tj)

print (_get(url='https://www.reed.co.uk/account/jobs/applications').url)

print (_get(url='https://www.totaljobs.com/Authenticated/MyApplications').url)