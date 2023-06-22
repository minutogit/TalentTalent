import sys
from subprocess import call

# Terminal command to start this setup.py: python setup.py
# This command builds the script using PyInstaller

# Define the path to your spec file
spec_file = 'talenttalent.app.spec'

if __name__ == '__main__':
    # If running 'python setup.py'
    if len(sys.argv) == 1:
        # Build the script with PyInstaller using the spec file
        call(['pyinstaller', spec_file])

    # Keep the window open until a key is pressed
    input("\nPress any key to continue...")
