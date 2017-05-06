# service.bluetooth.standby
This Kodi service addon will disconnect specific bluetooth devices after a user-configurable timeout value.

# Supported platforms
Tested on LibreELEC and Arch Linux, should work on any Linux system with dbus/bluez5

# Purpose
I created this addon to save battery life on my PS3 Bluetooth remote. It will stay connected indefinitely otherwise and quickly drain the batteries.  Currently LibreELEC/OpenELEC has a method to disconnect standby-enabled bluetooth devices, but only when the Kodi screensaver is activated, therefore as long as any media file or stream is playing, devices will remain connected. With this addon, devices will disconnect after a specified timeout value (between 1 and 60 minutes).
