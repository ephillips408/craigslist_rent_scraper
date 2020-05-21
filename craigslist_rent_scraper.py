from bs4 import BeautifulSoup
import requests
import pandas as pd

def simple_rent_scraper(craig_prefix):

    url = f'https://{craig_prefix}.craigslist.org/d/apts-housing-for-rent/search/apa'
    rental_dict = {}
    rental_num = 0

    while True:

        response = requests.get(url)
        rent_data = response.text
        rent_soup = BeautifulSoup(rent_data, 'html.parser')
        listings = rent_soup.find_all('p', {'class' : 'result-info'})

        for listing in listings:

            beds_tag = listing.find('span', {'class' : 'housing'}) # This contains both bedrooms and sqft.

            title = listing.find('a', {'class' : 'result-title hdrlnk'}).text

            neighborhood_tag = listing.find('span', {'class' : 'result-hood'})
            neighborhood = neighborhood_tag.text[2:-1] if neighborhood_tag else 'N/A'


            if beds_tag:
                bedrooms = int(beds_tag.text.strip().split()[0][0]) if beds_tag.text.strip().split()[0][1:3] == 'br' else 'N/A'
            else:
                bedrooms = 'N/A'

            price = int(listing.select_one('.result-meta .result-price').text[1:]) # Removes the dollar sign and changes type to int

            if beds_tag:
                if 'ft2' in listing.find('span', {'class' : 'housing'}).text.split()[0]:
                    sqft = int(listing.find('span', {'class' : 'housing'}).text.split()[0][0:-3]) # Removes the ft2

                elif len(listing.find('span', {'class' : 'housing'}).text.split()) > 2 and 'ft2' in listing.find('span', {'class' : 'housing'}).text.split()[2]:
                    sqft = int(listing.find('span', {'class' : 'housing'}).text.split()[2][0:-3]) # Removes the ft2
            else:
                sqft = 'N/A'

            posting_time = listing.find('time', {'class' : 'result-date'})['datetime']

            rental_num += 1
            rental_dict[rental_num] = [title, neighborhood, bedrooms, sqft, posting_time]
        # End of for loop
        url_tag = rent_soup.find('a', {'class' : 'button next'})['href']

        if url_tag:
            url = f'https://{craig_prefix}.craigslist.org/d/apts-housing-for-rent/search/apa' + url_tag
            print (url)
        else:
            break
        # End of while loop
    rentals_df = pd.DataFrame.from_dict(rental_dict,
                                    orient = 'index',
                                    columns = ['Title', 'Neighborhood', 'Bedrooms', 'Square Feet', 'Posting Time'])
    return rentals_df         
