Client Deployment Preparation
========================
The second and last step in building a distributable Toontown Journey client is preparing the distribution and all of its files. There are three steps to doing this:

* [Patching the client](02-patching.md)
* **Writing the distribution files**
* [Uploading the distribution with FTP](04-uploading.md)

This document outlines how to accomplish the second task.

- - -

Writing the distribution files is quite simple with the deployment utility. The file writing feature is not its own module; it is done inside of the deployment utility. It will compress all patched files and add them to the distribution directory.

# Usage
There is no usage to writing the distribution files. deploy.py will write the files for you.
