#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import parse
import pdfplumber
import pandas as pd
from collections import namedtuple


# In[2]:


#Column Names
Line= namedtuple('Line_test', 'referral_id patient_id patient_name patient_date_of_birth patient_sex gp_suggested_priority gp_suggested_specialty referral_short_text referral_date referring_gp_site_name')
file = 'Example_Clinical_Information_Summary.pdf'


# In[3]:


lines = []
with pdfplumber.open(file) as pdf:
    pages = pdf.pages
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split('\n'):
            #print(line)
            if re.findall('Referring Organisation:  (.*)  Clinical', line):
                referring_gp_site_name=re.compile('Referring Organisation:  (.*)  Clinical').search(line).group(1)
            elif re.findall(r'UBRN:  (.*)  Age', line):
                referral_id=re.compile(r'UBRN:  (.*)  Age').search(line).group(1)
            elif re.findall(r'NHS:  (.*)  Gender:  (.*)', line):
                patient_id=re.compile(r'NHS:  (.*)  Gender').search(line).group(1)
                if re.findall(r'Gender:  (.*)', line):
                    patient_sex =re.compile(r'Gender:  (.*) ').search(line).group(1)

            elif re.findall(r'Patient:  (.*)  Date', line):
                patient_name=re.compile(r'Patient:  (.*)  Date').search(line).group(1)
                if re.findall('Date of Birth:  (.*) ', line):
                    patient_date_of_birth= re.compile('Date of Birth:  (.*) ').search(line).group(1)
                  
            elif re.findall(r'Priority:  (.*)', line):
                gp_suggested_priority=re.compile(r'Priority:  (.*) ').search(line).group(1)
                
            elif re.findall(r'Clinical Context:  (.*)/', line):
                gp_suggested_specialty=re.compile(r'Clinical Context:  (.*)/').search(line).group(1)
            
            elif re.findall('Clinical Term:  (.*) ', line):
                referral_short_text=re.compile(r'Clinical Term:  (.*)').search(line).group(1)
            
            elif re.findall(r'Referral Created Date:  (.*)', line):
                referral_date=re.compile(r'Referral Created Date:  (.*\d{4})').search(line).group(1)
            
            elif re.findall(r'Referring Organisation:  (.*)', line):
                referring_gp_site_name=re.compile(r'Referring Organisation:  (.*)').search(line).group(1)
            
            elif re.compile('^Referring Organisation:  (.*)  Clinical').search(line):
                referring_gp_site_name=re.compile('^Referring Organisation:  (.*)  Clinical').search(line).group(1)
            


# In[4]:


lines = []
with pdfplumber.open(file) as pdf:
    pages = pdf.pages
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split('\n'):
            #print(line)
            if re.findall('Referring Organisation:  (.*)  Clinical', line):
                referring_gp_site_name=re.compile('Referring Organisation:  (.*)  Clinical').search(line).group(1)
            elif re.findall(r'UBRN:  (.*)  Age', line):
                referral_id=re.compile(r'UBRN:  (.*)  Age').search(line).group(1)
            elif re.findall(r'NHS:  (.*)  Gender:  (.*)', line):
                patient_id=re.compile(r'NHS:  (.*)  Gender').search(line).group(1)
                if re.findall(r'Gender:  (.*)', line):
                    patient_sex =re.compile(r'Gender:  (.*) ').search(line).group(1)

            elif re.findall(r'Patient:  (.*)  Date', line):
                patient_name=re.compile(r'Patient:  (.*)  Date').search(line).group(1)
                if re.findall('Date of Birth:  (.*) ', line):
                    patient_date_of_birth= re.compile('Date of Birth:  (.*) ').search(line).group(1)
                  
            elif re.findall(r'Priority:  (.*)', line):
                gp_suggested_priority=re.compile(r'Priority:  (.*) ').search(line).group(1)
                
            elif re.findall(r'Clinical Context:  (.*)/', line):
                gp_suggested_specialty=re.compile(r'Clinical Context:  (.*)/').search(line).group(1)
            
            elif re.findall('Clinical Term:  (.*) ', line):
                referral_short_text=re.compile(r'Clinical Term:  (.*)').search(line).group(1)
            
            elif re.findall(r'Referral Created Date:  (.*)', line):
                referral_date=re.compile(r'Referral Created Date:  (.*\d{4})').search(line).group(1)
            
            elif re.findall(r'Referring Organisation:  (.*)', line):
                referring_gp_site_name=re.compile(r'Referring Organisation:  (.*)').search(line).group(1)
            
            elif re.compile('^Referring Organisation:  (.*)  Clinical').search(line):
                referring_gp_site_name=re.compile('^Referring Organisation:  (.*)  Clinical').search(line).group(1)
            lines.append(Line(referral_id,patient_id, patient_name,patient_date_of_birth,patient_sex,gp_suggested_priority,gp_suggested_specialty,referral_short_text,referral_date,referring_gp_site_name))


# In[5]:


df = pd.DataFrame(lines)
df.drop_duplicates(['referral_id'],keep='last')


# In[6]:


df.drop_duplicates(['referral_id'],keep='last').to_csv('Example_Clinical_Information_Summary.csv', index=False)

