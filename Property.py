import uuid

class Property:
    def __init__(self, price, address, description, image, let_agreed, num_beds, num_baths, num_living_rooms, link):
        self.id = str(uuid.uuid4())  # Unique ID for each property
        self.price = price           # Price of the property
        self.address = address       # Address of the property
        self.description = description  # Description of the property
        self.num_beds = num_beds        # Number of bedrooms
        self.num_baths = num_baths      # Number of bathrooms
        self.num_living_rooms = num_living_rooms  # Number of living rooms
        self.image = image            # URL or path to the property's image
        self.let_agreed = let_agreed    # Rental status of the property
        self.link = link                # Link to the website listing

    def __str__(self):
        """
        Returns a formatted string representation of the property details.
        """
        let_agreed_status = 'Let Agreed' if self.let_agreed else 'Available'
        return (f'Property Details:\n'
                f'Price: {self.price}\n'
                f'Address: {self.address}\n'
                f'Description: {self.description}\n'
                f'Image: {self.image}\n'
                f'Number of Beds: {self.num_beds}\n'
                f'Number of Living Rooms: {self.num_living_rooms}\n'
                f'Number of Baths: {self.num_baths}\n'
                f'Status: {let_agreed_status}'
                f'Link: {self.link}')