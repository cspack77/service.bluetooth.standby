# service.bluetooth.standby
This Kodi service addon will disconnect a selected bluetooth device after a user-configurable time period (assuming no buttons are pressed during that period).

# Supported platforms
Tested on LibreELEC and Arch Linux, should work on any Linux system with dbus/bluez5

# Purpose
I created this addon to save battery life on my PS3 Bluetooth remote. It will stay connected indefinitely otherwise and quickly drain the batteries.  Currently LibreELEC/OpenELEC has a method to disconnect standby-enabled bluetooth devices, but only when the Kodi screensaver is activated, therefore as long as any media file or stream is playing, the device will remain connected. With this addon, the device will disconnect after a specified period of no buttons being pressed on the remote (between 1 and 60 minutes).
