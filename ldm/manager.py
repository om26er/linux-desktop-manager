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
        'path': '/ScreenSaver',
        'interface': 'org.gnome.ScreenSaver',
        'methods': {
            'is_locked': 'GetActive',
            'lock': 'Lock'
        }
    }
}


class DisplayManager:
    def __init__(self, environment='kde'):
        if environment not in DBUS_DATA.keys():
            raise RuntimeError('Supported environments: {}'.format(', '.join(DBUS_DATA.keys())))
        bus = dbus.SessionBus()
        screen_saver = bus.get_object(DBUS_DATA[environment]['service_name'], DBUS_DATA[environment]['path'])
        self.iface = dbus.Interface(screen_saver, DBUS_DATA[environment]['interface'])
        self.environment = environment

    def is_screen_locked(self):
        return getattr(self.iface, DBUS_DATA[self.environment]['methods']['is_locked'])()

    def lock_screen(self):
        if not self.is_screen_locked():
            getattr(self.iface, DBUS_DATA[self.environment]['methods']['lock'])()
        return self.is_screen_locked()
