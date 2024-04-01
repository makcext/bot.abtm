import random

# mock_country_api.py
async def get_countries():
    # Mock API call to get a list of countries
    return ['USA', 'Canada', 'Mexico', 'UK', 'Germany', 'France']

async def get_services():
    # Mock API call to get a list of services
    return ['Adobe', 'Amazon', 'Apple', 'Google', 'Microsoft', 'Netflix']

async def get_numbers(country: str, service: str):
    # Mock API call to get a list of available numbers country: str, service: str
    return ['+1234567890', '+2345678901', '+3456789012', '+4567890123', '+5678901234']

async def generate_mock_data():
    countries = ['USA', 'Canada', 'Mexico', 'UK', 'Germany']
    services = ['Adobe', 'Amazon', 'Apple', 'Google', 'Microsoft']
    numbers = []

    for _ in range(100):  # Change the range to 100 to generate 100 numbers
        country = random.choice(countries)
        service = random.choice(services)
        number = f"+{random.randint(1000000000, 9999999999)}"
        numbers.append((country, service, number))
        

    return numbers


    
