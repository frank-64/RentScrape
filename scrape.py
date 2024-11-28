import requests
from bs4 import BeautifulSoup
from Property import Property
from properties_db import PropertiesDB
from emails import send_property_email_update
import asyncio

def get_text(div, class_name):
    """Helper function to extract text from a div with a specific class, or return None if not found."""
    return div.find('div', class_=class_name).text.strip() if div.find('div', class_=class_name) else None

def get_last_word(div, class_name):
    """Helper function to extract the last word from a div's text (e.g., number of rooms)."""
    text = get_text(div, class_name)
    return text.split()[-1] if text else None

def extract_property_details_from_div(div):
    # Extract details using helper functions
    address = get_text(div, 'p_address') 
    price = get_text(div, 'p_price')
    description = get_text(div, 'p_description')
    num_beds = get_last_word(div, 'num_bed')
    num_living_rooms = get_last_word(div, 'num_rec')
    num_baths = get_last_word(div, 'num_bath')
    link = div.find('a')['href']

    # Get the image URL
    img_tag = div.find('div', class_='mainImg').find('img') if div.find('div', class_='mainImg') else None
    img_url = img_tag['src'] if img_tag else None
    
    # Check for 'let agreed' status
    let_agreed = bool(div.find('div', class_='let_agreed'))

    return Property(price, address, description, img_url, let_agreed, num_beds, num_baths, num_living_rooms, link)

## Pull properties from site
async def scrape(db_name='properties.db'):
    # Initiate Properties DB
    with PropertiesDB(db_name) as db:
        db.create_table()

        url = 'https://www.hackney-leigh.co.uk/properties-to-let/orderby-lp/'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        property_listings_divs = soup.find_all('div', class_='propertyListing')

        for div in property_listings_divs:
            property = extract_property_details_from_div(div)

            if db.has_duplicate_address(property.address):
                continue
            db.add_property(property)

            # if(not property.let_agreed):
            #     await send_property_email_update(property)

            print(f"New property with address: {property.address} added.")

