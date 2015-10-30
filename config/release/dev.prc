# Distribution:
distribution dev

# Art assets:
model-path resources

# Server:
server-version TTJ-1.0
min-access-level 100
want-mega-invasions #t
shard-low-pop 50
shard-mid-pop 100

# RPC:
want-rpc-server #t
rpc-server-endpoint http://localhost:8080/

# DClass files (in reverse order):
dc-file astron/dclass/toon.dc
dc-file astron/dclass/otp.dc

# Core features:
want-pets #t
want-parties #t
want-gifting #t
want-game-tables #f
want-find-four #f
want-chinese-checkers #f
want-checkers #f
want-cogdominiums #t
want-mega-invasions #t
safe-harbours Toon Valley
# Chat:
want-whitelist #f

# Cashbot boss:
want-resistance-toonup #t
want-resistance-restock #t
want-resistance-dance #f

# Optional:
want-yin-yang #f

# Developer options:
show-population #t
force-skip-tutorial #t
want-instant-parties #t


estate-day-night #t

# Server Performance:
smooth-min-suggest-resync 1
smooth-enable-smoothing 1
smooth-enable-prediction 1
smooth-lag .1
smooth-prediction-lag 1
cog-thief-ortho 0

#database stuff
accountdb-type mysqldb
mysql-login toontown
mysql-password some_pass

