# service.bluetooth.standby
This Kodi service addon will disconnect specific bluetooth devices after a user-configurable timeout value.

# Supported platforms
LibreELEC
OpenELEC

# Purpose
Currently LibreELEC/OpenELEC will disconnect standby-enabled bluetooth devices only when the Kodi screensaver is activated, therefore as long as any media file or stream is playing, devices will remain connected. This can lead to quick battery drain.  With this addon, devices will disconnect after a specified timeout value (between 1 and 60 minutes).
