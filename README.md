Toontown Journey
================
Toontown Journey is a private server to revive Disney's Toontown Online.

### The Rules

Below are the rules for contributing to this project.

1. When we are out of open beta always merge pull requests into the dev branch. A week before our scheduled release we test the dev branch and make sure its functional then merge it into master.

###Database

The local database is for development servers. No admin access given by default.

The development database is also for development servers, but everyone is given admin access.

The MySQL database is for production servers. It uses the login server's MySQL to use base64 to hash passwords in order to secure user information. The ClientServicesManager uberdog will authenticate users through the login server's MySQL.

The remote database is unused, it may be used later for remote developer access to the public gameserver.
