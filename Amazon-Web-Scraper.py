#!/usr/bin/env python
# coding: utf-8

# In[188]:


#####AMAZON WEB SCRAPER####

import requests
import csv
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import datetime
import smtplib  # Library for sending email to the users.


# Setting up the URL.
def our_url(search_term, page):
    search_term = search_term.replace(' ', '+')
    template = f'https://www.amazon.com/s?k={search_term}&crid=BO6C6THEGQES&page={page}'
    return template


# Function to extract a record from the website.
def extract_record(item):
    atag = item.h2.a
    description = atag.text
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text

    except AttributeError:
        return

    try:
        rating = item.i.text
        comment_count = item.find('span', {'class': 'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = 'N/A'
        comment_count = 'N/A'

    result = (description, price, rating, comment_count, url)

    return result


# The main function.        
def main(search_term):
    driver = webdriver.Chrome()
    records = []

    # For navigating through the 20 webpages of Amazon website.
    for p in range(1, 21):

        driver.get(our_url(search_term, p))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        all_records = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in all_records:

            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    # Saving data to a file

    with open('Amazon.csv', 'w', newline='', encoding='utf-8') as f:

        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Comment-Count', 'URL'])
        writer.writerows(records)


# USER has to make a call to the main function with their search result as an argument
# For example: main('Laptops for data analysts')
# USER can use any search string according to their own search use.


# In[189]:


main('laptops dell')

# In[ ]:
