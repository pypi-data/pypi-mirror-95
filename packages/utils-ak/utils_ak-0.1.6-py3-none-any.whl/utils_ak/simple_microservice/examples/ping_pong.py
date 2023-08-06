import time
import asyncio

from utils_ak.zmq import endpoint
from utils_ak.simple_microservice import SimpleMicroservice

import logging
logging.basicConfig(level=logging.INFO)



class Ping(SimpleMicroservice):
    def __init__(self, *args, **kwargs):
        super().__init__('Ping', *args, **kwargs)
        self.add_callback('ping', '', self.send_ping)

    def send_ping(self, topic, msg):
        self.logger.info(f'Received {topic} {msg}')
        time.sleep(1)
        self.publish_json('pong', '', {'msg': 'ping'})


class Pong(SimpleMicroservice):
    def __init__(self, *args, **kwargs):
        super().__init__('Pong', *args, **kwargs)
        self.add_callback('pong', '', self.send_pong)

    def send_pong(self, topic, msg):
        self.logger.info(f'Received {topic} {msg}')
        time.sleep(1)
        self.publish_json('ping', '', {'msg': 'pong'})

ping_logger = logging.getLogger('ping')
pong_logger = logging.getLogger('pong')


def run_ping():
    ping = Ping(logger=ping_logger, message_broker=('zmq',  {'endpoints': {'ping': {'type': 'sub', 'endpoint': endpoint('localhost', 6554)},
                                        'pong': {'type': 'sub', 'endpoint': endpoint('localhost', 6555)}}}) )

    async def send_initial():
        await asyncio.sleep(1.0)
        ping.send_ping('init', 'init')

    ping.tasks.append(asyncio.ensure_future(send_initial()))
    ping.run()


def run_pong():
    Pong(logger=pong_logger, message_broker=('zmq',  {'endpoints': {'ping': {'type': 'sub', 'endpoint': endpoint('localhost', 6554)},
                                        'pong': {'type': 'sub', 'endpoint': endpoint('localhost', 6555)}}})).run()


if __name__ == '__main__':
    import multiprocessing
    multiprocessing.Process(target=run_ping).start()
    multiprocessing.Process(target=run_pong).start()
