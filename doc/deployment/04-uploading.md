Client Deployment Preparation
========================
The second and last step in building a distributable Toontown Journey client is preparing the distribution and all of its files. There are three steps to doing this:

* [Patching the client](02-patching.md)
* [Writing the distribution files](03-writing.md)
* **Uploading the distribution with FTP**

This document outlines how to accomplish the third task.

- - -

Uploading the client is quite simple with the deployment utility. It will use the built-in Python ftplib module to upload all distribution files to the Toontown Journey download server. deploy.json contains all of the FTP credentials and download server information.

# Usage
There is no usage to uploading the distribution files. deploy.py will upload the files for you.
