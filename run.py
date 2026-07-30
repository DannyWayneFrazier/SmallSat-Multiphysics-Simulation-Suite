import sys
import os

# This line fixes the folder path issue automatically
sys.path.append(os.path.join(os.path.dirname(__file__), 'satellite_game'))

from satellite_game import main

if __name__ == "__main__":
    main.play_orbital_command()
