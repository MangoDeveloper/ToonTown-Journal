Running the Client
========================
In order to play Toontown Journey, an executable named journey.exe must be used to run the game and read the frozen modules inside of GameData.pyd.

This document explains how running the client works.

- - -

Running the client is quite simple, all you have to do is run the executable. But how does running the client work? In reality, the journey.exe executable is just a simple Python module called journey.py compiled to an executable. The module will import GameData.pyd ONCE to load the frozen modules, and then import JourneyStart.py to start the Toontown Journey game.

# Usage
You simply run the journey.exe executable (on Windows).
