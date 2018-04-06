import dbus

DBUS_DATA = {
    'kde': {
        'service_name': 'org.kde.screensaver',
        'path': '/ScreenSaver',
        'interface': 'org.freedesktop.ScreenSaver',
        'methods': {
            'is_locked': 'GetActive',
            'lock': 'Lock'
        }
    },
    'unity': {
        'service_name': 'org.gnome.ScreenSaver',
        'path': '/com/canonical/Unity/Session',
        'interface': 'com.canonical.Unity.Session',
        'methods': {
            'is_locked': 'IsLocked',
            'lock': 'Lock'
        }
    },
    'gnome': {
        'service_name': 'org.gnome.ScreenSaver',
        'path': '/org/gnome/ScreenSaver',
        'interface': 'org.gnome.ScreenSaver',
        'methods': {
            'is_locked': 'GetActive',
            'lock': 'Lock'
        }
    }
}

DBUS_DATA.update({'ubuntu:gnome': DBUS_DATA['gnome']})
DBUS_DATA.update({'ubuntu:unity': DBUS_DATA['unity']})


class Display:
    def __init__(self, environment):
        if environment not in DBUS_DATA.keys():
            raise RuntimeError('Supported environments: {}'.format(', '.join(DBUS_DATA.keys())))
        bus = dbus.SessionBus()
        self.screen_saver = bus.get_object(DBUS_DATA[environment]['service_name'],
                                           DBUS_DATA[environment]['path'])
        self.iface = dbus.Interface(self.screen_saver, DBUS_DATA[environment]['interface'])
        self.environment = environment

    async def is_locked(self):
        return getattr(self.iface, DBUS_DATA[self.environment]['methods']['is_locked'])()

    async def lock(self):
        if not await self.is_locked():
            getattr(self.iface, DBUS_DATA[self.environment]['methods']['lock'])()
        return await self.is_locked()
