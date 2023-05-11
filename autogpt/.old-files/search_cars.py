# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import re
import json
import schedule
import time

# Define search parameters
make = 'Toyota'
model = 'Sienna'
trim = 'Platinum'
year = ['2022', '2023']
features = ['Digital Rearview mirror', '1500w inverter', 'Entertainment Package']

# Define function to scrape dealership websites
def scrape_dealership(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for listing in soup.find_all('div', class_='vehicle-card__content'):
        try:
            title = listing.find('h2', class_='vehicle-card__title').text.strip()
            price = listing.find('div', class_='vehicle-card__price').text.strip()
            details = listing.find('div', class_='vehicle-card__details').text.strip()

            if all(feature in details for feature in features) and make in title and model in title and trim in title and any(y in title for y in year):
                if 'MSRP' in price:
                    price = price.replace('MSRP', '').strip()
                    price = re.sub('[^0-9]', '', price)
                    if int(price) > 0:
                        results.append({'title': title, 'price': int(price), 'url': url})
        except:
            pass
    return results

# Define function to make HTTP requests to online marketplaces
def search_marketplace(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for listing in soup.find_all('div', class_='s-item__wrapper clearfix'):
        try:
            title = listing.find('h3', class_='s-item__title').text.strip()
            price = listing.find('span', class_='s-item__price').text.strip()
            if 'to' in price:
                price = price.split('to')[0].strip()
            price = re.sub('[^0-9]', '', price)
            if int(price) > 0:
                results.append({'title': title, 'price': int(price), 'url': url})
        except:
            pass
    return results

# Schedule the script to run every hour
def job():
    # Scrape dealership websites
    results = []
    results += scrape_dealership('https://www.toyota.com/sienna/features/platinum')
    results += scrape_dealership('https://www.toyotaofnaperville.com/new-vehicles/sienna/')
    results += scrape_dealership('https://www.toyotaoforlando.com/new-toyota-sienna.htm')

    # Search online marketplaces
    results += search_marketplace('https://www.ebay.com/sch/i.html?_from=R40&_nkw=2022+2023+toyota+sienna+platinum&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=2022+2023+toyota+sienna+platinum+inverter')
    results += search_marketplace('https://www.cars.com/for-sale/searchresults.action/?dealerType=all&')
    
    # Save results to a text file
    with open('search_results.txt', 'w') as f:
        f.write(json.dumps(results))

schedule.every(1).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
