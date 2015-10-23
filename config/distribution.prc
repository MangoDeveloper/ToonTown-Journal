# Client
window-title Toontown Journey[Alpha]
server-version TTJ-version-1.0
audio-library-name p3fmod_audio
sync-video #f
want-dev #f
preload-avatars #t
want-keep-alive #f
texture-anisotropic-degree 16
smooth-lag 0.4
server-port 7198
# Display pipes
aux-display pandagl
aux-display p3tinydisplay
smooth-min-suggest-resync 15
texture-power-2 none
gl-check-errors #f
want-rpc-server #t
rpc-server-endpoint http://localhost:8080/
garbage-collect-states #f

# Resources
model-path /
model-cache-models #f
model-cache-textures #f
vfs-mount phase/phase_3.mf /
vfs-mount phase/phase_3.5.mf /
vfs-mount phase/phase_4.mf /
vfs-mount phase/phase_5.mf /
vfs-mount phase/phase_5.5.mf /
vfs-mount phase/phase_6.mf /
vfs-mount phase/phase_7.mf /
vfs-mount phase/phase_8.mf /
vfs-mount phase/phase_9.mf /
vfs-mount phase/phase_10.mf /
vfs-mount phase/phase_11.mf /
vfs-mount phase/phase_12.mf /
vfs-mount phase/phase_13.mf /
default-model-extension .bam

want-pets #t
want-news-tab #t
want-news-page #t
want-gardening #f
want-toontorial #t
want-gifting #f
want-new-toonhall #t
want-cheesy-expirations #f
want-old-fireworks #t
want-skip-button #f
estate-day-night #t
show-total-population #t
# Chat Settings
force-avatar-understandable #t
force-player-understandable #t

# Holidays/Event Manager
force-holiday-decorations 6
want-glove-colors #t
#accountdb-type mysqldb
mysql-login toontown
mysql-password some_pass
