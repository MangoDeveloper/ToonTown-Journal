Building the Client
===================
The first step in building a distributable Toontown Journey client is building ```GameData.pyd```. ```GameData.pyd``` is a blob of frozen Python code. It contains all of the code necessary to run the game. There are two steps to building this file:

* [Prepare for building](00-preparing.md)
* **Build the frozen Python module**

This document outlines how to accomplish the second task.

- - -

After preparing the client using the ```prepare_client.py``` utility, the deployment utility is all set to build! It will simply use the ```build_client.py``` utility and create a frozen Python module named ```GameData.pyd``` with Microsoft Visual C++ 2010.

## Usage ##

There is no usage to building the client. deploy.py will build the client for you.
