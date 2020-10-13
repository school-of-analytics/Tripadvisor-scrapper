# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:55:24 2020

@author: Biswajeet
"""

import streamlit as st
import re
import json
import base64
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas.core.common import flatten

st.title("Trip Advisor France Scrapper")
st.sidebar.write("""
# Enter the Trip Advisor URL
""")
st.sidebar.write("""
#### Trip Advisor URL must start with https://  
""")
st.sidebar.write("""
#### URL must be a France(.fr) url  
""")
st.text("")
st.text("")
st.sidebar.write("""
#### Example: 
""")
st.text("")
st.sidebar.write("""
#### _https://www.tripadvisor.fr/Attractions-g11038881-Activities-c56-t208-Occitanie.html_
""")
url = st.sidebar.text_input("Trip Advisor URL")
button_was_clicked = st.sidebar.button("SUBMIT")


#url = 'https://www.tripadvisor.fr/Attractions-g11038881-Activities-c56-t208-Occitanie.html'
#url = 'https://www.tripadvisor.fr/Attractions-g11038881-Activities-c61-Occitanie.html'
#url = 'https://www.tripadvisor.fr/Attractions-g11038881-Activities-c40-Occitanie.html'
#url = 'https://www.tripadvisor.fr/Attractions-g187144-Activities-c61-Ile_de_France.html'
#url = 'https://www.tripadvisor.fr/Attractions-g11038881-Activities-c56-t208-oa30-Occitanie.html'
def tripadvisor(urll):
    html = requests.get(urll).text
    soup=BeautifulSoup(html,"html.parser")
    data = soup.findAll('div',attrs={'class':'_6sUF3jUd'})
    
    hotel_name = []
    
    hotel_link= []
    
    for div in data:
        links = div.findAll('h2')
        for a in links:
            hotel_name.append(a.text)
            
    
    for div in data:
        links = div.findAll('a',attrs={'class':'_1QKQOve4'})
        for a in links:
            hotel_link.append("https://www.tripadvisor.fr" + a['href'])
    
    hotel_data = pd.DataFrame(list(zip(hotel_name,hotel_link)),columns = ['Hotel Name','Hotel Link'])
    #url = 'https://www.tripadvisor.fr/Attraction_Review-g196629-d12447489-Reviews-Canyoning_Saint_Lary-Saint_Lary_Soulan_Hautes_Pyrenees_Occitanie.html'
    
    #url = 'https://www.tripadvisor.fr/Attraction_Review-g1841271-d13280719-Reviews-Escape_Dimension_La_Croisee_des_Mondes-Saleilles_Perpignan_Pyrenees_Orientales_.html'
    mail = []
    phone = []
    website = []
    address = []
    for i in hotel_data['Hotel Link']:
        html_data = requests.get(i).text
        data = re.search(r'window\.__WEB_CONTEXT__=(\{.*?\});', html_data).group(1)
        data = json.loads(data.replace('pageManifest', '"pageManifest"'))
        soup=BeautifulSoup(html_data,"html.parser")
        
        def get_emails(val):
            if isinstance(val, dict):
                for k, v in val.items():
                    if k == 'email':
                        if v:
                            yield v
                    else:
                        yield from get_emails(v)
            elif isinstance(val, list):
                for v in val:
                    yield from get_emails(v)
                    
        def get_phones(val):
            if isinstance(val, dict):
                for k, v in val.items():
                    if k == 'phone':
                        if v:
                            yield v
                    else:
                        yield from get_phones(v)
            elif isinstance(val, list):
                for v in val:
                    yield from get_phones(v)
                    
        def get_websites(val):
            if isinstance(val, dict):
                for k, v in val.items():
                    if k == 'website':
                        if v:
                            yield v
                    else:
                        yield from get_websites(v)
            elif isinstance(val, list):
                for v in val:
                    yield from get_websites(v)
        
        try:
            
            for email in get_emails(data):
                email = base64.b64decode(email).decode('utf-8')
                email = re.search(r'mailto:(.*)_', email).group(1)
                mail1 = []
                mail1.append(email)
            mail.append(mail1[0])
        except:
            for email in get_emails(data):
                mail1 = []
                mail1.append(email)
            mail.append(mail1[0])
        
        #print(mail[0])
        
        
        try:
            
            for email in get_phones(data):
                email = base64.b64decode(email).decode('utf-8')
                phone1 = []
                phone1.append(email)
            phone.append(phone1[0])
        except:
            for email in get_phones(data):
                phone1 = []
                phone1.append(email)
            phone.append(phone1[0])    
        
        #print(phone[0])
        
    
        try:
        
            for email in get_websites(data):
                email = base64.b64decode(email).decode('utf-8')
                website1=[]
                website1.append(email)
            website.append(website1[0])
        except:
            for email in get_websites(data):
                website1=[]
                website1.append(email)
            website.append(website1[0]) 
    
    #print(website[0])
    
    
        try:
            divs = soup.findAll("div",attrs={'class':'LjCWTZdN'})
            div = divs[0]
            for span in div:
                address1 = []
                address1.append(span.text)
            address.append(address1)
            # try:
            #      for span in soup.findAll("div",attrs={'class':'_2hDw2pmg'}):
            #          address1 = []
            #          address1.append(span.text)
            #      address.append(address1[0])
            # except:
            #      address.append('not available')
        except:
            address.append('not available')
    
    address = list(flatten(address))
    hotel_data['Hotel Website'] = website
    hotel_data['Hotel Phone'] = phone
    hotel_data['Hotel Email'] = mail
    hotel_data['Hotel Address'] = address
    return hotel_data
    #print(address[1])

main_data = pd.DataFrame()  
if url == '':
    st.write("Please enter the trip advisor url")
    st.write("Wait for some minutes to load the data")
else:
    main_data = tripadvisor(url)
    st.table(main_data)
    
csv = main_data.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (while downloading save by writing file name with .csv)'
st.markdown(href, unsafe_allow_html=True)
st.text("")
st.text("")
st.write(" Developed by Biswajeet Swaro")
st.write("bjswaro123@gmail.com")
st.write("+91-9040813360")