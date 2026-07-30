import sys
import os

# This line automatically configures the satellite_game folder path
sys.path.append(os.path.join(os.path.dirname(__file__), 'satellite_game'))

from satellite_game import main

if __name__ == "__main__":
    main.play_orbital_command()
