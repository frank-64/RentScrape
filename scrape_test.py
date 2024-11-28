import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from Property import Property
from properties_db import PropertiesDB
import requests
import sqlite3

# Import the functions to test
from scrape import (
    get_text, 
    get_last_word, 
    extract_property_details_from_div, 
    scrape
)

# Mock HTML sample for testing
SAMPLE_HTML = """
<div class="propertyListing">
    <div class="p_address">123 Test Street, London</div>
    <div class="p_price">£1,500 pcm</div>
    <div class="p_description">Lovely 2 bedroom flat</div>
    <div class="num_bed">2 Beds</div>
    <div class="num_rec">1 Living Room</div>
    <div class="num_bath">1 Bath</div>
    <div class="mainImg"><img src="http://example.com/property.jpg"/></div>
</div>
"""

def test_get_text():
    """Test the get_text helper function."""
    soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
    div = soup.find('div', class_='propertyListing')
    
    # Test existing class
    assert get_text(div, 'p_address') == '123 Test Street, London'
    
    # Test non-existent class
    assert get_text(div, 'non_existent') is None

def test_get_last_word():
    """Test the get_last_word helper function."""
    soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
    div = soup.find('div', class_='propertyListing')
    
    # Test existing class
    assert get_last_word(div, 'num_bed') == 'Beds'
    assert get_last_word(div, 'num_rec') == 'Room'
    
    # Test non-existent class
    assert get_last_word(div, 'non_existent') is None

def test_extract_property_details():
    """Test extracting property details from a div."""
    soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
    div = soup.find('div', class_='propertyListing')
    
    property = extract_property_details_from_div(div)
    
    assert isinstance(property, Property)
    assert property.address == '123 Test Street, London'
    assert property.price == '£1,500 pcm'
    assert property.description == 'Lovely 2 bedroom flat'
    assert property.num_beds == 'Beds'
    assert property.num_living_rooms == 'Room'
    assert property.num_baths == 'Bath'
    assert property.image == 'http://example.com/property.jpg'
    assert property.let_agreed == False

@pytest.fixture
def mock_send_email():
    """Fixture to mock the send_email function."""
    return MagicMock()

@pytest.fixture
def mock_requests():
    """Fixture to mock the mock_requests function."""
    return MagicMock()

@pytest.mark.asyncio
async def test_scrape_function(mock_send_email, mock_requests):
    """Test the main scrape function."""

    # Patch external dependencies
    with (
        patch('requests.get') as mock_requests,
        patch('emails.send_property_email_update') as mock_send_email
    ):
        # Mock requests.get response
        mock_response = MagicMock()
        mock_response.content = SAMPLE_HTML.encode('utf-8')
        mock_requests.return_value = mock_response

        # Mock send_email function
        mock_send_email.return_value = None

        # Use the in-memory database
        db_name = 'properties_test.db'
        with PropertiesDB(db_name) as db:
            db.create_table()

        # Run the function you are testing
        scrape(db_name)

        # Verify interactions
        # mock_requests.assert_called_once_with('https://www.hackney-leigh.co.uk/properties-to-let/orderby-lp/')
        # mock_send_email.assert_called_once()

def test_property_with_let_agreed():
    """Test handling of a property marked as let agreed."""
    html_with_let_agreed = """
    <div class="propertyListing">
        <div class="p_address">456 Sold Street, London</div>
        <div class="p_price">£2,000 pcm</div>
        <div class="let_agreed"></div>
    </div>
    """
    soup = BeautifulSoup(html_with_let_agreed, 'html.parser')
    div = soup.find('div', class_='propertyListing')
    
    property = extract_property_details_from_div(div)
    
    assert property.let_agreed == True
    assert property.address == '456 Sold Street, London'

# Additional edge case tests can be added here
def test_property_without_image():
    """Test extracting property details when no image is present."""
    html_without_image = """
    <div class="propertyListing">
        <div class="p_address">789 No Image Street, London</div>
        <div class="p_price">£1,800 pcm</div>
    </div>
    """
    soup = BeautifulSoup(html_without_image, 'html.parser')
    div = soup.find('div', class_='propertyListing')
    
    property = extract_property_details_from_div(div)
    
    assert property.image is None