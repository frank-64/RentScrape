import requests
import sqlite3
from bs4 import BeautifulSoup
from Property import Property

def scrape():
    # Set up the SQLite database
    conn = sqlite3.connect('properties.db')
    cursor = conn.cursor()

    # Create a table to store the properties if it doesn't already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY,
        address TEXT,
        price TEXT,
        description TEXT,
        num_beds INTEGER,
        num_living_rooms INTEGER,
        num_baths INTEGER,
        image TEXT,
        let_agreed BOOLEAN
    )
    ''')

    url = 'https://www.hackney-leigh.co.uk/properties-to-let/orderby-lp/'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    property_listings_divs = soup.find_all('div', class_='propertyListing')

    for div in property_listings_divs:
        # Find the address
        address = div.find('div', class_='p_address').text.strip() if div.find('div', class_='p_address') else None

        cursor.execute("SELECT 1 FROM properties WHERE address = ?", (address,))
        if cursor.fetchone():
            print(f"Property with address '{address}' already exists. Skipping.")
            continue  # Skip this property if address exists in the database
        
        # Find the price
        price = div.find('div', class_='p_price').text.strip() if div.find('div', class_='p_price') else None
        
        # Find the description
        description = div.find('div', class_='p_description').text.strip() if div.find('div', class_='p_description') else None

        # Get num of beds, baths and living rooms: e.g. of string is ' 2' hence splice
        num_beds = div.find('div', class_='num_bed').text.strip().split()[-1] if div.find('div', class_='num_bed') else None
        num_living_rooms = div.find('div', class_='num_rec').text.strip().split()[-1] if div.find('div', class_='num_rec') else None
        num_baths = div.find('div', class_='num_bath').text.strip().split()[-1] if div.find('div', class_='num_bath') else None

        # Get the image div
        main_img_div = div.find('div', class_='mainImg')

        img_tag = main_img_div.find('img')  # Find the <img> tag inside the div
        # Get the image URL
        img_url = img_tag['src'] if img_tag else None 

        let_agreed = bool(div.find('div', class_='let_agreed'))

        cursor.execute('''
        INSERT INTO properties (address, price, description, num_beds, num_living_rooms, num_baths, image, let_agreed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (address, price, description, num_beds, num_living_rooms, num_baths, img_url, let_agreed))

        print(f"New property with address: {address} added.")

    conn.commit()
    conn.close()