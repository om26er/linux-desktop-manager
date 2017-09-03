import asyncio
import logging
import os

from autobahn.wamp.types import RegisterOptions
from autobahn.asyncio.wamp import (
    ApplicationSession,
    ApplicationRunner,
)

from ldm import manager

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class DisplayController(ApplicationSession):
    async def onJoin(self, details):
        LOGGER.info('Joined realm \'{}\'.'.format(details.realm))
        display = manager.Display(os.environ.get('XDG_CURRENT_DESKTOP', 'KDE').lower())
        machine_id = await display.get_machine_id()
        options = RegisterOptions(match='exact', invoke='roundrobin')
        await self.register(display.is_locked,
                            'com.om26er.ldm.machine-{}.is_screen_locked'.format(machine_id),
                            options)
        await self.register(display.lock,
                            'com.om26er.ldm.machine-{}.lock_screen'.format(machine_id),
                            options)
        LOGGER.info('Registered all procedures, ready to go.')
        LOGGER.info('Machine ID: {}'.format(machine_id))

    def onDisconnect(self):
        LOGGER.info('Session disconnected.')
        asyncio.get_event_loop().stop()


def main():
    runner = ApplicationRunner(url=u'ws://ldm.om26er.com/ws', realm=u'ldm')
    runner.run(DisplayController)


if __name__ == '__main__':
    main()
