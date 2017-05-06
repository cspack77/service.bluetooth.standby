# -*- coding: utf-8 -*-

import os
import xbmc
import xbmcaddon
import dbus

selfAddon = xbmcaddon.Addon()
addon_id = selfAddon.getAddonInfo('id')
addon_name = selfAddon.getAddonInfo('name')

def kodi_log(message, level=xbmc.LOGDEBUG):
    xbmc.log(addon_name + ' -> ' + str(message), level)

def get_settings():
    global timeout
    global device_name
    global device_path
    timeout = int(selfAddon.getSetting('standby_timeout'))
    device_name = selfAddon.getSetting('device_name')
    device_path = selfAddon.getSetting('device_path')

def is_device_connected(device_path):
    props = dbus.Interface(bus.get_object('org.bluez', device_path), 
                            'org.freedesktop.DBus.Properties')
    if props.Get('org.bluez.Device1', 'Connected'):
        device_connected = True
    else:
        device_connected = False
    return device_connected

def disconnect_device(device_path):
    if is_device_connected(device_path):
        device = dbus.Interface(bus.get_object('org.bluez', device_path), 
                                                'org.bluez.Device1')
        device.Disconnect()
        kodi_log('Device: ' + device_path + ' disconnected')
    else:
        kodi_log('Timeout reached, device ' + device_path + ' already disconnected')

class XbmcMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onSettingsChanged(self):
        get_settings()
        kodi_log('Settings changed: Timeout: ' + str(timeout) + ' Device: ' + device_name)

if __name__ == '__main__':

    get_settings()

    kodi_log('Service started. Device = [' + device_path + '] Standby timeout = ' + str(timeout) + ' minutes.', level=xbmc.LOGNOTICE)

    bus = dbus.SystemBus()

    monitor = XbmcMonitor()

    while not monitor.abortRequested():

        if monitor.waitForAbort(60):
            break

        idle_time = xbmc.getGlobalIdleTime()
        idle_time_in_minutes = int(idle_time)/60

        kodi_log('Idle time: ' + str(idle_time) + ' Idle time (minutes): ' + str(idle_time_in_minutes) + ' Timeout: ' + str(timeout))

        if idle_time_in_minutes >= timeout:
            kodi_log("Timeout reached, disconnecting device")
            if not device_path == None:
                disconnect_device(device_path)

    kodi_log('Service stopped.', level=xbmc.LOGNOTICE)
