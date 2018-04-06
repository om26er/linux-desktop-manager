import asyncio
import os

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import RegisterOptions
import dbus

from linux_desktop_manager.controller import manager

PROCEDURE_IS_LOCKED = 'com.om26er.ldm.machine-{}.is_screen_locked'
PROCEDURE_LOCK = 'com.om26er.ldm.machine-{}.lock_screen'


def get_machine_id():
    bus = dbus.SessionBus()
    obj = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
    iface = dbus.Interface(obj, 'org.freedesktop.DBus.Peer')
    return str(iface.get_dbus_method('GetMachineId')())


class ClientSession(ApplicationSession):

    def __init__(self, config=None):
        super().__init__(config)
        self.machine_id = get_machine_id()
        self.display = manager.Display(os.environ.get('XDG_CURRENT_DESKTOP', 'KDE').lower())
        self.register_options = RegisterOptions(match='exact', invoke='roundrobin')

    async def onJoin(self, details):
        self.log.info("Successfully joined session {}".format(details.session))

        self.register(self.display.is_locked, PROCEDURE_IS_LOCKED.format(self.machine_id), self.register_options)
        self.register(self.display.lock, PROCEDURE_LOCK.format(self.machine_id), self.register_options)

    def onLeave(self, details):
        self.log.info("session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("connection to router closed")
        asyncio.get_event_loop().stop()


def main():
    runner = ApplicationRunner(url="ws://localhost:8080/ws", realm="realm1")
    runner.run(ClientSession)


if __name__ == '__main__':
    main()
