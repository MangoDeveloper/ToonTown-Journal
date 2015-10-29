Client Build Preparation
========================
The first step in building a distributable Toontown Journey client is building ```GameData.pyd```. ```GameData.pyd``` is an encrypted blob of frozen Python code. It contains all of the code necessary to run the game. There are two steps to building this file:

* **Prepare for building**
* [Build the frozen Python module](01-building.md)

This document outlines how to accomplish the first task.

- - -

Preparing the client for building is quite simple when using the ```prepare_client.py``` utility. What it does is it creates a build directory with all of the necessary files for running a client. All server-specific files get removed. Next, it removes all ```__debug__``` blocks from the code, as they may pose a security risk, or be highly developer specific. After that, a file called ```game_data.py``` is generated. This file contains the PRC file data, (stripped) DC file, and time zone info. If a ```REVISION``` token was provided in the ```--server-ver``` option, it gets replaced in the PRC file data with the first 7 characters of the GitHub revision. Finally, if ```--build-mfs``` is provided, any phase files that were modified get compiled.

# Usage
There is no usage to preparing the client. deploy.py will prepare the client for you.
