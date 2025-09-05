import unittest
from unittest.mock import patch, MagicMock
from pokedex import PokeAPI, MongoDB, PokedexCLI

class TestPokeAPI(unittest.TestCase):
    """This is a Unit test for PokeAPI class."""

    @patch('pokedex.requests.get')
    def test_get_pokemon_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {'name': 'pikachu'}
        mock_get.return_value = mock_resp

        api = PokeAPI()
        result = api.get_pokemon('pikachu')
        self.assertEqual(result['name'], 'pikachu')

    @patch('pokedex.requests.get')
    def test_get_pokemon_by_type_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {'pokemon': [{'pokemon': {'name': 'pikachu'}}]}
        mock_get.return_value = mock_resp

        api = PokeAPI()
        result = api.get_pokemon_by_type('electric')
        self.assertEqual(result[0]['pokemon']['name'], 'pikachu')

class TestMongoDB(unittest.TestCase):
    """Unit tests for MongoDB class."""

    @patch('pokedex.MongoClient')
    def test_save_search(self, mock_client):
        db = MongoDB()
        db.col = MagicMock()
        db.save_search('pikachu', {'name': 'pikachu'})
        db.col.insert_one.assert_called_once()

    @patch('pokedex.MongoClient')
    def test_get_last_five_searches(self, mock_client):
        db = MongoDB()
        db.col = MagicMock()
        db.col.aggregate.return_value = [{'doc': {'query': 'pikachu', 'timestamp': 'now'}}]
        result = db.get_last_five_searches()
        self.assertEqual(result[0]['query'], 'pikachu')

class TestPokedexCLI(unittest.TestCase):
    """Unit tests for PokedexCLI class."""

    @patch('pokedex.PokeAPI')
    @patch('pokedex.MongoDB')
    @patch('pokedex.WebexBot')
    def test_search_pokemon(self, mock_webex, mock_mongo, mock_api):
        cli = PokedexCLI()
        cli.api.get_pokemon.return_value = {
            'name': 'pikachu',
            'types': [{'type': {'name': 'electric'}}],
            'abilities': [{'ability': {'name': 'static'}}],
            'stats': [{'stat': {'name': 'speed'}, 'base_stat': 90}],
            'sprites': {'front_default': 'http://img'}
        }
        cli.webex.send_card = MagicMock()
        cli.db.save_search = MagicMock() 
        with patch('builtins.print') as mock_print:
            cli.search_pokemon('pikachu')
            mock_print.assert_any_call("\nName: Pikachu")
            mock_print.assert_any_call("Type(s): electric")
            mock_print.assert_any_call("Abilities: static")
            mock_print.assert_any_call("Base Stats:")

    @patch('pokedex.PokeAPI')
    @patch('pokedex.MongoDB')
    @patch('pokedex.WebexBot')
    def test_show_last_searches(self, mock_webex, mock_mongo, mock_api):
        cli = PokedexCLI()
        cli.db.get_last_five_searches = MagicMock(return_value=[
            {'query': 'pikachu', 'timestamp': 'now'},
            {'query': 'bulbasaur', 'timestamp': 'now'}
        ])
        with patch('builtins.print') as mock_print:
            cli.show_last_searches()
            mock_print.assert_any_call("\nLast 5 unique searches:")
            mock_print.assert_any_call("- pikachu at now")
            mock_print.assert_any_call("- bulbasaur at now")

if __name__ == '__main__':
    unittest.main()