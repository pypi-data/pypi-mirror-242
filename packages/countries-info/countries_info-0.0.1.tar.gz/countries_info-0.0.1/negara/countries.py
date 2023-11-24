import requests

class restcountries:
    base_url = "https://restcountries.com/v3.1"

    def __init__(self):
        pass

    def get_country_info(self, country_code):
        endpoint = f"/alpha/{country_code.lower()}"
        response = requests.get(f"{self.base_url}{endpoint}")
        
        if response.status_code == 200:
            country_info = response.json()
            return country_info
        else:
            return {"error": "Failed to retrieve country information."}
