# Mini Pokedex CLI Setup & Usage Instructions


## Environment Setup

1. **Install Python 3.11**
   - Download from [python.org](https://www.python.org/downloads/release/python-3110/)
   - Ensure `python3.11` is available in your PATH.
   - MAKE SURE TO DOWNLOAD THE file " Mini PokedexCL.rar " , uncompress it
   - MAKE SURE TO open the folder in Visual Studio Code 

2. **Install uv (Python package manager)**
   - Run: `pip install uv`

3. **Create and activate a virtual environment**
   - Run: `uv venv .venv`
   - Activate (Windows PowerShell): `./.venv/Scripts/Activate.ps1` or `.\.venv\Scripts\activate`

4. **Install dependencies**
   - Run: `uv pip install -r requirements.txt`

5. **Configure .env file**
   - Add your Webex bot token and verify MongoDB credentials in `.env`.

6. **limitations**
-  This app is ready for the mongoDB connection
- For the MongoDB connection  make sure to run the app inside the same VPN/VPC as the data bases, or ask the admin to open access (firewall + bindIp) for your machine.

- This app  will work with any MongoDB server (local, on-prem, or Atlas). However it is currently set to work on the specific on-prem hosts advised on 
the .env file with port 27017 


## Usage

Run the CLI:

```powershell
python main.py

or simply run the file main.py
```

## Features
- Search Pokémon by name or ID
- List Pokémon by type
- Stores searches in MongoDB
- Retrieves last 5 unique searches
- Sends Webex card notifications on successful search to the webex room 

## what is expected to see:

- CLI Menu :

Mini Pokedex CLI

1. Search pokemon by name
2. Search pokemon by ID
3. Retrieve last five searches
4. Exit

Enter Pokémon name: pikachu

Name: Pikachu
Type(s): electric
Abilities: static, lightning-rod
Base Stats:
  hp: 35
  attack: 55
  defense: 40
  special-attack: 50
  special-defense: 50
  speed: 90

(Webex notification sent!)

- On the webex room the  adaptive card will display as the following :

- please copy and paste the following payload sample on this link :
https://adaptivecards.io/designer/ to see the adaptive card view :

{
  "type": "AdaptiveCard",
  "version": "1.0",
  "body": [
    {
      "type": "TextBlock",
      "text": "Pikachu Stats",
      "weight": "Bolder",
      "size": "Medium"
    },
    {
      "type": "Image",
      "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
      "size": "Medium"
    },
    {
      "type": "FactSet",
      "facts": [
        {
          "title": "Type(s)",
          "value": "electric"
        },
        {
          "title": "Abilities",
          "value": "static, lightning-rod"
        },
        {
          "title": "Base Stats",
          "value": "hp: 35, attack: 55, defense: 40, special-attack: 50, special-defense: 50, speed: 90"
        }
      ]
    }
  ]
}

## (OPTIONAL) Unit test:

-There is a test_pokedex.py  Unit test created using "MagicMock" 
- how to run it :
   
   - Make sure the virtual enviroment is active , if not run:
              .\.venv\Scripts\activate
  -  python -m unittest test_pokedex.py

- Run the tests using unittest:

  python -m unittest test_pokedex.py

  or simply run the file test_pokedex.py on VS

You should see output indicating the results of your tests (e.g., OK if all pass)




## References
- [PokeAPI Docs](https://pokeapi.co/)
- [Webex API](https://developer.webex.com/docs/api/v1/messages/create-a-message)
- [Webex Cards](https://developer.webex.com/messaging/docs/buttons-and-cards)
- [Webex Python SDK](https://github.com/CiscoDevNet/webexteamssdk)
- [pymongo](https://pymongo.readthedocs.io/)
- [uv](https://docs.astral.sh/uv/)


