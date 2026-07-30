import sys
import os

# Tells Python to look inside your 'satelite game' folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'satelite game'))

# Imports the main loop from that folder and runs it
from main import play_orbital_command

if __name__ == "__main__":
    play_orbital_command()
