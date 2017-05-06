# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import dbus

addon = xbmcaddon.Addon("service.bluetooth.standby")

bus = dbus.SystemBus()

manager = dbus.Interface(bus.get_object('org.bluez', '/'), 
    'org.freedesktop.DBus.ObjectManager')
objects = manager.GetManagedObjects()

device_list = []
for path, interfaces in objects.iteritems():
    if not "org.bluez.Device1" in interfaces.keys():
        continue
    device = { 
        "path" : str(path),
        "name" : str(interfaces["org.bluez.Device1"]["Name"]),
        "address" : str(interfaces["org.bluez.Device1"]["Address"]),
    }   
    device_list.append(device)

selection = []
for device in device_list:
    selection.append(device["name"] + " - " + device["address"])
 
dialog = xbmcgui.Dialog()
idx = dialog.select('Select Bluetooth Device', selection)
if idx > -1:
    device_name = device_list[idx]["name"]
    device_path = device_list[idx]["path"]
    addon.setSetting('device_path', device_path)
    addon.setSetting('device_name', device_name)
