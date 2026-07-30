import sys
import os

# This tells Python to look inside the satellite_game folder for files
sys.path.append(os.path.join(os.path.dirname(__file__), 'satellite_game'))

from satellite_game import main

if __name__ == "__main__":
    main.main() # This calls the main function inside your main.py
