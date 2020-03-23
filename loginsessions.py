import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

### Define the urls for login pages and the pages
### and the pages containing the information we wish to parse
### later on.......
login_url_tj = 'https://www.totaljobs.com/account/signin'
tj_applied = 'https://www.totaljobs.com/apply/myapplications?role=stepstoneuk-profile:applications,stepstoneuk-profile:basic,stepstoneuk-profile:contactable&authorisationToken=Pil3~bwj~_oJUmDO4fsuCkdY9aXBkaXQdNYGfPIpf0LjO_3Q3KaSblmMXYuBZcQn'

login_url_reed = 'https://www.reed.co.uk/account/signin'
reed_applied = 'https://www.reed.co.uk/account/jobs/applications'

### Define the requests module
session = requests.session()

### Initiate the GET page for login and search for tokens
### if the login pages require one
site = session.get(login_url_reed)
reed_content = bs(site.content, 'html.parser')

token = reed_content.find("input", {"name":"__RequestVerificationToken"})["value"]

### Define our dictionary of login information
login_reed = {
        
        '__RequestVerificationToken': token,
        'Credentials.Email': 'youremail',
        'Credentials.Password': 'yourpassword',
        'Credentials.RememberMe': 'true',
        'Credentials.SignInAttempts': 0,
        'ReturnUrl': '/', 
        
       }

### Initiate the POST module, posts our dictionary of login
### information to the clients server
s = session.post(login_url_reed, data=login_reed)

### Once login has been confirmed we proceed to the page/s 
### of information to parse
s = session.get(reed_applied)
s = s.text
s = bs(s, 'html.parser')

### This sequence is specific to each webpages format
### find and parse the relevant information
s = s.find_all('script', type='text/javascript')
s = s[4]
s = s.get_text()
s = re.findall('\[(.*?)\]',s)
s = s[0:-1]
s = ''.join(s)
s = s.replace('null','"None"')
s = s.replace('true','"true"')
s = s.replace('false','"false"')

### After the sequence we should have a string of relevant information
### we can convert this to a list of dictionaries
### which makes it easier to request different keys
s = eval(s)

### Now we can create new lists of information ready for exporting
### to excel for dashboards or visualisations within python
app = []
jt = []

for d in s:
    d = d['JobTitle']
    jt.append(d)
  
for i in s:
    i = i['AppliedOn']
    app.append(i)   
    
reed_data = pd.DataFrame({'Job Title': jt, 'Date Applied': app})
reed_data.to_excel('reed_dash.xlsx', index=False)
    

'''    
with open('reed_dash.csv','w', newline='') as f:
    field_names = ['Job Title','Date Applied']
    reed_writer = csv.DictWriter(f, delimiter=',', fieldnames=field_names)

    reed_writer.writeheader()
    reed_writer.writerow({'Job Title':jt, 'Date Applied':app})
    
print (len(jt))
'''
