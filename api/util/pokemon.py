import requests
import json

def poke_api(pokemon):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    if response.status_code == 200:
        data = response.json()
        types = [type_info['type']['name'] for type_info in data['types']]
        return types
    else:
        # Handle error if the Pokemon is not found or any other HTTP error occurs
        print(f"Error: {response.status_code}")
        return None