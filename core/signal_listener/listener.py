import asyncio
import signal

from ..server import Server

class SignalListener:
    @staticmethod
    async def handle_signal(sig: signal.Signals):
        await Server.server.shutdown()

    async def register_signal_handler(self, *signals: signal.Signals):
        loop = asyncio.get_event_loop()

        for sig in signals:
            loop.add_signal_handler(sig, lambda signal = sig: asyncio.create_task(self.handle_signal(signal)))