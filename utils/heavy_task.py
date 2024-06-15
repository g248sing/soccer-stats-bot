from typing import Union
import os
import sys
import asyncio
from asyncio.events import AbstractEventLoop
from time import sleep
from threading import Thread
from queue import Empty, Queue
from functools import wraps

from nextcord import Interaction
from nextcord.ext.commands.context import Context
import structlog

from utils import Singleton

class _HeavyTaskManager(metaclass=Singleton):
    MAX_LONG_TASKS = int(os.getenv('MAX_LONG_TASKS', default='5'))
    NUM_THREADS = 2

    def __init__(self) -> None:
        self.tasks = Queue(self.MAX_LONG_TASKS)
        self.main_loop = asyncio.get_running_loop()
        self.active = True
        self.consumer_threads = [
            Thread(target=self._consumer, args=(self.main_loop,), daemon=True)
            for _ in range(self.NUM_THREADS)
        ]
        for thread in self.consumer_threads:
            thread.start()
        self.logger = structlog.get_logger()

    def _consumer(self, main_loop: AbstractEventLoop):
        while self.active:
            try:
                # get the next task from the queue or sleep when empty
                try:
                    ctx, task, args, kwargs = self.tasks.get_nowait()
                except Empty:
                    sleep(2)
                    continue

                try:
                    # run the task in the thread
                    reply_coroutine = task(ctx, *args, **kwargs)
                    # run the reply coroutine in the event loop of the main thread
                    future = asyncio.run_coroutine_threadsafe(
                        reply_coroutine, main_loop)
                    future.result(timeout=5)
                    del reply_coroutine
                except Exception as e:
                    self.logger.error(f"Error running task!", exc_info=e)
            except:
                continue
        return

    def make_heavy_task(self, task, ctx: Union[Context, Interaction]):
        @wraps(task)
        def heavy_task(*args, **kwargs):
            if self.tasks.qsize() >= self.MAX_LONG_TASKS:
                self.logger.info(f"Tast count: {self.tasks.qsize()}")
                raise Exception('Queue full')
            # won't ever block as only one producer
            # TODO: check if the consumer thread is dead
            self.tasks.put((ctx, task, args, kwargs))
        return heavy_task


make_heavy_task = _HeavyTaskManager().make_heavy_task
