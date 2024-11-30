from sqlite_db import SQLiteDB
import logging

class PropertiesDB(SQLiteDB): 
    def __init__(self, db_name):
        super().__init__(db_name)

    def create_table(self):
        self.execute_query('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY,
            address TEXT,
            price TEXT,
            description TEXT,
            num_beds INTEGER,
            num_living_rooms INTEGER,
            num_baths INTEGER,
            image TEXT,
            let_agreed BOOLEAN,
            link TEXT
        )
        ''')

    # Function to check for duplicates
    def has_duplicate_address(self, address):
        result = self.fetch_one("SELECT 1 FROM properties WHERE address = ?", (address,))
        if result:
            logging.info(f"Property with address '{address}' already exists. Skipping.")
            return True
        return False

    def add_property(self, property):
        self.execute_query('''
        INSERT INTO properties (address, price, description, num_beds, num_living_rooms, num_baths, image, let_agreed, link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (property.address, property.price, property.description, property.num_beds, property.num_living_rooms, property.num_baths, property.image, property.let_agreed, property.link))