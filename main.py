"""
main.py - Mini Pokedex CLI

.
"""
import os
import sys
from dotenv import load_dotenv
from pokedex import PokedexCLI

load_dotenv()

def main():
    """Initializes and runs the Mini Pokedex CLI application."""
    cli = PokedexCLI()
    cli.run()
    
    """Runs the main function if this script is executed directly."""
if __name__ == "__main__":
    main()
