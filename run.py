import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'orbital_command'))

from orbital_command import main

if __name__ == "__main__":
    main.play_orbital_command()
