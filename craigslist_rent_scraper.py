from bs4 import BeautifulSoup
import requests
import pandas as pd

craig_prefix = ''
url = f'https://{craig_prefix}.craigslist.org/d/apts-housing-for-rent/search/apa'

response = requests.get(url)
rent_data = response.text
rent_soup = BeautifulSoup(rent_data, 'html.parser')

listings = rent_soup.find_all('p', {'class' : 'result-info'})

for listing in listings:

    title = listing.find('a', {'class' : 'result-title hdrlnk'}).text

    neighborhood_tag = listing.find('span', {'class' : 'result-hood'})
    neighborhood = neighborhood_tag.text if neighborhood_tag else 'N/A'

    beds_tag = listing.find('span', {'class' : 'housing'})
    if beds_tag:
        bedrooms = int(beds_tag.text.strip().split()[0][0]) if beds_tag.text.strip().split()[0][1:3] == 'br' else 'N/A'
    else:
        bedrooms = 'N/A'

    price = float(listing.select_one('.result-meta .result-price').text[1:]) # Removes the dollar sign and changes type to int

    if beds_tag:
        if 'ft2' in listing.find('span', {'class' : 'housing'}).text.split()[0]:
            sqft = int(listing.find('span', {'class' : 'housing'}).text.split()[0][0:-3]) # Removes the ft2

        elif len(listing.find('span', {'class' : 'housing'}).text.split()) > 2 and 'ft2' in listing.find('span', {'class' : 'housing'}).text.split()[2]:
            sqft = int(listing.find('span', {'class' : 'housing'}).text.split()[2][0:-3]) # Removes the ft2
    else:
        sqft = 'N/A'

    posting_time = listing.find('time', {'class' : 'result-date'})['datetime']


    print (f'Description: {title} \nArea: {neighborhood} \nBedrooms: {bedrooms} \nPrice: {price} \nSquare Feet: {sqft} \nPosting Time: {posting_time}\n')
