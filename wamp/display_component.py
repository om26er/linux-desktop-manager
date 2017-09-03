import asyncio
import logging

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
        display = manager.DisplayManager('kde')
        await self.register(display.is_screen_locked, 'com.om26er.ldm.is_screen_locked')
        await self.register(display.lock_screen, 'com.om26er.ldm.lock_screen')
        LOGGER.info('Registered all procedures, ready to go.')

    def onDisconnect(self):
        LOGGER.info('Session disconnected.')
        asyncio.get_event_loop().stop()


def main():
    runner = ApplicationRunner(url=u'ws://www.om26er.com/ws', realm=u'ldm')
    runner.run(DisplayController)


if __name__ == '__main__':
    main()
