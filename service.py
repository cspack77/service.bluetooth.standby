# -*- coding: utf-8 -*-

import os
import xbmc
import xbmcaddon
import dbus
from xml.dom import minidom

selfAddon = xbmcaddon.Addon()
addon_id = selfAddon.getAddonInfo('id')
addon_name = selfAddon.getAddonInfo('name')
libreelec_config_file = '/storage/.kodi/userdata/addon_data/service.libreelec.settings/oe_settings.xml'

def kodi_log(message, level=xbmc.LOGDEBUG):
    xbmc.log(addon_name + ' -> ' + str(message), level)

def get_settings():
    global timeout
    global debug
    debug = selfAddon.getSetting('debug_mode')
    timeout = int(selfAddon.getSetting('standby_timeout'))

def get_standby_devices():
    if os.path.exists(libreelec_config_file):
        xml_conf = minidom.parse(libreelec_config_file)
        xml_bluetooth = xml_conf.getElementsByTagName('bluetooth')
        for xml_standby in xml_bluetooth:
            for xml_standby_devices in xml_standby.getElementsByTagName('standby'):
                standby_devices = xml_standby_devices.firstChild.nodeValue
        if debug == 'true':
            kodi_log('Standby devices: ' + standby_devices)
        return standby_devices

def is_device_connected(device_path):
    props = dbus.Interface(bus.get_object('org.bluez', device_path), 
                            'org.freedesktop.DBus.Properties')
    if props.Get('org.bluez.Device1', 'Connected'):
        device_connected = True
    else:
        device_connected = False
    return device_connected

def disconnect_device(device_path):
    device = dbus.Interface(bus.get_object('org.bluez', device_path), 
                                                'org.bluez.Device1')
    device.Disconnect()
    if debug == 'true':
        kodi_log('Device: ' + device_path + ' disconnected')

def disconnect_devices():
    if not standby_devices == None:
        devices = standby_devices.split(',')
        if len(devices) > 0:
            for device_path in devices:
                if is_device_connected(device_path):
                    disconnect_device(device_path)
                elif debug == 'true':
                    kodi_log('Timeout reached, device ' + device_path + ' already disconnected')

class XbmcMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onSettingsChanged(self):
        get_settings()
        if debug == 'true':
            kodi_log('Settings changed: Timeout: ' + str(timeout) + ' Debug: ' + debug)

if __name__ == '__main__':

    get_settings()

    kodi_log('Service started. Standby timeout = ' + str(timeout) + ' minutes.', level=xbmc.LOGNOTICE)

    monitor = XbmcMonitor()

    bus = dbus.SystemBus()

    standby_devices = get_standby_devices()

    while not monitor.abortRequested():

        if monitor.waitForAbort(60):
            break

        idle_time = xbmc.getGlobalIdleTime()
        idle_time_in_minutes = int(idle_time)/60

        if debug == 'true':
            kodi_log('Idle time: ' + str(idle_time) + ' Idle time (minutes): ' + str(idle_time_in_minutes) + ' Timeout: ' + str(timeout))

        if idle_time_in_minutes >= timeout:
            if debug == 'true':
                kodi_log("Timeout reached, disconnecting devices")
            disconnect_devices()

    kodi_log('Service stopped.', level=xbmc.LOGNOTICE)
