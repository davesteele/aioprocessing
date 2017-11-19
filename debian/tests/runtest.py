#!/usr/bin/python3


import time
import asyncio
import aioprocessing
import multiprocessing


def func(queue, event, lock, items):
    """ Demo worker function.

    This worker function runs in its own process, and uses
    normal blocking calls to aioprocessing objects, exactly 
    the way you would use oridinary multiprocessing objects.

    """
    with lock:
        event.set()
        for item in items:
            time.sleep(1)
            queue.put(item+5)
    queue.close()


@asyncio.coroutine
def example(queue, event, lock):
    l = [1,2]
    p = aioprocessing.AioProcess(target=func, args=(queue, event, lock, l))
    p.start()
    while True:
        result = yield from queue.coro_get()
        if result is None:
            break
        print("Got result {}".format(result))
    yield from p.coro_join()


@asyncio.coroutine
def example2(queue, event, lock):
    yield from event.coro_wait()
    with (yield from lock):
        yield from queue.coro_put(78)
        yield from queue.coro_put(None) # Shut down the worker


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    queue = aioprocessing.AioQueue()
    lock = aioprocessing.AioLock()
    event = aioprocessing.AioEvent()
    tasks = [
        asyncio.async(example(queue, event, lock)), 
        asyncio.async(example2(queue, event, lock)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
