import uuid

class Property:
    def __init__(self, price, address, description, image, let_agreed):
        self.id = str(uuid.uuid4())  # Unique ID for each property
        self.price = price           # Price of the property
        self.address = address       # Address of the property
        self.description = description  # Description of the property
        self.image = image           # Image URL of the property
        self.let_agreed = let_agreed   # Let Agreed status (True or False)

    def __str__(self):
        # Return a formatted string for property details
        let_agreed_status = 'Let Agreed' if self.let_agreed else 'Available'
        return (f'Property Details:\n'
                f'Price: {self.price}\n'
                f'Address: {self.address}\n'
                f'Description: {self.description}\n'
                f'Image: {self.image}\n'
                f'Status: {let_agreed_status}')
