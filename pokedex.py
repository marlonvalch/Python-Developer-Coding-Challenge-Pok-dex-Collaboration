"""
pokedex.py - Main CLI logic for Mini Pokedex

Contains the PokedexCLI class with  OOP structure for API, DB, and Webex integration:
"""
import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from webexteamssdk import WebexTeamsAPI

# This function load_dotenv() will Load environment variables :
load_dotenv()

#Make sure to Expand the regions ">" " to check the code of each class/section:

#region  API ===============================================================
class PokeAPI:
    """Handles interaction with the PokeAPI."""
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
    TYPE_URL = "https://pokeapi.co/api/v2/type/"

    def get_pokemon(self, query):
        """Fetches Pokémon data by name or ID."""
        try:
            resp = requests.get(f"{self.BASE_URL}{query.lower()}")
            resp.raise_for_status()  # Raise an error for bad http responses
            return resp.json()
        except Exception as e:
            raise Exception(f"PokeAPI error: {e}")

    def get_pokemon_by_type(self, type_name):
        """Fetches all Pokémon of a given type."""
        try:
            resp = requests.get(f"{self.TYPE_URL}{type_name.lower()}")
            resp.raise_for_status()
            return resp.json()['pokemon']
        except Exception as e:
            raise Exception(f"PokeAPI error: {e}")
#endregion

#region  DB  ===============================================================
class MongoDB:
    """Handles MongoDB dynamic connection and operations using the .env file for the credentials and connection string """
    def __init__(self):
        hosts = os.getenv('MONGO_HOSTS').split(',')
        username = os.getenv('MONGO_USERNAME')
        password = os.getenv('MONGO_PASSWORD')
        port = os.getenv('MONGO_PORT')
        dbname = os.getenv('MONGO_DATABASE')
        uri = f"mongodb://{username}:{password}@{','.join([f'{h}:{port}' for h in hosts])}/{dbname}?authSource=admin"
        self.client = MongoClient(uri)
        self.db = self.client[dbname]
        self.col = self.db['searches']

    def save_search(self, query, data):
        """Stores a search result in MongoDB."""
        try:
            self.col.insert_one({
                'timestamp': datetime,
                'query': query,
                'data': data
            })
        except Exception as e:
            raise Exception(f"MongoDB error: {e}")

    def get_last_five_searches(self):
        """Retrieves last 5 unique search queries."""
        try:
            pipeline = [
                {"$sort": {"timestamp": -1}},
                {"$group": {"_id": "$query", "doc": {"$first": "$$ROOT"}}},
                {"$limit": 5}
            ]
            return [doc['doc'] for doc in self.col.aggregate(pipeline)]
        except Exception as e:
            raise Exception(f"MongoDB error: {e}")
#endregion

#region  WEBEX ===============================================================
class WebexBot:
    """Handles Webex room creation and notifications."""
    def __init__(self):
        token = os.getenv('WEBEX_BOT_TOKEN')
        self.api = WebexTeamsAPI(access_token=token)
        self.room = None
        self.user_ids = [
            'marintor', 'luisrher', 'rafvega', 'cadiazar', 'lreyescr'
        ]
        self.setup_room()

    def setup_room(self):
        """Creates a Webex room and adds users."""
        try:
            self.room = self.api.rooms.create('Mini Pokedex CLI Room')
            for uid in self.user_ids:
                self.api.memberships.create(self.room.id, personEmail=f"{uid}@cisco.com")
        except Exception as e:
            print(f"Webex room setup error: {e}")

    def send_card(self, pokemon):
        """Sends a Webex card with Pokémon image and stats."""
        try:
            card = {
                "type": "AdaptiveCard",
                "version": "1.0",
                "body": [
                    {"type": "TextBlock", "text": f"{pokemon['name'].title()} Stats", "weight": "Bolder", "size": "Medium"},
                    {"type": "Image", "url": pokemon['sprites']['front_default'], "size": "Medium"},
                    {"type": "FactSet", "facts": [
                        {"title": "Type(s)", "value": ', '.join([t['type']['name'] for t in pokemon['types']])},
                        {"title": "Abilities", "value": ', '.join([a['ability']['name'] for a in pokemon['abilities']])},
                        {"title": "Base Stats", "value": ', '.join([f"{s['stat']['name']}: {s['base_stat']}" for s in pokemon['stats']])}
                    ]}
                ]
            }
            self.api.messages.create(roomId=self.room.id, text="Pokémon Search Result", attachments=[{"contentType": "application/vnd.microsoft.card.adaptive", "content": card}])
        except Exception as e:
            print(f"Webex card error: {e}")
#endregion

#region  CLI MENU ===============================================================
class PokedexCLI:
    """Main CLI class for user interaction."""
    def __init__(self):
        self.api = PokeAPI()
        self.db = MongoDB()
        self.webex = WebexBot()

    def run(self):
        """Runs the CLI menu loop."""
        while True:
            print("\nMini Pokedex CLI")
            print("1. Search pokemon by name.")
            print("2. Search pokemon by ID.")
            print("3. Retrieve last five searchs.")
            print("4. Exit")
            choice = input("Enter an option: ").strip()
            try:
                if choice == '1':
                    name = input("Enter Pokémon name: ").strip()
                    self.search_pokemon(name)
                elif choice == '2':
                    pid = input("Enter Pokémon ID: ").strip()
                    self.search_pokemon(pid)
                elif choice == '3':
                    self.show_last_searches()
                elif choice == '4':
                    print("Exiting...")
                    sys.exit(0)
                else:
                    print("Invalid option. Try again.")
            except Exception as e:
                print(f"Error: {e}")

    def search_pokemon(self, query):
        """Searches for a Pokémon and displays details."""
        try:
            pokemon = self.api.get_pokemon(query)
            self.webex.send_card(pokemon) #This method sends the card to the webexroom created
            self.db.save_search(query, pokemon)
            print(f"\nName: {pokemon['name'].title()}")
            print(f"Type(s): {', '.join([t['type']['name'] for t in pokemon['types']])}")
            print(f"Abilities: {', '.join([a['ability']['name'] for a in pokemon['abilities']])}")
            print("Base Stats:")
            for stat in pokemon['stats']:
                print(f"  {stat['stat']['name']}: {stat['base_stat']}")
        except Exception as e:
            print(f"Search error: {e}")

    def show_last_searches(self):
        """Displays last 5 unique search queries."""
        try:
            searches = self.db.get_last_five_searches()
            print("\nLast 5 unique searches:")
            for s in searches:
                print(f"- {s['query']} at {s['timestamp']}")
        except Exception as e:
            print(f"MongoDB error: {e}")

    def list_pokemon_by_type(self, type_name):
        """Lists all Pokémon of a given type."""
        try:
            pokemons = self.api.get_pokemon_by_type(type_name)
            print(f"\nPokémon of type {type_name}:")
            # Complex list comprehension: get all names
            names = [p['pokemon']['name'] for p in pokemons]
            for name in names:
                print(f"- {name}")
        except Exception as e:
            print(f"Type search error: {e}")
#endregion